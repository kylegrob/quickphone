<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - Requirements Catalog and Memo.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - Requirements Catalog and Memo

# Quick Phone Repair Management System Requirements Catalogue and Memo

MIS 4173 | Sprint 2, revised for Sprint 3 |  Fall 2026

## Memo

To: Ashiqullah Pardisi, Quick Phone; Dr. John Drake

From: Kyle Robertson, Ehsanullah Pardisi, Bara Abusamhan, and Leonard Mann

Date: October 8, 2026 (revised October 19, 2026)

Subject: Requirements for repair tracking and parts inventory, and our comparison with an AI catalogue

Our catalogue holds 14 functional and 6 nonfunctional requirements. Nine are confirmed by the client’s September 21 correspondence. FR08’s pickup step is confirmed (#2), but releasing a device only after payment is our decision, so FR08 stays proposed. The rest remain proposed. We built it from the Student Consulting MOU and our Sprint 1 process diagram. An AI catalogue generated from the same notes holds 31 requirements (Appendix A). We judged 11 to restate ours, 10 salient, 7 spurious and 3 in conflict. Three salient items exposed gaps, which we added: the Awaiting Parts status (FR06), receiving stock against an approved order (FR09) and daily backup (NFR06). All ten salient items are now part of this single catalog: the Source column marks every requirement an AI item created or refined (AI-xx), and Appendix A, at the end of this document, maps each of the 31 AI items to its catalog row.

### What the client confirmed

The September 21 correspondence confirmed seven items, which the catalogue cites by number. Four of them changed our Sprint 1 assumptions. Parts are deducted when a technician records them, with no reservation step (FR07). The Owner approves every purchase order (FR10). Customers receive one pickup notification email from the store’s account (FR12), and Technicians cannot send it (NFR05).

- Four roles use the system: Owner, Manager, Technician and Front Desk.

- The workflow runs intake, diagnosis, approval, repair, notification, payment and closure.

- Inventory is deducted automatically when a technician records a part as used.

- Every purchase order needs Owner approval.

- Customers are notified by email only, when the repair is completed.

- Owner, Manager and Front Desk may send notifications; Technicians may not.

- Notifications are sent from the store’s email account.

### AI comparison

We gave Claude Opus 5.5 the September 21 notes and asked for a complete catalogue; the prompt is in Appendix A. The session had already seen our draft, so the comparison was not fully independent. The seven spurious items have no client source: revenue and productivity reports, editable email templates, warranty tracking, three invented performance targets and an untestable privacy clause. Each of the three conflicts broke a client rule. The AI emailed customers automatically when a job was marked complete, which would let a Technician trigger an email, so FR12 is staff-sent. It let the Owner create the orders the Owner approves, so creation stays with the Manager (FR10). It ranked multi-store support Could, though Quick Phone already runs two stores, so FR13 and FR14 are Must.

### Stopping decision

We consider elicitation complete for this slice. The September 21 correspondence brought confirmations, not new processes. Every Must is client-confirmed or traces to a Sprint 1 document (the System Request or the process model), and the AI’s 31 items added refinements but no new user or process. Two blocking questions remain (see Questions for client confirmation). If either answer adds scope, we reopen elicitation for that item only. The use cases, data flow diagrams and data model were cross-checked against this catalogue on October 8 and again on October 19, after the Sprint 2 feedback: appointment scheduling is now in scope as an optional workflow (FR01, UC-12, DFD 1.0). The prototype, interface designs, technical specifications and training materials remain due December 9, 2026.

## Requirements catalogue

Priority is our assessment: Must supports the core workflow; Should can follow if time permits. Status shows whether the client confirmed the item, with the confirmation number. Source shows where the requirement came from: the client’s September 21 confirmations (#1 to #7), Sprint 1 documents and process model, or the AI catalogue (AI-xx, in blue). The acceptance check is a practical test for the prototype, kept in its own column for test planning, and each item names the use case it traces to. Out of scope for the December prototype: stock transfers between stores (each store’s stock is tracked separately), part reservation, text messages, a customer self-service portal, online payment, and links to outside accounting or point-of-sale software.

### Functional requirements

| ID Area | Priority Status | Source | Requirement | Acceptance check | Use case |
|---|---|---|---|---|---|
| FR01 Appointments | Should Proposed | Sprint 1 backlog (story 16) Sprint 3 scope decision | Front Desk can book, reschedule or cancel an optional drop-off appointment for a customer and select an available technician. Walk-in customers need no appointment; a booked appointment pre-fills the repair job at check-in. | Book, reschedule and cancel a sample appointment; check in a walk-in with no appointment; verify a booked appointment pre-fills the job. | UC-12 |
| FR02 Intake and lookup | Must Confirmed #2 | Client confirmation #2 AI-FR03 (intake fields) | Front Desk can find a customer by phone or a job by ticket number. At check-in, Front Desk links the customer and device (type, brand, model, serial or IMEI, condition) to a new repair job and records the reported problem. | Search by phone and by ticket number; create a job and retrieve its customer, device and past repairs. | UC-01, UC-06, UC-13 |
| FR03 Claim ticket | Must Proposed | Sprint 1 System Request (lost devices) Sprint 1 process model | The system produces a claim ticket and device tag carrying the job’s ticket number, and can reprint them. | Print both for a sample intake, reprint them, and match them to the job. | UC-01 |
| FR04 Assignment | Must Proposed | Sprint 1 process model | Front Desk assigns a technician at check-in; each Technician sees only their own job queue. | Assign a job and verify it appears in that technician’s queue only. | UC-01, UC-02 |
| FR05 Diagnosis and quote | Must Confirmed #2 | Client confirmation #2 AI-FR05 (approval date and recorder) | A Technician records a diagnosis, checks stock at their store and enters a quote of labor and parts. Front Desk records the customer’s approval or decline, with the date and who approved, before repair begins. | Save a diagnosis and quote; record a decline and verify the job cannot move to In Repair. | UC-02, UC-03 |
| FR06 Job status | Must Confirmed #2 | Client confirmation #2 AI-FR06 (Awaiting Parts, gap) | Jobs move through Checked In, Diagnosing, Awaiting Approval, In Repair, Awaiting Parts, Ready for Pickup, Returned Unrepaired and Closed. | Step a job through each status; verify the open repairs view at each step. | UC-01 to UC-06, UC-10 |
| FR07 Parts usage | Must Confirmed #3 | Client confirmation #3 AI-FR07 | When a Technician records a part used on a job, that store’s stock is deducted automatically, and stock cannot go below zero. A part that is out of stock is recorded as needed on the job. | Record a part used and verify stock drops; verify an entry below zero is blocked. | UC-02, UC-04 |
| FR08 Pickup and payment | Must Proposed (step confirmed #2) | Client confirmation #2 Sprint 1 System Request (no payment processing); Sprint 2 team decision (release only after payment) | Front Desk matches the device tag to the ticket, verifies photo ID, records the amount, method and status of payment taken at the store’s register, and closes the job. A device is released only after payment is recorded. | Try to close an unpaid job (blocked); pay and close it (succeeds). | UC-06 |
| FR09 Inventory | Must Proposed | Sprint 1 process model AI-FR12 (receive against PO, gap) | A Manager can add parts, record stock received against an approved purchase order, including partial deliveries, and record count adjustments with a reason. | Receive a partial delivery; post an adjustment; verify quantities and the order status. | UC-07, UC-10 |
| FR10 Purchasing | Must Confirmed #4 | Client confirmation #4 AI-FR08 (low-stock list) AI-FR11 (decision back to requester) | A Manager can maintain suppliers, review parts at or below their reorder point and jobs waiting on parts, and create purchase orders linked to those jobs. The Owner approves or rejects every order before it is placed; the decision appears in the Manager’s queue, and a rejected order returns to Draft with a reason. | Submit an order and verify it cannot be placed or received until approved; reject one and verify it returns to Draft. | UC-07 to UC-10 |
| FR11 Inventory import | Should Proposed | Sprint 1 Feasibility Analysis (data conversion) | A Manager can import existing part records from a spreadsheet file, with feedback on invalid rows. | Import a valid file; verify a malformed row is rejected and reported without silent data loss. | UC-07 |
| FR12 Pickup notification | Must Confirmed #5, #7 | Client confirmation #5, #7 AI-FR15 (store email address) | When a job reaches Ready for Pickup, an Owner, Manager or Front Desk user can send the customer a pickup notification email from the store’s email account, telling them the device is ready to collect; the system records the sender and time. Email is the only customer channel. | Send the email for a test job; verify delivery from the store account and the logged sender. | UC-05 |
| FR13 Dashboard | Must Proposed | Sprint 1 System Request (one view of both stores) | The Owner can view open repairs and parts availability together, by store. | Compare dashboard totals with sample job and stock records for each store. | UC-13 |
| FR14 Users and locations | Must Confirmed #1 | Client confirmation #1 | A Manager or the Owner can maintain store details and staff accounts, giving each account one of the four roles and a store; only the Owner can assign the Owner role. | Create a user in each role and verify access; verify a Manager cannot assign Owner. | UC-11 |

### Nonfunctional requirements

| ID Area | Priority Status | Source | Requirement | Acceptance check | Use case |
|---|---|---|---|---|---|
| NFR01 Authorization | Must Confirmed #1 | Client confirmation #1 | Access to customer, job, inventory and purchasing records follows the four approved roles. | A Technician attempts to approve a purchase order and is blocked. | All |
| NFR02 Data accuracy | Must Proposed | Sprint 1 System Request (accurate records) | Appointment, job, stock and payment changes persist without contradictory records, and each status change, stock adjustment, approval and release records who made it and when. | Save, refresh and reconcile a sample transaction across views; verify its history shows the user and time. | All |
| NFR03 Usability | Should Proposed | Sprint 1 Feasibility Analysis (adoption) | Front Desk and Technician tasks use clear forms and readable queues. | A representative user completes an intake and a status update with the prototype without help. | UC-01 to UC-04 |
| NFR04 Privacy | Must Proposed | Sprint 1 System Request (customer data) | Customer contact and device details are visible only to staff with an operational need. | Review each role’s visible fields with the client. | All |
| NFR05 Notification permission | Must Confirmed #6 | Client confirmation #6 AI-FR14 | Technicians cannot send customer email. | A Technician attempts to send a pickup notification and is blocked. | UC-05 |
| NFR06 Backup | Should Proposed | AI-NFR05 (gap) | Job, customer and inventory records are backed up daily and can be restored. | Restore a backup to a test copy; verify a sample job and stock level match. | None (hosting backup) |

## Questions for client confirmation

### Blocking: answer before the Sprint 4 build starts (November 2)

- Is the pickup notification sent by staff or automatically when a repair is marked complete? (FR12)

- Is there a spending threshold below which a purchase order skips Owner approval, or an urgent path when the Owner is unavailable? (FR10)

### Deferred to Sprint 3 design

- How is technician availability determined for booking, and who may reschedule? (FR01)

- Should the customer sign at pickup? UC-06 captures a signature, but no requirement covers it. (FR08)

- Does a diagnostic fee apply when a quote is declined or a device cannot be repaired? (FR05)

- Who sets each part’s reorder point? (FR10)

- Is a phone call the right fallback for customers without email, and who approves the email text? (FR12)

- Do the intake fields match how staff check in devices today? (FR02)

- How are warranty and rework jobs handled, and how long may a device sit uncollected?

## Appendix A: AI-generated catalogue

Generated by Claude Opus 5.5 on September 30, 2026 from the September 21 notes only. Prompt: “You are a systems analyst. From the interview notes below, produce a complete requirements catalogue for Quick Phone’s repair management system. List functional and nonfunctional requirements, each with an ID and a priority (Must, Should or Could).” The Team verdict and Maps to columns are the team’s judgement, added afterward.

### AI functional requirements

| ID | AI requirement | AI priority | Team verdict | Maps to |
|---|---|---|---|---|
| AI-FR01 | Users log in with unique credentials. | Must | Restates | NFR01 |
| AI-FR02 | The system supports four roles: Owner, Manager, Technician, Front Desk. | Must | Restates | FR14 |
| AI-FR03 | At intake, staff create a repair ticket capturing customer name, phone, email, device make, model, serial or IMEI, reported issue and device condition. | Must | Salient | FR02 |
| AI-FR04 | A technician records the diagnosis, estimated cost and estimated completion time. | Must | Restates | FR05 |
| AI-FR05 | Staff record customer approval of the estimate, with method and time, before repair begins. | Must | Salient | FR05 |
| AI-FR06 | Technicians update repair status: In Repair, Awaiting Parts, Completed. | Must | Salient (gap) | FR06 |
| AI-FR07 | Recording a part used on a repair deducts it from inventory automatically. | Must | Salient | FR07 |
| AI-FR08 | The system alerts the Manager when a part falls below its reorder level. | Should | Salient | FR10 |
| AI-FR09 | Managers add and edit parts, with quantity, unit cost and supplier. | Must | Restates | FR09 |
| AI-FR10 | A Manager or the Owner creates purchase orders. | Must | Conflict | FR10 |
| AI-FR11 | The Owner approves or rejects each PO; the requester is notified of the decision. | Must | Salient | FR10 |
| AI-FR12 | Staff record parts received against an approved PO, increasing stock. | Should | Salient (gap) | FR09 |
| AI-FR13 | The system sends the customer an email automatically when a repair is marked Completed. | Must | Conflict | FR12 |
| AI-FR14 | Only Owner, Manager and Front Desk can send notifications; Technicians cannot. | Must | Salient | NFR05 |
| AI-FR15 | Notification emails are sent from the store’s email address. | Must | Salient | FR12 |
| AI-FR16 | The Owner or Manager can edit the notification email template. | Could | Spurious | None |
| AI-FR17 | Staff record payment amount, method and date, and generate a receipt. | Must | Restates | FR08 |
| AI-FR18 | A ticket is closed after payment; closed tickets are read-only. | Must | Restates | FR08 |
| AI-FR19 | The system keeps customer records with repair history. | Should | Restates | FR02 |
| AI-FR20 | Staff search tickets by customer, phone, ticket number or status. | Should | Restates | FR02 |
| AI-FR21 | The Owner views reports on revenue, repair volume, technician productivity and inventory value. | Should | Spurious | None |
| AI-FR22 | The system records warranty periods on completed repairs. | Could | Spurious | Open question |

### AI nonfunctional requirements

| ID | AI requirement | AI priority | Team verdict | Maps to |
|---|---|---|---|---|
| AI-NFR01 | Passwords are stored securely and access is role-based. | Must | Restates | NFR01 |
| AI-NFR02 | Pages load within 2 seconds. | Should | Spurious | None |
| AI-NFR03 | The system is available 99.5% of business hours. | Should | Spurious | None |
| AI-NFR04 | New staff become productive within 1 hour of training. | Should | Restates | NFR03 |
| AI-NFR05 | Data is backed up automatically every day. | Must | Salient (gap) | NFR06 |
| AI-NFR06 | Inventory changes, PO approvals and emails sent are logged. | Should | Restates | NFR02 |
| AI-NFR07 | Completion emails are sent within 5 minutes. | Should | Spurious | None |
| AI-NFR08 | Customer personal data is protected under applicable privacy regulations. | Must | Spurious | None (privacy is covered by NFR04) |
| AI-NFR09 | The system can support multiple store locations. | Could | Conflict | FR13, FR14 |
