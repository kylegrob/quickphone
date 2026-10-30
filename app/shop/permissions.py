"""Role-based access (NFR01). Every rule is checked on the server; templates only
hide what a role cannot use."""
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.urls import reverse

from .models import FRONT_DESK, MANAGER, OWNER, TECHNICIAN, ScreenAccess, Store, StorePartStock

DESK_ROLES = (OWNER, MANAGER, FRONT_DESK)        # job list, approval, payment, release
CHECKIN_ROLES = DESK_ROLES + (TECHNICIAN,)       # check-in, appointments, claim ticket (owner, 2026-10-30)
EMAIL_ROLES = (OWNER, MANAGER, FRONT_DESK, TECHNICIAN)  # owner Oct 23 #1, approved for build 2026-10-28
BENCH_ROLES = (TECHNICIAN, MANAGER, OWNER)       # diagnosis, quote, repair work (owner, 2026-10-30)
PRICE_ROLES = (OWNER,)                           # labor cost per part is set by the Owner (2026-10-30)
STOCK_ROLES = (OWNER, MANAGER)                   # inventory, purchase orders, suppliers, staff
PO_APPROVER_ROLES = (OWNER, MANAGER)             # owner Oct 23 #2
PASSCODE_ROLES = (OWNER, MANAGER)                # plus the assigned technician (decision 2026-10-28)

# Open question to the owner: may a Manager approve an order they created?
# The team chose to allow it for now (2026-10-28); history keeps both names.
ALLOW_SELF_APPROVAL_OF_PO = True


# Screens the Owner can open or close for each role. Defaults are what each role could open before
# the matrix existed. Business rules (who approves an order, who sees a passcode or contact details,
# own-job work, the Owner role) stay in code and do not change with screen access.
SCREENS = {
    "dashboard": ("Dashboard", (OWNER,)),
    "checkin": ("Check in, appointments and claim tickets", CHECKIN_ROLES),
    "jobs": ("Repair jobs: customer approval, payment, release", DESK_ROLES),
    "bench": ("My repair jobs: diagnosis, quotes, repair work", BENCH_ROLES),
    "inventory": ("Inventory and parts", STOCK_ROLES),
    "orders": ("Purchase orders", STOCK_ROLES),
    "staff": ("Staff, suppliers and stores", STOCK_ROLES),
}


def _overrides(request):
    if getattr(request, "_screen_overrides", None) is None:
        request._screen_overrides = {
            (role, screen): allowed for role, screen, allowed in ScreenAccess.objects.values_list(
                "role", "screen", "allowed")
        }
    return request._screen_overrides


def screen_default(role, screen):
    return role in SCREENS[screen][1]


def can_open(request, screen):
    user = request.user
    if not user.is_authenticated:
        return False
    return _overrides(request).get((user.role, screen), screen_default(user.role, screen))


def screen_required(screen):
    """Opens a screen only to the roles the Owner has allowed (NFR01)."""
    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if not can_open(request, screen):
                raise PermissionDenied("Your role cannot use this page.")
            return view(request, *args, **kwargs)
        return wrapped
    return decorator


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


# screen key, label, URL name
NAV = [
    ("dashboard", "Dashboard", "dashboard"),
    ("checkin", "Check in", "checkin"),
    ("jobs", "Repair jobs", "jobs"),
    ("bench", "My repair jobs", "bench"),
    ("inventory", "Inventory", "inventory"),
    ("orders", "Purchase orders", "po_list"),
    ("staff", "Staff and suppliers", "staff"),
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
        "po_list": "orders", "po_detail": "orders", "access": "access",
        "staff": "staff", "staff_new": "staff", "staff_edit": "staff", "supplier_new": "staff",
        "supplier_edit": "staff", "store_edit": "staff",
    }.get(current, "")
    ctx = {
        "nav_items": [(reverse(url), label, key == section) for key, label, url in NAV if can_open(request, key)]
        + ([(reverse("access"), "Access", section == "access")] if user.role == OWNER else []),
        "active_store": request.store,
        "open_screens": {key: can_open(request, key) for key in SCREENS},
    }
    if user.role == OWNER:
        ctx["all_stores"] = Store.objects.all()
    if can_open(request, "inventory") and request.store:
        ctx["low_stock_count"] = sum(
            1 for s in StorePartStock.objects.filter(store=request.store, part__active_flag=True) if s.is_low
        )
    return ctx
