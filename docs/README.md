# Document index

**Status:** *Submitted* = the version the team turned in (from the shared OneDrive). *Draft* = newer work not yet submitted. *Superseded* = kept for history; a draft replaces it. Every Office file has a Markdown copy under `_text/` at the same path plus `.md`.

## Admin

| File | Status | Notes |
|---|---|---|
| [admin/MIS 4173 Team Contract.docx](admin/) | Signed Aug 30 | Roles rotate each sprint; accountable owner per sprint; AI disclosure rules |
| [admin/Student Consulting MOU.docx](admin/) | Signed Sep 9–13 | Scope, deliverables, sprint calendar, confidentiality |

## Course rules

Transcribed from Canvas so assistants can read them; Canvas stays authoritative.

| File | Notes |
|---|---|
| [course/project-spec.md](course/project-spec.md) | Every deliverable, when it is due, revision policy, team roles, log templates |
| [course/ai-guidelines.md](course/ai-guidelines.md) | Required AI workflow, what to log, Mermaid and Codex rules, submission checklist |
| [course/sprint-3-presentation.md](course/sprint-3-presentation.md) | What the Sprint 3 presentation must show, its evidence and the rubric |
| [course/sprint-4-6-deliverables.md](course/sprint-4-6-deliverables.md) | Sprint 4, 5 and 6 purposes, deliverables and the shared 100-point rubric |

Method reference for every deliverable: Dennis, Wixom, Roth & Haley, *Systems Analysis and Design*, 8th ed. (Wiley, 2021). The PDF is not stored in this repository.

## Planning and reviews

| File | Notes |
|---|---|
| [review-sprints-1-3.md](review-sprints-1-3.md) | Oct 22 check of the current Sprint 1–3 deliverables against the textbook and feedback; findings not yet acted on |
| [plan-sprints-4-6.md](plan-sprints-4-6.md) | Proposed delivery plan for Sprints 4–6, mapped to textbook Ch. 6–13; for the team to adopt or change |

## Sprint 1: problem definition and feasibility

| File | Status | Current version |
|---|---|---|
| Sprint 1 - System Request.docx | Superseded | sprint-3/drafts/Sprint 3 - System Request (revised).docx |
| Sprint 1 - Feasibility Analysis.docx | Superseded | sprint-3/drafts/Sprint 3 - Feasibility Analysis v2.2.docx |
| Sprint 1 - Backlog.docx | Superseded | sprint-3/drafts/Sprint 3 - Product Backlog.xlsx |
| Sprint 1 - Presentation.pptx | Submitted | Slides 3–5 are images only |

The full-length Systems Request (v1.1 at Sprint 1) is not on OneDrive; v1.2 is in `sprint-3/drafts/`.

## Sprint 2: requirements and analysis

| File | Status | Current version |
|---|---|---|
| Sprint 2 - Requirements Catalog and Memo.docx | Superseded (Sep 25 draft) | sprint-3/drafts/Sprint 3 - Requirements Catalog and Memo.docx |
| Sprint 2 - Use Cases.docx | Superseded | sprint-3/drafts/Sprint 3 - Use Cases.docx |
| Sprint 2 - ERD Diagram.docx / .pdf / .png | Superseded (24 entities) | sprint-3/drafts/Sprint 3 - DFD and ERD Models.docx |
| DFDs/ (4 PNGs) | Superseded | Same, plus the slide deck |
| Sprint 2 - Presentation.pptx | Submitted | Its requirement and entity counts are stale |

The OneDrive folder also held `ERD Diagram.docx`, an exact duplicate of the Sprint 2 ERD; only its PDF export is kept here, renamed. The PNG is the ERD image extracted from the .docx so it can be viewed directly.

## Sprint 3: analysis refinement and design (in progress, Oct 19–25)

| File | Status | Notes |
|---|---|---|
| Quick Phone Sprint 3 Prototypes.pptx | Draft | Three interface alternatives (A Workspace, B Guided Counter, C Operations Board), four screens each (appointments, check-in, technician, manager), 12 slides. Oct 23: trace panels re-traced to the rev 2 DFDs, data stores, catalog and use cases. Screenshots still predate the Oct 23 owner answers (Owner PO approval, no passcode, device on the appointment) |
| Sprint 3 - Presentation.pptx | Draft | Team's 14-slide deck (Oct 22; slide 4 alternative matrix and hardware/software summary added Oct 23): changes and fixes, acquisition and technical approach, physical DFD and ERD, three prototypes, limitations/risks/decisions, uncertainty/next steps; speaker scripts on every slide but the prototypes. Prototype traces moved to the rev 2 DFD numbering on Oct 23 |
| drafts/Sprint 3 - Change Log.docx | Draft | How Sprint 1 and Sprint 2 feedback changed each deliverable |
| drafts/Sprint 3 - Requirements Catalog and Memo.docx | Draft | **Catalog of record**: 14 FR + 6 NFR, with Source and Use case columns and Appendix A |
| drafts/Sprint 3 - Use Cases.docx | Draft | UC-01 to UC-13 with inputs, outputs and traces (UC-13 View Repair Status added Oct 22) |
| drafts/Sprint 3 - DFD and ERD Models.docx | Draft | Logical and physical DFDs (Level 0 complete and in four slide parts), 16-entity ERD with the complete physical ERD (Fig. 6.9), data dictionary |
| drafts/Sprint 3 - DFD and ERD Slides.pptx | Draft | 42 slide-sized diagrams with speaker notes |
| drafts/Sprint 3 - Alternative Matrix and Hardware-Software Specification.docx | Draft | Weighted alternative matrix (SAD 8e Fig. 6-6: custom Django/PostgreSQL 415, subscription 350, spreadsheet 285), sensitivity table, architecture and hardware/software specification (Fig. 7-10). Provisional until the owner answers who supports the system |
| drafts/Sprint 3 - Physical DFDs (full set).pdf | Draft | **Physical DFD submission:** reading guide, Level 0 to Level 1 balancing table, context, complete Level 0, eight Level 1s (Oct 22 relabel: textbook flow names, right-angle lines; Oct 23: PostgreSQL and Django references, boundary around each screen user as in Figs. 9-2 and 9-4; Oct 23 owner clarifications, with a page mapping each answer to the diagrams) |
| drafts/Sprint 3 - Physical ERD (full).pdf | Draft | **Physical ERD submission:** all 16 tables, each relationship named both ways as in SAD 8e Fig. 10-8 (Oct 23), plus a notes page (textbook steps, derived columns, the physical DFD flow behind each system field). Oct 23 owner clarifications: optional technician keys, optional device type and brand, encrypted device_passcode |
| drafts/QuickPhone_Use_Case_Diagram.png | Draft | |
| drafts/Sprint 3 - System Request (revised).docx | Draft | One-page system request |
| drafts/Sprint 3 - Systems Request v1.2.docx | Draft | Full systems request, including owner decisions (7.2) |
| drafts/Sprint 3 - Feasibility Analysis v2.2.docx | Draft | Cost figures unchanged from v2.1 |
| drafts/Sprint 3 - Product Backlog.xlsx | Draft | Changes listed on its "Sprint 3 Changes" sheet |
| drafts/Sprint 3 - Owner Design Review Packet.docx | Draft | Sponsor feedback packet: rate three interface alternatives, open business rules, equipment, record check. Screenshots and yellow team notes to fill before sending |

## Sprint 4: working system and specification (Nov 2–8)

| File | Status | Notes |
|---|---|---|
| sprint-4/drafts/ (Requirements Catalog and Memo, Use Cases) | Draft | Sprint 3 documents revised for the Oct 30 owner direction: quote at check-in, one approval, Technician check-in, Manager and Owner repair, device list, Owner-set screen access (FR15 added). DFDs and the use case diagram image are not yet updated |
| deliverables/Sprint4_models/ (local only: `deliverables/` is git-ignored) | Draft | ERD slide source and renders for 19 entities (QUOTE_LINE, DEVICE_MODEL, SCREEN_ACCESS added; PART.sku, PART.labor_cost); `render_erd.sh` rebuilds `slides/`. `dfd_slides.html` holds partial, unreviewed DFD edits from a session that was stopped, so the DFDs are not yet updated |
| [../app/](../app/README.md) | Draft | Working system for the training session: Django 5.2 + PostgreSQL, Prototype A screens, 17 tables (ERD + QUOTE_LINE), 38 automated tests, resettable training data and a 60-minute session plan. Oct 28 build decisions and the documents they affect are in [project-context.md](project-context.md) |
| Specification document | Not started | Needs the test cases and results from `app/shop/tests.py` |

## Logs (updated every sprint)

| File | Purpose |
|---|---|
| admin/AI Decision Log.xlsx | Every major AI use: what it produced, accept/modify/reject, why, who |
| admin/Change Log.xlsx | Running record of changes to submitted deliverables: cause and effect on later work. Sprint 3 rows from the .docx draft log folded in on Oct 22 |
| admin/Time Log.xlsx | Hours per member per sprint, one sheet per sprint |
