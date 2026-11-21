"""Front Desk screens: appointments, check-in, repair jobs and pickup (Workspace design)."""
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .. import models as m
from .. import services
from ..audit import viewed_passcode
from ..permissions import (EMAIL_ROLES, can_open, can_see_contact, role_required,
                           screen_required)
from .common import attempt, get_job, picker_parts, quote_lines, store_jobs, to_int

def _day(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return timezone.localdate()


def _customers_by_phone(phone):
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) < 4:
        return m.Customer.objects.none()
    matches = [c.pk for c in m.Customer.objects.all() if digits in "".join(ch for ch in c.phone if ch.isdigit())]
    return m.Customer.objects.filter(pk__in=matches).prefetch_related("devices")[:10]


def _new_customer(request, errors):
    first, last = request.POST.get("first_name", "").strip(), request.POST.get("last_name", "").strip()
    phone, email = request.POST.get("phone", "").strip(), request.POST.get("email", "").strip()
    if not (first and last and phone):  # phone is required, email optional
        errors.append("Enter the customer's first name, last name and phone.")
        return None
    if len([c for c in phone if c.isdigit()]) < 7:
        errors.append("Enter a full phone number.")
        return None
    if _customers_by_phone(phone).exists():
        errors.append("A customer with this phone number already exists. Search by phone and select them.")
        return None
    if email:
        try:
            validate_email(email)
            if len(email) > m.Customer._meta.get_field("email").max_length:
                raise ValidationError("too long")
        except ValidationError:  # defect D-6, 2026-11-08: a bad address only failed later, at send
            errors.append("Enter a valid email address, or leave it blank.")
            return None
    return m.Customer.objects.create(first_name=first, last_name=last, phone=phone, email=email or None)


def _chosen_device_model(post, errors):
    """The device picked from the list, or one the staff member just added (2026-10-30)."""
    if post.get("device_model_id"):
        entry = m.DeviceModel.objects.filter(pk=to_int(post["device_model_id"])).first()
        if not entry:
            errors.append("Pick the device from the list.")
        return entry
    if post.get("new_brand", "").strip() or post.get("new_model", "").strip():
        try:
            return services.add_device_model(post.get("new_type"), post.get("new_brand"), post.get("new_model"))
        except services.RuleError as exc:
            errors.append(str(exc))
            return None
    errors.append("Pick the device from the list, or add it if it is not there.")
    return None


def _model_hint(post):
    """Model name used only to list the likeliest parts first."""
    entry = m.DeviceModel.objects.filter(pk=to_int(post.get("device_model_id"))).first()
    return entry.model if entry else post.get("new_model", "")


def _invalid_checkin_fields(post, errors, customer):
    """Fields to mark invalid after a failed check-in, so the error is tied to the field (WCAG 3.3.1)."""
    bad = set()
    if not customer:
        bad |= {f for f in ("first_name", "last_name", "phone") if not post.get(f, "").strip()}
        if any("phone number" in e for e in errors):
            bad.add("phone")
        if any("email" in e for e in errors):
            bad.add("email")
    if any(e.startswith("Pick the device") for e in errors):
        bad.add("device_model")
    if not post.get("reported_issue", "").strip():
        bad.add("reported_issue")
    return bad


# Check-in (UC-01, DFD 2.0) -----------------------------------------------------

@screen_required("checkin")
def checkin(request):
    store = request.store
    day = _day(request.GET.get("date"))
    appointment = None
    if request.GET.get("appointment"):
        appointment = get_object_or_404(m.Appointment, pk=to_int(request.GET["appointment"]), store=store,
                                         appt_status=m.APPT_BOOKED)
    customer_id = to_int(request.POST.get("customer_id") or request.GET.get("customer"))
    customer = appointment.customer if appointment else (
        m.Customer.objects.filter(pk=customer_id).first() if customer_id else None)
    phone = request.GET.get("phone", "").strip()
    errors = []

    if request.method == "POST":
        with transaction.atomic():
            if not customer:
                customer = _new_customer(request, errors)
            device = None
            # A device picked from the list, or added, wins over the on-file radio that is ticked by default.
            picked_other = any(request.POST.get(k, "").strip() for k in ("device_model_id", "new_brand", "new_model"))
            if customer and request.POST.get("device_id") and not picked_other:
                device = customer.devices.filter(pk=to_int(request.POST["device_id"])).first()
            elif customer:
                entry = _chosen_device_model(request.POST, errors)
                if entry:
                    device = m.Device.objects.create(
                        customer=customer, model=entry.model, device_type=entry.device_type, brand=entry.brand,
                        serial_or_imei=request.POST.get("serial_or_imei", "").strip() or None)
            tech = services.repairers(store).filter(pk=to_int(request.POST.get("technician_id"))).first()
            if customer and not device and not errors:  # a device_id that is not this customer's
                errors.append("Pick the device from the list, or add it if it is not there.")
            if device and not errors:
                try:
                    job = services.check_in(
                        request.user, store, device, request.POST.get("reported_issue", ""),
                        request.POST.get("intake_condition", "").strip(), request.POST.get("passcode", ""),
                        tech, appointment, quote_lines(request.POST))
                except services.RuleError as exc:
                    errors.append(str(exc))
            if errors:
                customer = m.Customer.objects.filter(pk=customer_id).first() if customer_id else (
                    appointment.customer if appointment else None)
                transaction.set_rollback(True)  # after the lookup: no queries run once it is set
            else:
                messages.success(request, f"Job {job.ticket_number} created.")
                return redirect(reverse("job_ticket", args=[job.pk]) + "?print=1")
        for e in errors:
            messages.error(request, e)
    invalid = _invalid_checkin_fields(request.POST, errors, customer) if errors else set()

    start = timezone.make_aware(datetime.combine(day, datetime.min.time()))
    appointments = m.Appointment.objects.filter(
        store=store, scheduled_at__gte=start, scheduled_at__lt=start + timedelta(days=1),
        appt_status=m.APPT_BOOKED).select_related("customer", "technician", "repair_type")
    return render(request, "shop/checkin.html", {
        "day": day, "days": [timezone.localdate() + timedelta(days=i) for i in range(settings.APPOINTMENT_DAYS_AHEAD)],
        "appointments": appointments, "appointment": appointment, "customer": customer, "phone": phone,
        "matches": _customers_by_phone(phone) if phone and not customer else [],
        "technicians": services.repairers(store), "device_types": m.DEVICE_TYPES, "post": request.POST,
        "device_models": m.DeviceModel.objects.all(), "brands": m.DeviceModel.objects.order_by("brand").values_list("brand", flat=True).distinct(),
        "parts": picker_parts(store, _model_hint(request.POST), request.POST),
        "preselected_tech": appointment.technician_id if appointment else to_int(request.POST.get("technician_id")),
        "invalid": invalid,
        "awaiting_answer": m.RepairJob.objects.filter(store=store, status=m.AWAITING_APPROVAL)
        .select_related("device__customer").order_by("pk") if can_open(request, "jobs") else [],
        "other_device": any(request.POST.get(k, "").strip() for k in ("device_model_id", "new_brand", "new_model")),
    })


# Appointments (UC-12, DFD 1.0) -------------------------------------------------

@screen_required("checkin")
def appointment_edit(request, pk=None):
    store = request.store
    appointment = get_object_or_404(m.Appointment, pk=pk, store=store, appt_status=m.APPT_BOOKED) if pk else None
    day = _day(request.GET.get("date") or (timezone.localdate(appointment.scheduled_at) if appointment else None))
    customer_id = to_int(request.POST.get("customer_id") or request.GET.get("customer"))
    customer = appointment.customer if appointment else (
        m.Customer.objects.filter(pk=customer_id).first() if customer_id else None)
    phone = request.GET.get("phone", "").strip()
    repair_types = m.RepairType.objects.filter(active_flag=True)
    type_id = to_int(request.POST.get("repair_type_id") or request.GET.get("type"))
    repair_type = repair_types.filter(pk=type_id).first() if type_id else (
        appointment.repair_type if appointment and appointment.repair_type in repair_types else None)

    if request.method == "POST":
        errors = []
        with transaction.atomic():
            if not customer:
                customer = _new_customer(request, errors)
            when = None
            try:
                when = datetime.fromisoformat(request.POST.get("slot", ""))
                if timezone.is_naive(when):  # the form always sends the zone; only an altered request lacks it
                    raise ValueError
            except ValueError:
                when = None
                errors.append("Pick a time.")
            if not repair_type:
                errors.append("Pick the repair type.")
            tech = services.repairers(store).filter(pk=to_int(request.POST.get("technician_id"))).first()
            if customer and when and not errors:
                ok = attempt(request, services.save_appointment, store, customer, when, tech, request.user, appointment,
                             repair_type, success=f"Appointment saved for {services.clock(when)} on {when:%a %b %d}.")
                if ok:
                    return redirect(f"/checkin/?date={when.date().isoformat()}")
                errors.append("")
            transaction.set_rollback(True)
        for e in filter(None, errors):
            messages.error(request, e)
        if not appointment:
            customer = m.Customer.objects.filter(pk=customer_id).first() if customer_id else None

    slots = []
    minutes = services.appointment_minutes(repair_type, appointment)
    for when in services.slot_times(day) if repair_type else []:
        slots.append({"when": when, "label": services.clock(when),
                      "busy": sorted(services.busy_technicians(store, when, minutes, appointment)),
                      "full": services.slot_is_full(store, when, minutes, appointment) or when < timezone.now(),
                      "selected": appointment and appointment.scheduled_at == when})
    return render(request, "shop/appointment_form.html", {
        "appointment": appointment, "customer": customer, "phone": phone, "day": day, "slots": slots,
        "repair_types": repair_types, "repair_type": repair_type, "minutes": minutes,
        "days": [timezone.localdate() + timedelta(days=i) for i in range(settings.APPOINTMENT_DAYS_AHEAD)],
        "matches": _customers_by_phone(phone) if phone and not customer else [],
        "technicians": services.repairers(store), "post": request.POST,
    })


@screen_required("checkin")
def appointment_cancel(request, pk):
    appointment = get_object_or_404(m.Appointment, pk=pk, store=request.store)
    if request.method == "POST":
        attempt(request, services.cancel_appointment, appointment, success="Appointment cancelled.")
    return redirect(f"/checkin/?date={timezone.localdate(appointment.scheduled_at).isoformat()}")


# Repair jobs (FR02, FR06, UC-13) ----------------------------------------------

@screen_required("jobs")
def jobs(request):
    qs = store_jobs(request)
    if request.user.role == m.OWNER:
        qs = qs.filter(store=request.store)
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "open")
    if q:
        digits = "".join(c for c in q if c.isdigit())
        match = Q(ticket_number__iexact=q) | Q(ticket_number__iexact=f"QP-{q}")
        if len(digits) >= 4:
            match |= Q(device__customer__in=_customers_by_phone(q).values("pk"))
        qs = qs.filter(match)
    elif status == "open":
        qs = qs.exclude(status=m.CLOSED)
    elif status in m.JOB_STATUSES:
        qs = qs.filter(status=status)
    counts = {s: store_jobs(request).filter(store=request.store, status=s).count() for s in m.OPEN_STATUSES}
    return render(request, "shop/jobs.html", {"jobs": qs, "q": q, "status": status, "counts": counts,
                                              "statuses": m.JOB_STATUSES})


@screen_required("jobs")
def job_detail(request, pk):
    job = get_job(request, pk)
    if request.method == "POST":
        action, user = request.POST.get("action"), request.user
        if action == "approve":
            attempt(request, services.record_decision, job, user, True, success="Approval recorded.")
        elif action == "decline":
            attempt(request, services.record_decision, job, user, False,
                    success="Decline recorded.")
        elif action == "payment":
            attempt(request, services.record_payment, job, user, request.POST.get("amount") or "0",
                    request.POST.get("method"), success="Payment recorded.")
        elif action == "void_payment":
            attempt(request, services.void_payment, job, user, to_int(request.POST.get("payment_id")),
                    request.POST.get("reason", ""), success="Payment voided.")
        elif action == "release":
            attempt(request, services.release_device, job, user, request.POST.get("id_verified") == "on",
                    request.POST.get("receipt_signed") == "on", success=f"{job.ticket_number} released and closed.")
        elif action == "assign" and user.role in (m.OWNER, m.MANAGER):
            tech = services.repairers(job.store).filter(pk=to_int(request.POST.get("technician_id"))).first()
            attempt(request, services.assign, job, tech, user, success="Technician updated.")
        return redirect("job_detail", job.pk)
    quote = job.current_quote
    return render(request, "shop/job_detail.html", {
        "job": job, "quote": quote, "quotes": job.quotes.order_by("quote_id").prefetch_related("lines__part"), "steps": _steps(job),
        "passcode": viewed_passcode(request.user, job),
        "can_email": request.user.role in EMAIL_ROLES, "can_contact": can_see_contact(request.user), "technicians": services.repairers(job.store),
        "due": max((job.final_cost or 0) - job.amount_paid, 0),
        "history": job.history.select_related("changed_by"), "past_jobs": job.device.jobs.exclude(pk=job.pk),
    })


@role_required(*EMAIL_ROLES)
def job_notify(request, pk):
    if request.user.role == m.TECHNICIAN:
        job = get_object_or_404(m.RepairJob, pk=pk, assigned_tech=request.user)
    else:
        job = get_job(request, pk)
    if request.method == "POST":
        attempt(request, services.send_pickup_notification, job, request.user,
                success="Pickup notification sent.")
    to_bench = request.user.role == m.TECHNICIAN or (
        request.POST.get("back") == "bench" and services.can_repair_at(request.user, job.store))
    return redirect("bench_job" if to_bench else "job_detail", job.pk)


@screen_required("checkin")
def job_ticket(request, pk):
    return render(request, "shop/ticket.html", {"job": get_job(request, pk)})


@screen_required("jobs")
def job_receipt(request, pk):
    """The receipt the customer signs at pickup (decision 2026-11-08). Reprintable after release."""
    job = get_job(request, pk)
    if job.status not in (m.READY, m.UNREPAIRED, m.CLOSED):
        messages.error(request, "The receipt is printed at pickup.")
        return redirect("job_detail", job.pk)
    approved = job.quotes.filter(decision=m.Q_APPROVED).prefetch_related("lines__part") if job.final_cost is not None else []
    return render(request, "shop/receipt.html", {
        "job": job, "lines": [line for quote in approved for line in quote.lines.all()],
        "labor": sum((quote.labor_amount for quote in approved), 0),
        "due": max((job.final_cost or 0) - job.amount_paid, 0),
    })


def _steps(job):
    """The status bar on the job and bench screens."""
    order = [m.CHECKED_IN, m.DIAGNOSING, m.AWAITING_APPROVAL, m.IN_REPAIR, m.READY, m.CLOSED]
    labels = ["Checked In", "Diagnosing", "Approval", "In Repair", "Ready", "Closed"]
    position = {m.AWAITING_PARTS: m.IN_REPAIR, m.UNREPAIRED: m.READY}.get(job.status, job.status)
    reached = order.index(position)
    return [{"label": label, "done": i < reached, "current": i == reached} for i, label in enumerate(labels)]
