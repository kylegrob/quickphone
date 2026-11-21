"""Tests named after the requirements catalogue's acceptance checks, plus failure and
security cases."""
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

    def listed(self, model):
        return m.DeviceModel.objects.get(model=model)

    def job(self, issue):
        return m.RepairJob.objects.get(reported_issue=issue)


class CheckInTests(Base):
    def test_fr02_fr03_walk_in_creates_job_with_ticket_and_history(self):
        self.login(self.desk)
        r = self.client.post(reverse("checkin"), {
            "first_name": "Test", "last_name": "Walkin", "phone": "(919) 555-0999", "email": "",
            "device_model_id": self.listed("iPhone 11").pk, "reported_issue": "Speaker crackles",
            "technician_id": "",
        })
        job = m.RepairJob.objects.get(reported_issue="Speaker crackles")
        self.assertRedirects(r, reverse("job_ticket", args=[job.pk]) + "?print=1")
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


class QuoteAtCheckInTests(Base):
    """Owner, 2026-10-30: quote shown at check-in from part cost plus the Owner's labor; re-approved
    only for an additional repair. Technician, Manager and Owner can check in and repair."""

    def check_in(self, user, lines, tech=None, issue="Cracked screen at counter"):
        cust = m.Customer.objects.get(last_name="Walsh")
        dev = m.Device.objects.create(customer=cust, model="iPhone 13", brand="Apple")
        return s.check_in(user, self.store1, dev, issue, "", "", tech, None, lines)

    def test_quote_is_part_cost_plus_owner_labor_and_stored_approved(self):
        job = self.check_in(self.desk, [(self.part("QP-SCR-IP13"), 1), (self.part("QP-ADH-KIT"), 1)])
        q = job.current_quote
        self.assertEqual((q.parts_amount, q.labor_amount, q.total_amount),
                         (Decimal("64.00"), Decimal("55.00"), Decimal("119.00")))
        self.assertEqual((q.decision, q.decision_by), (m.Q_APPROVED, self.desk))
        self.assertEqual((job.final_cost, job.status), (Decimal("119.00"), m.CHECKED_IN))
        self.assertEqual(q.lines.count(), 2)

    def test_checkin_without_parts_has_no_quote(self):
        job = self.check_in(self.desk, [])
        self.assertIsNone(job.current_quote)

    def test_checkin_screen_posts_a_quote(self):
        self.login(self.desk)
        cust = m.Customer.objects.get(last_name="Walsh")
        scr = self.part("QP-SCR-IP13")
        self.client.post(reverse("checkin"), {
            "customer_id": cust.pk, "device_model_id": self.listed("iPhone 13").pk, "reported_issue": "Screen via form",
            f"use_{scr.pk}": "on", f"qty_{scr.pk}": "1"})
        job = self.job("Screen via form")
        self.assertEqual(job.current_quote.total_amount, Decimal("117.00"))
        self.assertEqual((job.current_quote.decision, job.current_quote.decision_by), (m.Q_APPROVED, self.desk))
        page = self.client.get(reverse("checkin"))
        self.assertContains(page, "Repair quote")
        self.assertNotContains(page, "quote_approved")

    def test_confirmed_diagnosis_starts_repair_without_second_approval(self):
        job = self.check_in(self.desk, [(self.part("QP-BAT-IP12"), 1)], tech=self.sam)
        s.start_diagnosis(job, self.sam)
        s.confirm_repair(job, self.sam, "Battery fails load test.")
        self.assertEqual(job.status, m.IN_REPAIR)
        self.assertEqual(job.quotes.count(), 1)

    def test_confirm_needs_an_approved_quote(self):
        job = self.job("Joy-Con drift")
        s.claim(job, self.sam)
        s.start_diagnosis(job, self.sam)
        with self.assertRaises(s.RuleError):
            s.confirm_repair(job, self.sam, "Looks fine")

    def test_out_of_stock_approved_quote_waits_for_parts(self):
        job = self.check_in(self.desk, [(self.part("QP-SCR-IP14"), 1)], tech=self.sam)  # none on hand
        s.start_diagnosis(job, self.sam)
        s.confirm_repair(job, self.sam, "Panel dead.")
        self.assertEqual(job.status, m.AWAITING_PARTS)
        self.assertTrue(job.parts.filter(part__sku="QP-SCR-IP14", part_status=m.PART_NEEDED).exists())

    def test_additional_repair_needs_approval_and_adds_to_total(self):
        job = self.check_in(self.desk, [(self.part("QP-BAT-IP12"), 1)], tech=self.sam)  # 28 + 40
        s.start_diagnosis(job, self.sam)
        s.confirm_repair(job, self.sam, "Battery fails.")
        s.submit_quote(job, self.sam, "Port is also damaged.", None, [(self.part("QP-CHG-USBC"), 1)])  # 15 + 35
        self.assertEqual(job.status, m.AWAITING_APPROVAL)
        with self.assertRaises(s.RuleError):
            s.complete_repair(job, self.sam, "")  # no work until approved
        s.record_decision(job, self.desk, True)
        self.assertEqual((job.status, job.final_cost), (m.IN_REPAIR, Decimal("118.00")))
        self.assertIn("Additional repair: Port is also damaged.", job.diagnosis_notes)

    def test_declined_additional_repair_keeps_the_approved_one(self):
        job = self.check_in(self.desk, [(self.part("QP-BAT-IP12"), 1)], tech=self.sam)
        s.start_diagnosis(job, self.sam)
        s.confirm_repair(job, self.sam, "Battery fails.")
        s.submit_quote(job, self.sam, "Port is also damaged.", None, [(self.part("QP-CHG-USBC"), 1)])
        s.record_decision(job, self.desk, False)
        self.assertEqual((job.status, job.final_cost), (m.IN_REPAIR, Decimal("68.00")))

    def test_unrepairable_drops_the_quote_fee(self):
        job = self.check_in(self.desk, [(self.part("QP-BAT-IP12"), 1)], tech=self.sam)
        s.start_diagnosis(job, self.sam)
        s.mark_unrepairable(job, self.sam, "Board is dead.")
        self.assertIsNone(job.final_cost)

    def test_technician_checks_in_but_cannot_open_the_job_list(self):
        self.login(self.sam)
        self.assertEqual(self.client.get(reverse("checkin")).status_code, 200)
        self.assertEqual(self.client.get(reverse("appointment_new")).status_code, 200)
        cust = m.Customer.objects.get(last_name="Walsh")
        r = self.client.post(reverse("checkin"), {"customer_id": cust.pk, "device_model_id": self.listed("Pixel 7").pk,
                                                  "reported_issue": "Tech walk-in", "technician_id": self.sam.pk})
        job = self.job("Tech walk-in")
        self.assertRedirects(r, reverse("job_ticket", args=[job.pk]) + "?print=1")
        self.assertEqual(job.history.get().changed_by, self.sam)
        self.assertEqual(self.client.get(reverse("jobs")).status_code, 403)

    def test_manager_and_owner_repair_devices(self):
        for user in (self.manager, self.owner):
            job = self.check_in(self.desk, [(self.part("QP-BAT-IP12"), 1)], issue=f"Bench {user.role}")
            self.login(user)
            self.client.post(reverse("bench_job", args=[job.pk]), {"action": "claim"})
            job.refresh_from_db()
            self.assertEqual(job.assigned_tech, user)
            for action, data in [("start", {}), ("confirm", {"diagnosis_notes": "ok"}),
                                 ("complete", {"repair_notes": "done"})]:
                self.client.post(reverse("bench_job", args=[job.pk]), {"action": action, **data})
            job.refresh_from_db()
            self.assertEqual(job.status, m.READY, user.role)
            self.assertEqual(self.client.get(reverse("bench")).status_code, 200)

    def test_manager_can_be_assigned_a_job_but_front_desk_cannot(self):
        job = self.job("Joy-Con drift")
        s.assign(job, self.manager, self.manager)
        with self.assertRaises(s.RuleError):
            s.assign(job, self.desk, self.manager)

    def test_only_owner_sets_labor(self):
        scr = self.part("QP-SCR-IP13")
        form = {"sku": scr.sku, "part_name": scr.part_name, "device_model": scr.device_model, "standard_cost": "62.00"}
        self.login(self.manager)
        self.client.post(reverse("part_edit", args=[scr.pk]), {**form, "labor_cost": "99.00", "active_flag": "on"})
        scr.refresh_from_db()
        self.assertEqual(scr.labor_cost, Decimal("55.00"))
        self.login(self.owner)
        self.client.post(reverse("part_edit", args=[scr.pk]), {**form, "labor_cost": "99.00", "active_flag": "on"})
        scr.refresh_from_db()
        self.assertEqual(scr.labor_cost, Decimal("99.00"))


class DeviceListTests(Base):
    """Check-in picks a device from a list; staff add one that is missing (2026-10-30)."""

    def post(self, user=None, **fields):
        self.login(user or self.desk)
        cust = m.Customer.objects.get(last_name="Walsh")
        return self.client.post(reverse("checkin"), {"customer_id": cust.pk, "reported_issue": "List test", **fields})

    def test_starter_list_is_loaded_and_offered_at_check_in(self):
        self.assertTrue(m.DeviceModel.objects.filter(brand="Apple", model="iPhone 13").exists())
        self.login(self.desk)
        self.assertContains(self.client.get(reverse("checkin")), "iPhone 13")

    def test_listed_device_is_copied_to_the_customer_device(self):
        self.post(device_model_id=self.listed("Galaxy S22").pk)
        d = self.job("List test").device
        self.assertEqual((d.brand, d.model, d.device_type), ("Samsung", "Galaxy S22", "Phone"))

    def test_free_text_model_is_refused_without_the_add_step(self):
        self.post(model="Made Up 9", brand="Nobody")
        self.assertFalse(m.RepairJob.objects.filter(reported_issue="List test").exists())
        self.assertFalse(m.DeviceModel.objects.filter(model="Made Up 9").exists())

    def test_unknown_list_id_is_refused(self):
        self.post(device_model_id="99999")
        self.assertFalse(m.RepairJob.objects.filter(reported_issue="List test").exists())

    def test_missing_device_can_be_added_and_is_then_on_the_list(self):
        self.post(user=self.sam, new_type="Phone", new_brand="Apple", new_model="iPhone 16")
        entry = m.DeviceModel.objects.get(model="iPhone 16")
        self.assertEqual((entry.brand, entry.device_type), ("Apple", "Phone"))
        self.assertEqual(self.job("List test").device.model, "iPhone 16")

    def test_a_picked_or_added_device_wins_over_the_device_on_file(self):
        cust = m.Customer.objects.get(last_name="Santos")
        on_file = cust.devices.first()
        self.login(self.desk)
        self.client.post(reverse("checkin"), {"customer_id": cust.pk, "device_id": on_file.pk,
                                              "new_type": "Phone", "new_brand": "Motorola", "new_model": "Moto G Power",
                                              "reported_issue": "Other device"})
        self.assertEqual(self.job("Other device").device.model, "Moto G Power")
        self.client.post(reverse("checkin"), {"customer_id": cust.pk, "device_id": on_file.pk,
                                              "reported_issue": "Same device"})
        self.assertEqual(self.job("Same device").device, on_file)

    def test_adding_an_existing_device_does_not_duplicate_it(self):
        before = m.DeviceModel.objects.count()
        self.post(new_type="Phone", new_brand="apple", new_model="IPHONE 13")
        self.assertEqual(m.DeviceModel.objects.count(), before)
        self.assertEqual(self.job("List test").device.model, "iPhone 13")

    def test_add_needs_brand_model_and_type(self):
        for fields in ({"new_brand": "Apple"}, {"new_model": "X"}, {"new_brand": "A", "new_model": "B", "new_type": "Toaster"}):
            self.post(**fields)
        self.assertFalse(m.RepairJob.objects.filter(reported_issue="List test").exists())


class ScreenAccessTests(Base):
    """The Owner opens or closes screens for each role (2026-10-30). Defaults match the earlier role rules."""

    def save(self, **boxes):
        """Posts the matrix as the Owner, with the defaults ticked plus the given changes ({'inventory|Front Desk': True})."""
        from .permissions import SCREENS
        data = {f"{screen}|{role}": "on" for screen, (_, roles) in SCREENS.items() for role in roles}
        for key, on in boxes.items():
            data.pop(key, None)
            if on:
                data[key] = "on"
        self.login(self.owner)
        return self.client.post(reverse("access"), data)

    def test_defaults_match_the_role_rules(self):
        self.login(self.desk)
        self.assertEqual(self.client.get(reverse("inventory")).status_code, 403)
        self.assertEqual(self.client.get(reverse("checkin")).status_code, 200)
        self.login(self.sam)
        self.assertEqual(self.client.get(reverse("jobs")).status_code, 403)
        self.assertEqual(self.client.get(reverse("bench")).status_code, 200)

    def test_saving_the_defaults_stores_nothing(self):
        self.save()
        self.assertEqual(m.ScreenAccess.objects.count(), 0)

    def test_owner_can_open_a_screen_for_a_role(self):
        self.save(**{"inventory|Front Desk": True})
        self.assertEqual(m.ScreenAccess.objects.get().allowed, True)
        self.login(self.desk)
        self.assertEqual(self.client.get(reverse("inventory")).status_code, 200)
        self.assertContains(self.client.get(reverse("checkin")), "Inventory")
        self.assertEqual(self.client.get(reverse("po_list")).status_code, 403)  # orders is its own screen

    def test_owner_can_close_a_screen_for_a_role(self):
        self.save(**{"orders|Manager": False})
        self.login(self.manager)
        self.assertEqual(self.client.get(reverse("po_list")).status_code, 403)
        self.assertEqual(self.client.get(reverse("inventory")).status_code, 200)
        self.assertNotContains(self.client.get(reverse("inventory")), 'class="btn" href="/orders/"')

    def test_closing_every_screen_for_a_role_gives_a_clear_refusal(self):
        from .permissions import SCREENS
        self.save(**{f"{screen}|Technician": False for screen in SCREENS})
        self.login(self.sam)
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 403)

    def test_home_goes_to_the_first_open_screen(self):
        self.save(**{"bench|Technician": False, "checkin|Technician": True, "checkin|Front Desk": True})
        self.login(self.sam)
        self.assertRedirects(self.client.get(reverse("home")), reverse("checkin"), target_status_code=200)

    def test_only_the_owner_reaches_the_access_screen(self):
        for user in (self.manager, self.desk, self.sam):
            self.login(user)
            self.assertEqual(self.client.get(reverse("access")).status_code, 403, user.role)
            self.assertEqual(self.client.post(reverse("access"), {"inventory|Front Desk": "on"}).status_code, 403)
        self.assertEqual(m.ScreenAccess.objects.count(), 0)

    def test_owner_cannot_lock_themself_out_of_access(self):
        from .permissions import SCREENS
        self.save(**{f"{screen}|Owner": False for screen in SCREENS})
        self.assertEqual(self.client.get(reverse("access")).status_code, 200)

    def test_reset_restores_defaults(self):
        self.save(**{"inventory|Front Desk": True})
        self.client.post(reverse("access"), {"action": "reset"})
        self.assertEqual(m.ScreenAccess.objects.count(), 0)
        self.login(self.desk)
        self.assertEqual(self.client.get(reverse("inventory")).status_code, 403)

    def test_screen_access_does_not_override_business_rules(self):
        self.save(**{"orders|Technician": True, "jobs|Technician": True})
        po = m.PurchaseOrder.objects.get(po_status=m.PO_PENDING)
        self.login(self.sam)
        self.assertEqual(self.client.get(reverse("po_detail", args=[po.pk])).status_code, 200)
        self.client.post(reverse("po_detail", args=[po.pk]), {"action": "approve"})
        po.refresh_from_db()
        self.assertEqual(po.po_status, m.PO_PENDING)  # still only a Manager or the Owner approves
        page = self.client.get(reverse("job_detail", args=[self.job("Cracked screen").pk])).content.decode()
        self.assertIn("555-0142", page)  # Technicians see customer contact (team decision, 2026-11-02)

    def test_the_matrix_page_lists_every_screen_and_role(self):
        self.login(self.owner)
        page = self.client.get(reverse("access")).content.decode()
        for label in ("Dashboard", "Purchase orders", "Inventory and parts", "My repair jobs"):
            self.assertIn(label, page)
        for role in m.ROLES:
            self.assertIn(f"<th class=\"num\" scope=\"col\">{role}</th>", page)


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


class RepairTypeSlotTests(Base):
    """2026-11-20: the appointment length comes from the repair type."""

    def at(self, hour, minute=0, days=2):  # tomorrow has seeded bookings
        return timezone.make_aware(datetime.combine(timezone.localdate() + timedelta(days=days), time(hour, minute)))

    def kind(self, minutes, name=None):
        return m.RepairType.objects.create(type_name=name or f"Test {minutes}", slot_minutes=minutes)

    def test_booking_copies_the_repair_type_length(self):
        cust = m.Customer.objects.get(last_name="Bello")
        appt = s.save_appointment(self.store1, cust, self.at(10), self.sam, self.desk, repair_type=self.kind(90))
        self.assertEqual(appt.duration_minutes, 90)
        self.assertEqual(appt.ends_at, self.at(11, 30))

    def test_long_booking_blocks_the_technician_for_its_whole_length(self):
        a, b = m.Customer.objects.all()[:2]
        s.save_appointment(self.store1, a, self.at(10), self.sam, self.desk, repair_type=self.kind(90))
        with self.assertRaises(s.RuleError):  # 11:00 is inside Sam's 10:00-11:30 booking
            s.save_appointment(self.store1, b, self.at(11), self.sam, self.desk, repair_type=self.kind(30, "x"))
        s.save_appointment(self.store1, b, self.at(11, 30), self.sam, self.desk, repair_type=self.kind(30, "y"))

    def test_new_booking_cannot_run_into_a_later_one(self):
        a, b = m.Customer.objects.all()[:2]
        s.save_appointment(self.store1, a, self.at(11), self.sam, self.desk, repair_type=self.kind(30))
        with self.assertRaises(s.RuleError):  # a 60-minute booking at 10:30 overlaps Sam's 11:00
            s.save_appointment(self.store1, b, self.at(10, 30), self.sam, self.desk, repair_type=self.kind(60))

    def test_overlapping_bookings_fill_the_store(self):
        customers = list(m.Customer.objects.all()[:3])
        long = self.kind(120)
        s.save_appointment(self.store1, customers[0], self.at(9), self.sam, self.desk, repair_type=long)
        s.save_appointment(self.store1, customers[1], self.at(10), self.jordan, self.desk, repair_type=long)
        self.assertTrue(s.slot_is_full(self.store1, self.at(10, 30), 30))  # both technicians busy
        self.assertFalse(s.slot_is_full(self.store1, self.at(12), 30))
        with self.assertRaises(s.RuleError):
            s.save_appointment(self.store1, customers[2], self.at(10, 30), None, self.desk, repair_type=self.kind(30))

    def test_booking_cannot_run_past_closing(self):
        cust = m.Customer.objects.get(last_name="Bello")
        with self.assertRaises(s.RuleError):  # last slot 17:00, closes 17:30
            s.save_appointment(self.store1, cust, self.at(17), None, self.desk, repair_type=self.kind(60))

    def test_inactive_repair_type_cannot_be_booked(self):
        kind = self.kind(30)
        kind.active_flag = False
        kind.save()
        with self.assertRaises(s.RuleError):
            s.save_appointment(self.store1, m.Customer.objects.first(), self.at(10), None, self.desk,
                               repair_type=kind)

    def test_booking_screen_needs_a_repair_type(self):
        self.login(self.desk)
        cust = m.Customer.objects.get(last_name="Bello")
        page = self.client.get(reverse("appointment_new"), {"customer": cust.pk})
        self.assertContains(page, "Pick the repair type first.")
        self.client.post(reverse("appointment_new"), {"customer_id": cust.pk, "slot": self.at(14).isoformat()})
        self.assertFalse(m.Appointment.objects.filter(customer=cust, scheduled_at=self.at(14)).exists())
        kind = m.RepairType.objects.get(type_name="Water damage")
        page = self.client.get(reverse("appointment_new"), {"customer": cust.pk, "type": kind.pk})
        self.assertContains(page, f"Time slot ({kind.slot_minutes} minutes)")
        self.client.post(reverse("appointment_new"), {"customer_id": cust.pk, "repair_type_id": kind.pk,
                                                      "slot": self.at(14).isoformat()})
        appt = m.Appointment.objects.get(customer=cust, scheduled_at=self.at(14))
        self.assertEqual((appt.repair_type, appt.duration_minutes), (kind, kind.slot_minutes))

    def test_manager_sets_length_and_front_desk_cannot(self):
        kind = m.RepairType.objects.get(type_name="Screen replacement")
        self.login(self.desk)
        r = self.client.post(reverse("repair_type_edit", args=[kind.pk]),
                             {"type_name": kind.type_name, "slot_minutes": "45"})
        self.assertEqual(r.status_code, 403)
        self.login(self.manager)
        self.client.post(reverse("repair_type_edit", args=[kind.pk]),
                         {"type_name": kind.type_name, "slot_minutes": "50", "active_flag": "on"})
        kind.refresh_from_db()
        self.assertNotEqual(kind.slot_minutes, 50)  # not a 15-minute step
        self.client.post(reverse("repair_type_edit", args=[kind.pk]),
                         {"type_name": kind.type_name, "slot_minutes": "45", "active_flag": "on"})
        kind.refresh_from_db()
        self.assertEqual(kind.slot_minutes, 45)

    def test_changing_a_type_keeps_existing_bookings(self):
        kind = self.kind(60)
        appt = s.save_appointment(self.store1, m.Customer.objects.first(), self.at(10), None, self.desk,
                                  repair_type=kind)
        kind.slot_minutes = 120
        kind.save()
        appt.refresh_from_db()
        self.assertEqual(appt.duration_minutes, 60)


class IntakeContactTests(Base):
    """A new customer needs a phone number; email is optional."""

    def post(self, **fields):
        self.login(self.desk)
        data = {"first_name": "Test", "last_name": "Contact", "phone": "", "email": "",
                "device_model_id": self.listed("iPhone 11").pk, "reported_issue": "Contact test"}
        data.update(fields)
        return self.client.post(reverse("checkin"), data)

    def test_fr02_no_phone_is_blocked_even_with_an_email(self):
        html = self.post(email="email.only@example.com").content.decode()
        self.assertIn("first name, last name and phone", html)
        self.assertFalse(m.RepairJob.objects.filter(reported_issue="Contact test").exists())
        tag = html[html.index('id="new_phone"'):]
        self.assertIn('aria-invalid="true"', tag[:tag.index(">")])

    def test_fr02_phone_only_customer_is_accepted(self):
        self.post(phone="(919) 555-0901")
        cust = m.RepairJob.objects.get(reported_issue="Contact test").customer
        self.assertEqual((cust.phone, cust.email), ("(919) 555-0901", None))

    def test_fr02_search_is_by_phone_not_email(self):
        self.login(self.desk)
        select = f'href="?customer={m.Customer.objects.get(email="m.santos@example.com").pk}"'
        self.assertContains(self.client.get(reverse("checkin"), {"phone": "555-0142"}), select)
        self.assertNotContains(self.client.get(reverse("checkin"), {"phone": "m.santos@example.com"}), select)


class POApprovalEmailTests(Base):
    """2026-11-20: submitting an order emails the people who can approve it."""

    def draft(self, by):
        po = m.PurchaseOrder.objects.create(store=self.store1, supplier=m.Supplier.objects.first(), created_by=by)
        part = m.Part.objects.first()
        m.POLine.objects.create(purchase_order=po, part=part, quantity_ordered=2, unit_cost=part.standard_cost)
        return po

    def test_submit_emails_store_manager_and_owner_not_submitter(self):
        mail.outbox.clear()
        po = self.draft(self.manager)
        recipients, sent = s.submit_po(po, self.manager)
        self.assertTrue(sent)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertIn(self.owner.email, msg.to)
        self.assertNotIn(self.manager.email, msg.to)
        self.assertNotIn("manager2@quickphone.test", msg.to)  # the other store's Manager
        self.assertIn(po.number, msg.subject)
        self.assertEqual(msg.from_email, self.store1.email_address)

    def test_failed_email_still_submits(self):
        from unittest import mock
        po = self.draft(self.manager)
        with mock.patch("shop.services.send_mail", side_effect=OSError):
            recipients, sent = s.submit_po(po, self.manager)
        po.refresh_from_db()
        self.assertEqual((po.po_status, sent), (m.PO_PENDING, False))

    def test_screen_says_who_was_emailed(self):
        po = self.draft(self.manager)
        self.login(self.manager)
        r = self.client.post(reverse("po_detail", args=[po.pk]), {"action": "submit"}, follow=True)
        self.assertContains(r, "Emailed")


class VoidPaymentTests(Base):
    """2026-11-20: a payment recorded by mistake can be voided before release; history keeps it."""

    def test_mistaken_payment_is_voided_and_logged(self):
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, "5.00", "Cash")
        pay = job.payments.get()
        s.void_payment(job, self.desk, pay.pk, "Wrong amount")
        self.assertEqual(job.payments.get().payment_status, "Voided")
        self.assertEqual(job.amount_paid, 0)
        note = job.history.order_by("-pk").first()
        self.assertEqual(note.changed_by, self.desk)
        self.assertIn("$5.00 Cash", note.note)
        self.assertIn("voided", note.note)

    def test_release_is_blocked_again_after_voiding_the_payment(self):
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, job.final_cost, "Card")
        s.void_payment(job, self.desk, job.payments.get().pk, "Wrong amount")
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, True, True)

    def test_payment_cannot_be_voided_after_release(self):
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, job.final_cost, "Card")
        s.release_device(job, self.desk, True, True)
        with self.assertRaises(s.RuleError):
            s.void_payment(job, self.desk, job.payments.get().pk, "Wrong amount")
        self.assertTrue(job.payments.exists())

    def test_cannot_void_another_jobs_payment(self):
        job, other = self.job("Will not charge"), self.job("Keyboard not responding")
        s.record_payment(other, self.desk, "10.00", "Cash")
        with self.assertRaises(s.RuleError):
            s.void_payment(job, self.desk, other.payments.get().pk, "Wrong job")
        self.assertTrue(other.payments.exists())

    def test_screen_voids_payment(self):
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, "5.00", "Cash")
        self.login(self.desk)
        page = self.client.get(reverse("job_detail", args=[job.pk]))
        self.assertContains(page, 'value="void_payment"')
        r = self.client.post(reverse("job_detail", args=[job.pk]),
                             {"action": "void_payment", "payment_id": job.payments.get().pk, "reason": "Wrong amount"}, follow=True)
        self.assertContains(r, "Payment voided.")
        self.assertEqual(job.payments.get().payment_status, "Voided")
        self.assertEqual(job.amount_paid, 0)

    def test_technician_without_jobs_access_cannot_void_payment(self):
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, "5.00", "Cash")
        self.login(self.jordan)
        r = self.client.post(reverse("job_detail", args=[job.pk]),
                             {"action": "void_payment", "payment_id": job.payments.get().pk, "reason": "Wrong amount"})
        self.assertEqual(r.status_code, 403)
        self.assertTrue(job.payments.exists())


class KeepTypedInputTests(Base):
    """2026-11-20: a refused action shows the form again with what was typed."""

    def test_refused_mark_ready_keeps_notes_and_quantities(self):
        job = self.job("Cracked screen")
        self.login(self.sam)
        r = self.client.post(reverse("bench_job", args=[job.pk]), {
            "action": "complete", "repair_notes": "Replaced screen, tested touch",
            f"used_{self.part('QP-SCR-IP13').pk}": "99", f"used_{self.part('QP-ADH-KIT').pk}": "1"})
        self.assertEqual(r.status_code, 200)  # not a redirect
        self.assertContains(r, "Replaced screen, tested touch")
        self.assertContains(r, f'name="used_{self.part("QP-SCR-IP13").pk}" value="99"')
        self.assertContains(r, "short")
        job.refresh_from_db()
        self.assertEqual(job.status, m.IN_REPAIR)

    def test_refused_add_work_keeps_reason_and_opens_the_section(self):
        job = self.job("Cracked screen")
        self.login(self.sam)
        r = self.client.post(reverse("bench_job", args=[job.pk]),
                             {"action": "add_work", "charge": "no", "diagnosis_notes": "Loose flex cable"})
        self.assertContains(r, "Loose flex cable")
        self.assertContains(r, '<details class="more" open><summary>Add parts or work')
        self.assertContains(r, 'value="no" checked')

    def test_part_needing_buttons_are_marked_for_the_script(self):
        job = self.job("Cracked screen")
        self.login(self.sam)
        self.assertContains(self.client.get(reverse("bench_job", args=[job.pk])), 'class="btn needs-part"')

    def test_refused_staff_account_keeps_names(self):
        self.login(self.manager)
        r = self.client.post(reverse("staff_new"), {
            "first_name": "Casey", "last_name": "Nguyen", "email": "sam@quickphone.test", "role": m.FRONT_DESK,
            "store_id": self.store1.pk, "password": "a-long-enough-phrase-26"})
        self.assertContains(r, 'value="Casey"')
        self.assertContains(r, 'value="Nguyen"')
        self.assertContains(r, 'value="sam@quickphone.test" maxlength="120" required aria-invalid="true"')

    def test_refused_part_keeps_typed_values(self):
        self.login(self.manager)
        r = self.client.post(reverse("part_new"), {
            "sku": "QP-SCR-IP13", "part_name": "Typed name", "standard_cost": "12.50", "quantity_on_hand": "7"})
        self.assertContains(r, 'value="Typed name"')
        self.assertContains(r, 'value="12.50"')
        self.assertContains(r, 'name="quantity_on_hand" value="7"')
        self.assertContains(r, 'placeholder="QP-SCR-IP13" aria-invalid="true"')

    def test_refused_repair_type_keeps_name_and_marks_minutes(self):
        self.login(self.manager)
        r = self.client.post(reverse("repair_type_new"), {"type_name": "Back glass", "slot_minutes": "50"})
        self.assertContains(r, 'value="Back glass"')
        self.assertContains(r, 'name="slot_minutes" aria-invalid="true"')
        self.assertFalse(m.RepairType.objects.filter(type_name="Back glass").exists())


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

    def test_assigned_technician_records_approval_on_bench(self):
        """2026-11-20: the customer's answer can be recorded from the assigned job as well."""
        job = self.job("Shuts off under 20 percent")
        self.login(self.sam)
        page = self.client.get(reverse("bench_job", args=[job.pk]))
        self.assertContains(page, "Customer approved")
        self.client.post(reverse("bench_job", args=[job.pk]), {"action": "approve"})
        job.refresh_from_db()
        self.assertEqual(job.status, m.IN_REPAIR)
        self.assertEqual(job.current_quote.decision_by, self.sam)

    def test_other_technician_cannot_record_approval(self):
        job = self.job("Shuts off under 20 percent")
        self.login(self.jordan)  # Sam's job: not in Jordan's bench at all
        r = self.client.post(reverse("bench_job", args=[job.pk]), {"action": "approve"})
        self.assertEqual(r.status_code, 404)
        job.refresh_from_db()
        self.assertEqual(job.status, m.AWAITING_APPROVAL)

    def test_checkin_lists_jobs_waiting_for_the_customers_answer(self):
        job = self.job("Shuts off under 20 percent")
        self.login(self.desk)
        page = self.client.get(reverse("checkin"))
        self.assertContains(page, "Waiting for the customer")
        self.assertContains(page, reverse("job_detail", args=[job.pk]))
        self.login(self.sam)  # Technicians cannot open Repair jobs, so no list
        self.assertNotContains(self.client.get(reverse("checkin")), "Waiting for the customer")

    def test_fr05_decline_blocks_repair(self):
        job = self.job("Shuts off under 20 percent")
        s.record_decision(job, self.desk, False)
        self.assertEqual(job.status, m.UNREPAIRED)
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

    def test_fr07_completion_takes_quoted_parts_off_stock(self):
        job = self.job("Cracked screen")  # In Repair on screen + adhesive kit
        before = {sku: self.on_hand(sku) for sku in ("QP-SCR-IP13", "QP-ADH-KIT")}
        s.complete_repair(job, self.sam, "Screen replaced.")
        self.assertEqual(job.status, m.READY)
        for sku, n in before.items():
            self.assertEqual(self.on_hand(sku), n - 1, sku)
            txn = m.InventoryTxn.objects.filter(part__sku=sku, txn_type=m.TXN_USED).get()
            self.assertEqual((txn.quantity_change, txn.recorded_by), (-1, self.sam))
        self.assertEqual(sorted(job.parts.filter(part_status=m.PART_USED).values_list("part__sku", flat=True)),
                         ["QP-ADH-KIT", "QP-SCR-IP13"])

    def test_fr07_completion_uses_the_quantities_the_technician_entered(self):
        job = self.job("Cracked screen")
        before = self.on_hand("QP-SCR-IP13"), self.on_hand("QP-ADH-KIT")
        s.complete_repair(job, self.sam, "", [(self.part("QP-SCR-IP13"), 2), (self.part("QP-ADH-KIT"), 0)])
        self.assertEqual((self.on_hand("QP-SCR-IP13"), self.on_hand("QP-ADH-KIT")), (before[0] - 2, before[1]))

    def test_fr07_stock_cannot_go_below_zero(self):
        job = self.job("Cracked screen")
        adhesive = self.on_hand("QP-ADH-KIT")
        with self.assertRaises(s.RuleError):
            s.complete_repair(job, self.sam, "", [(self.part("QP-SCR-IP13"), 99), (self.part("QP-ADH-KIT"), 1)])
        job.refresh_from_db()
        self.assertEqual(job.status, m.IN_REPAIR)
        self.assertEqual((self.on_hand("QP-SCR-IP13"), self.on_hand("QP-ADH-KIT")), (4, adhesive))  # nothing taken
        with self.assertRaises(s.RuleError):
            s.adjust_stock(self.store1, self.part("QP-SCR-IP13"), -99, "count", self.manager)
        self.assertEqual(self.on_hand("QP-SCR-IP13"), 4)

    def test_added_part_in_stock_is_taken_on_completion(self):
        job = self.job("Cracked screen")
        charger = self.on_hand("QP-CHG-USBC")
        self.assertFalse(s.add_parts(job, self.sam, [(self.part("QP-CHG-USBC"), 1)]))
        self.assertEqual(job.status, m.IN_REPAIR)
        self.assertIn("QP-CHG-USBC", [p.sku for p, _ in s.planned_parts(job)])
        s.complete_repair(job, self.sam, "")
        self.assertEqual(self.on_hand("QP-CHG-USBC"), charger - 1)
        self.assertFalse(job.parts.filter(part_status=m.PART_NEEDED).exists())

    def test_parts_received_for_a_waiting_job_are_taken_once_on_completion(self):
        job = self.job("Green line on display")  # Awaiting Parts: QP-SCR-IP14, none on hand
        s.adjust_stock(self.store1, self.part("QP-SCR-IP14"), 2, "delivery", self.manager)
        job.status = m.IN_REPAIR
        job.save()
        self.assertEqual(s.planned_parts(job), [(self.part("QP-SCR-IP14"), 1)])
        s.complete_repair(job, job.assigned_tech, "")
        self.assertEqual(self.on_hand("QP-SCR-IP14"), 1)

    def test_bench_add_work_charges_or_adds_free_parts(self):
        job = self.job("Cracked screen")
        url, charger = reverse("bench_job", args=[job.pk]), self.part("QP-CHG-USBC")
        self.login(self.sam)
        self.client.post(url, {"action": "add_work", "charge": "no", f"use_{charger.pk}": "on", f"qty_{charger.pk}": "1"})
        job.refresh_from_db()
        self.assertEqual((job.status, job.quotes.count()), (m.IN_REPAIR, 1))
        self.assertIn(charger, [p for p, _ in s.planned_parts(job)])
        self.client.post(url, {"action": "add_work", "charge": "yes", "diagnosis_notes": "Port worn.",
                               f"use_{charger.pk}": "on", f"qty_{charger.pk}": "1"})
        job.refresh_from_db()
        self.assertEqual((job.status, job.quotes.count()), (m.AWAITING_APPROVAL, 2))

    def test_bench_completion_form_consumes_parts(self):
        job = self.job("Cracked screen")
        before = self.on_hand("QP-SCR-IP13")
        self.login(self.sam)
        page = self.client.get(reverse("bench_job", args=[job.pk])).content.decode()
        self.assertNotIn('value="use_part"', page)
        self.assertIn(f'name="used_{self.part("QP-SCR-IP13").pk}"', page)
        self.client.post(reverse("bench_job", args=[job.pk]), {
            "action": "complete", "repair_notes": "done", f"used_{self.part('QP-SCR-IP13').pk}": "1",
            f"used_{self.part('QP-ADH-KIT').pk}": "1"})
        job.refresh_from_db()
        self.assertEqual((job.status, self.on_hand("QP-SCR-IP13")), (m.READY, before - 1))

    def complete_on_bench(self, job):
        self.login(self.sam)
        return self.client.post(reverse("bench_job", args=[job.pk]), {
            "action": "complete", "repair_notes": "done", f"used_{self.part('QP-SCR-IP13').pk}": "1",
            f"used_{self.part('QP-ADH-KIT').pk}": "1"}, follow=True)

    def test_fr12_marking_ready_sends_no_email(self):
        """Owner, Oct 23 #1: the pickup notification is sent by a click, never automatically."""
        mail.outbox.clear()
        job = self.job("Cracked screen")
        r = self.complete_on_bench(job)
        job.refresh_from_db()
        self.assertEqual((job.status, job.email_status), (m.READY, None))
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(r, "Send pickup notification")

    def test_fr06_out_of_stock_approval_waits_for_parts(self):
        job = self.job("Green line on display")
        self.assertEqual(job.status, m.AWAITING_PARTS)
        self.assertTrue(job.parts.filter(part__sku="QP-SCR-IP14", part_status=m.PART_NEEDED).exists())

    def test_fr08_unpaid_release_blocked_then_paid_release_succeeds(self):
        job = self.job("Will not charge")
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, True, True)
        s.record_payment(job, self.desk, job.final_cost, "Card")
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, False, True)  # ID not checked
        s.release_device(job, self.desk, True, True)
        self.assertEqual(job.status, m.CLOSED)
        self.assertTrue(job.id_verified_flag)

    def test_unrepaired_device_released_without_fee(self):
        job = self.job("Keyboard not responding")
        s.release_device(job, self.desk, True, True)
        self.assertEqual(job.status, m.CLOSED)

    def test_nfr02_every_change_records_who_and_when(self):
        job = self.job("Will not charge")
        statuses = list(job.history.order_by("history_id").values_list("status", flat=True))
        self.assertEqual(statuses[0], m.CHECKED_IN)
        self.assertIn(m.READY, statuses)
        self.assertTrue(all(h.changed_by_id and h.changed_at for h in job.history.all()))


class DecisionOnBenchTests(Base):
    def test_fr05_assigned_repairer_records_the_decision_on_the_bench(self):
        """2026-11-20: the repairer assigned to the job may record the customer's answer; nobody else's bench can."""
        job = m.RepairJob.objects.filter(status=m.AWAITING_APPROVAL, assigned_tech__isnull=False).first()
        tech = job.assigned_tech
        other = self.jordan if tech != self.jordan else self.sam
        self.login(other)
        r = self.client.post(reverse("bench_job", args=[job.pk]), {"action": "approve"})
        self.assertEqual(r.status_code, 404)
        job.refresh_from_db()
        self.assertEqual(job.status, m.AWAITING_APPROVAL)
        self.login(tech)
        self.client.post(reverse("bench_job", args=[job.pk]), {"action": "approve"})
        job.refresh_from_db()
        self.assertIn(job.status, (m.IN_REPAIR, m.AWAITING_PARTS))
        self.assertTrue(job.quotes.filter(decision=m.Q_APPROVED, decision_by=tech).exists())


class NotificationTests(Base):
    def test_fr12_email_from_store_account_logs_sender(self):
        job = self.job("Will not charge")
        s.send_pickup_notification(job, self.desk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "store1@quickphone.test")
        self.assertEqual(mail.outbox[0].to, ["n.kowalski@example.com"])
        self.assertEqual((job.email_status, job.email_sent_by), ("Sent", self.desk))

    def test_fr12_technician_may_send_pickup_notification(self):
        """Owner answer Oct 23 #1 (supersedes NFR05).
        Technicians also see customer contact since the team decision of 2026-11-02."""
        job = self.job("Will not charge")
        self.login(self.jordan)
        page = self.client.get(reverse("bench_job", args=[job.pk])).content.decode()
        self.assertIn("n.kowalski@example.com", page)
        self.client.post(reverse("job_notify", args=[job.pk]))
        job.refresh_from_db()
        self.assertEqual(job.email_sent_by, self.jordan)

    def test_fr12_no_send_button_for_a_customer_without_email(self):
        job = self.job("Will not charge")
        m.Customer.objects.filter(pk=job.customer.pk).update(email=None)
        for user, url in ((self.desk, "job_detail"), (self.jordan, "bench_job")):
            self.login(user)
            page = self.client.get(reverse(url, args=[job.pk]))
            self.assertNotContains(page, reverse("job_notify", args=[job.pk]))
            self.assertNotContains(page, "Send pickup notification")
            self.assertContains(page, "No email on file")

    def test_bench_shows_whether_pickup_notification_was_sent(self):
        """2026-11-20: the bench shows the notification state, in the job list and on the job."""
        job = self.job("Will not charge")
        self.login(self.jordan)
        page = self.client.get(reverse("bench_job", args=[job.pk])).content.decode()
        self.assertIn("Not sent yet", page)
        self.assertIn("Pickup notification: not sent", page)
        self.assertIn("Send pickup notification", page)
        r = self.client.post(reverse("job_notify", args=[job.pk]), {"back": "bench"}, follow=True)
        self.assertRedirects(r, reverse("bench_job", args=[job.pk]))
        page = r.content.decode()
        self.assertIn("Pickup notification: sent", page)
        self.assertIn("Send again", page)

    def test_manager_sending_from_bench_returns_to_bench(self):
        job = self.job("Will not charge")
        job.assigned_tech = self.manager
        job.save()
        self.login(self.manager)
        r = self.client.post(reverse("job_notify", args=[job.pk]), {"back": "bench"})
        self.assertRedirects(r, reverse("bench_job", args=[job.pk]))
        r = self.client.post(reverse("job_notify", args=[job.pk]))
        self.assertRedirects(r, reverse("job_detail", args=[job.pk]))

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
    def test_nfr04_technician_sees_customer_contact(self):
        from .permissions import can_see_contact
        for user in (self.sam, self.desk, self.manager, self.owner):
            self.assertTrue(can_see_contact(user), user.role)
        self.login(self.sam)
        cust = m.Customer.objects.get(phone__contains="0142")
        page = self.client.get(reverse("checkin"), {"customer": cust.pk}).content.decode()
        self.assertIn("555-0142", page)
        self.assertIn("m.santos@example.com", page)
        self.assertEqual(self.client.get(reverse("jobs")).status_code, 403)  # payment and release stay with the desk

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


class AccessibilityMarkupTests(Base):
    """Checks from the Nov 2 responsive and accessibility audit (WCAG 2.2 AA)."""

    def test_every_page_has_skip_link_and_menu_button(self):
        self.login(self.desk)
        html = self.client.get(reverse("checkin")).content.decode()
        self.assertIn('href="#main"', html)
        self.assertIn('<main id="main"', html)
        self.assertIn('aria-controls="site-menu"', html)

    def test_store_switch_needs_a_button_not_a_change_event(self):
        # WCAG 3.2.2: choosing a store must not reload the page by itself.
        self.login(self.owner)
        html = self.client.get(reverse("dashboard")).content.decode()
        self.assertNotIn("onchange", html)
        self.assertIn(">Switch</button>", html)

    def test_failed_check_in_marks_the_missing_fields(self):
        self.login(self.desk)
        html = self.client.post(reverse("checkin"), {"reported_issue": ""}).content.decode()
        for field in ("first_name", "last_name", "new_phone", "issue"):
            tag = html[html.index(f'id="{field}"'):]
            self.assertIn('aria-invalid="true"', tag[:tag.index(">")], field)

    def test_quote_total_is_announced(self):
        self.login(self.desk)
        html = self.client.get(reverse("checkin")).content.decode()
        self.assertIn('aria-live="polite"', html)


class SecurityTests(Base):
    """Controls from the security analysis (2026-11-06)."""

    def setUp(self):
        super().setUp()
        from django.core.cache import cache
        cache.clear()
        self.store2 = m.Store.objects.get(store_name="Store 2")

    def _settings_in_new_process(self, env, expr):
        """Loads settings.py fresh, outside the test runner, with only the given QP_ variables."""
        import os
        import subprocess
        import sys
        from django.conf import settings
        clean = {k: v for k, v in os.environ.items() if not k.startswith("QP_")}
        clean.update(env, DJANGO_SETTINGS_MODULE="quickphone.settings")
        code = f"import django; django.setup(); from django.conf import settings as s; print({expr})"
        return subprocess.run([sys.executable, "-c", code], cwd=settings.BASE_DIR, env=clean,
                              capture_output=True, text=True)

    def _live_env(self):
        from cryptography.fernet import Fernet
        return {"QP_DB_ENGINE": "sqlite", "QP_SECRET_KEY": "k" * 60, "QP_PASSCODE_KEY": Fernet.generate_key().decode()}

    def _store2_job(self):
        desk2 = m.Employee.objects.get(email="desk2@quickphone.test")
        device = m.Device.objects.filter(customer__phone__contains="0142").first()
        return s.check_in(desk2, self.store2, device, "Store 2 only")

    # F1: fail closed
    def test_f1_live_settings_refuse_to_start_without_keys(self):
        r = self._settings_in_new_process({"QP_DB_ENGINE": "sqlite"}, "s.DEBUG")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("QP_SECRET_KEY", r.stderr)
        r = self._settings_in_new_process({"QP_DB_ENGINE": "sqlite", "QP_SECRET_KEY": "k" * 60}, "s.DEBUG")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("QP_PASSCODE_KEY", r.stderr)

    def test_f1_debug_is_off_unless_asked_for(self):
        r = self._settings_in_new_process(self._live_env(), "s.DEBUG")
        self.assertEqual(r.stdout.strip(), "False", r.stderr)

    # F2: HTTPS
    def test_f2_live_settings_use_https_only_cookies(self):
        r = self._settings_in_new_process(
            self._live_env(), "s.SESSION_COOKIE_SECURE, s.CSRF_COOKIE_SECURE, s.SECURE_SSL_REDIRECT, s.SECURE_HSTS_SECONDS > 0")
        self.assertEqual(r.stdout.strip(), "True True True True", r.stderr)

    # F3: sessions
    def test_f3_session_ends_after_inactivity_and_browser_close(self):
        from django.conf import settings
        self.assertLessEqual(settings.SESSION_COOKIE_AGE, 60 * 60)
        self.assertTrue(settings.SESSION_SAVE_EVERY_REQUEST)
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)

    # F4: sign-in
    def test_f4_account_locks_after_repeated_failures(self):
        from django.conf import settings
        for _ in range(settings.LOGIN_MAX_FAILURES):
            self.client.post(reverse("login"), {"username": "desk1@quickphone.test", "password": "wrong-guess"})
        r = self.client.post(reverse("login"), {"username": "desk1@quickphone.test", "password": TRAINING_PASSWORD})
        self.assertContains(r, "This account is locked after")
        self.assertNotIn("_auth_user_id", self.client.session)
        r = self.client.post(reverse("login"), {"username": "sam@quickphone.test", "password": TRAINING_PASSWORD})
        self.assertEqual(r.status_code, 302)  # other accounts are not affected

    def fail(self, email="desk1@quickphone.test"):
        return self.client.post(reverse("login"), {"username": email, "password": "wrong-guess"})

    def test_f4_the_failure_that_locks_says_locked_with_minutes(self):
        """2026-11-20: a locked account is told it is locked, not that the password is wrong."""
        from django.conf import settings
        for _ in range(settings.LOGIN_MAX_FAILURES - 1):
            self.assertNotContains(self.fail(), "locked after")
        r = self.fail()
        self.assertContains(r, "This account is locked after")
        self.assertContains(r, f"Try again in {settings.LOGIN_LOCK_MINUTES} minutes")
        self.assertNotContains(r, "Email or password is not correct")

    def test_f4_last_tries_are_warned(self):
        from django.conf import settings
        for _ in range(settings.LOGIN_MAX_FAILURES - 3):
            self.assertNotContains(self.fail(), "will lock this account")
        self.assertContains(self.fail(), "2 more failed tries will lock this account")
        self.assertContains(self.fail(), "1 more failed try will lock this account")

    def test_f4_inactive_account_is_told_so_only_with_right_password(self):
        self.desk.active_flag = False
        self.desk.save()
        r = self.client.post(reverse("login"), {"username": "desk1@quickphone.test", "password": TRAINING_PASSWORD})
        self.assertContains(r, "This account is turned off")
        self.assertNotContains(self.fail(), "turned off")

    def test_f4_nobody_can_end_a_lock_early(self):
        """The unlock was removed: a lock ends only by itself."""
        from django.conf import settings
        from .auth import is_locked
        for _ in range(settings.LOGIN_MAX_FAILURES):
            self.fail()
        self.login(self.manager)
        self.assertContains(self.client.get(reverse("staff")), "Locked")
        page = self.client.get(reverse("staff_edit", args=[self.desk.pk]))
        self.assertContains(page, "The lock ends by itself")
        self.assertNotContains(page, "Unlock")
        self.client.post(reverse("staff_edit", args=[self.desk.pk]), {"action": "unlock"})
        self.assertTrue(is_locked("desk1@quickphone.test"))
        self.client.post(reverse("staff_edit", args=[self.desk.pk]), {
            "first_name": "Fatima", "last_name": "Reyes", "email": "desk1@quickphone.test", "role": m.FRONT_DESK,
            "store_id": self.store1.pk, "active_flag": "on", "password": "A-new-long-passphrase-26"})
        self.assertTrue(is_locked("desk1@quickphone.test"))

    def test_f4_successful_sign_in_resets_the_count(self):
        from .auth import failures
        for _ in range(2):
            self.client.post(reverse("login"), {"username": "desk1@quickphone.test", "password": "wrong-guess"})
        self.assertEqual(failures("desk1@quickphone.test"), 2)
        self.client.post(reverse("login"), {"username": "desk1@quickphone.test", "password": TRAINING_PASSWORD})
        self.assertEqual(failures("desk1@quickphone.test"), 0)

    def test_f4_common_numeric_or_short_password_is_refused(self):
        self.login(self.manager)
        for i, weak in enumerate(["password123", "12345678901", "short1"]):
            self.client.post(reverse("staff_new"), {
                "first_name": "Weak", "last_name": "Pass", "email": f"weak{i}@quickphone.test",
                "role": m.FRONT_DESK, "store_id": self.store1.pk, "password": weak})
            self.assertFalse(m.Employee.objects.filter(email=f"weak{i}@quickphone.test").exists(), weak)

    # F6: passcode retention
    def test_f6_passcode_deleted_when_device_released(self):
        from .crypto import encrypt_passcode
        job = self.job("Will not charge")
        job.device_passcode = encrypt_passcode("2468")
        job.save()
        s.record_payment(job, self.desk, job.final_cost, "Card")
        s.release_device(job, self.desk, True, True)
        job.refresh_from_db()
        self.assertIsNone(job.device_passcode)
        self.assertIn("passcode deleted", job.history.latest("history_id").note)

    # F9: training seed
    def test_f9_seed_refuses_when_debug_is_off(self):
        from django.core.management import CommandError, call_command
        jobs = m.RepairJob.objects.count()
        with self.assertRaises(CommandError):
            call_command("seed_training", yes=True)
        self.assertEqual(m.RepairJob.objects.count(), jobs)

    # F11: upload size
    def test_f11_oversized_import_is_refused(self):
        from .views.inventory import MAX_IMPORT_BYTES
        self.login(self.manager)
        header = b"sku,part_name,device_model,grade,standard_cost,supplier,quantity_on_hand,reorder_point\n"
        f = io.BytesIO(header + b"x" * MAX_IMPORT_BYTES)
        f.name = "parts.csv"
        r = self.client.post(reverse("inventory_import"), {"file": f}, follow=True)
        self.assertContains(r, "larger than 1 MB")

    # G1: controls that had no test
    def test_g1_other_store_records_cannot_be_opened_by_id(self):
        job = self._store2_job()
        self.login(self.desk)
        self.assertEqual(self.client.get(reverse("job_detail", args=[job.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("job_ticket", args=[job.pk])).status_code, 404)
        self.client.post(reverse("job_detail", args=[job.pk]), {"action": "release", "id_verified": "on", "receipt_signed": "on"})
        job.refresh_from_db()
        self.assertNotEqual(job.status, m.CLOSED)
        part = m.Part.objects.filter(default_supplier__isnull=False).first()
        manager2 = m.Employee.objects.get(email="manager2@quickphone.test")
        po = s.add_to_po(self.store2, part, 1, manager2)
        self.login(self.manager)
        self.assertEqual(self.client.get(reverse("po_detail", args=[po.pk])).status_code, 404)

    def test_g1_technician_cannot_open_another_technicians_job(self):
        job = m.RepairJob.objects.filter(assigned_tech=self.jordan).exclude(status=m.CLOSED).first()
        self.login(self.sam)
        self.assertEqual(self.client.get(reverse("bench_job", args=[job.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("bench_job", args=[job.pk]), {"action": "start"}).status_code, 404)

    def test_g1_staff_cannot_change_own_role(self):
        self.login(self.manager)
        self.client.post(reverse("staff_edit", args=[self.manager.pk]), {
            "first_name": self.manager.first_name, "last_name": self.manager.last_name, "email": self.manager.email,
            "role": m.TECHNICIAN, "store_id": self.store1.pk, "active_flag": "on"})
        self.manager.refresh_from_db()
        self.assertEqual(self.manager.role, m.MANAGER)

    def test_g1_store_switch_does_not_redirect_off_site(self):
        self.login(self.owner)
        r = self.client.post(reverse("switch_store"), {"store_id": self.store2.pk, "next": "https://evil.example/"})
        self.assertNotIn("evil.example", r["Location"])

    def test_g1_form_post_without_csrf_token_is_refused(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.desk)
        job = self.job("Will not charge")
        r = client.post(reverse("job_detail", args=[job.pk]), {"action": "payment", "amount": "1", "method": "Cash"})
        self.assertEqual(r.status_code, 403)
        self.assertFalse(m.Payment.objects.filter(repair_job=job).exists())


class DefectRegressionTests(Base):
    """One test per defect found by the system tests (specification section 3.3, 2026-11-08)."""

    def waiting_job_short_of_one(self):
        """Quoted 2 of a part with 1 on hand, so the job waits with only the shortfall recorded as needed."""
        device = m.Customer.objects.get(first_name="Maria").devices.get(model="iPhone 13")
        job = s.check_in(self.desk, self.store1, device, "Two digitizers", technician=self.sam,
                         quote_lines=[(self.part("QP-DIG-IPD9"), 2)])
        s.start_diagnosis(job, self.sam)
        s.confirm_repair(job, self.sam, "Needs two")
        self.assertEqual(job.status, m.AWAITING_PARTS)
        return job

    def test_d1_fr06_job_keeps_waiting_until_the_full_quantity_is_in_stock(self):
        job = self.waiting_job_short_of_one()
        self.assertEqual(s.release_waiting_jobs(self.store1, self.manager), [])
        job.refresh_from_db()
        self.assertEqual(job.status, m.AWAITING_PARTS)

    def test_d1_fr06_job_resumes_when_the_full_quantity_is_in_stock_and_can_finish(self):
        job = self.waiting_job_short_of_one()
        s.adjust_stock(self.store1, self.part("QP-DIG-IPD9"), 1, "Found one", self.manager)
        job.refresh_from_db()
        self.assertEqual(job.status, m.IN_REPAIR)
        s.complete_repair(job, self.sam, "Done")
        self.assertEqual(self.on_hand("QP-DIG-IPD9"), 0)

    def test_d2_fr06_count_increase_releases_a_waiting_job(self):
        job = self.job("Battery swelling")
        released = s.adjust_stock(self.store1, self.part("QP-BAT-S22"), 1, "Found in back room", self.manager)
        job.refresh_from_db()
        self.assertEqual([j.pk for j in released], [job.pk])
        self.assertEqual(job.status, m.IN_REPAIR)

    def test_d2_count_decrease_releases_nothing(self):
        self.assertEqual(s.adjust_stock(self.store1, self.part("QP-ADH-KIT"), -1, "Damaged", self.manager), [])
        self.assertEqual(self.job("Battery swelling").status, m.AWAITING_PARTS)

    def test_d3_fr08_bad_payment_amounts_are_refused(self):
        job = self.job("Will not charge")
        for bad in ("ABCD", "NaN", "Infinity", "0.005", "100000000"):
            with self.subTest(amount=bad), self.assertRaises(s.RuleError):
                s.record_payment(job, self.desk, bad, "Cash")
        self.assertEqual(job.payments.count(), 0)

    def test_d3_fr08_non_numeric_amount_on_the_screen_shows_a_message(self):
        self.login(self.desk)
        job = self.job("Will not charge")
        response = self.client.post(reverse("job_detail", args=[job.pk]),
                                    {"action": "payment", "amount": "ABCD", "method": "Cash"}, follow=True)
        self.assertContains(response, "Enter the amount as a number")

    def test_d5_tampered_ids_do_not_cause_a_server_error(self):
        self.client.raise_request_exception = False
        self.login(self.desk)
        maria = m.Customer.objects.get(first_name="Maria")
        device = maria.devices.get(model="iPhone 13")
        jobs_before = m.RepairJob.objects.count()
        posts = [("checkin", {"customer_id": maria.pk, "device_id": device.pk, "reported_issue": "x", "technician_id": "abc"}),
                 ("checkin", {"customer_id": maria.pk, "device_id": "abc", "reported_issue": "x"}),
                 ("checkin", {"customer_id": "abc", "reported_issue": "x"}),
                 ("appointment_new", {"customer_id": maria.pk, "slot": "2030-01-01T10:00:00"})]
        results = [self.client.post(reverse(name), data).status_code for name, data in posts]
        results.append(self.client.get(reverse("checkin") + "?appointment=abc").status_code)
        self.login(self.manager)
        results.append(self.client.post(reverse("inventory"), {"part_id": "abc", "action": "adjust"}).status_code)
        self.login(self.owner)
        results.append(self.client.post(reverse("switch_store"), {"store_id": "abc"}).status_code)
        self.assertTrue(all(code < 500 for code in results), results)
        self.assertEqual(m.RepairJob.objects.count(), jobs_before + 1)  # only the first post was a complete job

    def test_d6_fr02_malformed_customer_email_is_refused(self):
        self.login(self.desk)
        before = m.Customer.objects.count()
        response = self.client.post(reverse("checkin"), {
            "first_name": "Riley", "last_name": "Test", "phone": "(919) 555-0999", "email": "not-an-email",
            "device_model_id": self.listed("iPhone 13").pk, "reported_issue": "No sound"}, follow=True)
        self.assertContains(response, "valid email address")
        self.assertEqual(m.Customer.objects.count(), before)


class ReceiptTests(Base):
    """The customer signs a printed receipt at pickup (decision 2026-11-08, FR08)."""

    def paid_job(self):
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, "50.00", "Card")
        return job

    def test_fr08_release_needs_the_signed_receipt(self):
        job = self.paid_job()
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, True, False)
        job.refresh_from_db()
        self.assertEqual(job.status, m.READY)
        self.assertIsNone(job.signature_file)

    def test_fr08_signed_release_records_the_paper_receipt(self):
        job = self.paid_job()
        s.release_device(job, self.desk, True, True)
        job.refresh_from_db()
        self.assertEqual(job.status, m.CLOSED)
        self.assertEqual(job.signature_file, f"Paper receipt {job.ticket_number}")
        self.assertIn("receipt signed", job.history.first().note)

    def test_fr08_unrepaired_device_also_needs_the_signed_receipt(self):
        job = self.job("Keyboard not responding")
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, True, False)
        s.release_device(job, self.desk, True, True)
        self.assertEqual(job.status, m.CLOSED)

    def test_fr08_receipt_shows_charges_and_a_signature_line(self):
        self.login(self.desk)
        job = self.paid_job()
        response = self.client.get(reverse("job_receipt", args=[job.pk]))
        self.assertContains(response, job.ticket_number)
        self.assertContains(response, "Customer signature")
        self.assertContains(response, "50.00")

    def test_fr08_receipt_waits_for_pickup(self):
        self.login(self.desk)
        job = self.job("Cracked screen")
        response = self.client.get(reverse("job_receipt", args=[job.pk]), follow=True)
        self.assertContains(response, "printed at pickup")

    def test_nfr04_receipt_has_no_passcode_and_technician_cannot_open_it(self):
        job = self.job("Cracked screen")
        s.complete_repair(job, self.sam, "Done")
        self.login(self.desk)
        self.assertNotContains(self.client.get(reverse("job_receipt", args=[job.pk])), "482916")
        self.login(self.sam)
        self.assertEqual(self.client.get(reverse("job_receipt", args=[job.pk])).status_code, 403)



class ThermalSlipTests(Base):
    """The ticket, tag and receipt print on an 80 mm thermal receipt printer (decision 2026-11-20)."""

    def test_ticket_and_receipt_use_the_slip_layout(self):
        self.login(self.desk)
        ticket = self.client.get(reverse("job_ticket", args=[self.job("Cracked screen").pk]))
        self.assertContains(ticket, '<body class="print-slip">', html=False)
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, "50.00", "Card")
        self.assertContains(self.client.get(reverse("job_receipt", args=[job.pk])), '<body class="print-slip">', html=False)
        self.assertNotContains(self.client.get(reverse("jobs")), "print-slip")

    def test_print_dialog_opens_only_when_asked(self):
        self.login(self.desk)
        url = reverse("job_ticket", args=[self.job("Cracked screen").pk])
        self.assertNotContains(self.client.get(url), "window.print();")
        self.assertContains(self.client.get(url, {"print": "1"}), "window.print();")

    def test_job_screen_print_links_open_the_dialog(self):
        self.login(self.desk)
        job = self.job("Will not charge")
        page = self.client.get(reverse("job_detail", args=[job.pk]))
        self.assertContains(page, reverse("job_ticket", args=[job.pk]) + "?print=1")
        self.assertContains(page, reverse("job_receipt", args=[job.pk]) + "?print=1")

class DeploymentTests(TestCase):
    """Live-server setup for the live deployment (2026-11-06):
    the setup_live command, the shared lockout cache and the WhiteNoise static-file settings."""

    def _run_setup(self, answers, passwords, **options):
        from unittest import mock
        from django.core.management import call_command
        out, err = io.StringIO(), io.StringIO()
        with mock.patch("builtins.input", side_effect=answers), \
                mock.patch("shop.management.commands.setup_live.getpass.getpass", side_effect=passwords):
            call_command("setup_live", stdout=out, stderr=err, **options)
        return out.getvalue(), err.getvalue()

    STORE_ANSWERS = ["North", "1 Main St, Raleigh", "919-555-0101", "north@shop.example",
                     "South", "2 Oak Ave, Raleigh", "919-555-0102", "south@shop.example"]
    OWNER_ANSWERS = ["Pat", "Example", "Owner@Shop.example"]
    GOOD_PASSWORD = "harbor-violet-71"

    def test_setup_live_creates_stores_and_owner_with_hashed_password(self):
        self._run_setup(self.STORE_ANSWERS + self.OWNER_ANSWERS, [self.GOOD_PASSWORD] * 2)
        self.assertEqual(list(m.Store.objects.values_list("store_name", flat=True)), ["North", "South"])
        owner = m.Employee.objects.get()
        self.assertEqual((owner.role, owner.store.store_name, owner.email), (m.OWNER, "North", "Owner@shop.example"))
        self.assertNotEqual(owner.password, self.GOOD_PASSWORD)
        self.assertTrue(owner.check_password(self.GOOD_PASSWORD))
        self.assertTrue(self.client.login(username=owner.email, password=self.GOOD_PASSWORD))

    def test_setup_live_rejects_weak_and_mismatched_passwords_before_saving(self):
        _, err = self._run_setup(self.STORE_ANSWERS + self.OWNER_ANSWERS,
                                 ["short", "short", self.GOOD_PASSWORD, "different-one-22",
                                  self.GOOD_PASSWORD, self.GOOD_PASSWORD])
        self.assertIn("too short", err)
        self.assertIn("do not match", err)
        self.assertTrue(m.Employee.objects.get().check_password(self.GOOD_PASSWORD))

    def test_setup_live_asks_again_for_an_invalid_email(self):
        answers = ["North", "1 Main St", "919-555-0101", "not-an-email", "north@shop.example"] + self.OWNER_ANSWERS
        _, err = self._run_setup(answers, [self.GOOD_PASSWORD] * 2, stores=1)
        self.assertIn("valid email", err)
        self.assertEqual(m.Store.objects.get().email_address, "north@shop.example")

    def test_setup_live_refuses_a_database_that_already_has_records(self):
        from django.core.management.base import CommandError
        Command().load()
        before = (m.Store.objects.count(), m.Employee.objects.count())
        with self.assertRaises(CommandError):
            self._run_setup([], [])
        self.assertEqual((m.Store.objects.count(), m.Employee.objects.count()), before)

    def test_lockout_count_works_with_the_database_cache(self):
        from django.core.management import call_command
        from django.test import override_settings
        from . import auth
        db_cache = {"default": {"BACKEND": "django.core.cache.backends.db.DatabaseCache", "LOCATION": "qp_cache"}}
        with override_settings(CACHES=db_cache):
            call_command("createcachetable", verbosity=0)
            for _ in range(5):
                auth.record_failure("someone@shop.example")
            self.assertTrue(auth.is_locked("SOMEONE@shop.example"))
            auth.clear_failures("someone@shop.example")
            self.assertFalse(auth.is_locked("someone@shop.example"))

    def _live_process(self, code, extra_env=None):
        import os
        import subprocess
        import sys
        from cryptography.fernet import Fernet
        from django.conf import settings
        env = {k: v for k, v in os.environ.items() if not k.startswith("QP_")}
        env.update({"QP_DB_ENGINE": "sqlite", "QP_SECRET_KEY": "k" * 60,
                    "QP_PASSCODE_KEY": Fernet.generate_key().decode(),
                    "DJANGO_SETTINGS_MODULE": "quickphone.settings"}, **(extra_env or {}))
        return subprocess.run([sys.executable, "-c", code], cwd=settings.BASE_DIR, env=env,
                              capture_output=True, text=True)

    def test_live_settings_use_shared_cache_and_whitenoise(self):
        r = self._live_process(
            "import django; django.setup(); from django.conf import settings as s; "
            "print(s.CACHES['default']['BACKEND'], s.STORAGES['staticfiles']['BACKEND'], "
            "'whitenoise.middleware.WhiteNoiseMiddleware' in s.MIDDLEWARE)")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.split(), ["django.core.cache.backends.db.DatabaseCache",
                                            "whitenoise.storage.CompressedManifestStaticFilesStorage", "True"])

    def test_live_migrate_creates_the_cache_table(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "live.sqlite3")
            r = self._live_process(
                "import django; django.setup(); from django.core.management import call_command; "
                "call_command('migrate', verbosity=0); from django.db import connection; "
                "print('qp_cache' in connection.introspection.table_names())",
                {"QP_SQLITE_PATH": path})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.strip(), "True")


class SecurityPermissionFixTests(Base):
    def staff_data(self, user=None, role=m.FRONT_DESK):
        return {"first_name": "Casey", "last_name": "River", "email": user.email if user else "casey@quickphone.test",
                "role": role, "store_id": self.store1.pk, "password": "Distinct-long-phrase-472", "active_flag": "on"}

    def grant(self, role, screen):
        m.ScreenAccess.objects.update_or_create(role=role, screen=screen, defaults={"allowed": True})

    def test_manager_cannot_create_manager_or_owner(self):
        self.login(self.manager)
        for role in (m.MANAGER, m.OWNER):
            response = self.client.post(reverse("staff_new"), self.staff_data(role=role))
            self.assertContains(response, "Only the Owner can give")
        self.assertFalse(m.Employee.objects.filter(email="casey@quickphone.test").exists())

    def test_staff_screen_override_cannot_escalate_low_privilege_accounts(self):
        for user in (self.sam, self.desk):
            self.grant(user.role, "staff")
            self.login(user)
            self.assertEqual(self.client.get(reverse("staff_new")).status_code, 403)
            self.assertEqual(self.client.post(reverse("staff_new"), self.staff_data(role=m.MANAGER)).status_code, 403)
            self.assertEqual(self.client.post(reverse("staff_edit", args=[self.manager.pk]), self.staff_data(self.manager)).status_code, 403)

    def test_manager_cannot_reset_peer_or_demote_peer(self):
        peer = m.Employee.objects.create_user("peer@quickphone.test", "Another-long-phrase-42", store=self.store1,
                                              first_name="Peer", last_name="Manager", role=m.MANAGER)
        before = peer.password
        self.login(self.manager)
        self.assertEqual(self.client.post(reverse("staff_edit", args=[peer.pk]), self.staff_data(peer)).status_code, 403)
        peer.refresh_from_db()
        self.assertEqual((peer.role, peer.password), (m.MANAGER, before))

    def test_manager_can_manage_front_desk_and_technician(self):
        self.login(self.manager)
        for user in (self.desk, self.sam):
            self.assertEqual(self.client.post(reverse("staff_edit", args=[user.pk]), self.staff_data(user, user.role)).status_code, 302)
            user.refresh_from_db()
            self.assertTrue(user.check_password("Distinct-long-phrase-472"))

    def test_owner_can_create_and_reset_manager(self):
        self.login(self.owner)
        self.assertEqual(self.client.post(reverse("staff_new"), self.staff_data(role=m.MANAGER)).status_code, 302)
        self.assertEqual(self.client.post(reverse("staff_edit", args=[self.manager.pk]), self.staff_data(self.manager, m.MANAGER)).status_code, 302)
        self.assertTrue(m.AuditEvent.objects.filter(action="staff_created", actor=self.owner).exists())

    def test_manager_cannot_manage_other_store_accounts(self):
        other = m.Employee.objects.get(email="manager2@quickphone.test")
        self.login(self.manager)
        self.assertEqual(self.client.get(reverse("staff_edit", args=[other.pk])).status_code, 404)

    def test_manager_can_update_own_profile_without_changing_role(self):
        self.login(self.manager)
        self.assertEqual(self.client.post(reverse("staff_edit", args=[self.manager.pk]), self.staff_data(self.manager, m.MANAGER)).status_code, 302)
        self.manager.refresh_from_db()
        self.assertEqual(self.manager.role, m.MANAGER)

    def test_dashboard_override_only_returns_home_store(self):
        for user in (self.manager, self.sam, self.desk):
            self.grant(user.role, "dashboard")
            self.login(user)
            session = self.client.session
            session["store_id"] = m.Store.objects.exclude(pk=self.store1.pk).first().pk
            session.save()
            response = self.client.get(reverse("dashboard"))
            self.assertEqual([s["store"].pk for s in response.context["stores"]], [user.store_id])
            self.assertNotContains(response, "Both stores at a glance")
            self.assertNotContains(response, "Open this store&#x27;s jobs")

    def test_dashboard_stays_closed_by_default_and_owner_sees_both(self):
        self.login(self.sam)
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 403)
        self.login(self.owner)
        self.assertEqual(len(self.client.get(reverse("dashboard")).context["stores"]), m.Store.objects.count())

    def test_technician_contact_lookup_and_assigned_passcode_remain_available(self):
        self.login(self.sam)
        job = self.job("Cracked screen")
        response = self.client.get(reverse("bench_job", args=[job.pk]))
        self.assertContains(response, "482916")
        self.assertContains(response, job.customer.phone)
        self.assertEqual(self.client.get(reverse("checkin"), {"customer": job.customer.pk}).status_code, 200)

    def test_manager_can_still_self_approve_po_but_technician_cannot(self):
        po = m.PurchaseOrder.objects.create(store=self.store1, supplier=m.Supplier.objects.first(),
                                            created_by=self.manager, po_status=m.PO_PENDING)
        s.approve_po(po, self.manager)
        po.refresh_from_db()
        self.assertEqual(po.approved_by, self.manager)
        with self.assertRaises(s.RuleError):
            s.approve_po(po, self.sam)


class PaymentVoidSecurityTests(Base):
    def paid(self):
        job = self.job("Will not charge")
        s.record_payment(job, self.desk, job.final_cost, "Card")
        return job, job.payments.get()

    def test_void_retains_original_payment_and_excludes_it_from_balance(self):
        job, payment = self.paid()
        original = (payment.amount, payment.method, payment.paid_at)
        s.void_payment(job, self.desk, payment.pk, "Duplicate register entry")
        payment.refresh_from_db()
        self.assertEqual((payment.amount, payment.method, payment.paid_at), original)
        self.assertEqual(payment.payment_status, "Voided")
        self.assertEqual(payment.voided_by, self.desk)
        self.assertEqual(payment.void_reason, "Duplicate register entry")
        self.assertIsNotNone(payment.voided_at)
        self.assertEqual(job.amount_paid, 0)
        self.assertTrue(m.AuditEvent.objects.filter(action="payment_voided", actor=self.desk, target_id=str(payment.pk)).exists())
        with self.assertRaises(s.RuleError):
            s.release_device(job, self.desk, True, True)

    def test_void_requires_reason_and_cannot_repeat(self):
        job, payment = self.paid()
        for reason in ("", "   ", "x" * 201):
            with self.assertRaises(s.RuleError):
                s.void_payment(job, self.desk, payment.pk, reason)
        s.void_payment(job, self.desk, payment.pk, "Duplicate")
        with self.assertRaises(s.RuleError):
            s.void_payment(job, self.desk, payment.pk, "Changed again")
        self.assertEqual(m.AuditEvent.objects.filter(action="payment_voided", target_id=str(payment.pk)).count(), 1)

    def test_void_cannot_cross_store_even_with_screen_override(self):
        job, payment = self.paid()
        other = m.Employee.objects.get(email="manager2@quickphone.test")
        with self.assertRaises(s.RuleError):
            s.void_payment(job, other, payment.pk, "Wrong store")
        self.login(other)
        self.assertEqual(self.client.post(reverse("job_detail", args=[job.pk]), {
            "action": "void_payment", "payment_id": payment.pk, "reason": "Wrong store"}).status_code, 404)
        payment.refresh_from_db()
        self.assertEqual(payment.payment_status, "Paid")

    def test_technician_can_void_when_owner_grants_repair_jobs(self):
        job, payment = self.paid()
        m.ScreenAccess.objects.create(role=m.TECHNICIAN, screen="jobs", allowed=True)
        self.login(self.jordan)
        response = self.client.post(reverse("job_detail", args=[job.pk]), {
            "action": "void_payment", "payment_id": payment.pk, "reason": "Duplicate entry"}, follow=True)
        self.assertContains(response, "Payment voided.")
        self.assertContains(response, "Duplicate entry")
        self.assertContains(response, "Voided")
        self.assertNotContains(response, 'value="delete_payment"')
        payment.refresh_from_db()
        self.assertEqual(payment.voided_by, self.jordan)

    def test_receipt_excludes_voided_payments(self):
        job, payment = self.paid()
        s.void_payment(job, self.desk, payment.pk, "Duplicate")
        s.record_payment(job, self.desk, job.final_cost, "Cash")
        self.login(self.desk)
        response = self.client.get(reverse("job_receipt", args=[job.pk]))
        self.assertNotContains(response, ", Card</dt>")
        self.assertContains(response, ", Cash</dt>")
        self.assertEqual(job.amount_paid, job.final_cost)

    def test_stale_job_cannot_void_payment_after_release(self):
        job, payment = self.paid()
        stale = m.RepairJob.objects.get(pk=job.pk)
        s.release_device(job, self.desk, True, True)
        with self.assertRaises(s.RuleError):
            s.void_payment(stale, self.desk, payment.pk, "Late correction")
        payment.refresh_from_db()
        self.assertEqual(payment.payment_status, "Paid")


    def test_payment_correction_rolls_back_when_audit_record_fails(self):
        from unittest.mock import patch
        job, payment = self.paid()
        history_count = job.history.count()
        with patch("shop.audit.record", side_effect=RuntimeError("Audit storage failed")):
            with self.assertRaises(RuntimeError):
                s.void_payment(job, self.desk, payment.pk, "Duplicate")
        payment.refresh_from_db()
        self.assertEqual(payment.payment_status, "Paid")
        self.assertEqual(payment.void_reason, "")
        self.assertEqual(job.history.count(), history_count)

    def test_service_refuses_technician_without_repair_jobs_access(self):
        job, payment = self.paid()
        with self.assertRaises(s.RuleError):
            s.void_payment(job, self.jordan, payment.pk, "Duplicate")
        payment.refresh_from_db()
        self.assertEqual(payment.payment_status, "Paid")


class AuditRecordTests(Base):
    def test_signins_and_failures_are_logged_without_credentials(self):
        self.client.post(reverse("login"), {"username": self.desk.email, "password": "bad-password"})
        failed = m.AuditEvent.objects.get(action="sign_in", outcome="Failure")
        self.assertNotIn("bad-password", str(failed.details))
        self.assertNotIn(self.desk.email, str(failed.details))
        self.assertIn("login_hash", failed.details)
        self.client.post(reverse("login"), {"username": self.desk.email, "password": TRAINING_PASSWORD})
        self.assertTrue(m.AuditEvent.objects.filter(action="sign_in", outcome="Success", actor=self.desk).exists())

    def test_passcode_audit_records_viewer_without_passcode(self):
        job = self.job("Cracked screen")
        self.login(self.sam)
        self.client.get(reverse("bench_job", args=[job.pk]))
        event = m.AuditEvent.objects.get(action="passcode_view", target_id=str(job.pk))
        self.assertEqual(event.actor, self.sam)
        self.assertNotIn("482916", str(event.details))
        self.login(self.desk)
        self.client.get(reverse("job_detail", args=[job.pk]))
        self.assertFalse(m.AuditEvent.objects.filter(action="passcode_view", actor=self.desk).exists())

    def test_only_owner_can_read_audit_even_with_all_screens_open(self):
        from .permissions import SCREENS
        for user in (self.manager, self.sam, self.desk):
            for screen in SCREENS:
                m.ScreenAccess.objects.update_or_create(role=user.role, screen=screen, defaults={"allowed": True})
            self.login(user)
            self.assertEqual(self.client.get(reverse("audit_events")).status_code, 403)
        self.login(self.owner)
        self.assertContains(self.client.get(reverse("audit_events")), "Audit records")

    def test_permission_changes_and_reset_are_recorded(self):
        self.login(self.owner)
        self.client.post(reverse("access"), {"dashboard|Manager": "on"})
        self.assertTrue(m.AuditEvent.objects.filter(action="screen_access_changed", actor=self.owner,
                                                    details__role=m.MANAGER, details__screen="dashboard").exists())
        self.client.post(reverse("access"), {"action": "reset"})
        self.assertTrue(m.AuditEvent.objects.filter(action="screen_access_reset", actor=self.owner).exists())

    def test_audit_events_are_read_only_in_application(self):
        event = m.AuditEvent.objects.create(action="test", actor=self.owner)
        event.action = "changed"
        with self.assertRaises(ValueError):
            event.save()
        with self.assertRaises(ValueError):
            event.delete()
        with self.assertRaises(ValueError):
            m.AuditEvent.objects.filter(pk=event.pk).update(action="changed")
        with self.assertRaises(ValueError):
            m.AuditEvent.objects.filter(pk=event.pk).delete()
