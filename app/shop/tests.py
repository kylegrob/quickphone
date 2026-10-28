"""Tests named after the catalog acceptance checks (Sprint 3 Requirements Catalog)
plus the failure and security cases the course AI guidelines ask for."""
import io
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from . import models as m
from . import services as s
from .crypto import decrypt_passcode
from .management.commands.seed_training import TRAINING_PASSWORD, Command


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        Command().load()

    def setUp(self):
        self.store1 = m.Store.objects.get(store_name="Store 1")
        self.desk = m.Employee.objects.get(email="desk1@quickphone.test")
        self.sam = m.Employee.objects.get(email="sam@quickphone.test")
        self.jordan = m.Employee.objects.get(email="jordan@quickphone.test")
        self.manager = m.Employee.objects.get(email="manager1@quickphone.test")
        self.owner = m.Employee.objects.get(email="owner@quickphone.test")

    def login(self, user):
        self.client.force_login(user)

    def part(self, sku):
        return m.Part.objects.get(sku=sku)

    def on_hand(self, sku, store=None):
        return m.StorePartStock.objects.get(store=store or self.store1, part__sku=sku).quantity_on_hand

    def job(self, issue):
        return m.RepairJob.objects.get(reported_issue=issue)


class CheckInTests(Base):
    def test_fr02_fr03_walk_in_creates_job_with_ticket_and_history(self):
        self.login(self.desk)
        r = self.client.post(reverse("checkin"), {
            "first_name": "Test", "last_name": "Walkin", "phone": "(919) 555-0999", "email": "",
            "device_type": "Phone", "brand": "Apple", "model": "iPhone 11", "reported_issue": "Speaker crackles",
            "technician_id": "",
        })
        job = m.RepairJob.objects.get(reported_issue="Speaker crackles")
        self.assertRedirects(r, reverse("job_ticket", args=[job.pk]))
        self.assertEqual(job.ticket_number, f"QP-{1000 + job.pk}")
        self.assertEqual(job.status, m.CHECKED_IN)
        self.assertEqual(job.history.get().changed_by, self.desk)

    def test_fr02_duplicate_phone_is_blocked(self):
        self.login(self.desk)
        self.client.post(reverse("checkin"), {
            "first_name": "Maria", "last_name": "Again", "phone": "919-555-0142", "model": "iPhone 15",
            "reported_issue": "Duplicate test"})
        self.assertFalse(m.RepairJob.objects.filter(reported_issue="Duplicate test").exists())
        self.assertEqual(m.Customer.objects.filter(phone__contains="0142").count(), 1)

    def test_fr02_search_by_ticket_and_phone(self):
        self.login(self.desk)
        job = self.job("Cracked screen")
        self.assertContains(self.client.get(reverse("jobs"), {"q": job.ticket_number}), job.ticket_number)
        self.assertContains(self.client.get(reverse("jobs"), {"q": "555-0142"}), job.ticket_number)

    def test_passcode_is_encrypted_and_hidden_from_front_desk(self):
        job = self.job("Cracked screen")
        self.assertNotIn("482916", job.device_passcode)
        self.assertEqual(decrypt_passcode(job.device_passcode), "482916")
        self.login(self.desk)
        self.assertNotContains(self.client.get(reverse("job_detail", args=[job.pk])), "482916")
        self.login(self.manager)
        self.assertContains(self.client.get(reverse("job_detail", args=[job.pk])), "482916")
        self.login(self.sam)
        self.assertContains(self.client.get(reverse("bench_job", args=[job.pk])), "482916")


class AppointmentTests(Base):
    def slot(self, days=1, hour=14):
        return timezone.make_aware(datetime.combine(timezone.localdate() + timedelta(days=days), time(hour, 0)))

    def test_fr01_book_reschedule_cancel(self):
        cust = m.Customer.objects.get(last_name="Bello")
        appt = s.save_appointment(self.store1, cust, self.slot(), self.sam, self.desk)
        s.save_appointment(self.store1, cust, self.slot(hour=15), self.sam, self.desk, appt)
        appt.refresh_from_db()
        self.assertEqual(appt.scheduled_at, self.slot(hour=15))
        s.cancel_appointment(appt)
        self.assertEqual(appt.appt_status, m.APPT_CANCELLED)

    def test_fr01_technician_cannot_be_double_booked(self):
        a, b = m.Customer.objects.all()[:2]
        s.save_appointment(self.store1, a, self.slot(), self.sam, self.desk)
        with self.assertRaises(s.RuleError):
            s.save_appointment(self.store1, b, self.slot(), self.sam, self.desk)

    def test_fr01_full_slot_is_blocked(self):
        customers = list(m.Customer.objects.all()[:3])
        s.save_appointment(self.store1, customers[0], self.slot(), self.sam, self.desk)
        s.save_appointment(self.store1, customers[1], self.slot(), self.jordan, self.desk)
        with self.assertRaises(s.RuleError):  # two technicians, two bookings
            s.save_appointment(self.store1, customers[2], self.slot(), None, self.desk)

    def test_fr01_appointment_prefills_check_in(self):
        appt = m.Appointment.objects.get(customer__last_name="Santos")
        self.login(self.desk)
        r = self.client.post(reverse("checkin") + f"?appointment={appt.pk}", {
            "customer_id": appt.customer_id, "device_id": appt.customer.devices.first().pk,
            "reported_issue": "Booked drop-off", "technician_id": self.sam.pk})
        job = m.RepairJob.objects.get(reported_issue="Booked drop-off")
        self.assertEqual(job.appointment, appt)
        appt.refresh_from_db()
        self.assertEqual(appt.appt_status, m.APPT_CHECKED_IN)


class WorkflowTests(Base):
    def test_fr04_technician_sees_only_own_queue(self):
        self.login(self.sam)
        page = self.client.get(reverse("bench")).content.decode()
        self.assertIn(self.job("Cracked screen").ticket_number, page)
        self.assertNotIn(self.job("Will not charge").ticket_number, page)  # Jordan's
        r = self.client.get(reverse("bench_job", args=[self.job("Will not charge").pk]))
        self.assertEqual(r.status_code, 404)

    def test_technician_can_claim_open_job(self):
        job = self.job("Joy-Con drift")
        s.claim(job, self.sam)
        self.assertEqual(job.assigned_tech, self.sam)
        with self.assertRaises(s.RuleError):
            s.claim(job, self.jordan)

    def test_fr05_decline_blocks_repair(self):
        job = self.job("Shuts off under 20 percent")
        s.record_decision(job, self.desk, False)
        self.assertEqual(job.status, m.UNREPAIRED)
        with self.assertRaises(s.RuleError):
            s.record_part_used(job, self.sam, self.part("QP-BAT-IP12"), 1)
        with self.assertRaises(s.RuleError):
            s.complete_repair(job, self.sam, "")

    def test_fr05_quote_total_and_approval_recorded(self):
        job = self.job("Shuts off under 20 percent")
        q = job.current_quote
        self.assertEqual(q.total_amount, Decimal("68.00"))
        s.record_decision(job, self.desk, True)
        q.refresh_from_db()
        self.assertEqual((q.decision, q.decision_by), (m.Q_APPROVED, self.desk))
        self.assertEqual(job.status, m.IN_REPAIR)

    def test_fr07_part_used_deducts_stock(self):
        job = self.job("Cracked screen")
        before = self.on_hand("QP-SCR-IP13")
        s.record_part_used(job, self.sam, self.part("QP-SCR-IP13"), 1)
        self.assertEqual(self.on_hand("QP-SCR-IP13"), before - 1)
        txn = m.InventoryTxn.objects.filter(part__sku="QP-SCR-IP13", txn_type=m.TXN_USED).get()
        self.assertEqual((txn.quantity_change, txn.recorded_by), (-1, self.sam))

    def test_fr07_stock_cannot_go_below_zero(self):
        job = self.job("Cracked screen")
        with self.assertRaises(s.RuleError):
            s.record_part_used(job, self.sam, self.part("QP-SCR-IP13"), 99)
        with self.assertRaises(s.RuleError):
            s.adjust_stock(self.store1, self.part("QP-SCR-IP13"), -99, "count", self.manager)
        self.assertEqual(self.on_hand("QP-SCR-IP13"), 4)

    def test_fr06_out_of_stock_approval_waits_for_parts(self):
        job = self.job("Green line on display")
        self.assertEqual(job.status, m.AWAITING_PARTS)
        self.assertTrue(job.parts.filter(part__sku="QP-SCR-IP14", part_status=m.PART_NEEDED).exists())

    def test_fr08_unpaid_release_blocked_then_paid_release_succeeds(self):
        job = self.job("Will not charge")
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, True)
        s.record_payment(job, self.desk, job.final_cost, "Card")
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, False)  # ID not checked
        s.release_device(job, self.desk, True)
        self.assertEqual(job.status, m.CLOSED)
        self.assertTrue(job.id_verified_flag)

    def test_unrepaired_device_released_without_fee(self):
        job = self.job("Keyboard not responding")
        s.release_device(job, self.desk, True)
        self.assertEqual(job.status, m.CLOSED)

    def test_nfr02_every_change_records_who_and_when(self):
        job = self.job("Will not charge")
        statuses = list(job.history.order_by("history_id").values_list("status", flat=True))
        self.assertEqual(statuses[0], m.CHECKED_IN)
        self.assertIn(m.READY, statuses)
        self.assertTrue(all(h.changed_by_id and h.changed_at for h in job.history.all()))


class NotificationTests(Base):
    def test_fr12_email_from_store_account_logs_sender(self):
        job = self.job("Will not charge")
        s.send_pickup_notification(job, self.desk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "store1@quickphone.test")
        self.assertEqual(mail.outbox[0].to, ["n.kowalski@example.com"])
        self.assertEqual((job.email_status, job.email_sent_by), ("Sent", self.desk))

    def test_fr12_technician_may_send_without_seeing_address(self):
        """Owner answer Oct 23 #1, approved for the build on 2026-10-28 (supersedes NFR05)."""
        job = self.job("Will not charge")
        self.login(self.jordan)
        page = self.client.get(reverse("bench_job", args=[job.pk])).content.decode()
        self.assertNotIn("n.kowalski@example.com", page)
        self.client.post(reverse("job_notify", args=[job.pk]))
        job.refresh_from_db()
        self.assertEqual(job.email_sent_by, self.jordan)

    def test_fr12_not_sent_before_repair_complete(self):
        with self.assertRaises(s.RuleError):
            s.send_pickup_notification(self.job("Cracked screen"), self.desk)


class PurchasingTests(Base):
    def test_fr10_order_cannot_be_received_until_approved(self):
        po = s.add_to_po(self.store1, self.part("QP-BAT-S22"), 4, self.manager)
        line = po.lines.get()
        with self.assertRaises(s.RuleError):
            s.receive_po(po, self.manager, {line.pk: 4})
        s.submit_po(po, self.manager)
        with self.assertRaises(s.RuleError):
            s.receive_po(po, self.manager, {line.pk: 4})

    def test_fr10_reject_returns_to_draft_with_reason(self):
        po = m.PurchaseOrder.objects.get(po_status=m.PO_PENDING)
        with self.assertRaises(s.RuleError):
            s.reject_po(po, self.manager, "")
        s.reject_po(po, self.manager, "Wrong quantity")
        self.assertEqual((po.po_status, po.rejection_reason), (m.PO_DRAFT, "Wrong quantity"))

    def test_nfr01_technician_cannot_approve_po(self):
        po = m.PurchaseOrder.objects.get(po_status=m.PO_PENDING)
        self.login(self.sam)
        r = self.client.post(reverse("po_detail", args=[po.pk]), {"action": "approve"})
        self.assertEqual(r.status_code, 403)
        with self.assertRaises(s.RuleError):
            s.approve_po(po, self.sam)
        po.refresh_from_db()
        self.assertEqual(po.po_status, m.PO_PENDING)

    def test_nfr01_front_desk_cannot_open_inventory(self):
        self.login(self.desk)
        self.assertEqual(self.client.get(reverse("inventory")).status_code, 403)

    def test_fr09_partial_delivery_then_full_releases_waiting_job(self):
        po = m.PurchaseOrder.objects.get(po_status=m.PO_PENDING)  # 3 x iPhone 14 screen, linked to the job
        job = self.job("Green line on display")
        s.approve_po(po, self.manager)
        line = po.lines.get()
        released = s.receive_po(po, self.manager, {line.pk: 1})
        po.refresh_from_db()
        self.assertEqual(po.po_status, m.PO_ORDERED)  # partial: still open
        self.assertEqual([j.pk for j in released], [job.pk])
        self.assertEqual(self.on_hand("QP-SCR-IP14"), 1)
        s.receive_po(po, self.manager, {line.pk: 2})
        po.refresh_from_db()
        self.assertEqual(po.po_status, m.PO_RECEIVED)
        with self.assertRaises(s.RuleError):
            s.receive_po(po, self.manager, {line.pk: 1})

    def test_fr09_adjustment_needs_reason(self):
        before = self.on_hand("QP-ADH-KIT")
        with self.assertRaises(s.RuleError):
            s.adjust_stock(self.store1, self.part("QP-ADH-KIT"), -2, " ", self.manager)
        self.assertEqual(self.on_hand("QP-ADH-KIT"), before)
        s.adjust_stock(self.store1, self.part("QP-ADH-KIT"), -2, "Damaged in drawer", self.manager)
        self.assertEqual(self.on_hand("QP-ADH-KIT"), before - 2)

    def test_low_stock_alert_shows_on_inventory(self):
        self.login(self.manager)
        self.assertContains(self.client.get(reverse("inventory")), "Low-stock alert")

    def test_fr11_import_rejects_file_with_bad_row(self):
        self.login(self.manager)
        csv_text = ("sku,part_name,device_model,grade,standard_cost,supplier,quantity_on_hand,reorder_point\n"
                    "QP-NEW-1,Speaker,iPhone 11,OEM,9.50,Supplier A,4,1\n"
                    "QP-NEW-2,Mic,iPhone 11,OEM,abc,Supplier A,4,1\n")
        f = io.BytesIO(csv_text.encode())
        f.name = "parts.csv"
        r = self.client.post(reverse("inventory_import"), {"file": f})
        self.assertContains(r, "Nothing was imported")
        self.assertFalse(m.Part.objects.filter(sku="QP-NEW-1").exists())

    def test_fr11_import_valid_file(self):
        self.login(self.manager)
        f = io.BytesIO(b"sku,part_name,device_model,grade,standard_cost,supplier,quantity_on_hand,reorder_point\n"
                       b"QP-NEW-1,Speaker,iPhone 11,OEM,9.50,Supplier A,4,1\n")
        f.name = "parts.csv"
        self.client.post(reverse("inventory_import"), {"file": f})
        self.assertEqual(self.on_hand("QP-NEW-1"), 4)


class AccessTests(Base):
    def test_nfr04_technician_never_sees_customer_contact(self):
        self.login(self.sam)
        page = self.client.get(reverse("bench_job", args=[self.job("Cracked screen").pk])).content.decode()
        self.assertNotIn("555-0142", page)
        self.assertNotIn("m.santos@example.com", page)
        self.assertEqual(self.client.get(reverse("jobs")).status_code, 403)
        self.assertEqual(self.client.get(reverse("checkin")).status_code, 403)

    def test_fr14_manager_cannot_assign_owner_role(self):
        self.login(self.manager)
        self.client.post(reverse("staff_new"), {
            "first_name": "New", "last_name": "Boss", "email": "newboss@quickphone.test", "role": m.OWNER,
            "store_id": self.store1.pk, "password": "a-long-password"})
        self.assertFalse(m.Employee.objects.filter(email="newboss@quickphone.test").exists())

    def test_fr14_owner_creates_user_in_each_role(self):
        self.login(self.owner)
        for i, role in enumerate(m.ROLES):
            self.client.post(reverse("staff_new"), {
                "first_name": "T", "last_name": str(i), "email": f"t{i}@quickphone.test", "role": role,
                "store_id": self.store1.pk, "password": "a-long-password"})
            self.assertEqual(m.Employee.objects.get(email=f"t{i}@quickphone.test").role, role)

    def test_manager_fixed_to_home_store(self):
        self.login(self.manager)
        store2 = m.Store.objects.get(store_name="Store 2")
        r = self.client.post(reverse("switch_store"), {"store_id": store2.pk})
        self.assertEqual(r.status_code, 403)

    def test_fr13_owner_dashboard_compares_stores(self):
        self.login(self.owner)
        r = self.client.get(reverse("dashboard"))
        self.assertContains(r, "Store 1")
        self.assertContains(r, "Store 2")

    def test_login_with_training_password(self):
        r = self.client.post(reverse("login"), {"username": "desk1@quickphone.test", "password": TRAINING_PASSWORD})
        self.assertRedirects(r, reverse("home"), target_status_code=302)

    def test_inactive_account_cannot_sign_in(self):
        self.desk.active_flag = False
        self.desk.save()
        r = self.client.post(reverse("login"), {"username": "desk1@quickphone.test", "password": TRAINING_PASSWORD})
        self.assertEqual(r.status_code, 200)

    def test_every_screen_renders_for_its_role(self):
        pages = {
            self.desk: ["checkin", "jobs", "appointment_new"],
            self.sam: ["bench"],
            self.manager: ["inventory", "po_list", "staff", "part_new", "inventory_import", "staff_new", "supplier_new"],
            self.owner: ["dashboard", "inventory", "jobs", "checkin"],
        }
        for user, names in pages.items():
            self.login(user)
            for name in names:
                self.assertEqual(self.client.get(reverse(name)).status_code, 200, f"{user.role} {name}")
        self.login(self.desk)
        for job in m.RepairJob.objects.filter(store=self.store1):
            self.assertEqual(self.client.get(reverse("job_detail", args=[job.pk])).status_code, 200)
        self.login(self.manager)
        for po in m.PurchaseOrder.objects.all():
            self.assertEqual(self.client.get(reverse("po_detail", args=[po.pk])).status_code, 200)
