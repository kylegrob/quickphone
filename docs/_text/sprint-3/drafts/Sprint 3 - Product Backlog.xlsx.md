<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - Product Backlog.xlsx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - Product Backlog

## Sheet: README

| QuickPhone Repair Tracking System - Prioritized Product Backlog |  |
|---|---|
| Sprint 1 (Problem Definition & Feasibility), Sep 14-20, 2026 - Version 1.2 (revised for Sprint 3, Oct 19, 2026) |  |
| SHEETS |  |
| Product Backlog | All backlog items ranked by priority, in user story format with acceptance criteria, MoSCoW, story points, MVP slice and Level 0 DFD process. |
| Summary | Counts and story points by MoSCoW, release and slice, plus an MVP capacity check. |
| Epics | Feature groups mapped to Level 0 DFD processes. |
| Release Plan | Course sprints 1-6 with dates, goals and recommended build work in the weeks between sprints. |
| Sprint 1 Backlog | Tasks, owners and hours for Sprint 1, with per-member totals. |
| Non-Functional Reqs | Quality attributes and constraints (security, privacy, printing, performance). |
| Sprint 3 Changes | Every Sprint 3 change to this workbook, with the rows affected and the reason. |
| LEGEND |  |
| Yellow cell, blue text | Input you should edit (team names, capacity assumptions, actual hours, status). |
| Black text | Data or formulas - formulas recalculate automatically. |
| MoSCoW |  |
| Must | Required for the Sprint 4 working system demo (MVP). Without it the system fails its purpose. |
| Should | Important; build after the MVP if capacity allows (Release 1.1, before training). |
| Could | Nice to have; candidate for after handoff. |
| Won't | Explicitly excluded from this release (payments, customer portal, SMS, reporting, integrations, status emails other than completion, stock transfers). |
| STORY POINTS | Relative effort on a Fibonacci scale (1, 2, 3, 5, 8, 13). Initial analyst estimates - re-estimate as a team with planning poker in Sprint 2. |
| RANK | Order reflects business value (fewer status calls, fewer jobs stuck waiting on parts, no lost devices) and build dependencies. |
| SOURCES |  |
| Owner / team answers (Sep 14, 2026) | 2 stores; phones, tablets, laptops, consoles, other devices; record quote, final cost, paid flag; roles Front Desk, Technician, Owner, Manager (purchasing + user accounts); email-only alerts; supplier orders tracked only; scheduling = appointments + technician assignment; claim ticket, tag label, ID + ticket at pickup (on-screen signature removed Sep 16, 2026); low-stock list; receive against PO; part cost/supplier/model/grade; inventory import; reporting later; single database, no external services; 4-student team. |
| Analyst assumptions | Story points, MVP slices, build-window hours, performance volumes, label size and privacy rules are assumptions to confirm in Sprint 2. |
| Client confirmations (Sep 21, 2026) | Four roles; parts deducted automatically when recorded as used (no reservation); Owner approves every purchase order; one pickup notification email from the store account, sent by Owner, Manager or Front Desk, never a Technician. Sprint 3 scope decision (Oct 19, 2026): appointments optional (UC-12). |

## Sheet: Product Backlog

| Rank | ID | Epic ID | Epic | Title | User Story | Acceptance Criteria | MoSCoW | Story Points | Release / MVP Slice | DFD Process | Depends On | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PB-01 | E1 | Users, Roles & Locations | Staff login & role-based access | As a staff member, I want to log in with my own account so that I can only see and do what my role allows. | - Valid username/password opens the home screen for my role; invalid login shows a generic error. - Permissions for Front Desk, Technician, Manager and Owner are enforced on the server, not just hidden in the UI. - Session ends automatically after a period of inactivity. | Must | 5 | Slice 1 - Foundation | 9.0 |  | New |  |
| 2 | PB-02 | E1 | Users, Roles & Locations | Manage user accounts | As a manager, I want to create, edit and deactivate staff accounts and assign each a role and home store so that access stays current. | - Only the Manager role can open user administration. - A deactivated user cannot log in; their history remains on jobs. - Manager can reset a password to a temporary one that must be changed at next login. | Must | 3 | Slice 1 - Foundation | 9.0 | PB-01 | New |  |
| 3 | PB-03 | E1 | Users, Roles & Locations | Set up two store locations | As a manager, I want both store locations in the system so that jobs, appointments and stock are tracked per store. | - Each store has name, address, phone and business hours. - Every job, appointment and stock quantity belongs to exactly one store. - Lists and the dashboard can be filtered by store. | Must | 2 | Slice 1 - Foundation | 9.0 | PB-01 | New |  |
| 4 | PB-04 | E2 | Customer & Device Intake | Find or create customer | As front desk staff, I want to search customers by phone, name or email and add a new one if not found so that we avoid duplicate records. | - Search returns matching customers as I type. - Phone is required; email is optional but must be a valid format. - Entering a phone number that already exists shows a duplicate warning. - Customer record lists their open and past jobs. | Must | 3 | Slice 1 - Foundation | 2.0 | PB-01 | New |  |
| 5 | PB-05 | E2 | Customer & Device Intake | Record device details at intake | As front desk staff, I want to record the device type, make, model, serial/IMEI, condition and accessories left so that the right device is returned in the same condition. | - Device type is one of Phone, Tablet, Laptop, Console, Other. - Condition notes and accessories-left checklist are required before the job can be saved. - Device is linked to the customer and can be reused on future jobs. | Must | 3 | Slice 1 - Foundation | 2.0 | PB-04 | New |  |
| 6 | PB-06 | E2 | Customer & Device Intake | Create repair job at check-in | As front desk staff, I want to create a repair job with the reported fault, quote and promised date so that the device is tracked from the moment it arrives. | - System assigns a unique ticket number with a store prefix. - Status is set to Checked In with date/time and user recorded. - Quote amount and promised completion date are captured. - The new job appears on the open repairs dashboard immediately. | Must | 5 | Slice 1 - Foundation | 2.0 | PB-03, PB-05 | New |  |
| 7 | PB-07 | E2 | Customer & Device Intake | Print claim ticket | As front desk staff, I want to print a claim ticket for the customer so that they have proof of drop-off and their ticket number. | - Ticket shows store, ticket number, date, customer name and phone, device, reported fault, quote and terms. - Prints from the browser with no extra software. - Ticket can be reprinted from the job. | Must | 3 | Slice 1 - Foundation | 2.0 | PB-06 | New |  |
| 8 | PB-08 | E2 | Customer & Device Intake | Print device tag label | As front desk staff, I want to print a tag label to attach to the device so that devices are never mixed up or lost. | - Label shows ticket number in large text, customer last name, make/model and check-in date. - Layout fits the shop's label printer size (to be confirmed in Sprint 2). - Label can be reprinted from the job. | Must | 2 | Slice 1 - Foundation | 2.0 | PB-06 | New | Confirm label printer make/model and label size in Sprint 2. |
| 9 | PB-09 | E4 | Repair Job Workflow | Update job status with history | As a staff member, I want to move a job through the agreed statuses so that everyone knows exactly where each repair is. | - Statuses: Booked, Checked In, Diagnosing, Awaiting Customer Approval, Awaiting Parts, In Repair, QA/Testing, Ready for Pickup, Picked Up, plus Cancelled and Unrepairable/Returned. - Only allowed transitions can be selected. - Every change records user, date/time and an optional note, visible in the job history. | Must | 5 | Slice 2 - Repair Workflow | 3.0 / 4.0 | PB-06 | New |  |
| 10 | PB-10 | E3 | Appointments & Technician Scheduling | Assign technician to job | As front desk staff or a manager, I want to assign a job to a technician so that each technician has a clear work queue. | - Only active technicians at the job's store can be selected. - Reassignments are logged in the job history. - Technicians see a My Jobs queue sorted by promised date. | Must | 3 | Slice 2 - Repair Workflow | 2.0 | PB-02, PB-06 | New |  |
| 11 | PB-11 | E4 | Repair Job Workflow | Record diagnosis & revise quote | As a technician, I want to record the diagnosis and work performed and revise the quote so that front desk can inform the customer accurately. | - Notes are time-stamped with the author. - A revised quote keeps both the original and new amounts. - If the revised quote is higher than the original, the job moves to Awaiting Customer Approval. | Must | 3 | Slice 2 - Repair Workflow | 3.0 | PB-09 | New |  |
| 12 | PB-12 | E4 | Repair Job Workflow | Record customer quote approval | As front desk staff, I want to record the customer's approval or decline of a quote so that no work is done without consent. | - Captures approved/declined, contact method, date/time and staff user. - Approval returns the job to its work status; decline allows Cancelled or Unrepairable/Returned. | Must | 2 | Slice 2 - Repair Workflow | 3.0 | PB-11 | New |  |
| 13 | PB-13 | E6 | Parts Inventory | Maintain parts catalog | As a manager, I want to add and edit parts with part number, description, compatible device model, grade, cost, supplier and reorder point so that inventory records are accurate. | - Required fields: part number, description, grade (e.g., OEM, Aftermarket, Refurbished), cost and default supplier. - Compatible device models are searchable. - Quantity on hand and reorder point are kept per store. | Must | 3 | Slice 3 - Inventory & Purchasing | 9.0 | PB-03 | New |  |
| 14 | PB-14 | E7 | Purchasing & Receiving | Maintain suppliers | As a manager, I want to keep supplier contact details so that parts and purchase orders reference the right supplier. | - Supplier has name, contact person, phone, email and notes. - Inactive suppliers cannot be selected on new purchase orders. | Must | 2 | Slice 3 - Inventory & Purchasing | 9.0 | PB-01 | New |  |
| 15 | PB-15 | E10 | Data Setup & Import | Import existing inventory (CSV) | As a manager, I want to import our current parts inventory from a CSV file so that we don't retype hundreds of parts. | - A downloadable CSV template defines the columns. - Validation lists row-level errors; nothing is imported until the file is error-free. - Summary shows how many parts were added, updated and skipped. | Must | 5 | Slice 3 - Inventory & Purchasing | 9.0 | PB-13, PB-14 | New | Request a sample export of the current inventory in Sprint 2. |
| 16 | PB-16 | E6 | Parts Inventory | Parts availability lookup | As a technician or front desk staff member, I want to search parts by device model and see on-hand and on-order quantities at both stores so that I can promise realistic dates. | - Search by device model or part number. - On-hand quantity is shown for each store. - On-order quantity comes from approved and ordered purchase orders. | Must | 3 | Slice 3 - Inventory & Purchasing | 3.0 / 8.0 | PB-13 | New | Reserved and available quantities removed with the reservation step (client #3). |
| 17 | PB-17 | E4 | Repair Job Workflow | Record parts used (auto-deduct) | As a technician, I want to record the parts I use on a job so that my store's stock is deducted automatically. | - Recording a part and quantity used deducts it from the job's store stock at once and logs an inventory transaction with user and date/time. - No reservation step: stock is not held for a job before it is used. - An entry that would take stock below zero is blocked and the part goes to the Manager's queue for a count correction. - An out-of-stock part is recorded as needed on the job and the job moves to Awaiting Parts. | Must | 5 | Slice 3 - Inventory & Purchasing | 4.0 | PB-09, PB-13 | New | Client #3 (Sep 21): reservation removed. Re-estimated 8 -> 5; confirm in planning poker. Traces FR07, UC-04. |
| 18 | PB-18 | E4 | Repair Job Workflow | Flag jobs awaiting parts | As a technician, I want a job to be flagged Awaiting Parts and linked to the missing part so that stalled jobs are visible and followed up. | - Setting Awaiting Parts requires the part and quantity needed. - The part appears on the low-stock list with the number of jobs waiting for it. - Days waiting is shown on the dashboard. | Must | 5 | Slice 3 - Inventory & Purchasing | 4.0 | PB-17 | New |  |
| 19 | PB-19 | E6 | Parts Inventory | Low stock list | As a manager, I want a low-stock list for each store so that I reorder before jobs stall. | - Lists parts where on hand <= reorder point or that are needed by Awaiting Parts jobs. - Shows on hand, on order and supplier; filter by store and supplier. - One action starts a draft purchase order for selected parts. | Must | 3 | Slice 3 - Inventory & Purchasing | 7.0 | PB-13, PB-18 | New | Reserved quantity removed with the reservation step (client #3). |
| 20 | PB-20 | E7 | Purchasing & Receiving | Create PO & submit for approval | As a manager, I want to create purchase orders and submit each to the owner so that no order is placed without the owner's approval. | - PO has number, supplier, receiving store, order date, expected date and lines (part, qty, unit cost); jobs Awaiting Parts can be linked. - PO statuses: Draft, Pending Approval, Approved, Ordered, Partially Received, Received, Cancelled. - Every PO needs Owner approval before it can be placed or received; a rejected PO returns to Draft with the Owner's reason. - Printable PO view; the system does not send orders to suppliers. | Must | 5 | Slice 3 - Inventory & Purchasing | 7.0 | PB-14 | New | Client #4 (Sep 21). Traces FR10, UC-08. Blocking: spending threshold or urgent path when the Owner is unavailable? |
| 21 | PB-44 | E7 | Purchasing & Receiving | Approve or reject purchase order | As the owner, I want to approve or reject each submitted purchase order so that I control all parts spending. | - Only the Owner sees the Pending Approval queue and can decide; other roles are blocked on the server. - Owner sees supplier, lines, total cost and linked jobs before deciding. - Approval records the Owner and date/time, sets Approved and moves the PO to the Manager's queue to place. - Rejection requires a reason and returns the PO to Draft for the Manager. | Must | 3 | Slice 3 - Inventory & Purchasing | 7.0 | PB-01, PB-20 | New | New for UC-09 (client #4, Sep 21). Traces FR10, NFR01; Sprint 3 DFD 7.3. |
| 22 | PB-21 | E7 | Purchasing & Receiving | Receive delivery against PO | As a manager, I want to receive deliveries against a purchase order so that stock levels update and waiting jobs are unblocked. | - Received quantity is entered per line; partial deliveries are allowed. - On-hand stock increases at the PO's receiving store. - PO status updates automatically. - Jobs awaiting the received parts are highlighted on the dashboard. | Must | 5 | Slice 3 - Inventory & Purchasing | 7.0 | PB-20 | New |  |
| 23 | PB-22 | E8 | Open Repairs Dashboard | Open repairs & parts dashboard | As any staff member, I want a single view of open repairs and parts availability so that I can manage the day's work at a glance. | - Shows counts and a list of open jobs by status, filterable by store, technician and status. - Overdue jobs (past promised date) and aging jobs are highlighted. - Includes an Awaiting Parts panel and a Low Stock panel. - Loads in under 2 seconds with realistic data volumes. | Must | 8 | Slice 4 - Dashboard & Pickup | 8.0 | PB-09, PB-18, PB-19 | New | Consider splitting into job list + parts panels in Sprint 2. |
| 24 | PB-23 | E8 | Open Repairs Dashboard | Quick job lookup | As front desk staff, I want to find a job by ticket number, customer phone or name so that I can answer "where's my phone?" calls in seconds. | - A search box is available on every page. - Result shows status, last update, technician and promised date. | Must | 2 | Slice 4 - Dashboard & Pickup | 8.0 | PB-06 | New |  |
| 25 | PB-24 | E5 | Pickup & Release | Verify & release device at pickup | As front desk staff, I want to verify the ticket number and check photo ID so that devices are released only to the right person. | - Ticket number entered must match the job. - ID Checked is required; neither the ID type nor the ID number is stored. - Status becomes Picked Up with user and date/time, and the job leaves the open repairs view. | Must | 3 | Slice 4 - Dashboard & Pickup | 6.0 | PB-09 | New | On-screen signature removed (Sep 16, 2026): no tablet or signature capture needed. Re-estimated from 5 to 3 points; confirm in Sprint 2 planning poker. Sprint 3: ID type no longer recorded (FR08). |
| 26 | PB-25 | E5 | Pickup & Release | Record final cost & paid flag | As front desk staff, I want to record the final repair cost and whether it has been paid so that unpaid repairs are not released by mistake. | - Final cost must be entered before a job can be set to Ready for Pickup. - Paid is a Yes/No flag; no payment is processed by the system. - Releasing an unpaid job requires a manager override with a note. | Must | 2 | Slice 4 - Dashboard & Pickup | 6.0 | PB-09 | New |  |
| 27 | PB-29 | E9 | Customer Email Alerts | Send pickup notification | As front desk staff, a manager or the owner, I want to send the customer one pickup notification email from the store's email account when the device is ready for pickup so that they don't have to call the store. | - The send action is offered only when the job is Ready for Pickup; one pickup notification per job, and no email for any other status. - Sent from the store's email account; Owner, Manager and Front Desk can send it; Technicians cannot, enforced on the server. - Sender, date/time and Sent/Failed are logged on the job; a failed send or missing email flags the job for a phone call. | Must | 5 | Slice 4 - Dashboard & Pickup | 5.0 | PB-02, PB-09 | New | Client #5-#7 (Sep 21): completion only, store account, no Technician send; Should -> Must. Traces FR12, NFR05, UC-05. Blocking: staff-sent or automatic? |
| 28 | PB-26 | E3 | Appointments & Technician Scheduling | Schedule optional appointment | As front desk staff, I want to book, reschedule or cancel an optional drop-off appointment with an available technician so that we can plan intake, while walk-in customers need none. | - Choosing a store and date shows the free times of that store's technicians. - Appointment records customer, store, time and technician; status Booked, or Cancelled when cancelled. - Front Desk can reschedule or cancel; a walk-in is checked in with no appointment. | Should | 5 | Release 1.1 | 1.0 | PB-03, PB-04 | New | Modeled by UC-12 (Sprint 3 scope decision: in scope, optional). Traces FR01; Sprint 3 DFD 1.0. Open: how technician availability is set, who may reschedule. |
| 29 | PB-27 | E3 | Appointments & Technician Scheduling | Convert appointment to check-in | As front desk staff, I want to check in a booked appointment so that customer and device details don't have to be re-entered. | - Check-in from an appointment pre-fills customer, device, issue and technician. - Appointment is marked Checked In; no-shows are marked No Show. | Should | 2 | Release 1.1 | 2.0 | PB-26, PB-06 | New | Modeled by UC-12 (step 5, 5a) and UC-01 alternate flow 1a. |
| 30 | PB-28 | E3 | Appointments & Technician Scheduling | Technician workload schedule | As a manager, I want to see each technician's assigned jobs by promised date so that work is balanced across technicians and stores. | - View by store and technician, grouped by promised date. - Overdue jobs are highlighted. - Jobs can be reassigned from this view. | Should | 3 | Release 1.1 | 1.0 / 8.0 | PB-10 | New |  |
| 31 | PB-32 | E6 | Parts Inventory | Stock adjustments with reason | As a manager, I want to adjust stock with a reason so that counts stay accurate when parts are damaged, lost or recounted. | - Reason required: Damaged, Lost, Count Correction or Returned to Supplier. - Every adjustment is logged with user and date; Manager role only. | Should | 3 | Release 1.1 | 9.0 | PB-13 | New |  |
| 32 | PB-33 | E4 | Repair Job Workflow | Job audit trail view | As the owner, I want a complete change log for a job so that disputes about lost devices or approvals can be resolved. | - Shows every field change, status change, note, print and email event with user and date/time. - Read-only. | Should | 2 | Release 1.1 | 8.0 | PB-09 | New |  |
| 33 | PB-45 | E10 | Data Setup & Import | Daily backup & restore | As the owner, I want job, customer and inventory records backed up automatically every day so that they can be restored after a failure. | - A backup of all job, customer and inventory records runs automatically once a day. - Each run's result and date/time is logged and visible to the Manager and Owner. - A backup restores to a test copy in which a sample job and stock level match the source. | Should | 3 | Release 1.1 | Not modelled | PB-01 | New | New for NFR06 in the Sprint 3 catalog (NFR-09 on this workbook; source AI-NFR05). Sprint 3 physical DFD 9.6. Restore test before handoff. |
| 34 | PB-34 | E5 | Pickup & Release | Uncollected device aging flag | As front desk staff, I want devices left in Ready for Pickup too long to be flagged so that we follow up and free up storage. | - Day threshold is configurable. - Flagged jobs appear on the dashboard; follow-up notes can be recorded. | Could | 2 | Future | 8.0 | PB-22 | New |  |
| 35 | PB-35 | E4 | Repair Job Workflow | Rush / priority flag | As front desk staff, I want to mark a job as rush so that technicians prioritise it. | - Rush jobs show a badge and sort first in queues. | Could | 1 | Future | 2.0 | PB-06 | New |  |
| 36 | PB-36 | E2 | Customer & Device Intake | Barcode / QR on ticket & tag | As a staff member, I want a barcode on the claim ticket and tag so that scanning it opens the job. | - Code encodes the ticket number and is generated inside the app (no third-party service). - Scanning into the search box with a USB scanner opens the job. | Could | 3 | Future | 2.0 | PB-07, PB-08 | New |  |
| 37 | PB-37 | E2 | Customer & Device Intake | Intake condition photos | As front desk staff, I want to attach photos of the device at intake so that pre-existing damage is documented. | - Up to 5 photos per job from upload or tablet camera. - Photos are visible on the job and stored by the application. | Could | 3 | Future | 2.0 | PB-06 | New |  |
| 38 | PB-38 | E4 | Repair Job Workflow | Warranty re-work link | As a technician, I want to link a returning fault to the original job so that warranty re-work is tracked and not charged. | - New job references the original ticket number. - System shows whether the original repair is within the warranty period. | Could | 3 | Future | 3.0 | PB-06 | New |  |
| 39 | PB-39 | E11 | Excluded This Release | Payment processing / POS | Collecting card or cash payments inside the system. | - Excluded by owner decision; only a paid Yes/No flag is recorded (PB-25). | Won't | 0 | Out of scope | n/a |  | Removed |  |
| 40 | PB-40 | E11 | Excluded This Release | Customer self-service portal / online booking | Customers logging in to book appointments or check status. | - Excluded: customers do not interact with the system directly. | Won't | 0 | Out of scope | n/a |  | Removed |  |
| 41 | PB-41 | E11 | Excluded This Release | SMS / text notifications | Text-message alerts to customers. | - Excluded: requires a third-party SMS provider; email only. | Won't | 0 | Out of scope | n/a |  | Removed |  |
| 42 | PB-42 | E11 | Excluded This Release | Reporting & analytics | Turnaround time, parts usage and technician throughput reports. | - Deferred to a later release by owner decision. | Won't | 0 | Later release | n/a |  | Removed |  |
| 43 | PB-43 | E11 | Excluded This Release | Third-party integrations | Links to accounting, supplier ordering or manufacturer warranty systems. | - Excluded: single database, no external systems. | Won't | 0 | Out of scope | n/a |  | Removed |  |
| 44 | PB-30 | E11 | Excluded This Release | Other status email alerts | As a manager, I want to enable email alerts for other key statuses so that customers stay informed without calling. | - Excluded: client confirmed one pickup notification email only, no other status emails (Sep 21 #5). | Won't | 0 | Out of scope | n/a |  | Removed | Removed in Sprint 3: other status emails are a non-goal. |
| 45 | PB-31 | E11 | Excluded This Release | Transfer stock between stores | As a manager, I want to transfer parts between the two stores so that one store's stock can unblock the other store's waiting jobs. | - Excluded: each store's stock is tracked separately (Sprint 2 catalog scope). | Won't | 0 | Out of scope | n/a |  | Removed | Removed in Sprint 3: stock transfers are out of scope. |

## Sheet: Sprint 3 Changes

| # | Backlog Item | Row (new) | Row (original) | Change | Reason / Source |
|---|---|---|---|---|---|
| 1 | PB-29 | 28 | 30 | Reworded as one completion email, sent from the store account by Owner, Manager or Front Desk; Technicians blocked. Should -> Must, moved to Slice 4, re-ranked into the Must band. | Client #5, #6, #7 (Sep 21); catalog FR12, NFR05; UC-05. |
| 2 | PB-17 | 18 | 18 | Reserve-then-consume replaced by automatic deduction when a part is recorded as used; below-zero entries blocked. Re-estimated 8 -> 5. | Client #3 (Sep 21); catalog FR07; UC-04. |
| 3 | PB-20 | 21 | 21 | Every PO is submitted for Owner approval before it can be placed or received; Pending Approval and Approved statuses added; a rejected PO returns to Draft with a reason. | Client #4 (Sep 21); catalog FR10; UC-08. |
| 4 | PB-44 | 22 | new | New Must story: Owner approves or rejects each purchase order (3 points, Slice 3). | UC-09 Approve Purchase Order had no backlog story. |
| 5 | PB-26 | 29 | 27 | Rewritten as the UC-12 story: book, reschedule or cancel an optional appointment with a technician; walk-ins need none. Marked as modeled by UC-12. Kept as Should, Release 1.1. | Sprint 3 scope decision (Sprint 2 review); catalog FR01; UC-12. Rewritten rather than duplicated so appointment points are not counted twice. |
| 6 | PB-27 | 30 | 28 | Appointment marked Checked In (not Arrived) and pre-fills the technician; marked as modeled by UC-12 and UC-01 1a. | UC-12 steps 5 and 5a; UC-01 alternate flow 1a. |
| 7 | PB-45 | 34 | new | New Should story: automatic daily backup with a tested restore (3 points, Release 1.1). | Catalog NFR06 (workbook NFR-09) had no story; source AI-NFR05. |
| 8 | PB-30 | 45 | 31 | Other status emails moved to Won't / Out of scope. | Follows change 1: client confirmed completion email only. |
| 9 | PB-16 | 17 | 17 | Reserved and available quantities removed from the lookup. | Follows change 2: no reservation step. |
| 10 | PB-19 | 20 | 20 | Reserved quantity removed from the low-stock list. | Follows change 2: no reservation step. |
| 11 | PB-31 | 46 | 32 | Stock transfers moved to Won't / Out of scope. | Catalog scope: each store's stock is tracked separately. |
| 12 | PB-24 | 26 | 25 | ID type no longer recorded; only the ID-checked flag. | Change log, FR08 (Sprint 2 requirements analysis). |
| 13 | All rows |  |  | Rank column renumbered 1-45 after the moves above; IDs unchanged. | Rank order follows MoSCoW. |
| 14 | Epics |  |  | E4, E6, E7, E9 and E10 descriptions updated (automatic deduction, no transfers, Owner approval, completion email, backup). | Match changes 1-6. |
| 15 | Release Plan |  |  | Build-window rows G9 and G11 list PB-44, PB-29 and PB-45. | New and re-prioritised stories. |
| 16 | README |  |  | Version 1.2; Sprint 3 Changes sheet listed; Sep 21 confirmations added to sources; Won't list extended. | Keep the guide current. |
| 17 | All items; Epics sheet |  |  | DFD Process column and the Epics mapping renumbered to the Sprint 3 Level 0 DFD: 1.0 Schedule Appointment, 2.0 Register Repair Job, 3.0 Record Diagnosis, 4.0 Record Repair Work, 5.0 Send Completion Notice, 6.0 Record Device Release, 7.0 Process Purchase Orders, 8.0 Report Repair Status, 9.0 Maintain Shop Records. Daily backup (PB-45) marked not modelled. | Sprint 3 DFD and ERD Models (rev 2) renumbered the processes; the backlog still used the Sprint 1 Level 0 numbers, so its traces pointed at the wrong processes. |

## Sheet: Summary

| Product Backlog Summary |  |  |  |
|---|---|---|---|
| All figures are formulas driven by the Product Backlog sheet. |  |  |  |
| Priority (MoSCoW) | Items | Story Points | % of Points |
| Must | 27 | 98 | 0.765625 |
| Should | 6 | 18 | 0.140625 |
| Could | 5 | 12 | 9.375E-2 |
| Won't | 7 | 0 | 0 |
| Total | 45 | 128 | 1 |
| By Release / MVP Slice |  |  |  |
| Release / MVP Slice | Items | Story Points | Target |
| Slice 1 - Foundation | 8 | 26 | Build Oct 12-18; demo Sprint 4 (Nov 2-8) |
| Slice 2 - Repair Workflow | 4 | 13 | Build Oct 19-25; demo Sprint 4 (Nov 2-8) |
| Slice 3 - Inventory & Purchasing | 10 | 39 | Build Oct 26-Nov 1; demo Sprint 4 (Nov 2-8) |
| Slice 4 - Dashboard & Pickup | 5 | 20 | Build Oct 26-Nov 1; demo Sprint 4 (Nov 2-8) |
| Release 1.1 | 6 | 18 | If capacity allows, Nov 9-15, before training (Sprint 5) |
| Future | 5 | 12 | After Dec 9 handoff |
| Out of scope | 6 | 0 | Not planned |
| Later release | 1 | 0 | Owner deferred (reporting) |
| Total | 45 | 128 |  |
| MVP Capacity Check (edit the yellow cells) |  |  |  |
| Team members | 4 | Source: team (4 students), Sept 14, 2026 |  |
| Build hours per member before the Sprint 4 demo | 40 | Assumption - replace with each member's real availability (Oct 12 - Nov 1) |  |
| Hours per story point | 2 | Assumption - recalibrate after Slice 1 is built |  |
| Capacity (story points) | 80 | Members x hours / hours per point |  |
| Must story points (MVP) | 98 | From MoSCoW table above |  |
| Buffer (capacity - Must) | -18 | Negative = MVP scope exceeds capacity |  |
| Result | Over capacity - split or move items to Release 1.1 |  |  |

## Sheet: Epics

| Epic ID | Epic | Description | Level 0 DFD Process | Backlog Items | Story Points | Must Points |
|---|---|---|---|---|---|---|
| E1 | Users, Roles & Locations | Staff accounts, role-based access (Front Desk, Technician, Manager, Owner) and the two store locations. | 9.0 | 3 | 10 | 10 |
| E2 | Customer & Device Intake | Customer lookup, device details, job creation, claim ticket and device tag label. | 2.0 | 7 | 22 | 16 |
| E3 | Appointments & Technician Scheduling | Drop-off appointment booking by store and time slot; assigning jobs to technicians and viewing workload. | 1.0 / 2.0 | 4 | 13 | 3 |
| E4 | Repair Job Workflow | Status workflow, diagnosis notes, quote approval, parts usage with automatic deduction and awaiting-parts tracking. | 3.0 / 4.0 | 8 | 26 | 20 |
| E5 | Pickup & Release | Final cost, paid flag, ticket/photo ID verification and release of the device. | 6.0 | 3 | 7 | 5 |
| E6 | Parts Inventory | Parts catalog, stock per store, availability lookup, low-stock list and adjustments. | 7.0 / 9.0 | 4 | 12 | 9 |
| E7 | Purchasing & Receiving | Suppliers, purchase orders with Owner approval, and receiving deliveries against approved purchase orders. | 7.0 | 4 | 15 | 15 |
| E8 | Open Repairs Dashboard | Single view of open repairs and parts availability; quick job lookup. | 8.0 | 2 | 10 | 10 |
| E9 | Customer Email Alerts | One pickup notification email per job, sent by staff from the store's email account. | 5.0 | 1 | 5 | 5 |
| E10 | Data Setup & Import | Importing the existing parts inventory from a spreadsheet (CSV) and daily backup. | 9.0 | 2 | 8 | 5 |
| E11 | Excluded This Release | Items deliberately out of scope for the Dec 9, 2026 handoff. | n/a | 7 | 0 | 0 |
| Total |  |  |  | 45 | 128 | 98 |

## Sheet: Release Plan

| Release Plan - Sprints 1 to 6 |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Course sprint dates provided by the team; gap-week build work is a recommendation. |  |  |  |  |  |  |
| Sprint | Theme | Start | End | Days | Goal | Key Deliverables / Work |
| Sprint 1 | Problem Definition & Feasibility | 2026-09-14 | 2026-09-20 | 7 | Approved problem definition, system boundary and prioritized backlog. | Problem statement; context diagram; Level 0 DFD; feasibility analysis; initial product backlog; risk register; Sprint 1 PSPI document. |
| Gap | Enablers (recommended) | 2026-09-21 | 2026-10-04 | 14 | Remove technical unknowns early. | Code repository and dev environment; hosting decision; spikes for label printing and SMTP email. |
| Sprint 2 | Requirements & Analysis | 2026-10-05 | 2026-10-11 | 7 | Must items analysed and ready to build. | Refined user stories/acceptance criteria; use case diagram; ERD and data dictionary; Level 1 DFDs for 2.0, 3.0, 5.0; role-permission matrix; job status transition diagram; MVP scope freeze. |
| Gap | Build Slice 1 (recommended) | 2026-10-12 | 2026-10-18 | 7 | Foundation working end to end. | PB-01 to PB-08: login, users, stores, customers, devices, job creation, claim ticket, tag label. |
| Sprint 3 | Interface Design | 2026-10-19 | 2026-10-25 | 7 | Validated screen designs for every MVP workflow. | Wireframes for check-in, job detail, dashboard, parts, PO and pickup; print layouts; front desk walkthrough. Continue Slice 2 build (PB-09 to PB-12). |
| Gap | Build Slices 3-4 (recommended) | 2026-10-26 | 2026-11-01 | 7 | MVP feature complete. | PB-13 to PB-25, PB-44 and PB-29: inventory, purchasing with Owner approval, awaiting parts, dashboard, pickup, pickup notification. Test data loaded. |
| Sprint 4 | Working System Demonstration | 2026-11-02 | 2026-11-08 | 7 | Demonstrate the MVP end to end. | Demo: check-in > repair with parts > PO receive > ready > pickup; test results; defect list. |
| Gap | Stabilise & Should items | 2026-11-09 | 2026-11-15 | 7 | Training-ready system. | Fix defects; import real inventory (PB-15); Should items if capacity allows (PB-26 to PB-28, PB-32, PB-33, PB-45). |
| Sprint 5 | Training Session | 2026-11-16 | 2026-11-22 | 7 | Staff at both stores can use the system confidently. | Training plan; user guide; quick-reference cards per role; training sessions; feedback log. |
| Gap | Address feedback | 2026-11-23 | 2026-11-29 | 7 | Incorporate training feedback. | Usability fixes; documentation updates. |
| Sprint 6 | Final Presentation & Handoff | 2026-11-30 | 2026-12-09 | 10 | Successful handoff to QuickPhone. | Final presentation; system and admin/setup documentation; source code handoff; lessons learned. Final deliverables due Dec 9, 2026. |

## Sheet: Sprint 1 Backlog

| Sprint 1 Backlog - Problem Definition & Feasibility (Sep 14 - 20, 2026) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sprint goal: Deliver an owner-approved problem definition and feasibility package - scope, system boundary (context diagram and Level 0 DFD), feasibility recommendation and a prioritized product backlog - so Sprint 2 can start requirements analysis. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Edit yellow cells: team names (L6:L9), Owner Key, Actual Hours and Status. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Task ID | Task | PSPI Deliverable | Owner Key | Owner | Est. Hours | Actual Hours | Remaining Hours | Due | Status | Key | Team Member | Scrum Role | Planned Hours | Remaining Hours |
| S1-01 | Sprint planning: confirm sprint goal, roles, working agreement | Sprint 1 plan | A | Member A | 2 |  | 2 | 2026-09-14 | In Progress | A | Member A | Scrum Master | 11 | 11 |
| S1-02 | Owner interview: confirm scope, current process and baseline figures for success measures | Interview notes | B | Member B | 3 |  | 3 | 2026-09-15 | To Do | B | Member B | Product Owner proxy / Business Analyst | 11 | 11 |
| S1-03 | Write problem statement, objectives, scope (in/out), constraints and assumptions | PSPI section 2 | B | Member B | 4 |  | 4 | 2026-09-16 | In Review | C | Member C | Systems Analyst / Modeler | 15 | 15 |
| S1-04 | Stakeholder and user role analysis | PSPI section 3 | B | Member B | 2 |  | 2 | 2026-09-16 | In Review | D | Member D | Technical Lead | 12 | 12 |
| S1-05 | Context diagram (Gane-Sarson) and flow descriptions | PSPI section 4 | C | Member C | 3 |  | 3 | 2026-09-16 | In Review |  | Total |  | 49 | 49 |
| S1-06 | Level 0 DFD with process and data store descriptions; balance check against context diagram | PSPI section 5 | C | Member C | 6 |  | 6 | 2026-09-17 | In Review |  |  |  |  |  |
| S1-07 | Technical feasibility, including spike plan for label printing | PSPI section 6.1 | D | Member D | 4 |  | 4 | 2026-09-17 | In Review |  |  |  |  |  |
| S1-08 | Economic feasibility: one-time cost (label printers), monthly technology costs, hours saved, alternatives (RepairShopr, RepairDesk) | PSPI section 6.2 | A | Member A | 4 |  | 4 | 2026-09-18 | In Review |  |  |  |  |  |
| S1-09 | Operational, schedule and legal/privacy feasibility | PSPI sections 6.3-6.5 | D | Member D | 3 |  | 3 | 2026-09-18 | In Review |  |  |  |  |  |
| S1-10 | Initial product backlog: epics, user stories, MoSCoW, planning-poker estimates | Product backlog workbook | C | Member C | 6 |  | 6 | 2026-09-18 | In Review |  |  |  |  |  |
| S1-11 | Risk register and open questions for Sprint 2 | PSPI sections 10-11 | D | Member D | 2 |  | 2 | 2026-09-18 | In Review |  |  |  |  |  |
| S1-12 | Hosting and technology options memo for Sprint 2 decision | Tech options memo | D | Member D | 3 |  | 3 | 2026-09-18 | To Do |  |  |  |  |  |
| S1-13 | Assemble PSPI document; peer review against Definition of Done | Sprint 1 PSPI document | A | Member A | 4 |  | 4 | 2026-09-18 | In Review |  |  |  |  |  |
| S1-14 | Sprint review with owner; record feedback and sign-off | Signed acceptance | B | Member B | 2 |  | 2 | 2026-09-19 | To Do |  |  |  |  |  |
| S1-15 | Sprint retrospective; refine backlog for Sprint 2 | Retro notes | A | Member A | 1 |  | 1 | 2026-09-20 | To Do |  |  |  |  |  |
| Total |  |  |  |  | 49 | 0 | 49 |  |  |  |  |  |  |  |

## Sheet: Non-Functional Reqs

| ID | Category | Requirement | Measure / Acceptance | MoSCoW |
|---|---|---|---|---|
| NFR-01 | Usability / Access | Web application usable in current Chrome, Edge and Safari on the existing counter and bench computers; responsive layout. | Front desk completes a check-in in under 3 minutes after training. | Must |
| NFR-02 | Architecture | Single relational database; no third-party services or integrations. The only outbound connection is optional email through the shop's existing mailbox (SMTP). | Architecture review in Sprint 2 confirms no other external dependencies. | Must |
| NFR-03 | Security | Individual accounts, hashed passwords, server-side role-based authorization, HTTPS, automatic logout after inactivity. | Role-permission tests pass for all four roles. | Must |
| NFR-04 | Privacy | Collect only necessary customer data. Do not store photo ID numbers (ID type and checked flag only). Device passcodes not stored in plain text - policy to be decided with owner. | Data dictionary reviewed against this rule in Sprint 2. | Must |
| NFR-05 | Auditability | Every status change, approval, pickup and stock movement records user and date/time. | Audit entries present for each event in Sprint 4 demo. | Must |
| NFR-06 | Multi-location | All jobs, appointments and stock are scoped to one of two stores; users can filter or switch store based on role. | Demo shows both stores with separate stock levels. | Must |
| NFR-07 | Printing | Claim ticket prints on a standard printer; device tag prints on the shop label printer using browser printing. | Test print on the actual printers before Sprint 5 training. | Must |
| NFR-08 | Performance | Dashboard and search respond quickly at shop scale. | Under 2 seconds with 2 stores, 20 users, 1,000 open jobs and 5,000 parts (assumed volumes). | Should |
| NFR-09 | Reliability | Automated daily database backup with a tested restore. | Restore test completed before handoff. | Should |
| NFR-10 | Maintainability / Handoff | Source code in version control; setup/admin guide and user guide delivered. | Delivered by Dec 9, 2026. | Must |
