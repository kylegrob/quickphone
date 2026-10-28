"""Role-based access (NFR01). Every rule is checked on the server; templates only
hide what a role cannot use."""
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.urls import reverse

from .models import FRONT_DESK, MANAGER, OWNER, TECHNICIAN, Store, StorePartStock

DESK_ROLES = (OWNER, MANAGER, FRONT_DESK)        # check-in, appointments, approval, payment, release
EMAIL_ROLES = (OWNER, MANAGER, FRONT_DESK, TECHNICIAN)  # owner Oct 23 #1, approved for build 2026-10-28
BENCH_ROLES = (TECHNICIAN,)                      # diagnosis, quote, repair work
STOCK_ROLES = (OWNER, MANAGER)                   # inventory, purchase orders, suppliers, staff
PO_APPROVER_ROLES = (OWNER, MANAGER)             # owner Oct 23 #2
PASSCODE_ROLES = (OWNER, MANAGER)                # plus the assigned technician (decision 2026-10-28)

# Open question to the owner: may a Manager approve an order they created?
# The team chose to allow it for now (2026-10-28); history keeps both names.
ALLOW_SELF_APPROVAL_OF_PO = True


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if request.user.role not in roles:
                raise PermissionDenied("Your role cannot use this page.")
            return view(request, *args, **kwargs)
        return wrapped
    return decorator


def can_see_passcode(user, job):
    return user.role in PASSCODE_ROLES or (user.role == TECHNICIAN and job.assigned_tech_id == user.pk)


def can_see_contact(user):
    """Technicians never see customer phone or email (NFR04, client confirmation #6)."""
    return user.role != TECHNICIAN


class ActiveStoreMiddleware:
    """Sets request.store. Only the Owner works across both stores; everyone else,
    Managers included, is fixed to their home store (decision 2026-10-28)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.store = None
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            request.store = user.store
            if user.role == OWNER and request.session.get("store_id"):
                request.store = Store.objects.filter(pk=request.session["store_id"]).first() or user.store
        return self.get_response(request)


NAV = [
    ("dashboard", "Dashboard", (OWNER,)),
    ("checkin", "Check in", DESK_ROLES),
    ("jobs", "Repair jobs", DESK_ROLES),
    ("bench", "Technician jobs", BENCH_ROLES),
    ("inventory", "Inventory and POs", STOCK_ROLES),
    ("staff", "Staff and suppliers", STOCK_ROLES),
]


def nav_context(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {}
    current = request.resolver_match.url_name if request.resolver_match else ""
    section = {
        "checkin": "checkin", "appointment_new": "checkin", "appointment_edit": "checkin",
        "jobs": "jobs", "job_detail": "jobs", "job_ticket": "jobs",
        "bench": "bench", "dashboard": "dashboard",
        "inventory": "inventory", "part_new": "inventory", "part_edit": "inventory", "inventory_import": "inventory",
        "po_list": "inventory", "po_detail": "inventory",
        "staff": "staff", "staff_new": "staff", "staff_edit": "staff", "supplier_new": "staff",
        "supplier_edit": "staff", "store_edit": "staff",
    }.get(current, "")
    ctx = {
        "nav_items": [(reverse(name), label, name == section) for name, label, roles in NAV if user.role in roles],
        "active_store": request.store,
    }
    if user.role == OWNER:
        ctx["all_stores"] = Store.objects.all()
    if user.role in STOCK_ROLES and request.store:
        ctx["low_stock_count"] = sum(
            1 for s in StorePartStock.objects.filter(store=request.store, part__active_flag=True) if s.is_low
        )
    return ctx
