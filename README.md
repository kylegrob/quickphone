# Quick Phone Repair Management System

MIS 4173 (Systems Analysis, Design and Development), Fall 2026, Professor John Drake. A student consulting project for **Quick Phone Repair & Designs** (Raleigh, NC; two stores). The system tracks every repair from check-in to pickup and manages parts inventory and purchase orders across both stores.

**Team:** Kyle Robertson, Ehsanullah Pardisi, Bara Abusamhan, Leonard Mann.

> Client information in this repository is confidential under the Student Consulting MOU. Keep the repository private and share it only with the team and course staff.

## Repository layout

```
app/              Working system (Django 5.2 + PostgreSQL); setup and rules in app/README.md
requirements/     Requirements Catalog and Memo (catalog of record)
use-cases/        Use case document and use case diagram
models/
  dfd/logical/    Context, Level 0 (complete and in four parts) and Level 1 DFDs
  dfd/physical/   The same set as physical DFDs
  erd/logical/    ERD overview, three detail views and the full ERD
  erd/physical/   The same set as the physical ERD
  19_DFD_ERD_Alignment   Which DFD data store holds each ERD entity
  source/         HTML sources the diagram images are rendered from
AGENTS.md         Instructions for AI assistants
CLAUDE.md         Points Claude Code at AGENTS.md
```

Each diagram comes as a slide-sized PNG and a vector PDF.

## Running the app

See [app/README.md](app/README.md) for setup, training data and logins.

## Sprint calendar

| Sprint | Dates | Focus |
|---|---|---|
| 1 | Sep 14–20 | Systems request, feasibility |
| 2 | Oct 5–11 | Requirements, use cases, logical DFDs and ERD |
| 3 | Oct 19–25 | Analysis refinement, physical models, interface design |
| 4 | Nov 2–8 | Technical specification, working system |
| 5 | Nov 16–22 | Deployment, training session, user manual |
| 6 | Nov 30–Dec 9 | Final presentation and handoff |
