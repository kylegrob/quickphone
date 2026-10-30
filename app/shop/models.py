"""Tables of the physical ERD (Sprint 3 DFD and ERD Models, Appendix A).

Table and column names match the physical data dictionary. Two additions were
approved during the Sprint 4 build (2026-10-28) and must be carried into the ERD:
QUOTE_LINE in D3 (the parts on a quote) and PART.sku.
"""
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q

OWNER, MANAGER, TECHNICIAN, FRONT_DESK = "Owner", "Manager", "Technician", "Front Desk"
ROLES = [OWNER, MANAGER, TECHNICIAN, FRONT_DESK]
DEVICE_TYPES = ["Phone", "Tablet", "Laptop", "Game console", "Other"]

CHECKED_IN, DIAGNOSING, AWAITING_APPROVAL, IN_REPAIR = "Checked In", "Diagnosing", "Awaiting Approval", "In Repair"
AWAITING_PARTS, READY, UNREPAIRED, CLOSED = "Awaiting Parts", "Ready for Pickup", "Returned Unrepaired", "Closed"
JOB_STATUSES = [CHECKED_IN, DIAGNOSING, AWAITING_APPROVAL, IN_REPAIR, AWAITING_PARTS, READY, UNREPAIRED, CLOSED]
OPEN_STATUSES = [s for s in JOB_STATUSES if s != CLOSED]

PO_DRAFT, PO_PENDING, PO_APPROVED, PO_ORDERED, PO_RECEIVED = "Draft", "Pending Approval", "Approved", "Ordered", "Received"
PO_STATUSES = [PO_DRAFT, PO_PENDING, PO_APPROVED, PO_ORDERED, PO_RECEIVED]


def choices(values):
    return [(v, v) for v in values]


# D7 Staff & Stores -------------------------------------------------------------

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=60, unique=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email_address = models.EmailField(max_length=120)
    business_hours = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = "store"
        ordering = ["store_id"]

    def __str__(self):
        return self.store_name


class EmployeeManager(BaseUserManager):
    def create_user(self, email, password, **fields):
        user = self.model(email=self.normalize_email(email), **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser):
    employee_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, db_column="store_id")
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=120, unique=True)
    role = models.CharField(max_length=12, choices=choices(ROLES))
    password = models.CharField(max_length=255, db_column="password_hash")
    active_flag = models.BooleanField(default=True)
    last_login = None  # not in the ERD

    objects = EmployeeManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    class Meta:
        db_table = "employee"
        ordering = ["first_name", "last_name"]
        constraints = [models.CheckConstraint(condition=Q(role__in=ROLES), name="employee_role_ck")]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.active_flag

    @property
    def is_owner(self):
        return self.role == OWNER

    @property
    def is_technician(self):
        return self.role == TECHNICIAN


class ScreenAccess(models.Model):
    """The Owner's override of which roles open which screen. No row means the default in
    permissions.SCREENS applies (2026-10-30)."""

    screen_access_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=12, choices=choices(ROLES))
    screen = models.CharField(max_length=20)
    allowed = models.BooleanField()
    updated_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, db_column="updated_by_id", null=True, blank=True, related_name="+"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "screen_access"
        constraints = [
            models.UniqueConstraint(fields=["role", "screen"], name="screen_access_uq"),
            models.CheckConstraint(condition=Q(role__in=ROLES), name="screen_access_role_ck"),
        ]


# D1 Customers & Devices --------------------------------------------------------

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "customer"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, db_column="customer_id", related_name="devices")
    device_type = models.CharField(max_length=20, blank=True, null=True)
    brand = models.CharField(max_length=40, blank=True, null=True)
    model = models.CharField(max_length=60)
    serial_or_imei = models.CharField(max_length=40, blank=True, null=True, db_index=True)

    class Meta:
        db_table = "device"

    def __str__(self):
        return " ".join(p for p in [self.brand, self.model] if p)


class DeviceModel(models.Model):
    """The list check-in picks a device from. Staff add a model here when it is missing (2026-10-30)."""

    device_model_id = models.AutoField(primary_key=True)
    device_type = models.CharField(max_length=20, choices=choices(DEVICE_TYPES))
    brand = models.CharField(max_length=40)
    model = models.CharField(max_length=60)

    class Meta:
        db_table = "device_model"
        ordering = ["brand", "model"]
        constraints = [models.UniqueConstraint(fields=["brand", "model"], name="device_model_uq")]

    def __str__(self):
        return f"{self.brand} {self.model}"


# D2 Appointments ---------------------------------------------------------------

APPT_BOOKED, APPT_CHECKED_IN, APPT_CANCELLED = "Booked", "Checked In", "Cancelled"


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, db_column="customer_id")
    store = models.ForeignKey(Store, on_delete=models.PROTECT, db_column="store_id")
    technician = models.ForeignKey(
        Employee, on_delete=models.PROTECT, db_column="technician_id", null=True, blank=True, related_name="+"
    )
    scheduled_at = models.DateTimeField()
    appt_status = models.CharField(
        max_length=12, default=APPT_BOOKED, choices=choices([APPT_BOOKED, APPT_CHECKED_IN, APPT_CANCELLED])
    )

    class Meta:
        db_table = "appointment"
        ordering = ["scheduled_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(appt_status__in=[APPT_BOOKED, APPT_CHECKED_IN, APPT_CANCELLED]), name="appt_status_ck"
            )
        ]


# D6 Suppliers ------------------------------------------------------------------

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100, unique=True)
    contact_name = models.CharField(max_length=80, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    active_flag = models.BooleanField(default=True)

    class Meta:
        db_table = "supplier"
        ordering = ["supplier_name"]

    def __str__(self):
        return self.supplier_name


# D4 Parts Inventory ------------------------------------------------------------

class Part(models.Model):
    part_id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=30, unique=True)  # added in Sprint 4 (Prototype A)
    default_supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, db_column="default_supplier_id", null=True, blank=True
    )
    part_name = models.CharField(max_length=100)
    device_model = models.CharField(max_length=60, blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True, null=True)
    standard_cost = models.DecimalField(max_digits=10, decimal_places=2)
    # Repair labor charged each time this part is fitted; set by the Owner (2026-10-30), feeds the quote.
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active_flag = models.BooleanField(default=True)

    class Meta:
        db_table = "part"
        ordering = ["part_name", "device_model"]
        constraints = [
            models.CheckConstraint(condition=Q(standard_cost__gte=0), name="part_cost_ck"),
            models.CheckConstraint(condition=Q(labor_cost__gte=0), name="part_labor_ck"),
        ]

    def __str__(self):
        return f"{self.part_name}, {self.device_model}" if self.device_model else self.part_name


class StorePartStock(models.Model):
    pk = models.CompositePrimaryKey("store_id", "part_id")
    store = models.ForeignKey(Store, on_delete=models.PROTECT, db_column="store_id")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, db_column="part_id", related_name="stock")
    quantity_on_hand = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)

    class Meta:
        db_table = "store_part_stock"
        constraints = [
            models.CheckConstraint(condition=Q(quantity_on_hand__gte=0), name="stock_not_negative_ck"),
            models.CheckConstraint(condition=Q(reorder_point__gte=0), name="reorder_point_ck"),
        ]

    @property
    def is_out(self):
        return self.quantity_on_hand == 0

    @property
    def is_low(self):
        return self.quantity_on_hand <= self.reorder_point


TXN_USED, TXN_RECEIVED, TXN_ADJUSTMENT, TXN_IMPORT = "Used", "Received", "Adjustment", "Import"


class InventoryTxn(models.Model):
    inventory_txn_id = models.BigAutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, db_column="store_id")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, db_column="part_id")
    recorded_by = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column="recorded_by_id")
    txn_type = models.CharField(max_length=12, choices=choices([TXN_USED, TXN_RECEIVED, TXN_ADJUSTMENT, TXN_IMPORT]))
    quantity_change = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True, null=True)
    txn_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_txn"
        ordering = ["-txn_at"]
        constraints = [
            models.CheckConstraint(condition=~Q(quantity_change=0), name="txn_change_not_zero_ck"),
            models.CheckConstraint(
                condition=Q(txn_type__in=[TXN_USED, TXN_RECEIVED, TXN_ADJUSTMENT, TXN_IMPORT]), name="txn_type_ck"
            ),
        ]


# D5 Purchase Orders ------------------------------------------------------------

class PurchaseOrder(models.Model):
    purchase_order_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, db_column="store_id")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, db_column="supplier_id")
    created_by = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column="created_by_id", related_name="+")
    approved_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, db_column="approved_by_id", null=True, blank=True, related_name="+"
    )
    po_status = models.CharField(max_length=20, default=PO_DRAFT, choices=choices(PO_STATUSES))
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    placed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = "purchase_order"
        ordering = ["-purchase_order_id"]
        constraints = [models.CheckConstraint(condition=Q(po_status__in=PO_STATUSES), name="po_status_ck")]

    @property
    def number(self):
        return f"PO-{2000 + self.purchase_order_id}"

    @property
    def total(self):
        return sum((line.quantity_ordered * line.unit_cost for line in self.lines.all()), 0)


class POLine(models.Model):
    po_line_id = models.AutoField(primary_key=True)
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, db_column="purchase_order_id", related_name="lines"
    )
    part = models.ForeignKey(Part, on_delete=models.PROTECT, db_column="part_id")
    quantity_ordered = models.IntegerField()
    quantity_received = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "po_line"
        constraints = [
            models.CheckConstraint(condition=Q(quantity_ordered__gt=0), name="po_line_qty_ck"),
            models.CheckConstraint(
                condition=Q(quantity_received__gte=0) & Q(quantity_received__lte=models.F("quantity_ordered")),
                name="po_line_received_ck",
            ),
            models.CheckConstraint(condition=Q(unit_cost__gte=0), name="po_line_cost_ck"),
        ]

    @property
    def line_total(self):
        return self.quantity_ordered * self.unit_cost

    @property
    def outstanding(self):
        return self.quantity_ordered - self.quantity_received


# D3 Repair Jobs ----------------------------------------------------------------

class RepairJob(models.Model):
    repair_job_id = models.AutoField(primary_key=True)
    ticket_number = models.CharField(max_length=12, unique=True)
    device = models.ForeignKey(Device, on_delete=models.PROTECT, db_column="device_id", related_name="jobs")
    store = models.ForeignKey(Store, on_delete=models.PROTECT, db_column="store_id")
    appointment = models.OneToOneField(
        Appointment, on_delete=models.PROTECT, db_column="appointment_id", null=True, blank=True
    )
    assigned_tech = models.ForeignKey(
        Employee, on_delete=models.PROTECT, db_column="assigned_tech_id", null=True, blank=True, related_name="jobs"
    )
    status = models.CharField(max_length=20, default=CHECKED_IN, choices=choices(JOB_STATUSES))
    reported_issue = models.CharField(max_length=500)
    device_passcode = models.CharField(max_length=255, blank=True, null=True)  # encrypted, see crypto.py
    intake_condition = models.CharField(max_length=500, blank=True, null=True)
    diagnosis_notes = models.CharField(max_length=2000, blank=True, null=True)
    repair_notes = models.CharField(max_length=2000, blank=True, null=True)
    check_in_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    email_sent_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, db_column="email_sent_by_id", null=True, blank=True, related_name="+"
    )
    email_status = models.CharField(max_length=10, blank=True, null=True, choices=choices(["Sent", "Failed"]))
    picked_up_at = models.DateTimeField(null=True, blank=True)
    id_verified_flag = models.BooleanField(default=False)
    signature_file = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "repair_job"
        ordering = ["-repair_job_id"]
        constraints = [
            models.CheckConstraint(condition=Q(status__in=JOB_STATUSES), name="job_status_ck"),
            models.CheckConstraint(condition=Q(final_cost__isnull=True) | Q(final_cost__gte=0), name="final_cost_ck"),
            models.CheckConstraint(
                condition=Q(picked_up_at__isnull=True) | Q(id_verified_flag=True), name="release_needs_id_ck"
            ),
        ]

    def __str__(self):
        return self.ticket_number

    @property
    def customer(self):
        return self.device.customer

    @property
    def current_quote(self):
        return self.quotes.order_by("-quote_id").first()

    @property
    def has_approved_quote(self):
        return self.quotes.filter(decision=Q_APPROVED).exists()

    @property
    def amount_paid(self):
        return sum((p.amount for p in self.payments.all()), 0)


class JobStatusHistory(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, db_column="repair_job_id", related_name="history")
    status = models.CharField(max_length=20, choices=choices(JOB_STATUSES))
    changed_by = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column="changed_by_id")
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = "job_status_history"
        ordering = ["-changed_at", "-history_id"]


Q_PENDING, Q_APPROVED, Q_DECLINED = "Pending", "Approved", "Declined"


class Quote(models.Model):
    quote_id = models.AutoField(primary_key=True)
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, db_column="repair_job_id", related_name="quotes")
    labor_amount = models.DecimalField(max_digits=10, decimal_places=2)
    parts_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # stored denormalization (ERD note)
    decision = models.CharField(max_length=10, default=Q_PENDING, choices=choices([Q_PENDING, Q_APPROVED, Q_DECLINED]))
    decision_at = models.DateTimeField(null=True, blank=True)
    decision_by = models.ForeignKey(
        Employee, on_delete=models.PROTECT, db_column="decision_by_id", null=True, blank=True, related_name="+"
    )

    class Meta:
        db_table = "quote"
        constraints = [
            models.CheckConstraint(condition=Q(labor_amount__gte=0) & Q(parts_amount__gte=0), name="quote_amounts_ck"),
            models.CheckConstraint(
                condition=Q(total_amount=models.F("labor_amount") + models.F("parts_amount")), name="quote_total_ck"
            ),
            models.CheckConstraint(condition=Q(decision__in=[Q_PENDING, Q_APPROVED, Q_DECLINED]), name="quote_decision_ck"),
        ]


class QuoteLine(models.Model):
    """Added in Sprint 4 (approved 2026-10-28): the parts a quote includes."""

    quote_line_id = models.AutoField(primary_key=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, db_column="quote_id", related_name="lines")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, db_column="part_id")
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "quote_line"
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gt=0), name="quote_line_qty_ck"),
            models.CheckConstraint(condition=Q(unit_cost__gte=0), name="quote_line_cost_ck"),
        ]

    @property
    def line_total(self):
        return self.quantity * self.unit_cost


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    repair_job = models.ForeignKey(RepairJob, on_delete=models.PROTECT, db_column="repair_job_id", related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=12, choices=choices(["Card", "Cash"]))
    payment_status = models.CharField(max_length=10, default="Paid", choices=choices(["Paid"]))
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment"
        constraints = [
            models.CheckConstraint(condition=Q(amount__gt=0), name="payment_amount_ck"),
            models.CheckConstraint(condition=Q(method__in=["Card", "Cash"]), name="payment_method_ck"),
        ]


PART_NEEDED, PART_USED = "Needed", "Used"


class JobPart(models.Model):
    job_part_id = models.AutoField(primary_key=True)
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, db_column="repair_job_id", related_name="parts")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, db_column="part_id")
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.SET_NULL, db_column="purchase_order_id", null=True, blank=True,
        related_name="linked_job_parts",
    )
    quantity = models.IntegerField()
    part_status = models.CharField(max_length=8, choices=choices([PART_NEEDED, PART_USED]))
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "job_part"
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gt=0), name="job_part_qty_ck"),
            models.CheckConstraint(condition=Q(part_status__in=[PART_NEEDED, PART_USED]), name="job_part_status_ck"),
        ]
