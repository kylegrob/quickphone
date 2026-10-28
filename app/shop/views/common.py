from django.contrib import messages
from django.shortcuts import get_object_or_404

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
