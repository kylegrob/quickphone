"""Front Desk screens: appointments, check-in, repair jobs and pickup (Prototype A, slides 1-2)."""
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .. import models as m
from .. import services
from ..crypto import decrypt_passcode
from ..permissions import EMAIL_ROLES, can_see_contact, can_see_passcode, role_required, screen_required
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
    if not (first and last and phone):
        errors.append("Enter the customer's first name, last name and phone.")
        return None
    if _customers_by_phone(phone).exists():
        errors.append("A customer with this phone number already exists. Search by phone and select them.")
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


# Check-in (UC-01, DFD 2.0) -----------------------------------------------------

@screen_required("checkin")
def checkin(request):
    store = request.store
    day = _day(request.GET.get("date"))
    appointment = None
    if request.GET.get("appointment"):
        appointment = get_object_or_404(m.Appointment, pk=request.GET["appointment"], store=store,
                                         appt_status=m.APPT_BOOKED)
    customer_id = request.POST.get("customer_id") or request.GET.get("customer")
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
                device = customer.devices.filter(pk=request.POST["device_id"]).first()
            elif customer:
                entry = _chosen_device_model(request.POST, errors)
                if entry:
                    device = m.Device.objects.create(
                        customer=customer, model=entry.model, device_type=entry.device_type, brand=entry.brand,
                        serial_or_imei=request.POST.get("serial_or_imei", "").strip() or None)
            tech = services.repairers(store).filter(pk=request.POST.get("technician_id") or 0).first()
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
                messages.success(request, f"Job {job.ticket_number} created. Print the claim ticket and device tag.")
                return redirect("job_ticket", job.pk)
        for e in errors:
            messages.error(request, e)

    start = timezone.make_aware(datetime.combine(day, datetime.min.time()))
    appointments = m.Appointment.objects.filter(
        store=store, scheduled_at__gte=start, scheduled_at__lt=start + timedelta(days=1),
        appt_status=m.APPT_BOOKED).select_related("customer", "technician")
    return render(request, "shop/checkin.html", {
        "day": day, "days": [timezone.localdate() + timedelta(days=i) for i in range(settings.APPOINTMENT_DAYS_AHEAD)],
        "appointments": appointments, "appointment": appointment, "customer": customer, "phone": phone,
        "matches": _customers_by_phone(phone) if phone and not customer else [],
        "technicians": services.repairers(store), "device_types": m.DEVICE_TYPES, "post": request.POST,
        "device_models": m.DeviceModel.objects.all(), "brands": m.DeviceModel.objects.order_by("brand").values_list("brand", flat=True).distinct(),
        "parts": picker_parts(store, _model_hint(request.POST), request.POST),
        "preselected_tech": appointment.technician_id if appointment else to_int(request.POST.get("technician_id")),
    })


# Appointments (UC-12, DFD 1.0) -------------------------------------------------

@screen_required("checkin")
def appointment_edit(request, pk=None):
    store = request.store
    appointment = get_object_or_404(m.Appointment, pk=pk, store=store, appt_status=m.APPT_BOOKED) if pk else None
    day = _day(request.GET.get("date") or (timezone.localdate(appointment.scheduled_at) if appointment else None))
    customer_id = request.POST.get("customer_id") or request.GET.get("customer")
    customer = appointment.customer if appointment else (
        m.Customer.objects.filter(pk=customer_id).first() if customer_id else None)
    phone = request.GET.get("phone", "").strip()

    if request.method == "POST":
        errors = []
        with transaction.atomic():
            if not customer:
                customer = _new_customer(request, errors)
            when = None
            try:
                when = datetime.fromisoformat(request.POST.get("slot", ""))
            except ValueError:
                errors.append("Pick a time.")
            tech = services.repairers(store).filter(pk=request.POST.get("technician_id") or 0).first()
            if customer and when and not errors:
                ok = attempt(request, services.save_appointment, store, customer, when, tech, request.user, appointment,
                             success=f"Appointment saved for {services.clock(when)} on {when:%a %b %d}.")
                if ok:
                    return redirect(f"/checkin/?date={when.date().isoformat()}")
                errors.append("")
            transaction.set_rollback(True)
        for e in filter(None, errors):
            messages.error(request, e)
        if not appointment:
            customer = m.Customer.objects.filter(pk=customer_id).first() if customer_id else None

    slots = []
    for when in services.slot_times(day):
        busy = list(services.booked(store, when, appointment).exclude(technician=None)
                    .values_list("technician_id", flat=True))
        slots.append({"when": when, "label": services.clock(when), "busy": busy,
                      "full": services.slot_is_full(store, when, appointment) or when < timezone.now(),
                      "selected": appointment and appointment.scheduled_at == when})
    return render(request, "shop/appointment_form.html", {
        "appointment": appointment, "customer": customer, "phone": phone, "day": day, "slots": slots,
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
                    success="Decline recorded. The device goes back unrepaired.")
        elif action == "payment":
            attempt(request, services.record_payment, job, user, request.POST.get("amount") or "0",
                    request.POST.get("method"), success="Payment recorded.")
        elif action == "release":
            attempt(request, services.release_device, job, user, request.POST.get("id_verified") == "on",
                    success=f"{job.ticket_number} released and closed.")
        elif action == "assign" and user.role in (m.OWNER, m.MANAGER):
            tech = services.repairers(job.store).filter(pk=request.POST.get("technician_id") or 0).first()
            attempt(request, services.assign, job, tech, user, success="Technician updated.")
        return redirect("job_detail", job.pk)
    quote = job.current_quote
    return render(request, "shop/job_detail.html", {
        "job": job, "quote": quote, "quotes": job.quotes.order_by("quote_id").prefetch_related("lines__part"), "steps": _steps(job),
        "passcode": decrypt_passcode(job.device_passcode) if can_see_passcode(request.user, job) else None,
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
                success="Pickup notification sent from the store's email account.")
    return redirect("bench_job" if request.user.role == m.TECHNICIAN else "job_detail", job.pk)


@screen_required("checkin")
def job_ticket(request, pk):
    return render(request, "shop/ticket.html", {"job": get_job(request, pk)})


def _steps(job):
    """The status bar on the job and bench screens (Prototype A)."""
    order = [m.CHECKED_IN, m.DIAGNOSING, m.AWAITING_APPROVAL, m.IN_REPAIR, m.READY, m.CLOSED]
    labels = ["Checked In", "Diagnosing", "Approval", "In Repair", "Ready", "Closed"]
    position = {m.AWAITING_PARTS: m.IN_REPAIR, m.UNREPAIRED: m.READY}.get(job.status, job.status)
    reached = order.index(position)
    return [{"label": label, "done": i < reached, "current": i == reached} for i, label in enumerate(labels)]
