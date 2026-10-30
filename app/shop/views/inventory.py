"""Manager screens: parts inventory, CSV import and purchase orders (Prototype A, slide 4)."""
import csv
import io
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .. import models as m
from .. import services
from ..permissions import PRICE_ROLES, screen_required
from .common import attempt, to_int


def _rows(store):
    stock = {s.part_id: s for s in m.StorePartStock.objects.filter(store=store)}
    open_lines = {}
    for line in m.POLine.objects.filter(purchase_order__store=store).exclude(
            purchase_order__po_status=m.PO_RECEIVED).select_related("purchase_order"):
        open_lines.setdefault(line.part_id, line.purchase_order)
    rows = []
    for part in m.Part.objects.filter(active_flag=True).select_related("default_supplier"):
        s = stock.get(part.pk) or m.StorePartStock(store=store, part=part)
        rows.append({"part": part, "stock": s, "po": open_lines.get(part.pk)})
    return rows


@screen_required("inventory")
def inventory(request):
    store, user = request.store, request.user
    if request.method == "POST":
        part = get_object_or_404(m.Part, pk=request.POST.get("part_id"))
        action = request.POST.get("action")
        if action == "adjust":
            attempt(request, services.adjust_stock, store, part, to_int(request.POST.get("change")),
                    request.POST.get("reason"), user, success=f"Stock of {part} adjusted.")
        elif action == "reorder":
            attempt(request, services.set_reorder_point, store, part, to_int(request.POST.get("reorder_point"), -1),
                    user, success=f"Reorder point for {part} saved.")
        elif action == "add_to_po":
            if attempt(request, services.add_to_po, store, part, to_int(request.POST.get("quantity"), 1), user,
                       success=lambda po: f"Added to draft {po.number} for {part.default_supplier}."):
                po = m.PurchaseOrder.objects.filter(store=store, supplier=part.default_supplier,
                                                    po_status=m.PO_DRAFT).first()
                return redirect("po_detail", po.pk)
        return redirect(request.get_full_path())

    rows = _rows(store)
    q, low_only = request.GET.get("q", "").strip().lower(), request.GET.get("low") == "1"
    shown = [r for r in rows
             if (not q or q in f"{r['part'].sku} {r['part'].part_name} {r['part'].device_model}".lower())
             and (not low_only or r["stock"].is_low)]
    waiting = m.RepairJob.objects.filter(store=store, status=m.AWAITING_PARTS)
    return render(request, "shop/inventory.html", {
        "rows": shown, "q": request.GET.get("q", ""), "low_only": low_only,
        "tracked": len(rows), "low": sum(r["stock"].is_low for r in rows), "out": sum(r["stock"].is_out for r in rows),
        "waiting": waiting, "low_rows": [r for r in rows if r["stock"].is_low],
        "orders": m.PurchaseOrder.objects.filter(store=store).exclude(po_status=m.PO_RECEIVED).select_related("supplier"),
    })


@screen_required("inventory")
def part_edit(request, pk=None):
    part = get_object_or_404(m.Part, pk=pk) if pk else m.Part()
    stock = m.StorePartStock.objects.filter(store=request.store, part=part).first() if pk else None
    if request.method == "POST":
        p = request.POST
        errors = []
        try:
            cost = Decimal(p.get("standard_cost", ""))
            if cost < 0:
                raise InvalidOperation
        except InvalidOperation:
            errors.append("Enter a unit cost of 0 or more.")
            cost = None
        labor = part.labor_cost
        if request.user.role in PRICE_ROLES:
            try:
                labor = Decimal(p.get("labor_cost") or "0")
                if labor < 0:
                    raise InvalidOperation
            except InvalidOperation:
                errors.append("Enter a labor cost of 0 or more.")
        if not p.get("sku", "").strip() or not p.get("part_name", "").strip():
            errors.append("Enter the SKU and part name.")
        elif m.Part.objects.filter(sku__iexact=p["sku"].strip()).exclude(pk=part.pk).exists():
            errors.append("Another part already uses this SKU.")
        if not errors:
            part.sku, part.part_name = p["sku"].strip().upper(), p["part_name"].strip()
            part.device_model, part.grade = p.get("device_model", "").strip() or None, p.get("grade", "").strip() or None
            part.standard_cost = cost
            if request.user.role in PRICE_ROLES:
                part.labor_cost = labor
            part.default_supplier = m.Supplier.objects.filter(pk=p.get("supplier_id") or 0).first()
            part.active_flag = p.get("active_flag") == "on" if pk else True
            with transaction.atomic():
                part.save()
                if not pk:
                    m.StorePartStock.objects.create(store=request.store, part=part,
                                                    reorder_point=max(to_int(p.get("reorder_point")), 0))
                    opening = to_int(p.get("quantity_on_hand"))
                    if opening > 0:
                        services.adjust_stock(request.store, part, opening, "Opening count", request.user,
                                              m.TXN_ADJUSTMENT)
            messages.success(request, f"{part} saved.")
            return redirect("inventory")
        for e in errors:
            messages.error(request, e)
    return render(request, "shop/part_form.html", {
        "part": part, "stock": stock, "can_price": request.user.role in PRICE_ROLES, "suppliers": m.Supplier.objects.filter(active_flag=True),
        "txns": m.InventoryTxn.objects.filter(store=request.store, part=part).select_related("recorded_by")[:15]
        if pk else [],
    })


IMPORT_COLUMNS = ["sku", "part_name", "device_model", "grade", "standard_cost", "supplier",
                  "quantity_on_hand", "reorder_point"]


@screen_required("inventory")
def import_csv(request):
    """FR11: import existing parts. The whole file is checked first; if any row is
    invalid nothing is imported and every bad row is listed, so no data is lost silently."""
    report = None
    if request.method == "POST" and request.FILES.get("file"):
        text = request.FILES["file"].read().decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(io.StringIO(text))
        missing = [c for c in IMPORT_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            messages.error(request, "Missing columns: " + ", ".join(missing))
            return redirect("inventory_import")
        suppliers = {s.supplier_name.lower(): s for s in m.Supplier.objects.all()}
        existing = {sku.lower() for sku in m.Part.objects.values_list("sku", flat=True)}
        good, bad, seen = [], [], set()
        for n, row in enumerate(reader, start=2):
            problems = []
            sku = (row.get("sku") or "").strip()
            if not sku:
                problems.append("SKU is empty")
            elif sku.lower() in existing or sku.lower() in seen:
                problems.append(f"SKU {sku} already exists")
            if not (row.get("part_name") or "").strip():
                problems.append("part name is empty")
            try:
                cost = Decimal((row.get("standard_cost") or "").strip().lstrip("$"))
                if cost < 0:
                    raise InvalidOperation
            except InvalidOperation:
                problems.append("unit cost is not a number of 0 or more")
                cost = None
            supplier_name = (row.get("supplier") or "").strip()
            if supplier_name and supplier_name.lower() not in suppliers:
                problems.append(f"supplier '{supplier_name}' is not on file")
            qty, reorder = to_int(row.get("quantity_on_hand"), -1), to_int(row.get("reorder_point"), -1)
            if qty < 0 or reorder < 0:
                problems.append("quantity and reorder point must be whole numbers of 0 or more")
            if problems:
                bad.append((n, sku or "(blank)", "; ".join(problems)))
            else:
                seen.add(sku.lower())
                good.append((row, cost, suppliers.get(supplier_name.lower()), qty, reorder))
        if bad:
            report = {"bad": bad, "good_count": len(good)}
        elif good:
            with transaction.atomic():
                for row, cost, supplier, qty, reorder in good:
                    part = m.Part.objects.create(
                        sku=row["sku"].strip().upper(), part_name=row["part_name"].strip(),
                        device_model=(row.get("device_model") or "").strip() or None,
                        grade=(row.get("grade") or "").strip() or None, standard_cost=cost, default_supplier=supplier)
                    m.StorePartStock.objects.create(store=request.store, part=part, reorder_point=reorder)
                    if qty:
                        services.adjust_stock(request.store, part, qty, "Imported from CSV", request.user, m.TXN_IMPORT)
            messages.success(request, f"Imported {len(good)} parts into {request.store}.")
            return redirect("inventory")
        else:
            messages.error(request, "The file has no rows.")
    return render(request, "shop/import.html", {"columns": IMPORT_COLUMNS, "report": report})


# Purchase orders (UC-08 to UC-10) ---------------------------------------------

@screen_required("orders")
def po_list(request):
    status = request.GET.get("status", "")
    orders = m.PurchaseOrder.objects.filter(store=request.store).select_related("supplier", "created_by", "approved_by")
    if status in m.PO_STATUSES:
        orders = orders.filter(po_status=status)
    counts = {s: m.PurchaseOrder.objects.filter(store=request.store, po_status=s).count() for s in m.PO_STATUSES}
    return render(request, "shop/po_list.html", {"orders": orders, "status": status, "counts": counts})


@screen_required("orders")
def po_detail(request, pk):
    po = get_object_or_404(m.PurchaseOrder.objects.select_related("supplier", "store"), pk=pk, store=request.store)
    user = request.user
    if request.method == "POST":
        action, p = request.POST.get("action"), request.POST
        if action == "save_lines" and po.po_status == m.PO_DRAFT:
            for line in po.lines.all():
                n = to_int(p.get(f"qty_{line.pk}"), line.quantity_ordered)
                if n <= 0 or p.get(f"remove_{line.pk}"):
                    line.delete()
                else:
                    line.quantity_ordered = n
                    line.save()
            part = m.Part.objects.filter(pk=p.get("add_part_id") or 0).first()
            if part:
                attempt(request, services.add_to_po, po.store, part, to_int(p.get("add_quantity"), 1), user)
            messages.success(request, "Order lines saved.")
        elif action == "submit":
            ids = [to_int(i) for i in p.getlist("link_job_part")]
            attempt(request, services.submit_po, po, user, ids, success="Submitted for a Manager's approval.")
        elif action == "approve":
            attempt(request, services.approve_po, po, user, success="Order approved. It can now be placed.")
        elif action == "reject":
            attempt(request, services.reject_po, po, user, p.get("reason"), success="Returned to Draft with your reason.")
        elif action == "ordered":
            attempt(request, services.mark_ordered, po, user, success="Marked as ordered from the supplier.")
        elif action == "receive":
            received = {line.pk: to_int(p.get(f"recv_{line.pk}")) for line in po.lines.all()}
            attempt(request, services.receive_po, po, user, received,
                    success=lambda jobs: "Stock received." + (
                        " Back to In Repair: " + ", ".join(j.ticket_number for j in jobs) if jobs else ""))
        elif action == "delete" and po.po_status == m.PO_DRAFT:
            po.delete()
            messages.success(request, "Draft deleted.")
            return redirect("po_list")
        return redirect("po_detail", po.pk)
    return render(request, "shop/po_detail.html", {
        "po": po, "lines": po.lines.select_related("part"), "waiting": services.waiting_job_parts(po),
        "linked": po.linked_job_parts.select_related("repair_job", "part"),
        "supplier_parts": m.Part.objects.filter(default_supplier=po.supplier, active_flag=True),
    })
