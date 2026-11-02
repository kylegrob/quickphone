"""Technician screen: assigned queue and one work card per job (Prototype A, slide 3).

The work card holds the quote and the repair together. Parts are not recorded one by one: marking the
job ready takes the planned parts off the store's stock (Kyle, 2026-11-02).

Technicians see the customer's name only; phone and email are never sent to this
screen (NFR04). Each technician sees only their own jobs plus open jobs to claim (FR04).
"""
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


def _used_lines(post):
    """(Part, quantity) from the completion form's used_<part id> boxes; None if the form had none."""
    keys = [k for k in post if k.startswith("used_")]
    if not keys:
        return None
    parts = m.Part.objects.in_bulk([to_int(k[5:]) for k in keys])
    return [(parts[to_int(k[5:])], to_int(post.get(k))) for k in keys if to_int(k[5:]) in parts]


@screen_required("bench")
def bench(request, pk=None):
    user, store = request.user, request.store
    mine = _visible(user, store).filter(assigned_tech=user).exclude(status=m.CLOSED)
    open_jobs = _visible(user, store).filter(assigned_tech__isnull=True)
    job = get_object_or_404(_visible(user, store), pk=pk) if pk else mine.first()

    if request.method == "POST" and job:
        action = request.POST.get("action")
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
        elif action == "add_work" and request.POST.get("charge") == "yes":
            attempt(request, services.submit_quote, job, user, request.POST.get("diagnosis_notes", ""),
                    None, quote_lines(request.POST),
                    success="Additional repair sent. Front Desk records the customer's decision.")
        elif action == "add_work":
            attempt(request, services.add_parts, job, user, quote_lines(request.POST),
                    success=lambda waits: "Parts added; the job waits in Awaiting Parts for the ones out of stock."
                    if waits else "Parts added; they come off stock when you mark the job ready.")
        elif action == "complete":
            attempt(request, services.complete_repair, job, user, request.POST.get("repair_notes", ""),
                    _used_lines(request.POST), success="Ready for pickup. Parts taken off stock.")
        return redirect("bench_job", job.pk)

    ctx = {"mine": mine, "open_jobs": open_jobs, "job": job}
    if job:
        quotes = list(job.quotes.order_by("quote_id").prefetch_related("lines__part"))
        parts = picker_parts(store, job.device.model)
        on_hand = {p.pk: p.on_hand for p in parts}
        plan = [{"part": p, "qty": q, "on_hand": on_hand.get(p.pk, 0)} for p, q in services.planned_parts(job)]
        ctx.update({
            "steps": _steps(job), "quote": quotes[-1] if quotes else None, "quotes": quotes,
            "has_approved": any(q.decision == m.Q_APPROVED for q in quotes), "parts": parts, "plan": plan,
            "used": job.parts.filter(part_status=m.PART_USED).select_related("part"),
            "needed": job.parts.filter(part_status=m.PART_NEEDED).select_related("part", "purchase_order"),
            "history": job.history.select_related("changed_by"),
            "passcode": decrypt_passcode(job.device_passcode) if can_see_passcode(user, job) else None,
            "has_email": bool(job.customer.email),
        })
    return render(request, "shop/bench.html", ctx)
