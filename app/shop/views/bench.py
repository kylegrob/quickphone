"""Technician screen: assigned queue, diagnosis and quote, repair work (Prototype A, slide 3).

Technicians see the customer's name only; phone and email are never sent to this
screen (NFR04). Each technician sees only their own jobs plus open jobs to claim (FR04).
"""
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .. import models as m
from .. import services
from ..crypto import decrypt_passcode
from ..permissions import BENCH_ROLES, can_see_passcode, role_required
from .common import attempt, to_int
from .desk import _steps


def _visible(user):
    return m.RepairJob.objects.filter(store=user.store).filter(
        Q(assigned_tech=user) | Q(assigned_tech__isnull=True, status=m.CHECKED_IN)
    ).select_related("device")


@role_required(*BENCH_ROLES)
def bench(request, pk=None):
    user = request.user
    mine = _visible(user).filter(assigned_tech=user).exclude(status=m.CLOSED)
    open_jobs = _visible(user).filter(assigned_tech__isnull=True)
    job = get_object_or_404(_visible(user), pk=pk) if pk else mine.first()

    if request.method == "POST" and job:
        action = request.POST.get("action")
        part = m.Part.objects.filter(pk=request.POST.get("part_id") or 0, active_flag=True).first()
        qty = to_int(request.POST.get("quantity"), 1)
        if action == "claim":
            attempt(request, services.claim, job, user, success=f"{job.ticket_number} is now in your queue.")
        elif action == "start":
            attempt(request, services.start_diagnosis, job, user)
        elif action == "quote":
            lines = []
            for p in m.Part.objects.filter(active_flag=True):
                n = to_int(request.POST.get(f"qty_{p.pk}"))
                if request.POST.get(f"use_{p.pk}") and n > 0:
                    lines.append((p, n))
            attempt(request, services.submit_quote, job, user, request.POST.get("diagnosis_notes", ""),
                    request.POST.get("labor_amount") or "0", lines,
                    success="Quote sent. Front Desk records the customer's decision.")
        elif action == "unrepairable":
            attempt(request, services.mark_unrepairable, job, user, request.POST.get("diagnosis_notes", ""),
                    success="Marked as not repairable. No diagnostic fee is charged.")
        elif action == "use_part" and part:
            attempt(request, services.record_part_used, job, user, part, qty,
                    success=f"Recorded {qty} x {part}; store stock reduced.")
        elif action == "request_part" and part:
            attempt(request, services.request_part, job, user, part, qty,
                    success="Part requested. The job waits in Awaiting Parts.")
        elif action == "complete":
            attempt(request, services.complete_repair, job, user, request.POST.get("repair_notes", ""),
                    success="Ready for pickup.")
        elif not part and action in ("use_part", "request_part"):
            messages.error(request, "Pick a part.")
        return redirect("bench_job", job.pk)

    ctx = {"mine": mine, "open_jobs": open_jobs, "job": job}
    if job:
        stock = {s.part_id: s.quantity_on_hand for s in m.StorePartStock.objects.filter(store=user.store)}
        quote = job.current_quote
        quoted = {line.part_id: line.quantity for line in quote.lines.all()} if quote else {}
        parts = list(m.Part.objects.filter(active_flag=True))
        for p in parts:
            p.on_hand, p.quoted = stock.get(p.pk, 0), quoted.get(p.pk, 0)
        # Parts for this device model first, so the likely picks are at the top.
        model = (job.device.model or "").lower()
        parts.sort(key=lambda p: (not (p.device_model and p.device_model.lower() in model), p.part_name))
        ctx.update({
            "steps": _steps(job), "quote": quote, "parts": parts,
            "used": job.parts.filter(part_status=m.PART_USED).select_related("part"),
            "needed": job.parts.filter(part_status=m.PART_NEEDED).select_related("part", "purchase_order"),
            "history": job.history.select_related("changed_by"),
            "passcode": decrypt_passcode(job.device_passcode) if can_see_passcode(user, job) else None,
            "has_email": bool(job.customer.email),
        })
    return render(request, "shop/bench.html", ctx)
