"""Set up an empty live system: the stores and the first Owner account (deployment plan, section 6).

The Employee model has no createsuperuser path, so this command is the only way to create the
first account on a new database. It asks for every value at the keyboard and reads the password
without echoing it; only the password hash is stored. It refuses to run on a database that
already has a store or an account, so it cannot overwrite a working system. After it finishes,
the Owner signs in and creates every other account on the Staff screen.

    python app/manage.py setup_live
"""
import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.db import transaction

from shop import models as m


class Command(BaseCommand):
    help = "Create the stores and the first Owner account on an empty live database."

    def add_arguments(self, parser):
        parser.add_argument("--stores", type=int, default=2, help="How many stores to create (default 2).")

    def ask(self, label, check=None):
        while True:
            value = input(f"{label}: ").strip()
            if not value:
                self.stderr.write("A value is required.")
                continue
            if check:
                try:
                    check(value)
                except ValidationError as e:
                    self.stderr.write(" ".join(e.messages))
                    continue
            return value

    def ask_password(self, owner):
        while True:
            first = getpass.getpass("Owner password (10+ characters, not shown): ")
            if first != getpass.getpass("Type it again: "):
                self.stderr.write("The two passwords do not match.")
                continue
            try:
                validate_password(first, user=owner)
            except ValidationError as e:
                self.stderr.write(" ".join(e.messages))
                continue
            return first

    def handle(self, *args, **options):
        if m.Store.objects.exists() or m.Employee.objects.exists():
            raise CommandError("Refused: this database already has stores or accounts. "
                               "Add staff on the Staff screen instead.")
        if options["stores"] < 1:
            raise CommandError("--stores must be 1 or more.")

        stores = []
        for i in range(1, options["stores"] + 1):
            self.stdout.write(f"Store {i}")
            stores.append(m.Store(
                store_name=self.ask("  Name"),
                address=self.ask("  Address"),
                phone=self.ask("  Phone"),
                email_address=self.ask("  Email the pickup notification is sent from", validate_email),
            ))
        if len({s.store_name.lower() for s in stores}) != len(stores):
            raise CommandError("Two stores have the same name. Nothing was saved; run the command again.")

        self.stdout.write("Owner account (home store is the first store; the Owner sees every store)")
        owner = m.Employee(
            first_name=self.ask("  First name"),
            last_name=self.ask("  Last name"),
            email=m.Employee.objects.normalize_email(self.ask("  Sign-in email", validate_email)),
            role=m.OWNER,
        )
        password = self.ask_password(owner)

        with transaction.atomic():
            for store in stores:
                store.save()
            owner.store = stores[0]
            owner.set_password(password)
            owner.save()
        self.stdout.write(self.style.SUCCESS(
            f"Created {len(stores)} store(s) and the Owner account {owner.email}. "
            "Sign in and add staff on the Staff screen."))
