from django.contrib import messages
from django.shortcuts import get_object_or_404

from .. import models as m
from ..models import OWNER, RepairJob
from ..services import RuleError


def store_jobs(request):
    """Jobs the user may open: the Owner sees both stores, everyone else their own."""
    qs = RepairJob.objects.select_related("device__customer", "assigned_tech", "store")
    return qs if request.user.role == OWNER else qs.filter(store=request.user.store)


def get_job(request, pk):
    return get_object_or_404(store_jobs(request), pk=pk)


def attempt(request, fn, *args, success=None, **kwargs):
    """Runs a service call; shows its rule message instead of failing. Returns True on success."""
    try:
        result = fn(*args, **kwargs)
    except RuleError as exc:
        messages.error(request, str(exc))
        return False
    if success:
        messages.success(request, success(result) if callable(success) else success)
    return True


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def quote_lines(post):
    """(Part, quantity) pairs ticked on a parts picker (check-in and the bench)."""
    lines = []
    for p in m.Part.objects.filter(active_flag=True):
        n = to_int(post.get(f"qty_{p.pk}"))
        if post.get(f"use_{p.pk}") and n > 0:
            lines.append((p, n))
    return lines


def picker_parts(store, model="", post=None):
    """Active parts with this store's stock and the form's ticked state, likely picks for the device first."""
    stock = {s.part_id: s.quantity_on_hand for s in m.StorePartStock.objects.filter(store=store)}
    parts = list(m.Part.objects.filter(active_flag=True))
    for p in parts:
        p.on_hand = stock.get(p.pk, 0)
        p.checked = bool(post and post.get(f"use_{p.pk}"))
        p.qty = max(to_int(post.get(f"qty_{p.pk}"), 1), 1) if post else 1
    model = (model or "").lower()
    parts.sort(key=lambda p: (not (p.device_model and p.device_model.lower() in model), p.part_name))
    return parts
