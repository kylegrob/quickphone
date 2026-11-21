# Quick Phone Repair Management System

A web application that tracks every repair at **Quick Phone Repair & Designs** from appointment and check-in through diagnosis, repair and pickup, and manages parts inventory and purchase orders across both stores.

Prepared for Quick Phone Repair & Designs by Kyle Robertson, Ehsanullah Pardisi, Bara Abusamhan and Leonard Mann.

## What it does

- **Front Desk:** book appointments, check customers in, print claim tickets, record the customer's quote decision and payment, send the pickup notification, and release the device.
- **Technicians:** claim jobs, diagnose, quote parts and labor, record repair work and mark a device ready for pickup.
- **Managers:** keep inventory, raise and receive purchase orders, and approve them.
- **Owner:** approve purchase orders, set labor rates, screen access and repair-type lengths, and see both stores on one dashboard.

## Repository layout

```
README.md       This file
app/            The application (Django, PostgreSQL). Setup, running, tests and deployment: app/README.md
planning/       Analysis and design documents behind the application
  README.md       Index of the documents and diagrams
  system-request.docx
  requirements-catalog.docx
  use-cases.docx, use-case-diagram.png
  specification.docx
  diagrams/       Data flow diagrams, entity relationship diagrams, alignment diagram
  business-rules.md       Decisions made with the owner that shape the application
```

## Quick start

The full instructions, including PostgreSQL setup and deployment, are in [app/README.md](app/README.md). To try the application with sample data and no database server:

```powershell
python -m venv .venv
.venv\Scripts\pip install -r app\requirements.txt
$env:QP_DB_ENGINE = 'sqlite'; $env:QP_DEBUG = '1'
.venv\Scripts\python app\manage.py migrate
.venv\Scripts\python app\manage.py seed_training --yes
.venv\Scripts\python app\manage.py runserver
```

Then open http://localhost:8000. The sample people, phone numbers and addresses are invented.

## Planning documents

Start with [planning/README.md](planning/README.md). The documents build on each other: the system request states the business need, the requirements catalog and use cases define what the system must do, the diagrams model its processes and data, and the specification describes how the application is built.
