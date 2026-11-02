# Quick Phone Repair Management System: Sprint 4 working system

This is the Sprint 4 working system, built to run a training session. It is a Django 5.2 web application with one PostgreSQL database for both stores, as the Sprint 3 alternative matrix and hardware/software specification chose. Its screens follow Prototype A (Workspace), which the owner selected (Curation Memo, Oct 24). The tables match the physical ERD (Appendix A of the DFD and ERD Models document), plus two additions approved on Oct 28: QUOTE_LINE and PART.sku. Every person, phone number and address in the sample data is invented.

## Set up once (Windows)

1. Install PostgreSQL 17 (`winget install PostgreSQL.PostgreSQL.17`), and put its `bin` folder on PATH so Python can find `libpq`.
2. Create the database and a login. Choose your own password and keep it out of this repository:
   `psql -U postgres -c "CREATE ROLE quickphone LOGIN PASSWORD '<your password>';"` then `psql -U postgres -c "CREATE DATABASE quickphone OWNER quickphone;"`
3. From the repository root: `python -m venv .venv` and `.venv\Scripts\pip install -r app\requirements.txt`.
4. Set `QP_DB_PASSWORD` to that password in your shell (PowerShell: `$env:QP_DB_PASSWORD = '<your password>'`). The other settings default to a local database called `quickphone`; see `quickphone/settings.py` for every `QP_` variable.
5. `.venv\Scripts\python app\manage.py migrate`

## Before each training session

`.venv\Scripts\python app\manage.py seed_training --yes` wipes the database and reloads the sample data, so every session starts from the same state. Then start the server with `.venv\Scripts\python app\manage.py runserver` and open http://localhost:8000.

Every training account uses the password in `TRAINING_PASSWORD` in `shop/management/commands/seed_training.py`. Hand it out on paper during the session; it exists only for the sample data. Pickup emails are written to `app/sent_emails/` rather than sent, so trainees can open the file and read what the customer would receive.

| Sign in as | Role | Lands on |
|---|---|---|
| desk1@quickphone.test | Front Desk, Store 1 | Check in |
| sam@quickphone.test, jordan@quickphone.test | Technician, Store 1 | Technician jobs |
| manager1@quickphone.test | Manager, Store 1 | Inventory and POs |
| owner@quickphone.test | Owner, both stores | Dashboard |
| desk2@, alex@, manager2@quickphone.test | Store 2 staff | |

## Training session plan (about 60 minutes)

The sample data has one Store 1 job at every step of the workflow, so each exercise starts from a realistic state. Trainees work in pairs, one on a Front Desk screen and one on a Technician screen, and swap halfway.

| # | Exercise (role) | What to do | What the trainee should notice |
|---|---|---|---|
| 1 | Check in from an appointment (Front Desk) | Check in, today's 9:30 appointment, Start check-in. Pick the iPhone 13 on file, type the problem, Create job | Customer and technician come from the appointment; ticket and tag share one number |
| 2 | Walk-in with a new customer (Front Desk) | Search a phone number that does not exist, enter the new customer and device, leave the technician open | Searching by phone first stops duplicate customers; an open job waits for a technician to claim it |
| 3 | Book and reschedule (Front Desk) | Book appointment for tomorrow; then Reschedule it to a time Sam is already booked | Full slots and booked technicians cannot be picked |
| 4 | Claim and diagnose (Technician) | Claim the open Nintendo Switch job, Start diagnosis, tick parts, Send quote | The total builds as parts are ticked, with the Owner's labor added; customer phone and email are never shown on the repair screen |
| 5 | Record the customer's answer (Front Desk) | Repair jobs, open the iPhone 12 job (Awaiting Approval), Customer approved | Repair cannot start before approval; the history records who recorded it |
| 6 | Repair and finish (Technician) | Open the iPhone 13 cracked screen job, check the parts list the quote filled in, add repair notes, Mark ready for pickup | The quote's parts come off stock when the job is marked ready; a job cannot be finished with more parts than are on hand |
| 7 | Order parts (Manager) | Inventory, Add to PO on the Galaxy S22 battery, link the waiting job, Submit; Approve; Mark as ordered; Receive delivery | Every order needs approval; receiving puts the waiting job back to In Repair |
| 8 | Pickup (Front Desk) | Open the Pixel 7 job (Ready for Pickup): Send pickup notification, try Release without paying, record payment, tick Photo ID checked, Release | A repaired device is never released before payment; the email comes from the store's account |
| 9 | Return unrepaired (Front Desk) | Open the IdeaPad job (Returned Unrepaired) and release it with no payment | No fee is charged for a device that cannot be repaired |
| 10 | Both stores (Owner) | Dashboard; switch to Store 2 | Open repairs and low stock side by side |

Ask trainees to finish exercises 1, 4 and 8 without help; that is the acceptance check for NFR03. Note anything that confused them; it is evidence for the Sprint 5 manual and the Change Log.

## Changes from the owner (Oct 30)

- **The quote is shown at check-in.** It is the part cost plus the labor the Owner sets for each part (Inventory, edit a part; only the Owner can change it). When the customer agrees, tick "The customer approves this quote"; repair then needs no second approval. Leave the parts blank when the device needs diagnosis first, and the technician quotes as before.
- **Only an additional repair is re-approved.** From Diagnosing or In Repair the technician sends an additional repair; Front Desk records the answer. A declined additional repair leaves the approved repair going. The approved total is the sum of the approved quotes.
- **Technicians can check in customers** and print the claim ticket, but still cannot open the job list, payment or release.
- **Managers and the Owner can repair devices**: they can be assigned a job, claim an open one and use the same repair screen ("My repair jobs").
- **Brand and model come from a list.** Check-in picks the device from a list (grouped by brand); "Device not on the list? Add it" adds a new type, brand and model for everyone. A model added with different capitalization is matched to the existing one. The starter list is in `shop/device_catalog.py`.
- **The Owner sets screen access by role.** The Access screen (Owner only) is a table of seven screens by four roles; the defaults are the earlier fixed rules and only changed boxes are stored. It controls which screens a role can open. It does not change the rules inside a screen: only a Manager or the Owner approves a purchase order, technicians work only on their own jobs, customer phone and email stay hidden from the Technician role, and only the Owner can give the Owner role. Opening Staff, suppliers and stores lets a role create accounts in its own store.
- Open for the owner: technicians now see customer phone and email on the check-in screen only; labor is charged per part times quantity, so a labor-only repair needs a zero-cost "service" part.

## Business rules decided for this build (Oct 28)

These answer open questions in `docs/project-context.md`. The documents listed in that file still need updating to match.

- **Technicians may send the pickup notification** (owner answer #1, Oct 23), but never see the customer's address. This supersedes NFR05.
- **Quoted parts are stored in a new QUOTE_LINE table**, so the technician sees them again after approval. JOB_PART "Needed" keeps its meaning: a part the job is waiting for.
- **A declined quote returns the device unrepaired.** Front Desk may record a fee, but none is required to release it.
- **The passcode** is visible to the assigned technician, Managers and the Owner.
- **Managers work only in their home store**; only the Owner switches stores.
- **A Manager may approve an order they created**; history keeps both names. Set `ALLOW_SELF_APPROVAL_OF_PO` in `shop/permissions.py` to change this.
- **PART has a SKU** (Prototype A shows one).

Still to confirm with the owner: store hours and appointment slot length (placeholders in `settings.py`), whether intake must collect an email address, and ticket printers.

## Tests

`$env:QP_DB_ENGINE='sqlite'; .venv\Scripts\python app\manage.py test shop` runs 38 tests named after the catalog's acceptance checks, including the security cases: a Technician approving an order, a Front Desk user opening inventory, an unpaid release, stock below zero, and a Manager creating an Owner account. `QP_DB_ENGINE=sqlite` exists only so tests and demos can run on a machine without PostgreSQL.

## Where things are

| Path | What it holds |
|---|---|
| `shop/models.py` | The 17 tables, named as in the physical ERD |
| `shop/services.py` | Every business rule, one function per workflow step (DFD 1.0 to 9.0) |
| `shop/permissions.py` | Who may do what (NFR01), checked on the server |
| `shop/views/` | Screens: `desk.py` Front Desk, `bench.py` Technician, `inventory.py` Manager, `records.py` Owner and records |
| `shop/templates/shop/` | Page layouts (Prototype A) |
| `shop/tests.py` | Automated tests |
| `shop/management/commands/seed_training.py` | Sample data for training |
