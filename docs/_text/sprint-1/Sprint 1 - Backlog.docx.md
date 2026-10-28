<!-- Auto-generated from docs/sprint-1/Sprint 1 - Backlog.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 1 - Backlog

Prioritized Product Backlog

Quick Phone Repair Management System

| Client | Quick Phone Repair & Designs, Raleigh, NC |
|---|---|
| Project sponsor | Ashiqullah Pardisi, Owner |
| Course | MIS 4173 – Systems Analysis & Design |
| Team | Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard |
| Sprint | Sprint 1 |
| Date | September 17, 2026 |

## 1. How This Backlog Is Ordered

Stories are ordered by the repair lifecycle first (intake, job workflow, release), then parts inventory, then purchasing, alerts, and reporting. Each block leaves the client with something usable, and no story depends on work that comes after it.

Priority. MoSCoW: Must means the system fails its purpose without it; Should means it delivers significant value but the system works without it; Could means it is a convenience.

Points. Relative estimates on a 1-3-5-8 scale, reviewed at each sprint planning session. The sprint column is a forecast, not a commitment.

## 2. Backlog

| # | User story | Priority | Points | Sprint |
|---|---|---|---|---|
| 1 | As a store manager, I want to manage user accounts, roles, and both store locations so staff only see what their role allows | Must | 5 | 2 |
| 2 | As front desk staff, I want to check in a customer and device and create a repair job so every device is logged | Must | 8 | 2 |
| 3 | As front desk staff, I want to print a claim ticket and device tag label so devices are not misplaced | Must | 5 | 2 |
| 4 | As front desk staff, I want to assign jobs to technicians and record quote approval so work starts only when approved | Must | 3 | 3 |
| 5 | As a technician, I want to record diagnoses and quotes so the front desk can get customer approval | Must | 3 | 3 |
| 6 | As a technician, I want to move a job through its statuses from check-in to pickup so anyone can answer status calls | Must | 5 | 3 |
| 7 | As front desk staff, I want to verify ticket number, photo ID, and signature and record final cost and paid status so devices go to the right person | Must | 5 | 3 |
| 8 | As a store manager, I want to add and edit parts with cost, supplier, device model, and grade so inventory is accurate | Must | 5 | 4 |
| 9 | As a store manager, I want to import existing inventory from a CSV file so launch does not require manual entry | Must | 3 | 4 |
| 10 | As a technician, I want to reserve and use parts on a job so stock levels stay current | Must | 5 | 4 |
| 11 | As a store manager, I want a low-stock list so I reorder before jobs stall | Should | 3 | 4 |
| 12 | As a store manager, I want to record purchase orders and receive deliveries against them so incoming stock is tracked | Should | 8 | 5 |
| 13 | As a customer, I want an email when my device status changes or it is ready so I do not have to call | Should | 5 | 5 |
| 14 | As the owner, I want a history of who checked in, approved, repaired, and released each device so staff are accountable | Should | 3 | 5 |
| 15 | As staff or the owner, I want a dashboard of open repairs and parts availability at both stores so we have one shared view | Should | 8 | 6 |
| 16 | As front desk staff, I want to schedule drop-off appointments by technician availability so workloads stay balanced | Should | 5 | 6 |
| 17 | As front desk staff, I want to search jobs by customer, phone, or ticket number so I can find jobs fast | Could | 3 | 6 |

## 3. Cross-Cutting Acceptance Criteria

These constraints come from the system request and apply across the stories listed, rather than standing as separate backlog items.

| Constraint | Applies to |
|---|---|
| Customer contact details and signatures are visible only to authorized roles | Stories 1, 2, 7, 14 |
| Photo ID is recorded as checked; the ID number is never stored | Story 7 |
| No payment processing, customer portal, text messaging, or third-party integrations | All stories |
| All data resides in a single database shared by both store locations | All stories |

## 4. Traceability

Every story traces to a business requirement in the approved system request: front desk intake and scheduling (stories 1-4, 16), technician workflow (5, 6, 10), pickup verification and payment recording (7), parts inventory and purchasing (8-12), customer email alerts (13), accountability history (14), and the staff dashboard (15).

## 5. Open Items

Story 13 depends on unresolved approval to send customer email from the shop mailbox. The status values in story 6 are assumed and need the owner’s confirmation. The required intake fields in story 2 have not been validated against how staff check in devices today.
