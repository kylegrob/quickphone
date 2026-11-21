# Quick Phone Repair Management System: application

A Django 5.2 web application with one PostgreSQL database for both stores. Its screens follow the Workspace design the owner selected, and its tables match the physical ERD in [../planning/diagrams/erd](../planning/diagrams/erd). The business rules it enforces are listed in [../planning/business-rules.md](../planning/business-rules.md). Every person, phone number and address in the sample data is invented.

## Set up once (Windows)

1. Install PostgreSQL 17 (`winget install PostgreSQL.PostgreSQL.17`), and put its `bin` folder on PATH so Python can find `libpq`.
2. Create the database and a login. Choose your own password and keep it out of this repository:
   `psql -U postgres -c "CREATE ROLE quickphone LOGIN PASSWORD '<your password>';"` then `psql -U postgres -c "CREATE DATABASE quickphone OWNER quickphone;"`
3. From the repository root: `python -m venv .venv` and `.venv\Scripts\pip install -r app\requirements.txt`.
4. Set `QP_DB_PASSWORD` to that password in your shell (PowerShell: `$env:QP_DB_PASSWORD = '<your password>'`), and `$env:QP_DEBUG = '1'` on a training machine. Debug is off unless `QP_DEBUG=1`, and with debug off the app refuses to start until `QP_SECRET_KEY` and `QP_PASSCODE_KEY` are set (see Security below). The other settings default to a local database called `quickphone`; see `quickphone/settings.py` for every `QP_` variable.
5. `.venv\Scripts\python app\manage.py migrate`

To try the application without PostgreSQL, set `$env:QP_DB_ENGINE = 'sqlite'` before step 5. That setting exists only for tests and demos.

## Running with sample data

With `QP_DEBUG=1` set, `.venv\Scripts\python app\manage.py seed_training --yes` wipes the database (it refuses when debug is off, so it cannot wipe a live system) and loads the sample data, including fictional staff accounts, so every session starts from the same state. Then start the server with `.venv\Scripts\python app\manage.py runserver` and open http://localhost:8000. Pickup emails are written to `app/sent_emails/` rather than sent.

## Tests

`$env:QP_DB_ENGINE='sqlite'; .venv\Scripts\python app\manage.py test shop` runs 182 regression tests; the November 20 local preview run passed all 182 (see planning/verification/current-regression.txt). Cases trace to the catalogue's acceptance checks. They include the security cases (a Technician approving an order, a Front Desk user opening inventory, an unpaid release, stock below zero, a Manager creating an Owner account, sign-in lockout, weak passwords, other-store records by ID, CSRF, settings that refuse to start without keys) and the live-deployment checks (the `setup_live` command, the shared lockout cache, and the live settings and migration).

## Printer setup (each front desk)

The claim ticket, device tag and pickup receipt print on an 80 mm thermal receipt printer with an auto-cutter, such as the Epson TM-m30III or Star mC-Print3. Printing goes through the browser, so the printer only has to be installed on the desk computer. Install the maker's Windows driver, set the paper to the 80 mm roll, set the driver to cut at the end of each page and trim blank paper at the bottom, and make it the Windows default printer. The device tag starts a new page, so it comes out as its own slip. To print without the dialog, open the app from a Chrome shortcut whose target ends with `--kiosk-printing`, with every other Chrome window closed. Chrome then sends each print straight to the default printer. After check-in the ticket page prints at once. On the job screen, the Reprint ticket and Print receipt buttons print the same way, and the Print button on either page prints again. Without the kiosk shortcut, the print dialog opens instead: pick the thermal printer, set Margins to None, and turn off Headers and footers.

## Security

[../planning/specification.docx](../planning/specification.docx), section 4, lists the assets, threats, controls and residual risks. A live deployment sets, at minimum, `QP_SECRET_KEY` (50+ random characters), `QP_PASSCODE_KEY` (a Fernet key: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`), `QP_ALLOWED_HOSTS` and the database and SMTP variables, and serves the app over HTTPS. Keep the passcode key backed up apart from the database: without it no stored passcode can be read. With debug off, cookies are HTTPS-only, HTTP is redirected (`QP_SSL_REDIRECT`), HSTS starts at 30 days (`QP_HSTS_SECONDS`), and `QP_BEHIND_PROXY=1` trusts a proxy's `X-Forwarded-Proto`. Sessions end after 30 idle minutes (`QP_SESSION_MINUTES`) or when the browser closes. Five failed sign-ins lock that account for 15 minutes (`QP_LOGIN_MAX_FAILURES`, `QP_LOGIN_LOCK_MINUTES`); with debug off the count is kept in a database cache table (`qp_cache`, created by `migrate`), so every server process sees it. New passwords need 10+ characters and cannot be common, all digits, or close to the person's name or email. A device's passcode is deleted when the device is released.

## Deploying a live system

Section 5 of the specification has the hosting plan and go-live steps. On the host, the build step is `pip install -r app/requirements.txt` then `python app/manage.py collectstatic --noinput`, the release step is `python app/manage.py migrate`, and the start command is `gunicorn --chdir app quickphone.wsgi --workers 2 --threads 4`. With debug off, WhiteNoise serves the stylesheet from the app, so no separate file server is needed. Set the variables in Security above plus `QP_BEHIND_PROXY=1`, `QP_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` and the `QP_EMAIL_` login. Never run `seed_training` on a live system (it refuses with debug off).

A new live database starts empty. Run `python app/manage.py setup_live` once, at a terminal on the host: it asks for each store's name, address, phone and sending email, then the Owner's name, sign-in email and password (typed twice and never shown), and refuses to run if the database already has a store or an account. The Owner then signs in and adds staff on the Staff screen. `setup_live --stores 1` creates a single store.

## Where things are

| Path | What it holds |
|---|---|
| `shop/models.py` | The 21 business tables, named as in the physical ERD (including D7 AuditEvent) |
| `shop/services.py` | Every business rule, one function per workflow step (DFD 1.0 to 9.0) |
| `shop/permissions.py` | Who may do what (NFR01), checked on the server |
| `shop/auth.py` | Sign-in lockout after repeated failures |
| `shop/views/` | Screens: `desk.py` Front Desk, `bench.py` Technician, `inventory.py` Manager, `records.py` Owner and records |
| `shop/templates/shop/` | Page layouts |
| `shop/tests.py` | Automated tests |
| `shop/management/commands/seed_training.py` | Sample data for training |
| `shop/management/commands/setup_live.py` | First-time setup of a live database |


## Security changes and database upgrade (November 20)

Apply migration `0008_payment_voids_audit_events` with `python app/manage.py migrate` before running this version against an existing database. Existing payments keep Paid status; new void fields start empty. A mistaken payment is now retained as Voided and requires a reason, with actor/time recorded; voids do not count toward the paid total or appear as payments on the receipt. The UI no longer deletes payment rows. Prior deleted rows cannot be reconstructed by this migration. Payment recording, voiding and release share a job-row transaction lock; verify simultaneous operations on PostgreSQL before live use.

The Owner can open Audit records to review security events. AuditEvent belongs to D7 Staff & Stores; payment void fields belong to D3 Repair Jobs. Audit events are read-only through the app and ORM update/delete operations; direct database administrator access remains outside that protection. Include the audit table in protected backups and agree its retention period before live use. Login failures store a hashed identifier, never the submitted password; passcode-view events identify the job and viewer without storing the passcode. Staff-screen overrides cannot grant account management: only Owner/Manager manage accounts, and only Owner manages other Manager/Owner accounts. Dashboard overrides show a non-Owner only their home store. Technician contact/lookup/assigned-passcode access and Manager/Owner PO self-approval remain in place.
