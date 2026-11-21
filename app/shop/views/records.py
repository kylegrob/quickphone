"""Home routing, the Owner's dashboard (FR13) and shop records: staff, suppliers, stores (FR14)."""
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import ValidationError, validate_password
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from ..audit import record
from .. import models as m
from .. import services
from ..permissions import NAV, SCREENS, can_open, role_required, screen_required
from ..auth import is_locked, minutes_left
from .common import keep_typed, to_int

HOME = {m.OWNER: "dashboard", m.MANAGER: "inventory", m.TECHNICIAN: "bench", m.FRONT_DESK: "checkin"}


@login_required
def home(request):
    """The role's usual first screen, or the first one the Owner has left open to it."""
    urls = {key: url for key, _, url in NAV}
    first = [k for k, url in urls.items() if url == HOME[request.user.role]]
    for key in first + list(urls):
        if can_open(request, key):
            return redirect(urls[key])
    raise PermissionDenied("No screens are open to your role. Ask the Owner.")


@role_required(m.OWNER)
def switch_store(request):
    if request.method == "POST":
        store = get_object_or_404(m.Store, pk=to_int(request.POST.get("store_id")))
        request.session["store_id"] = store.pk
    target = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        target = "home"
    return redirect(target or "home")


@screen_required("dashboard")
def dashboard(request):
    stores = []
    scope = m.Store.objects.all() if request.user.role == m.OWNER else m.Store.objects.filter(pk=request.user.store_id)
    for store in scope:
        jobs = m.RepairJob.objects.filter(store=store)
        low = [s for s in m.StorePartStock.objects.filter(store=store, part__active_flag=True).select_related("part")
               if s.is_low]
        stores.append({
            "store": store,
            "by_status": [(s, jobs.filter(status=s).count()) for s in m.OPEN_STATUSES],
            "open": jobs.exclude(status=m.CLOSED).count(),
            "low": sorted(low, key=lambda s: (s.quantity_on_hand, s.part.part_name)),
            "pending_pos": m.PurchaseOrder.objects.filter(store=store, po_status=m.PO_PENDING).count(),
        })
    return render(request, "shop/dashboard.html", {"stores": stores})


def _staff_scope(user):
    qs = m.Employee.objects.select_related("store")
    return qs if user.role == m.OWNER else qs.filter(store=user.store)


@screen_required("staff")
def staff(request):
    return render(request, "shop/staff.html", {
        "staff": _staff_scope(request.user).order_by("store_id", "role", "first_name"),
        "locked": {e.pk for e in _staff_scope(request.user) if is_locked(e.email)},
        "can_manage_staff": request.user.role in (m.OWNER, m.MANAGER),
        "suppliers": m.Supplier.objects.all(),
        "repair_types": m.RepairType.objects.all(),
        "stores": m.Store.objects.all() if request.user.role == m.OWNER else [request.user.store],
    })


@screen_required("staff")
@role_required(m.OWNER, m.MANAGER)
def staff_edit(request, pk=None):
    user = request.user
    employee = get_object_or_404(_staff_scope(user), pk=pk) if pk else m.Employee(store=user.store)
    if pk and employee.role in (m.OWNER, m.MANAGER) and user.role != m.OWNER:
        # Managers may update their own profile, but cannot reset a peer's credentials.
        if employee.pk != user.pk:
            record("staff_change", user, employee, outcome="Denied")
            raise PermissionDenied("Only the Owner can change a Manager or Owner account.")

    stores = m.Store.objects.all() if user.role == m.OWNER else m.Store.objects.filter(pk=user.store_id)
    roles = [r for r in m.ROLES if services.can_assign_role(user, r)]
    if employee.pk == user.pk and user.role == m.MANAGER:
        roles = [m.MANAGER]

    if request.method == "POST":
        p, errors = request.POST, []
        role = p.get("role")
        if role not in roles:
            errors.append("Only the Owner can give the Owner or Manager role.")
            record("staff_change", user, employee if pk else None, outcome="Denied")
        store = stores.filter(pk=to_int(p.get("store_id"))).first()
        if not store:
            errors.append("Pick a store.")
        email = p.get("email", "").strip().lower()
        if not (p.get("first_name", "").strip() and p.get("last_name", "").strip() and email):
            errors.append("Enter the first name, last name and email.")
        elif m.Employee.objects.filter(email__iexact=email).exclude(pk=employee.pk).exists():
            errors.append("Another account uses this email.")
        password = p.get("password", "")
        if not pk and not password:
            errors.append("Set a starting password.")
        if password:
            try:
                validate_password(password)
            except ValidationError as exc:
                errors.extend(exc.messages)
        if employee.pk == user.pk and (role != user.role or p.get("active_flag") != "on"):
            errors.append("You cannot change your own role or deactivate yourself.")
        if not errors:
            employee.first_name, employee.last_name = p["first_name"].strip(), p["last_name"].strip()
            employee.email, employee.role, employee.store = email, role, store
            employee.active_flag = p.get("active_flag") == "on" if pk else True
            if password:
                employee.set_password(password)
            with transaction.atomic():
                employee.save()
                record("staff_updated" if pk else "staff_created", user, employee,
                       store=employee.store, role=role, active=employee.active_flag,
                       password_changed=bool(password))
            messages.success(request, f"{employee} saved.")
            return redirect("staff")
        for e in errors:
            messages.error(request, e)
    stored_email = employee.email
    invalid = set()
    if request.method == "POST":  # refused: show what was typed (never the password)
        keep_typed(employee, request.POST, ["first_name", "last_name", "email"])
        if request.POST.get("role") in roles:
            employee.role = request.POST["role"]
        employee.store_id = to_int(request.POST.get("store_id")) or employee.store_id
        for e in errors:
            if e == "Enter the first name, last name and email.":
                invalid |= {f for f in ("first_name", "last_name", "email") if not request.POST.get(f, "").strip()}
            elif e == "Another account uses this email.":
                invalid.add("email")
            elif e == "Pick a store.":
                invalid.add("store")
            elif "role" in e:
                invalid.add("role")
            else:  # "Set a starting password." and the password validators' messages
                invalid.add("password")
    locked = bool(pk) and is_locked(stored_email)
    return render(request, "shop/staff_form.html", {
        "employee": employee, "stores": stores, "roles": roles, "invalid": invalid,
        "locked": locked, "lock_minutes": minutes_left(stored_email) if locked else None,
    })


@screen_required("staff")
@role_required(m.OWNER, m.MANAGER)
def supplier_edit(request, pk=None):
    supplier = get_object_or_404(m.Supplier, pk=pk) if pk else m.Supplier()
    if request.method == "POST":
        p = request.POST
        name = p.get("supplier_name", "").strip()
        if not name:
            messages.error(request, "Enter the supplier's name.")
        elif m.Supplier.objects.filter(supplier_name__iexact=name).exclude(pk=supplier.pk).exists():
            messages.error(request, "A supplier with this name exists.")
        else:
            supplier.supplier_name = name
            for field in ("contact_name", "phone", "email"):
                setattr(supplier, field, p.get(field, "").strip() or None)
            supplier.active_flag = p.get("active_flag") == "on" if pk else True
            with transaction.atomic():
                supplier.save()
                record("supplier_updated" if pk else "supplier_created", request.user, supplier)
            messages.success(request, f"{supplier} saved.")
            return redirect("staff")
        keep_typed(supplier, p, ["supplier_name", "contact_name", "phone", "email"])
    invalid = {"supplier_name"} if request.method == "POST" else set()
    return render(request, "shop/supplier_form.html", {"supplier": supplier, "invalid": invalid})


@screen_required("staff")
@role_required(m.OWNER)
def repair_type_edit(request, pk=None):
    """How long an appointment for each kind of repair holds a technician (2026-11-20)."""
    repair_type = get_object_or_404(m.RepairType, pk=pk) if pk else m.RepairType()
    if request.method == "POST":
        p = request.POST
        name, minutes = " ".join(p.get("type_name", "").split()), to_int(p.get("slot_minutes"))
        low, high = services.MIN_APPOINTMENT_MINUTES, services.MAX_APPOINTMENT_MINUTES
        if not name:
            messages.error(request, "Enter the repair type's name.")
        elif len(name) > 60:
            messages.error(request, "The name is too long.")
        elif m.RepairType.objects.filter(type_name__iexact=name).exclude(pk=repair_type.pk).exists():
            messages.error(request, "A repair type with this name exists.")
        elif minutes is None or not low <= minutes <= high or minutes % 15:
            messages.error(request, f"Set the appointment length in steps of 15, from {low} to {high} minutes.")
        else:
            repair_type.type_name, repair_type.slot_minutes = name, minutes
            repair_type.active_flag = p.get("active_flag") == "on" if pk else True
            with transaction.atomic():
                repair_type.save()
                record("repair_type_updated" if pk else "repair_type_created", request.user, repair_type)
            messages.success(request, f"{repair_type} saved. Appointments already booked keep their length.")
            return redirect("staff")
        keep_typed(repair_type, p, ["type_name", "slot_minutes"])
        invalid = {"slot_minutes"} if name and len(name) <= 60 and not m.RepairType.objects.filter(
            type_name__iexact=name).exclude(pk=repair_type.pk).exists() else {"type_name"}
    else:
        invalid = set()
    return render(request, "shop/repair_type_form.html", {"repair_type": repair_type, "invalid": invalid})


@screen_required("staff")
@role_required(m.OWNER, m.MANAGER)
def store_edit(request, pk):
    if request.user.role != m.OWNER and request.user.store_id != pk:
        raise PermissionDenied("Managers maintain their own store only.")
    store = get_object_or_404(m.Store, pk=pk)
    if request.method == "POST":
        p = request.POST
        if not all(p.get(f, "").strip() for f in ("store_name", "address", "phone", "email_address")):
            messages.error(request, "Enter the name, address, phone and email address.")
        else:
            for field in ("store_name", "address", "phone", "email_address", "business_hours"):
                setattr(store, field, p.get(field, "").strip() or None)
            with transaction.atomic():
                store.save()
                record("store_updated", request.user, store)
            messages.success(request, f"{store} saved.")
            return redirect("staff")
    return render(request, "shop/store_form.html", {"store": store})


# Access: which roles open which screen (NFR01, 2026-10-30) ---------------------------

@role_required(m.OWNER)
def access(request):
    """Owner-only, and not itself in the matrix, so the Owner cannot lock themselves out."""
    if request.method == "POST":
        if request.POST.get("action") == "reset":
            with transaction.atomic():
                previous = list(m.ScreenAccess.objects.values("role", "screen", "allowed"))
                m.ScreenAccess.objects.all().delete()
                record("screen_access_reset", request.user, previous=previous)
            messages.success(request, "Every screen is back to its default access.")
            return redirect("access")
        with transaction.atomic():
            for screen, (_, defaults) in SCREENS.items():
                for role in m.ROLES:
                    want = request.POST.get(f"{screen}|{role}") == "on"
                    previous = m.ScreenAccess.objects.filter(role=role, screen=screen).first()
                    before = previous.allowed if previous else role in defaults
                    if before != want:
                        record("screen_access_changed", request.user, role=role, screen=screen,
                               before=before, allowed=want)
                    if want == (role in defaults):
                        m.ScreenAccess.objects.filter(role=role, screen=screen).delete()
                    else:
                        m.ScreenAccess.objects.update_or_create(
                            role=role, screen=screen, defaults={"allowed": want, "updated_by": request.user})
        messages.success(request, "Access saved.")
        return redirect("access")
    overrides = {(a.role, a.screen): a for a in m.ScreenAccess.objects.select_related("updated_by")}
    rows = []
    for screen, (label, defaults) in SCREENS.items():
        cells = []
        for role in m.ROLES:
            override = overrides.get((role, screen))
            cells.append({"role": role, "name": f"{screen}|{role}", "on": override.allowed if override else role in defaults,
                          "changed": override is not None})
        rows.append({"label": label, "cells": cells})
    return render(request, "shop/access.html", {"rows": rows, "roles": m.ROLES})


@role_required(m.OWNER)
def audit_events(request):
    events = m.AuditEvent.objects.select_related("actor", "store")
    return render(request, "shop/audit_events.html", {"page": Paginator(events, 50).get_page(request.GET.get("page"))})
