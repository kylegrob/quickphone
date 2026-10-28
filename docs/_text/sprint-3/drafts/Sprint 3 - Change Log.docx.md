<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - Change Log.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - Change Log

Quick Phone Repair Management System

Sprint 3 Change Log

MIS 4173 | Sprint 3 | Fall 2026 | Team 4: Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann | October 19, 2026

This log records how feedback and new client information changed deliverables from earlier sprints, and how each change carried into later work. The Sprint 1 review asked for few specific changes, so the Sprint 1 revisions below come mainly from the client's September 21 confirmations and from the Sprint 2 review, which asked that the Sprint 1 documents be kept current. Each revised file carries a new version or "revised" label; earlier versions are kept unchanged for comparison.

## 1. Revisions to Sprint 1 deliverables

| Deliverable | What changed | Why | Effect on later deliverables |
|---|---|---|---|
| System Request (one page) and Systems Request v1.1 → v1.2 | Parts recorded as used are deducted from the store's stock automatically; the reservation step is removed. | Client confirmation #3 (September 21) | FR07; UC-04; DFD 4.3 Record Parts Usage; JOB_PART, STORE_PART_STOCK and INVENTORY_TXN. No reservation status or entity anywhere. |
| Both System Requests | Every purchase order needs the owner's approval before it is placed; the owner's role now includes it. | Client confirmation #4 | FR10; new UC-09 Approve Purchase Order; DFD 7.3 Record PO Approval; PURCHASE_ORDER gains ApprovedByID, ApprovedAt and RejectionReason. New owner question on a spending threshold. |
| Both System Requests | Customer alerts become one completion email from the store's account, sent by front desk, the manager or the owner; technicians cannot send it. Priority Should → Must. The mailbox decision is closed. | Client confirmations #5, #6, #7 | FR12 and NFR05; UC-05; DFD 5.0 Send Completion Notice; email fields on REPAIR_JOB and STORE.EmailAddress. Other status emails are now a non-goal. |
| Both System Requests | Access is named as four roles: owner, manager, technician and front desk. | Client confirmation #1 | FR14 and NFR01; UC-11; DFD 9.1; EMPLOYEE.Role. |
| Both System Requests | Drop-off appointments are optional; walk-ins need none. | Sprint 2 review: "Is an appointment required or optional?" | FR01; new UC-12 Schedule Appointment; DFD 1.0 with its own Level 1; APPOINTMENT is 0..1 per REPAIR_JOB. |
| Both System Requests | A device is released only once payment is recorded; only an ID-checked flag is stored (the ID type is no longer recorded). | Sprint 2 requirements analysis (FR08) | UC-06 4a; DFD 6.4 Close Repair Job reads D3 Repair Jobs (PAYMENT); REPAIR_JOB.IDVerifiedFlag; PAYMENT. |
| Systems Request v1.2 (assumptions) | "Parts can move between stores" replaced: each store's stock is tracked separately and transfers are out of scope. | Sprint 2 catalog scope | No transfer process in the DFDs and no transfer entity in the ERD. |
| Systems Request v1.2 (7.2 owner decisions) | Sponsor and team named; mailbox question marked resolved; two blocking questions added (staff-sent or automatic email; PO threshold or urgent path); passed deadlines moved to Sprint 3 for items still open. | Sprint 2 results | The same open items now appear in the catalog, the use cases and the Feasibility Analysis. |
| Product Backlog | Story 13 reworded for the single completion email; PB-17 changed to automatic deduction; PB-20 to owner approval; new stories for UC-09 Approve Purchase Order, UC-12 Schedule Appointment and daily backup (NFR06). | Client confirmations; Sprint 2 feedback | Backlog now matches the catalog, use cases and DFDs, so Sprint 3 planning starts from the revised scope. |
| Feasibility Analysis v2.1 → v2.2 | Mailbox confirmed; scale restated from the Sprint 2 catalog (14 functional requirements, 12 Must, 12 use cases); new organizational risk that purchase orders wait on the owner; recommendation moves from "continue to requirements analysis" to "continue into design". Cost and benefit figures are unchanged. | Client confirmations; Sprint 2 catalog | The equipment inventory, delivery-option comparison and post-handoff support decision stay open, so the physical DFDs and ERD state their web-application assumption as unconfirmed. |

## 2. Revisions to Sprint 2 deliverables (Sprint 2 feedback)

| Feedback point | What changed | Deliverable | Effect |
|---|---|---|---|
| Change log covered only artifacts first made in Sprint 2 | Sprint 1 documents revised (section 1) and this log written to show how each change carried forward. | System Request, Systems Request, Feasibility Analysis, this log | Earlier versions kept unchanged for comparison. |
| AI requirements not integrated; Appendix A missing | One catalog: each of the ten salient AI items is marked in the new Source column (AI-xx, in blue); Appendix A is included and maps all 31 AI items. | Requirements Catalog | Traceability from AI item to catalog row to use case. |
| Add a Source column | Each requirement names its source: client confirmation, Sprint 1 document or process model, Sprint 3 decision, or AI item. | Requirements Catalog | Justifies why each requirement is in scope. |
| Separate requirements and acceptance checks | Requirement, Acceptance check and Use case are now separate columns. | Requirements Catalog | Acceptance checks can be lifted straight into Sprint 3 test planning. |
| Document inputs and outputs per use case | Every use case lists Inputs, Outputs and what it Traces to (requirements, DFD processes, data stores). | Use Cases | Links each use case to the DFD process and stores that implement it. |
| Keep validating use cases with the client | Each use case records its Client validation status; the open items say which flows still need a walkthrough with the owner. | Use Cases | Validation planned before Sprint 3 design sign-off. |
| Missing context diagram | Logical and physical context diagrams added. | DFD and ERD Models | Top of the DFD hierarchy; balances with Level 0. |
| Processes named for people's work | All processes renamed for what the system does (e.g. Record Diagnosis, Record Repair Work, Retrieve Customer Record, Save Customer Record). | DFD and ERD Models (section 8) | Use case traces cite the new names. |
| Repeated entities and data stores | Every entity and store is drawn once per diagram, at every level, logical and physical. | DFD and ERD Models | None. |
| Appointment scheduling unclear | In scope and optional: process 1.0, UC-12 and FR01 rewritten; walk-ins skip it. | Catalog, Use Cases, DFDs, ERD, System Requests | Consistent across all five. |
| ERD too hard to read | ERD simplified from 22 to 16 entities and redrawn for 16:9 slides: an overview plus three detail diagrams with every key and attribute; every diagram also supplied as a slide deck and vector PDF; full data dictionary. | DFD and ERD Models; slide deck | Every table, key and relationship can be read on a slide and explained by each team member. |
| Diagrams must work on PowerPoint | All DFDs and ERDs redrawn at slide size (labels at least 19 px on a 1920×1080 slide); Level 0 shown complete and in three readable parts. | QuickPhone_Sprint3_DFD_ERD_Slides.pptx (40 slides with speaker notes) | The same images are used in the models document. |
| DFDs and ERD inconsistent | 7 data stores hold the 16 entities, each exactly once. ROLE and JOB_STATUS became checked columns; NOTIFICATION and JOB_NOTE became REPAIR_JOB columns; PO_JOB_LINK became JOB_PART.PurchaseOrderID; EMAIL_TEMPLATE and backup_log removed. The ERD overview draws each store around its entities; an alignment slide gives the store–entity and process × store matrices. | DFD and ERD Models; Use Cases (store references) | Every entity sits in exactly one store, and every store is created and read by some process. |

## 3. How the main changes carry through the models

Each change is traced from its source through the requirement, use case, DFD process and ERD entities that implement it, so a reviewer can follow it end to end.

| Change and source | Requirement | Use case | DFD process | ERD entities |
|---|---|---|---|---|
| Automatic parts deduction (client #3) | FR07 | UC-04 | 4.3 Record Parts Usage | JOB_PART, STORE_PART_STOCK, INVENTORY_TXN |
| Owner approves every PO (client #4) | FR10 | UC-09 | 7.3 Record PO Approval | PURCHASE_ORDER (ApprovedByID, ApprovedAt, RejectionReason) |
| One completion email, store account (#5–#7) | FR12, NFR05 | UC-05 | 5.0 Send Completion Notice | REPAIR_JOB email fields, STORE.EmailAddress |
| Four roles (#1) | FR14, NFR01 | UC-11 | 9.1 Maintain Staff Accounts | EMPLOYEE.Role |
| Optional appointments (Sprint 2 review) | FR01 | UC-12 | 1.0 Schedule Appointment | APPOINTMENT (0..1 per job) |
| Release only after payment | FR08 | UC-06 | 6.3, 6.4 | PAYMENT, REPAIR_JOB release fields |
| Daily backup (AI-NFR05) | NFR06 | — | not modelled (hosting platform) | — |

## 4. Files

| Deliverable | Previous version | Revised version |
|---|---|---|
| System Request | deliverables/QuickPhone_System_Request.docx | Sprint3_revised/Sprint 3 - System Request (revised).docx |
| Systems Request | deliverables/QuickPhone_Systems_Request.docx (v1.1) | Sprint3_revised/Sprint 3 - Systems Request v1.2.docx |
| Feasibility Analysis | deliverables/QuickPhone_Feasibility_Analysis_v2.1.docx | Sprint3_revised/Sprint 3 - Feasibility Analysis v2.2.docx |
| Requirements Catalog and Memo | Sprint2_revised/Sprint 2 - Requirements Catalog and Memo.docx | Sprint3_revised/Sprint 3 - Requirements Catalog and Memo.docx |
| Use Cases | Sprint2_revised/Sprint 2 - Use Cases.docx | Sprint3_revised/Sprint 3 - Use Cases.docx |
| Product Backlog | deliverables/QuickPhone_Product_Backlog.xlsx | Sprint3_revised/Sprint 3 - Product Backlog.xlsx (changes listed on its Sprint 3 Changes sheet) |
| DFDs and ERD | Sprint2_revised/DFDs/, QuickPhone_ERD.png | Sprint3_models/Sprint 3 - DFD and ERD Models.docx, with logical/ and physical/ PNG and PDF files |

## 5. Open items carried into Sprint 3

- Blocking: is the completion email sent by staff or automatically (FR12)? Is there a purchase-order spending threshold or urgent path (FR10)?

- Equipment, connectivity and records inventory, and the comparison of delivery options. Until it is done, the physical design's web-application assumption is unconfirmed.

- Who supports the system after the December 9 handoff (the top organizational risk), QuickPhone's own operating baselines, and payroll rates.

- Whether the customer signs at pickup (FR08), how technician availability is set and who may reschedule (FR01), the diagnostic-fee rule (FR05), and who sets reorder points (FR10).

- A walkthrough of every use case with the owner, including the new UC-12 and the intake fields in UC-01.
