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
from ..permissions import can_see_passcode, screen_required
from .common import attempt, picker_parts, quote_lines, to_int
from .desk import _steps


def _visible(user, store):
    return m.RepairJob.objects.filter(store=store).filter(
        Q(assigned_tech=user) | Q(assigned_tech__isnull=True, status=m.CHECKED_IN)
    ).select_related("device")


@screen_required("bench")
def bench(request, pk=None):
    user, store = request.user, request.store
    mine = _visible(user, store).filter(assigned_tech=user).exclude(status=m.CLOSED)
    open_jobs = _visible(user, store).filter(assigned_tech__isnull=True)
    job = get_object_or_404(_visible(user, store), pk=pk) if pk else mine.first()

    if request.method == "POST" and job:
        action = request.POST.get("action")
        part = m.Part.objects.filter(pk=request.POST.get("part_id") or 0, active_flag=True).first()
        qty = to_int(request.POST.get("quantity"), 1)
        if action == "claim":
            attempt(request, services.claim, job, user, success=f"{job.ticket_number} is now in your queue.")
        elif action == "start":
            attempt(request, services.start_diagnosis, job, user)
        elif action == "confirm":
            attempt(request, services.confirm_repair, job, user, request.POST.get("diagnosis_notes", ""),
                    success="Repair started on the quote the customer approved at check-in.")
        elif action == "quote":
            extra = job.has_approved_quote
            attempt(request, services.submit_quote, job, user, request.POST.get("diagnosis_notes", ""),
                    None, quote_lines(request.POST),
                    success="Additional repair sent. Front Desk records the customer's decision." if extra
                    else "Quote sent. Front Desk records the customer's decision.")
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

    ctx = {"mine": mine, "open_jobs": open_jobs, "job": job, "picked": bool(pk)}
    if job:
        quotes = list(job.quotes.order_by("quote_id").prefetch_related("lines__part"))
        quoted = {}
        for q in quotes:
            if q.decision == m.Q_APPROVED:
                for line in q.lines.all():
                    quoted[line.part_id] = quoted.get(line.part_id, 0) + line.quantity
        parts = picker_parts(store, job.device.model)
        for p in parts:
            p.quoted = quoted.get(p.pk, 0)
        ctx.update({
            "steps": _steps(job), "quote": quotes[-1] if quotes else None, "quotes": quotes,
            "has_approved": any(q.decision == m.Q_APPROVED for q in quotes), "parts": parts,
            "used": job.parts.filter(part_status=m.PART_USED).select_related("part"),
            "needed": job.parts.filter(part_status=m.PART_NEEDED).select_related("part", "purchase_order"),
            "history": job.history.select_related("changed_by"),
            "passcode": decrypt_passcode(job.device_passcode) if can_see_passcode(user, job) else None,
            "has_email": bool(job.customer.email),
        })
    return render(request, "shop/bench.html", ctx)
