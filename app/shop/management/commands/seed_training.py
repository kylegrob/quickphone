"""Loads the training data set: made-up stores, staff, customers, parts and jobs.

Every person, address and phone number here is invented (555 numbers, example.com
and .test addresses). The training password is for this sample data only and is
recorded here, in the project's seed file, not in any document or chat.

    python manage.py seed_training --yes      # wipes the database, then loads
"""
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.core.management import BaseCommand, CommandError, call_command
from django.db import transaction
from django.utils import timezone

from shop import models as m
from shop import services as s
from shop.device_catalog import STARTER_DEVICES

TRAINING_PASSWORD = "QuickPhone-Training-26"

STORES = [
    ("Store 1", "100 Example Avenue, Raleigh, NC", "(919) 555-0100", "store1@quickphone.test"),
    ("Store 2", "200 Sample Road, Raleigh, NC", "(919) 555-0200", "store2@quickphone.test"),
]
# (first, last, email, role, store index)
STAFF = [
    ("Olivia", "Grant", "owner@quickphone.test", m.OWNER, 0),
    ("Morgan", "Lee", "manager1@quickphone.test", m.MANAGER, 0),
    ("Fatima", "Reyes", "desk1@quickphone.test", m.FRONT_DESK, 0),
    ("Sam", "Patel", "sam@quickphone.test", m.TECHNICIAN, 0),
    ("Jordan", "Kim", "jordan@quickphone.test", m.TECHNICIAN, 0),
    ("Chris", "Hall", "manager2@quickphone.test", m.MANAGER, 1),
    ("Dana", "Brooks", "desk2@quickphone.test", m.FRONT_DESK, 1),
    ("Alex", "Moreno", "alex@quickphone.test", m.TECHNICIAN, 1),
]
SUPPLIERS = [("Supplier A", "Pat Quinn", "(800) 555-0111"), ("Supplier B", "Lee Chan", "(800) 555-0122"),
             ("Supplier C", None, "(800) 555-0133")]
# sku, name, model, grade, cost, supplier, (store 1 on hand, reorder), (store 2 on hand, reorder)
PARTS = [
    ("QP-SCR-IP13", "Screen assembly", "iPhone 13", "Grade A", "62.00", 0, (4, 3), (2, 2)),
    ("QP-SCR-IP14", "Screen assembly", "iPhone 14", "Grade A", "78.00", 0, (0, 3), (1, 2)),
    ("QP-DIG-IPD9", "Glass digitizer", "iPad 9th gen", "Grade A", "45.00", 0, (1, 2), (3, 1)),
    ("QP-HBF-IPD9", "Home button flex", "iPad 9th gen", "Grade A", "12.00", 0, (0, 1), (2, 1)),
    ("QP-ADH-KIT", "Adhesive strip kit", None, "Standard", "2.00", 0, (25, 10), (18, 10)),
    ("QP-BAT-IP12", "Battery", "iPhone 12", "Grade A", "28.00", 1, (6, 4), (5, 3)),
    ("QP-BAT-S22", "Battery", "Galaxy S22", "Grade A", "34.00", 1, (0, 2), (1, 2)),
    ("QP-BAT-A54", "Battery", "Galaxy A54", "Grade A", "30.00", 1, (3, 2), (4, 2)),
    ("QP-CHG-USBC", "Charging port", "Pixel 7", "OEM", "15.00", 2, (5, 2), (2, 2)),
    ("QP-CAM-IP13", "Rear camera", "iPhone 13", "OEM", "55.00", 2, (2, 1), (0, 1)),
]
# Repair labor the Owner has set for each part (placeholder prices for training, not the client's).
LABOR = {"QP-SCR-IP13": "55.00", "QP-SCR-IP14": "60.00", "QP-DIG-IPD9": "50.00", "QP-HBF-IPD9": "30.00",
         "QP-BAT-IP12": "40.00", "QP-BAT-S22": "45.00", "QP-BAT-A54": "40.00", "QP-CHG-USBC": "35.00",
         "QP-CAM-IP13": "50.00"}
CUSTOMERS = [
    ("Maria", "Santos", "(919) 555-0142", "m.santos@example.com"),
    ("David", "Okafor", "(919) 555-0157", "d.okafor@example.com"),
    ("Kevin", "Tran", "(919) 555-0163", "k.tran@example.com"),
    ("Aisha", "Bello", "(919) 555-0171", "a.bello@example.com"),
    ("Tom", "Walsh", "(919) 555-0188", None),
    ("Grace", "Liu", "(984) 555-0119", "g.liu@example.com"),
    ("Omar", "Haddad", "(984) 555-0126", "o.haddad@example.com"),
    ("Nina", "Kowalski", "(984) 555-0134", "n.kowalski@example.com"),
]


class Command(BaseCommand):
    help = "Wipe the database and load the made-up training data set."

    def add_arguments(self, parser):
        parser.add_argument("--yes", action="store_true", help="Confirm that every record will be deleted.")

    def handle(self, *args, **options):
        if not options["yes"]:
            raise CommandError("This deletes every record. Run again with --yes to confirm.")
        call_command("flush", interactive=False, verbosity=0)
        with transaction.atomic():
            self.load()
        self.stdout.write(self.style.SUCCESS(
            f"Training data loaded: {m.RepairJob.objects.count()} jobs, {m.Part.objects.count()} parts, "
            f"{m.Employee.objects.count()} staff accounts."))

    def load(self):
        stores = [m.Store.objects.create(store_name=n, address=a, phone=p, email_address=e,
                                         business_hours="Mon-Sat 9 AM-6 PM (placeholder)")
                  for n, a, p, e in STORES]
        staff = {}
        for first, last, email, role, si in STAFF:
            staff[first] = m.Employee.objects.create_user(email, TRAINING_PASSWORD, first_name=first,
                                                         last_name=last, role=role, store=stores[si])
        for device_type, brand, model in STARTER_DEVICES:
            m.DeviceModel.objects.get_or_create(brand=brand, model=model, defaults={"device_type": device_type})
        suppliers = [m.Supplier.objects.create(supplier_name=n, contact_name=c, phone=p) for n, c, p in SUPPLIERS]
        parts = {}
        for sku, name, model, grade, cost, si, st1, st2 in PARTS:
            part = m.Part.objects.create(sku=sku, part_name=name, device_model=model, grade=grade,
                                         standard_cost=Decimal(cost), labor_cost=Decimal(LABOR.get(sku, "0")),
                                         default_supplier=suppliers[si])
            parts[sku] = part
            for store, (qty, reorder) in zip(stores, (st1, st2)):
                m.StorePartStock.objects.create(store=store, part=part, reorder_point=reorder)
                if qty:
                    s.adjust_stock(store, part, qty, "Opening count", staff["Morgan"], m.TXN_IMPORT)
        cust = [m.Customer.objects.create(first_name=f, last_name=l, phone=p, email=e) for f, l, p, e in CUSTOMERS]
        maria, david, kevin, aisha, tom, grace, omar, nina = cust

        def device(c, kind, brand, model, serial=None):
            return m.Device.objects.create(customer=c, device_type=kind, brand=brand, model=model,
                                           serial_or_imei=serial)

        s1, s2 = stores
        desk, sam, jordan, alex, morgan = staff["Fatima"], staff["Sam"], staff["Jordan"], staff["Alex"], staff["Morgan"]
        maria_phone = device(maria, "Phone", "Apple", "iPhone 13", "356789104512345")
        david_phone = device(david, "Phone", "Samsung", "Galaxy S22")
        kevin_ipad = device(kevin, "Tablet", "Apple", "iPad 9th gen")

        # Today's and tomorrow's appointments (FR01). Created directly so past slots still show.
        tz = timezone.get_current_timezone()
        today, tomorrow = timezone.localdate(), timezone.localdate() + timedelta(days=1)
        for c, t, when in [(maria, sam, time(9, 30)), (david, jordan, time(11, 0)), (aisha, None, time(13, 30))]:
            m.Appointment.objects.create(customer=c, store=s1, technician=t,
                                         scheduled_at=datetime.combine(today, when, tz))
        m.Appointment.objects.create(customer=tom, store=s1, technician=sam,
                                     scheduled_at=datetime.combine(tomorrow, time(10, 0), tz))

        def job(store, dev, issue, tech, condition="", passcode="", by=desk):
            return s.check_in(by, store, dev, issue, condition, passcode, tech)

        # Store 1: one job in every step of the workflow.
        j = job(s1, kevin_ipad, "Shattered glass", sam, "Glass cracked across; display lights up")
        j = job(s1, device(aisha, "Phone", "Samsung", "Galaxy A54"), "No power after rain exposure", sam,
                "Slight corrosion at port")
        s.start_diagnosis(j, sam)
        j = job(s1, device(grace, "Phone", "Apple", "iPhone 12"), "Shuts off under 20 percent", sam)
        s.start_diagnosis(j, sam)
        s.submit_quote(j, sam, "Battery health 61%; fails load test. Replace battery.", "40.00",
                       [(parts["QP-BAT-IP12"], 1)])
        j = job(s1, maria_phone, "Cracked screen", sam, "Touch works; crack top-left", passcode="482916")
        s.start_diagnosis(j, sam)
        s.submit_quote(j, sam, "Display cracked, digitizer intact; replace screen assembly.", "55.00",
                       [(parts["QP-SCR-IP13"], 1), (parts["QP-ADH-KIT"], 1)])
        s.record_decision(j, desk, True)
        j = job(s1, device(omar, "Phone", "Apple", "iPhone 14"), "Green line on display", sam)
        s.start_diagnosis(j, sam)
        s.submit_quote(j, sam, "OLED panel fault; replace screen assembly.", "60.00", [(parts["QP-SCR-IP14"], 1)])
        s.record_decision(j, desk, True)  # out of stock, so Awaiting Parts
        j = job(s1, david_phone, "Battery swelling", jordan, "Back glass lifting")
        s.start_diagnosis(j, jordan)
        s.submit_quote(j, jordan, "Swollen battery; replace and reseal.", "45.00",
                       [(parts["QP-BAT-S22"], 1), (parts["QP-ADH-KIT"], 1)])
        s.record_decision(j, desk, True)
        j = job(s1, device(nina, "Phone", "Google", "Pixel 7"), "Will not charge", jordan)
        s.start_diagnosis(j, jordan)
        s.submit_quote(j, jordan, "Lint cleared; port pins damaged. Replace charging port.", "35.00",
                       [(parts["QP-CHG-USBC"], 1)])
        s.record_decision(j, desk, True)
        s.complete_repair(j, jordan, "Port replaced; charges at 18 W; tested with two cables.")
        j = job(s1, device(tom, "Laptop", "Lenovo", "IdeaPad 3"), "Keyboard not responding", jordan)
        s.start_diagnosis(j, jordan)
        s.mark_unrepairable(j, jordan, "Liquid damage to the board; keyboard controller failed. Not repairable.")
        job(s1, device(maria, "Game console", "Nintendo", "Switch"), "Joy-Con drift", None)
        # Quoted at the counter and approved at check-in, so the technician needs no second approval.
        s.check_in(desk, s1, device(david, "Phone", "Samsung", "Galaxy A54"), "Battery drains fast", "", "", sam,
                   None, [(parts["QP-BAT-A54"], 1)], True)

        # A Manager's purchase order waiting for approval, linked to the iPhone 14 job.
        po = s.add_to_po(s1, parts["QP-SCR-IP14"], 3, morgan)
        s.submit_po(po, morgan, list(s.waiting_job_parts(po).values_list("pk", flat=True)))

        # Store 2: a few jobs so the Owner's dashboard compares both stores.
        j = job(s2, device(grace, "Tablet", "Apple", "iPad 9th gen"), "Home button stuck", alex, by=staff["Dana"])
        s.start_diagnosis(j, alex)
        job(s2, device(omar, "Phone", "Samsung", "Galaxy A54"), "Cracked back glass", None, by=staff["Dana"])
