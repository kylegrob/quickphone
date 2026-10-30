"""Home routing, the Owner's dashboard (FR13) and shop records: staff, suppliers, stores (FR14)."""
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import ValidationError, validate_password
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .. import models as m
from .. import services
from ..permissions import NAV, SCREENS, can_open, role_required, screen_required

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
        store = get_object_or_404(m.Store, pk=request.POST.get("store_id"))
        request.session["store_id"] = store.pk
    target = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        target = "home"
    return redirect(target or "home")


@screen_required("dashboard")
def dashboard(request):
    stores = []
    for store in m.Store.objects.all():
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
        "suppliers": m.Supplier.objects.all(),
        "stores": m.Store.objects.all() if request.user.role == m.OWNER else [request.user.store],
    })


@screen_required("staff")
def staff_edit(request, pk=None):
    user = request.user
    employee = get_object_or_404(_staff_scope(user), pk=pk) if pk else m.Employee(store=user.store)
    if pk and employee.role == m.OWNER and user.role != m.OWNER:
        raise PermissionDenied("Only the Owner can change an Owner account.")
    stores = m.Store.objects.all() if user.role == m.OWNER else m.Store.objects.filter(pk=user.store_id)
    roles = [r for r in m.ROLES if services.can_assign_role(user, r)]
    if request.method == "POST":
        p, errors = request.POST, []
        role = p.get("role")
        if not services.can_assign_role(user, role):
            errors.append("Only the Owner can give the Owner role.")
        store = stores.filter(pk=p.get("store_id") or 0).first()
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
            employee.save()
            messages.success(request, f"{employee} saved.")
            return redirect("staff")
        for e in errors:
            messages.error(request, e)
    return render(request, "shop/staff_form.html", {"employee": employee, "stores": stores, "roles": roles})


@screen_required("staff")
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
            supplier.save()
            messages.success(request, f"{supplier} saved.")
            return redirect("staff")
    return render(request, "shop/supplier_form.html", {"supplier": supplier})


@screen_required("staff")
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
            store.save()
            messages.success(request, f"{store} saved.")
            return redirect("staff")
    return render(request, "shop/store_form.html", {"store": store})


# Access: which roles open which screen (NFR01, 2026-10-30) ---------------------------

@role_required(m.OWNER)
def access(request):
    """Owner-only, and not itself in the matrix, so the Owner cannot lock themselves out."""
    if request.method == "POST":
        if request.POST.get("action") == "reset":
            m.ScreenAccess.objects.all().delete()
            messages.success(request, "Every screen is back to its default access.")
            return redirect("access")
        with transaction.atomic():
            for screen, (_, defaults) in SCREENS.items():
                for role in m.ROLES:
                    want = request.POST.get(f"{screen}|{role}") == "on"
                    if want == (role in defaults):
                        m.ScreenAccess.objects.filter(role=role, screen=screen).delete()
                    else:
                        m.ScreenAccess.objects.update_or_create(
                            role=role, screen=screen, defaults={"allowed": want, "updated_by": request.user})
        messages.success(request, "Access saved. It applies the next time each person opens a screen.")
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
