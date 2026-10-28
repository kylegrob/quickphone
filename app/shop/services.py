"""Business rules, one function per step of the workflow (DFD processes 1.0 to 9.0).

Views call these functions and never change status, stock or orders directly, so
every rule is enforced in one place and every change is recorded with who made it
and when (NFR02).
"""
from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from . import models as m
from .crypto import encrypt_passcode
from .permissions import ALLOW_SELF_APPROVAL_OF_PO, EMAIL_ROLES, PO_APPROVER_ROLES


class RuleError(Exception):
    """A business rule blocked the action. The message is shown to the user."""


def set_status(job, status, user, note=""):
    job.status = status
    job.save()
    m.JobStatusHistory.objects.create(repair_job=job, status=status, changed_by=user, note=note or None)


# 1.0 Schedule Appointment (FR01, UC-12) -----------------------------------------

def slot_times(day):
    tz = timezone.get_current_timezone()
    first = datetime.combine(day, datetime.strptime(settings.APPOINTMENT_FIRST_SLOT, "%H:%M").time(), tz)
    last = datetime.combine(day, datetime.strptime(settings.APPOINTMENT_LAST_SLOT, "%H:%M").time(), tz)
    step = timedelta(minutes=settings.APPOINTMENT_SLOT_MINUTES)
    times = []
    while first <= last:
        times.append(first)
        first += step
    return times


def clock(when):
    return timezone.localtime(when).strftime("%I:%M %p").lstrip("0")


def technicians(store):
    return m.Employee.objects.filter(store=store, role=m.TECHNICIAN, active_flag=True)


def booked(store, when, exclude=None):
    qs = m.Appointment.objects.filter(store=store, scheduled_at=when, appt_status=m.APPT_BOOKED)
    return qs.exclude(pk=exclude.pk) if exclude else qs


def slot_is_full(store, when, exclude=None):
    return booked(store, when, exclude).count() >= max(technicians(store).count(), 1)


def save_appointment(store, customer, when, technician, user, appointment=None):
    if when < timezone.now():
        raise RuleError("Pick a time that has not passed.")
    if slot_is_full(store, when, appointment):
        raise RuleError("That time is full. Pick another time.")
    if technician and booked(store, when, appointment).filter(technician=technician).exists():
        raise RuleError(f"{technician.first_name} is booked at {clock(when)}. Pick another technician or time.")
    if technician and (technician.store_id != store.pk or technician.role != m.TECHNICIAN):
        raise RuleError("Pick a technician from this store.")
    appointment = appointment or m.Appointment(store=store)
    appointment.customer, appointment.scheduled_at, appointment.technician = customer, when, technician
    appointment.save()
    return appointment


def cancel_appointment(appointment):
    if appointment.appt_status != m.APPT_BOOKED:
        raise RuleError("Only a booked appointment can be cancelled.")
    appointment.appt_status = m.APPT_CANCELLED
    appointment.save()


# 2.0 Register Repair Job (FR02 to FR04, UC-01) ------------------------------------

@transaction.atomic
def check_in(user, store, device, reported_issue, intake_condition="", passcode="", technician=None, appointment=None):
    if not reported_issue.strip():
        raise RuleError("Enter the reported problem.")
    if technician and (technician.store_id != store.pk or technician.role != m.TECHNICIAN):
        raise RuleError("Pick a technician from this store.")
    if appointment:
        if appointment.appt_status != m.APPT_BOOKED:
            raise RuleError("This appointment is not open for check-in.")
        appointment.appt_status = m.APPT_CHECKED_IN
        appointment.save()
    job = m.RepairJob.objects.create(
        ticket_number=f"TMP-{timezone.now():%H%M%S%f}"[:12], device=device, store=store, appointment=appointment,
        assigned_tech=technician, reported_issue=reported_issue.strip(), intake_condition=intake_condition or None,
        device_passcode=encrypt_passcode(passcode.strip()),
    )
    job.ticket_number = f"QP-{1000 + job.pk}"
    job.save()
    m.JobStatusHistory.objects.create(repair_job=job, status=m.CHECKED_IN, changed_by=user,
                                      note="Checked in" + (" from appointment" if appointment else " as walk-in"))
    return job


def assign(job, technician, user):
    if job.status == m.CLOSED:
        raise RuleError("A closed job cannot be reassigned.")
    if technician and (technician.store_id != job.store_id or technician.role != m.TECHNICIAN):
        raise RuleError("Pick a technician from this store.")
    job.assigned_tech = technician
    job.save()
    m.JobStatusHistory.objects.create(repair_job=job, status=job.status, changed_by=user,
                                      note=f"Assigned to {technician}" if technician else "Unassigned")


def claim(job, tech):
    """Technicians may assign themselves to an open job (owner, Oct 23 #4)."""
    if job.assigned_tech_id:
        raise RuleError("This job is already assigned.")
    if job.store_id != tech.store_id:
        raise RuleError("This job belongs to another store.")
    assign(job, tech, tech)


# 3.0 Record Diagnosis (FR05, UC-02) --------------------------------------------

def _require_own_job(job, tech):
    if job.assigned_tech_id != tech.pk:
        raise RuleError("Only the assigned technician can work on this job.")


def start_diagnosis(job, tech):
    _require_own_job(job, tech)
    if job.status != m.CHECKED_IN:
        raise RuleError("Diagnosis starts from Checked In.")
    set_status(job, m.DIAGNOSING, tech)


def stock_for(store, part):
    return m.StorePartStock.objects.filter(store=store, part=part).first()


@transaction.atomic
def submit_quote(job, tech, diagnosis_notes, labor_amount, lines):
    """lines: list of (Part, quantity). Builds the quote and asks for the customer's decision."""
    _require_own_job(job, tech)
    if job.status != m.DIAGNOSING:
        raise RuleError("A quote can only be sent while the job is Diagnosing.")
    if not diagnosis_notes.strip():
        raise RuleError("Enter the diagnosis before sending the quote.")
    labor = Decimal(labor_amount)
    if labor < 0:
        raise RuleError("Labor cannot be negative.")
    if any(qty <= 0 for _, qty in lines):
        raise RuleError("Part quantities must be at least 1.")
    job.diagnosis_notes = diagnosis_notes.strip()
    job.quotes.filter(decision=m.Q_PENDING).delete()
    parts_amount = sum((part.standard_cost * qty for part, qty in lines), Decimal("0"))
    quote = m.Quote.objects.create(repair_job=job, labor_amount=labor, parts_amount=parts_amount,
                                   total_amount=labor + parts_amount)
    for part, qty in lines:
        m.QuoteLine.objects.create(quote=quote, part=part, quantity=qty, unit_cost=part.standard_cost)
    set_status(job, m.AWAITING_APPROVAL, tech, f"Quote ${quote.total_amount:.2f} sent for approval")
    return quote


def mark_unrepairable(job, tech, notes):
    """No diagnostic fee when a device cannot be repaired (owner, Oct 23 #5)."""
    _require_own_job(job, tech)
    if job.status not in (m.DIAGNOSING, m.CHECKED_IN):
        raise RuleError("Only a job in diagnosis can be marked as not repairable.")
    if not notes.strip():
        raise RuleError("Say why the device cannot be repaired.")
    job.diagnosis_notes = notes.strip()
    job.completed_at = timezone.now()
    set_status(job, m.UNREPAIRED, tech, "Cannot be repaired")


def _shortages(job):
    """Quote lines the store cannot cover from stock right now, as (part, quantity short)."""
    quote = job.quotes.filter(decision=m.Q_APPROVED).order_by("-quote_id").first()
    if not quote:
        return []
    used = {}
    for jp in job.parts.filter(part_status=m.PART_USED):
        used[jp.part_id] = used.get(jp.part_id, 0) + jp.quantity
    short = []
    for line in quote.lines.select_related("part"):
        still_needed = line.quantity - used.get(line.part_id, 0)
        stock = stock_for(job.store, line.part)
        on_hand = stock.quantity_on_hand if stock else 0
        if still_needed > on_hand:
            short.append((line.part, still_needed - on_hand))
    return short


@transaction.atomic
def record_decision(job, user, approved, note=""):
    """Front Desk records the customer's approval or decline (FR05, UC-03)."""
    if job.status != m.AWAITING_APPROVAL:
        raise RuleError("This job is not waiting for the customer's decision.")
    quote = job.quotes.filter(decision=m.Q_PENDING).order_by("-quote_id").first()
    quote.decision = m.Q_APPROVED if approved else m.Q_DECLINED
    quote.decision_at, quote.decision_by = timezone.now(), user
    quote.save()
    if not approved:
        job.completed_at = timezone.now()
        set_status(job, m.UNREPAIRED, user, note or "Customer declined the quote")
        return
    job.final_cost = quote.total_amount
    shortages = _shortages(job)
    if shortages:
        for part, qty in shortages:
            m.JobPart.objects.create(repair_job=job, part=part, quantity=qty, part_status=m.PART_NEEDED)
        set_status(job, m.AWAITING_PARTS, user, "Approved; parts requested: " +
                   ", ".join(f"{p} x{q}" for p, q in shortages))
    else:
        set_status(job, m.IN_REPAIR, user, note or "Customer approved the quote")


# 4.0 Record Repair Work (FR06, FR07, UC-04) ------------------------------------

@transaction.atomic
def record_part_used(job, tech, part, quantity):
    """Deducts the store's stock automatically; stock never goes below zero (FR07)."""
    _require_own_job(job, tech)
    if job.status != m.IN_REPAIR:
        raise RuleError("Parts are recorded while the job is In Repair.")
    if quantity <= 0:
        raise RuleError("Quantity must be at least 1.")
    stock = m.StorePartStock.objects.select_for_update().filter(store=job.store, part=part).first()
    if not stock or stock.quantity_on_hand < quantity:
        raise RuleError(f"Only {stock.quantity_on_hand if stock else 0} of {part} in stock. "
                        "Request the part instead.")
    m.StorePartStock.objects.filter(store=job.store, part=part).update(
        quantity_on_hand=stock.quantity_on_hand - quantity)
    m.InventoryTxn.objects.create(store=job.store, part=part, recorded_by=tech, txn_type=m.TXN_USED,
                                  quantity_change=-quantity, reason=f"Used on {job.ticket_number}")
    needed = job.parts.filter(part=part, part_status=m.PART_NEEDED).first()
    if needed:
        needed.part_status, needed.quantity, needed.recorded_at = m.PART_USED, quantity, timezone.now()
        needed.save()
    else:
        m.JobPart.objects.create(repair_job=job, part=part, quantity=quantity, part_status=m.PART_USED)


@transaction.atomic
def request_part(job, tech, part, quantity):
    """A technician requests a part that is out of stock; the job waits (owner, Oct 23 #3)."""
    _require_own_job(job, tech)
    if job.status != m.IN_REPAIR:
        raise RuleError("Parts are requested while the job is In Repair.")
    if quantity <= 0:
        raise RuleError("Quantity must be at least 1.")
    m.JobPart.objects.create(repair_job=job, part=part, quantity=quantity, part_status=m.PART_NEEDED)
    set_status(job, m.AWAITING_PARTS, tech, f"Requested {part} x{quantity}")


def complete_repair(job, tech, repair_notes):
    _require_own_job(job, tech)
    if job.status != m.IN_REPAIR:
        raise RuleError("Only a job In Repair can be marked ready.")
    job.repair_notes = (repair_notes or "").strip() or job.repair_notes
    job.completed_at = timezone.now()
    set_status(job, m.READY, tech, "Repair complete")


# 5.0 Send Pickup Notification (FR12, UC-05) ------------------------------------

def send_pickup_notification(job, user):
    """Staff click to send; it is never automatic (owner, Oct 23 #1)."""
    if user.role not in EMAIL_ROLES:
        raise RuleError("Your role cannot send customer email.")
    if job.status not in (m.READY, m.UNREPAIRED):
        raise RuleError("The pickup notification is sent when the device is ready to collect.")
    customer = job.customer
    if not customer.email:
        raise RuleError("No email address on file for this customer.")
    if job.status == m.READY:
        body = (f"Hello {customer.first_name},\n\nYour {job.device} (ticket {job.ticket_number}) is repaired and "
                f"ready to collect at {job.store.store_name}, {job.store.address}.\n")
        if job.final_cost is not None:
            body += f"Amount due: ${job.final_cost - job.amount_paid:.2f}.\n"
    else:
        body = (f"Hello {customer.first_name},\n\nYour {job.device} (ticket {job.ticket_number}) is ready to "
                f"collect at {job.store.store_name}, {job.store.address}. It was not repaired.\n")
    body += "Please bring your claim ticket and a photo ID.\n\n" + job.store.store_name + "\n" + job.store.phone
    try:
        send_mail(f"Your device is ready: {job.ticket_number}", body, job.store.email_address, [customer.email])
        job.email_status = "Sent"
    except Exception:
        job.email_status = "Failed"
    job.email_sent_at, job.email_sent_by = timezone.now(), user
    job.save()
    m.JobStatusHistory.objects.create(repair_job=job, status=job.status, changed_by=user,
                                      note=f"Pickup notification {job.email_status.lower()}")
    if job.email_status == "Failed":
        raise RuleError("The email could not be sent. Check the store's email settings and try again.")


# 6.0 Record Device Release (FR08, UC-06) ---------------------------------------

def record_payment(job, user, amount, method):
    """Records the fact of payment taken at the register; the system takes no payments."""
    amount = Decimal(amount)
    if job.status not in (m.READY, m.UNREPAIRED):
        raise RuleError("Payment is recorded at pickup.")
    if amount <= 0:
        raise RuleError("Enter an amount greater than zero.")
    if method not in ("Card", "Cash"):
        raise RuleError("Pick Card or Cash.")
    m.Payment.objects.create(repair_job=job, amount=amount, method=method)
    m.JobStatusHistory.objects.create(repair_job=job, status=job.status, changed_by=user,
                                      note=f"Payment ${amount:.2f} {method}")


def release_device(job, user, id_verified):
    """A repaired device is released only after payment is recorded; no override.
    A declined or unrepairable device may go back with no payment (decision 2026-10-28)."""
    if job.status not in (m.READY, m.UNREPAIRED):
        raise RuleError("Only a job Ready for Pickup or Returned Unrepaired can be released.")
    if not id_verified:
        raise RuleError("Check the customer's photo ID and tick the box.")
    if job.status == m.READY and job.amount_paid < (job.final_cost or 0):
        raise RuleError(f"Record payment first: ${(job.final_cost or 0) - job.amount_paid:.2f} still due.")
    job.id_verified_flag, job.picked_up_at = True, timezone.now()
    set_status(job, m.CLOSED, user, "Released to customer")


# 7.0 Process Purchase Orders (FR09, FR10, UC-08 to UC-10) -----------------------

def adjust_stock(store, part, change, reason, user, txn_type=m.TXN_ADJUSTMENT):
    if change == 0:
        raise RuleError("Enter a change other than zero.")
    if txn_type == m.TXN_ADJUSTMENT and not (reason or "").strip():
        raise RuleError("Give a reason for the count change.")
    with transaction.atomic():
        stock, _ = m.StorePartStock.objects.select_for_update().get_or_create(store=store, part=part)
        if stock.quantity_on_hand + change < 0:
            raise RuleError(f"Stock cannot go below zero (on hand: {stock.quantity_on_hand}).")
        m.StorePartStock.objects.filter(store=store, part=part).update(
            quantity_on_hand=stock.quantity_on_hand + change)
        m.InventoryTxn.objects.create(store=store, part=part, recorded_by=user, txn_type=txn_type,
                                      quantity_change=change, reason=(reason or "").strip() or None)


def set_reorder_point(store, part, value, user):
    """Managers set each part's reorder point (owner, Oct 23 #6)."""
    if user.role not in PO_APPROVER_ROLES:
        raise RuleError("Only a Manager or the Owner sets reorder points.")
    if value < 0:
        raise RuleError("The reorder point cannot be negative.")
    stock, _ = m.StorePartStock.objects.get_or_create(store=store, part=part)
    m.StorePartStock.objects.filter(store=store, part=part).update(reorder_point=value)


def draft_for_supplier(store, supplier, user):
    po = m.PurchaseOrder.objects.filter(store=store, supplier=supplier, po_status=m.PO_DRAFT).first()
    return po or m.PurchaseOrder.objects.create(store=store, supplier=supplier, created_by=user)


def add_to_po(store, part, quantity, user):
    if not part.default_supplier:
        raise RuleError("Set a supplier for this part first.")
    if quantity <= 0:
        raise RuleError("Quantity must be at least 1.")
    po = draft_for_supplier(store, part.default_supplier, user)
    line = po.lines.filter(part=part).first()
    if line:
        line.quantity_ordered += quantity
        line.save()
    else:
        m.POLine.objects.create(purchase_order=po, part=part, quantity_ordered=quantity, unit_cost=part.standard_cost)
    return po


def waiting_job_parts(po):
    """Part requests at this store, for parts on this order, not yet linked to an order."""
    return m.JobPart.objects.filter(
        repair_job__store=po.store, repair_job__status=m.AWAITING_PARTS, part_status=m.PART_NEEDED,
        part__in=[line.part_id for line in po.lines.all()],
    ).filter(Q(purchase_order__isnull=True) | Q(purchase_order=po)).select_related(
        "repair_job", "part", "repair_job__device")


def _require_status(po, *statuses):
    if po.po_status not in statuses:
        raise RuleError(f"This order is {po.po_status}.")


@transaction.atomic
def submit_po(po, user, linked_job_part_ids=()):
    _require_status(po, m.PO_DRAFT)
    if not po.lines.exists():
        raise RuleError("Add at least one part before submitting.")
    waiting = waiting_job_parts(po)
    waiting.update(purchase_order=None)
    waiting.filter(pk__in=linked_job_part_ids).update(purchase_order=po)
    po.po_status, po.rejection_reason = m.PO_PENDING, None
    po.save()


def approve_po(po, user):
    """A Manager approves every purchase order (owner, Oct 23 #2)."""
    if user.role not in PO_APPROVER_ROLES:
        raise RuleError("Only a Manager or the Owner approves purchase orders.")
    if not ALLOW_SELF_APPROVAL_OF_PO and po.created_by_id == user.pk:
        raise RuleError("Another Manager or the Owner must approve an order you created.")
    _require_status(po, m.PO_PENDING)
    po.po_status, po.approved_by, po.approved_at = m.PO_APPROVED, user, timezone.now()
    po.save()


def reject_po(po, user, reason):
    if user.role not in PO_APPROVER_ROLES:
        raise RuleError("Only a Manager or the Owner rejects purchase orders.")
    _require_status(po, m.PO_PENDING)
    if not (reason or "").strip():
        raise RuleError("Give a reason so the order can be fixed.")
    po.po_status, po.rejection_reason = m.PO_DRAFT, reason.strip()
    po.save()


def mark_ordered(po, user):
    _require_status(po, m.PO_APPROVED)
    po.po_status, po.placed_at = m.PO_ORDERED, timezone.now()
    po.save()


@transaction.atomic
def receive_po(po, user, received):
    """received: {po_line_id: quantity arriving now}. Partial deliveries keep the order open."""
    _require_status(po, m.PO_APPROVED, m.PO_ORDERED)
    any_received = False
    for line in po.lines.select_related("part"):
        qty = received.get(line.pk, 0)
        if qty < 0 or qty > line.outstanding:
            raise RuleError(f"{line.part}: receive between 0 and {line.outstanding}.")
        if qty:
            any_received = True
            line.quantity_received += qty
            line.save()
            adjust_stock(po.store, line.part, qty, f"Received on {po.number}", user, m.TXN_RECEIVED)
    if not any_received:
        raise RuleError("Enter the quantity that arrived.")
    if all(line.outstanding == 0 for line in po.lines.all()):
        po.po_status = m.PO_RECEIVED
    elif po.po_status == m.PO_APPROVED:
        po.po_status, po.placed_at = m.PO_ORDERED, po.placed_at or timezone.now()
    po.save()
    return release_waiting_jobs(po.store, user)


def release_waiting_jobs(store, user):
    """Jobs Awaiting Parts go back to In Repair once every requested part is in stock (UC-10)."""
    released = []
    for job in m.RepairJob.objects.filter(store=store, status=m.AWAITING_PARTS):
        needed = job.parts.filter(part_status=m.PART_NEEDED)
        if all((stock_for(store, jp.part) or m.StorePartStock(quantity_on_hand=0)).quantity_on_hand >= jp.quantity
               for jp in needed):
            set_status(job, m.IN_REPAIR, user, "Parts received")
            released.append(job)
    return released


# 9.0 Maintain Shop Records (FR11, FR14) ----------------------------------------

def can_assign_role(user, role):
    """Only the Owner can give the Owner role (FR14)."""
    return role in m.ROLES and (role != m.OWNER or user.role == m.OWNER)
