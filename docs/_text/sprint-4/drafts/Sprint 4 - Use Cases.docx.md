<!-- Auto-generated from docs/sprint-4/drafts/Sprint 4 - Use Cases.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 4 - Use Cases

## Sprint 2 Use Cases, revised for Sprints 3 and 4: Quick Phone Repair Management System

Thirteen core use cases cover appointment scheduling, the repair workflow, status reporting, parts inventory, purchasing and user access, built from the requirements the owner confirmed for Sprint 2. Each use case now lists its inputs, outputs and the requirements, DFD processes and data stores it traces to, so the use cases, DFDs and ERD can be checked against each other.

| Item | Detail |
|---|---|
| Client | Quick Phone Repair & Designs, Raleigh, NC |
| Project sponsor | Dr. Ashiqullah Pardisi, Owner |
| Course | MIS 4173 Systems Analysis & Design |
| Team | Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann |
| Sprint | Sprint 2 |

### 1. Actors

Four roles use the system. Customers and suppliers are outside it: customers receive email, and suppliers receive purchase orders sent outside the system.

| Actor | Responsibilities in the system | Sends customer email |
|---|---|---|
| Owner | Approves purchase orders, manages user accounts, sees all activity at both stores, sets the repair labor charge for each part and which roles open each screen, and can check in and repair devices | Yes |
| Manager | Maintains parts inventory, creates and receives purchase orders, manages staff accounts, can check in and repair devices | Yes |
| Technician | Checks in customers, diagnoses devices, confirms the quote approved at check-in or sends an additional repair, performs repairs, records parts used | No |
| Front Desk | Schedules appointments, checks in devices, records customer approval, notifies customers, releases devices and records payment | Yes |

### 2. Use Case Summary

| ID | Use case | Primary actor | Backlog stories |
|---|---|---|---|
| UC-01 | Check In Device | Front Desk (also Technician, Manager, Owner) | 2, 3, 4 |
| UC-02 | Diagnose Device and Prepare Quote | Technician (also Manager, Owner) | 5, 6, 10 |
| UC-03 | Record Customer Approval | Front Desk | 4 |
| UC-04 | Repair Device and Record Parts Used | Technician (also Manager, Owner) | 6, 10 |
| UC-05 | Send Pickup Notification | Front Desk (also Manager, Owner) | 13 |
| UC-06 | Release Device and Record Payment | Front Desk | 7 |
| UC-07 | Maintain Parts Inventory | Manager | 8, 9, 11 |
| UC-08 | Create Purchase Order | Manager | 12 |
| UC-09 | Approve Purchase Order | Owner | New in Sprint 2 |
| UC-10 | Receive Purchase Order | Manager | 12 |
| UC-11 | Manage User Accounts | Manager (also Owner) | 1 |
| UC-12 | Schedule Appointment | Front Desk | 16 (new in Sprint 3) |
| UC-13 | View Repair Status | Owner (also Front Desk) | 15 (new in Sprint 3) |

Backlog stories 14 and 17 (audit history, search) support these use cases and are not modeled separately. Story 16 (appointments) is now UC-12, and story 15 (dashboard) is UC-13.

### 3. Use Case Diagram

use case diagram · 4 actors, 13 use cases

Front Desk and Technician carry the repair workflow. Manager, Owner and Front Desk can all send the pickup notification. UC-12 Schedule Appointment and UC-13 View Repair Status (highlighted) are new in Sprint 3; UC-09 was new in Sprint 2.

### 4. Repair Workflow Use Cases

UC-01 to UC-06 take a job from intake to closure. Job statuses follow the confirmed workflow, and this is the master list used by catalog FR06 and the DFDs: Checked In, Diagnosing, Awaiting Approval, In Repair, Awaiting Parts, Ready for Pickup, Returned Unrepaired, Closed. A quote is built and approved at check-in when the customer has chosen the repair; UC-03 approval is then needed only for a quote with no earlier approval or for an additional repair.

#### UC-01 Check In Device

Primary actor: Front Desk. Secondary actors: Technician, Manager, Owner. Priority: High. Trigger: A customer brings a device to the counter (external).

Stakeholders and interests: Customer wants the device logged and a claim ticket. Technician needs complete intake details. Owner wants no lost devices.

Brief description: Front Desk or a Technician records the customer and device, shows the customer the quote when the repair is already chosen, creates a repair job, assigns a repairer and prints the claim ticket and device tag.

Relationships: Association: Front Desk, Technician, Manager, Owner.

Inputs: Customer phone number; new customer name, phone and email; a device already on file, or a device picked from the list of known models (or a missing model added to the list: type, brand, model) with its serial or IMEI; its condition and reported problem; repairer choice; the parts for the repair the customer wants, if chosen; the customer’s approval of the quote; the booked appointment, if any.

Outputs: Customer and device records; a repair job with ticket number and status Checked In; when the customer has chosen the repair, a quote (parts, labor, total) recorded as approved with who recorded it and when; printed claim ticket and device tag; the appointment marked Checked In.

Traces to: FR02, FR03, FR04, FR06, FR15. DFD 2.0 Register Repair Job (2.1 to 2.5); stores D1 Customers & Devices, D2 Appointments, D3 Repair Jobs, D7 Staff & Stores.

Client validation: Workflow step confirmed September 21 (#2). The intake fields still need a walkthrough against how staff check in devices today. Quote at check-in, Technician check-in and the device list: owner direction, October 30.

Normal flow of events:

- Front Desk searches for the customer by phone number.

- Front Desk selects the existing customer or enters name, phone and email.

- Front Desk selects one of the customer's devices already on file or picks the brand and model from the list of known devices, then records the serial or IMEI, its condition and reported problem.

- If the customer has chosen the repair, Front Desk ticks the parts; the system shows the quote: each part’s cost plus the Owner’s labor charge for it, and the total.

- The customer approves the quote and Front Desk records the approval.

- Front Desk assigns a technician, Manager or Owner, or leaves the job open to claim.

- The system creates the job with status Checked In and generates a ticket number.

- The system prints the claim ticket for the customer and the tag label for the device.

Alternate/exceptional flows:

- 1a. Customer has a booked appointment (UC-12): Front Desk opens it; the system pre-fills the customer and technician and marks the appointment Checked In. The appointment holds no device details, so Front Desk records the device at check-in.

- 2a. Customer has no email address: Front Desk saves the record and the system flags that no pickup notification can be sent.

- 3a. Customer brings more than one device: the customer is saved once, then steps 3 to 8 repeat for each device, so every device gets its own repair job, ticket number, claim ticket and tag.

- 3b. Device is not on the list: Front Desk adds its type, brand and model; the system adds it to the list for every later check-in and uses it for this job.

- 4a. Customer has not chosen a repair or wants a diagnosis first: Front Desk leaves the parts blank; the system makes no quote and the technician quotes after diagnosis (UC-02).

- 5a. Customer does not approve the quote: Front Desk clears the parts and the job is checked in without a quote.

- 8a. Printer fails: Front Desk reprints from the job record before the device leaves the counter.

#### UC-02 Diagnose Device and Prepare Quote

Primary actor: Technician. Secondary actors: Manager, Owner. Priority: High. Trigger: A job is assigned to the technician (external).

Stakeholders and interests: Technician wants a clear record of findings. Customer wants an accurate price before work starts.

Brief description: Technician records the diagnosis and, when the quote approved at check-in is right, starts the repair; otherwise checks parts availability and sends a quote, or an additional repair, for approval.

Relationships: Association: Technician, Manager, Owner.

Inputs: Job selection; diagnosis; for a job with no approved quote, or an additional repair, the parts needed (labor comes from the Owner’s charge for each part).

Outputs: Diagnosis note; stock on hand at the technician’s store; for a job with no approved quote, or an additional repair, a quote (labor, parts, total); status Diagnosing, then In Repair when the check-in quote stands, Awaiting Approval for a new quote or an additional repair, or Awaiting Parts or Returned Unrepaired.

Traces to: FR05, FR06, FR07, FR15. DFD 3.1 to 3.4; stores D3 Repair Jobs, D4 Parts Inventory.

Client validation: Workflow step confirmed (#2). Diagnostic-fee rule still to confirm. Quote built at check-in and approved once: owner direction, October 30.

Normal flow of events:

- Technician opens the assigned job and sets status to Diagnosing.

- Technician records the diagnosis.

- Technician selects the parts needed and the system shows stock at that store.

- The system totals the quote: each part’s cost plus the Owner’s labor charge for it. The Technician does not enter labor.

- The system sets status to Awaiting Approval.

Alternate/exceptional flows:

- 1a. The job was checked in with an approved quote (UC-01) and the diagnosis agrees: Technician confirms it and the system sets status to In Repair with no second approval.

- 1b. The diagnosis, or the repair later, finds an additional repair: Technician says why and picks the extra parts; the system totals the additional quote and sets status to Awaiting Approval (UC-03). The repair already approved stays approved.

- 2a. Device cannot be repaired: Technician records the finding and the system sets status to Returned Unrepaired with no repair charge.

- 3a. Part is out of stock: Technician records the part needed on the job; the system sets status to Awaiting Parts and the job appears on the Manager's list of jobs waiting on parts. When the part is received (UC-10), the job returns to Diagnosing in the technician's queue.

#### UC-03 Record Customer Approval

Primary actor: Front Desk. Priority: High. Trigger: A job reaches Awaiting Approval (temporal).

Stakeholders and interests: Customer wants to approve cost before work begins. Owner wants approval recorded before labor is spent.

Brief description: Front Desk contacts the customer with a new quote (one with no earlier approval, or an additional repair) and records the decision. A quote approved at check-in (UC-01) needs no second approval.

Relationships: Association: Front Desk.

Inputs: Customer decision (approve or decline), decision date, contact attempt note.

Outputs: List of jobs Awaiting Approval with the customer’s phone; the recorded decision and who recorded it; status In Repair, or Returned Unrepaired when a quote with no earlier approval is declined.

Traces to: FR05, FR06. DFD 3.5 Record Quote Decision; store D3 Repair Jobs (QUOTE).

Client validation: Approval stage confirmed (#2). Approval once, at check-in, and again only for an additional repair: owner direction, October 30.

Normal flow of events:

- Front Desk opens the list of jobs Awaiting Approval.

- Front Desk contacts the customer and gives the quote.

- Front Desk records the approval, the date and who approved.

- The system sets status to In Repair and the job appears in the technician's queue.

Alternate/exceptional flows:

- 2a. Customer cannot be reached: the job stays Awaiting Approval and Front Desk logs the attempt.

- 3a. Customer declines a quote with no earlier approval: Front Desk records the decline and the system sets status to Returned Unrepaired with no repair charge.

- 3b. Customer declines an additional repair: Front Desk records the decline; the repair approved earlier continues and the job returns to In Repair, or to Awaiting Parts if stock is short.

#### UC-04 Repair Device and Record Parts Used

Primary actor: Technician. Secondary actors: Manager, Owner. Priority: High. Trigger: A job reaches In Repair (temporal).

Stakeholders and interests: Technician wants to log work quickly at the bench. Manager needs stock counts to stay accurate.

Brief description: Technician completes the repair and records the parts used; the system deducts them from inventory automatically.

Relationships: Association: Technician, Manager, Owner.

Inputs: Job selection; each part and quantity used; repair notes; completion.

Outputs: Parts-used records; automatic stock deduction with an inventory transaction; Awaiting Parts notice; status Ready for Pickup.

Traces to: FR06, FR07. DFD 4.1 to 4.5; stores D3 Repair Jobs, D4 Parts Inventory.

Client validation: Automatic deduction confirmed (#3).

Normal flow of events:

- Technician opens the job and performs the repair.

- Technician records each part used and its quantity.

- The system deducts the quantities from that store's stock.

- Technician records repair notes and marks the repair complete.

- The system sets status to Ready for Pickup and adds the job to the notification list.

Alternate/exceptional flows:

- 2a. A different or extra part adds to the price: Technician sends it as an additional repair (UC-02 1b); the job returns to Awaiting Approval (UC-03) and the repair waits for approval. The repair already approved is not cancelled.

- 2b. Part is out of stock: Technician records the part needed on the job; the system sets status to Awaiting Parts and the job appears on the Manager's list of jobs waiting on parts. When the part is received (UC-10), the job returns to In Repair in the technician's queue.

- 3a. Deduction would take stock below zero: the system blocks the entry and the part appears in the Manager's queue for a count correction.

#### UC-05 Send Pickup Notification

Primary actor: Front Desk. Secondary actors: Manager, Owner. Priority: High. Trigger: A job reaches Ready for Pickup (temporal).

Stakeholders and interests: Customer wants to know the device is ready without calling. Owner wants fewer status calls.

Brief description: An authorized user sends the customer a pickup notification email from the store mailbox, telling them the device is ready to collect. Technicians cannot send email.

Relationships: Association: Front Desk, Manager, Owner.

Inputs: Job selection; confirmed final cost; send instruction.

Outputs: Pickup-ready job list; notification preview; pickup notification to the customer from the store’s account; notification record with sender, time and Sent or Failed.

Traces to: FR12, NFR05. DFD 5.0 Send Pickup Notification (5.1 to 5.5); stores D1 Customers & Devices, D3 Repair Jobs (email fields on REPAIR_JOB), D7 Staff & Stores.

Client validation: Email only, store account, no Technician sends: confirmed (#5, #6, #7). Staff-sent versus automatic is a blocking question.

Normal flow of events:

- User opens the list of jobs Ready for Pickup that have not been notified.

- User selects a job, confirms the final cost against the approved quote, and reviews the prefilled email with ticket number, final cost and pickup hours.

- User sends the email; the system sends it through the store email account.

- The system records the send date, time and sender on the job.

Alternate/exceptional flows:

- 1a. User is a Technician: the system hides the notification list and blocks the send action.

- 3a. Email fails or the customer has no email: the system flags the job and staff call the customer, then record the contact.

#### UC-06 Release Device and Record Payment

Primary actor: Front Desk. Priority: High. Trigger: The customer arrives to pick up the device (external).

Stakeholders and interests: Customer wants the device back quickly. Owner wants the device released only to the right person and payment recorded.

Brief description: Front Desk verifies the customer, records payment and closes the job.

Relationships: Association: Front Desk.

Inputs: Ticket number or phone; ID-checked confirmation; amount, method and payment status; customer signature.

Outputs: Pickup screen (job, final cost, customer name); payment record; release receipt; job Closed with who released it and when.

Traces to: FR02, FR08. DFD 6.0 Record Device Release (6.1 to 6.4); stores D1 Customers & Devices, D3 Repair Jobs (PAYMENT).

Client validation: Workflow step confirmed (#2). Whether the customer signs is still open.

Normal flow of events:

- Front Desk looks up the job by ticket number; the job must be Ready for Pickup or Returned Unrepaired.

- Front Desk matches the device tag to the ticket.

- Front Desk checks the customer's photo ID and marks it verified; the ID number is not stored.

- Front Desk records the amount paid against the final cost, the payment method and the payment status; the system records the time paid.

- The customer signs for the device and the system stores the signature.

- The system sets status to Closed and records who released the device.

Alternate/exceptional flows:

- 1a. Customer has no ticket: Front Desk finds the job by phone number and requires photo ID before release.

- 3a. ID does not match the customer record: Front Desk does not release the device and notifies the Manager.

- 4a. Customer cannot pay: Front Desk does not release the device, and the job stays open until payment is recorded.

- 4b. Nothing is owed (quote declined or device not repairable): Front Desk skips the payment step and goes to the signature; the system sets status to Closed. If the owner sets a diagnostic fee (open question, FR05), it is taken here as a normal payment.

### 5. Inventory, Purchasing and Account Use Cases

UC-07 to UC-10 keep parts in stock at each store, with the Owner approving every purchase order. Stock transfers between stores are out of scope. UC-11 controls who can do what.

#### UC-07 Maintain Parts Inventory

Primary actor: Manager. Priority: High. Trigger: A part is added, changed or counted, or the low-stock list needs review (external).

Stakeholders and interests: Technicians need accurate stock to quote and repair. Owner wants fewer jobs waiting on parts.

Brief description: Manager adds and edits parts, imports the starting inventory and reviews the low-stock list.

Relationships: Association: Manager.

Inputs: Part details (cost, supplier, device model, grade, quantity, reorder point; repair labor charge, set by the Owner only); CSV import file; count adjustment with reason.

Outputs: Part and stock records for the store; import report of rejected rows; adjustment transaction; low-stock list.

Traces to: FR09, FR10, FR11, FR15. DFD 9.3 Maintain Parts Catalog (9.5 in the physical model) and 7.1; stores D4 Parts Inventory, D6 Suppliers.

Client validation: Proposed; who sets reorder points is still open.

Normal flow of events:

- Manager opens inventory for a store.

- Manager adds or edits a part with cost, supplier, device model, grade, quantity and reorder point.

- The system saves the part and updates stock for that store.

- Manager reviews the low-stock list of parts at or below their reorder point.

Alternate/exceptional flows:

- 2a. First launch: Manager imports existing inventory from a CSV file and the system reports rows that failed validation.

- 2b. Physical count differs from the system: Manager records an adjustment with a reason.

#### UC-08 Create Purchase Order

Primary actor: Manager. Priority: High. Trigger: A part is on the low-stock list or a job is Awaiting Parts (temporal).

Stakeholders and interests: Manager wants to reorder quickly. Owner wants control over spending.

Brief description: Manager creates a purchase order and submits it to the Owner for approval.

Relationships: Association: Manager.

Inputs: Supplier; parts, quantities and unit costs; linked jobs Awaiting Parts; submit or save.

Outputs: Purchase order in Draft or Pending Approval with its lines and job links; an entry in the Owner’s approval queue.

Traces to: FR10. DFD 7.2 Record Purchase Order; stores D5 Purchase Orders, D6 Suppliers, D3 Repair Jobs.

Client validation: Owner approval of every PO confirmed (#4).

Normal flow of events:

- Manager selects the supplier.

- Manager adds parts, quantities and unit costs; the system totals the order.

- Manager links any jobs Awaiting Parts to the order.

- Manager submits the order; the system sets status to Pending Approval and the order appears in the Owner's approval queue.

Alternate/exceptional flows:

- 4a. Manager saves without submitting: the order stays in Draft and can be edited.

#### UC-09 Approve Purchase Order

Primary actor: Owner. Priority: High. Trigger: A purchase order reaches Pending Approval (temporal).

Stakeholders and interests: Owner wants to approve all spending. Manager needs a fast decision to keep repairs moving.

Brief description: Owner reviews a submitted purchase order and approves or rejects it.

Relationships: Association: Owner.

Inputs: Approve or reject decision; rejection reason.

Outputs: PO Approved with the Owner and date, or returned to Draft with the reason; an entry in the Manager’s placement queue.

Traces to: FR10, NFR01. DFD 7.3 Record Purchase Order Approval; store D5 Purchase Orders.

Client validation: Confirmed (#4). Spending threshold or urgent path is a blocking question.

Normal flow of events:

- Owner opens the list of orders Pending Approval.

- Owner reviews supplier, parts, total cost and linked jobs.

- Owner approves the order.

- The system sets status to Approved, records the Owner and date, and the order appears in the Manager's queue to place with the supplier.

Alternate/exceptional flows:

- 3a. Owner rejects the order: Owner enters a reason and the system returns it to Draft for the Manager.

#### UC-10 Receive Purchase Order

Primary actor: Manager. Priority: High. Trigger: The Owner approves an order, or a supplier delivery arrives at the store (external).

Stakeholders and interests: Manager wants stock updated on arrival. Technicians waiting on parts want to resume work.

Brief description: Manager records that an approved order was placed with the supplier, then records what arrived; the system adds it to stock.

Relationships: Association: Manager.

Inputs: Placed-with-supplier confirmation; quantity received per line.

Outputs: PO status Ordered, Partially Received or Received; stock increase with an inventory transaction; list of jobs released from Awaiting Parts.

Traces to: FR06, FR09, FR10. DFD 7.4 and 7.5; stores D3 Repair Jobs, D4 Parts Inventory, D5 Purchase Orders.

Client validation: Proposed; receiving against an approved order came from the AI catalogue (AI-FR12).

Normal flow of events:

- Manager places the approved order with the supplier outside the system and records it as placed; the system sets status to Ordered.

- When the delivery arrives, Manager opens the ordered purchase order.

- Manager enters the quantity received for each part.

- The system adds the quantities to that store's stock.

- The system moves each linked job out of Awaiting Parts, back to Diagnosing or In Repair, so it appears in the assigned technician's queue; the Manager sees the list of released jobs.

- The system sets the order to Received.

Alternate/exceptional flows:

- 1a. Order is not approved: the system blocks placing and receiving it.

- 3a. Partial delivery: the system sets the order to Partially Received and keeps the rest open.

#### UC-11 Manage User Accounts

Primary actor: Manager. Secondary actor: Owner. Priority: High. Trigger: A staff member joins, leaves or changes role (external).

Stakeholders and interests: Owner wants each person limited to their role. Staff need working logins.

Brief description: Manager or Owner creates, edits and deactivates accounts and assigns each one a role and store. The Owner also sets which screens each role can open.

Relationships: Association: Manager, Owner.

Inputs: Staff member name, email, role and store; deactivation request. For the Owner: which screens each role can open.

Outputs: Staff account with its role’s permissions; confirmation, or a block when a Manager tries to assign Owner.

Traces to: FR14, NFR01. DFD 9.1 Maintain Staff Accounts and 9.2 Maintain Store Details; store D7 Staff & Stores.

Client validation: Four roles confirmed (#1).

Normal flow of events:

- User opens account management.

- User enters the staff member's name and email.

- User assigns a role (Owner, Manager, Technician or Front Desk) and a store location.

- The system creates the account and applies that role's permissions.

Alternate/exceptional flows:

- 1a. Staff member leaves: User deactivates the account; the system keeps their history on past jobs.

- 3a. Manager tries to assign the Owner role: the system blocks it; only the Owner can.

- 4a. Owner changes which screens a role can open: the system saves the change and applies it the next time anyone in that role opens a screen. Rules inside a screen (who approves a purchase order, who sees contact details) do not change.

### 6. Appointment Scheduling Use Case

Sprint 2 feedback asked whether appointments are required, optional or in scope, and where they are modeled. Decision: appointment scheduling is in scope and optional. Walk-in customers need none; a booked appointment pre-fills the job at check-in (UC-01 1a). It is modeled as UC-12, DFD process 1.0 and the APPOINTMENT entity (0..1 per repair job).

#### UC-12 Schedule Appointment

Primary actor: Front Desk. Priority: Medium (FR01 is a Should). Trigger: A customer calls or visits to arrange a drop-off time (external).

Stakeholders and interests: Customer wants a set drop-off time. Technician wants a predictable queue. Front Desk wants the job pre-filled when the customer arrives.

Brief description: Front Desk books, reschedules or cancels an optional drop-off appointment with an available technician at a store.

Relationships: Association: Front Desk. UC-01 Check In Device uses the appointment when one exists.

Inputs: Store and date; customer phone, or name, phone and email for a new customer; chosen time and technician; reschedule or cancel request.

Outputs: Free times for that store and date; appointment record (Booked, Cancelled or No Show) and confirmation; the pre-filled job when the customer checks in (UC-01).

Traces to: FR01. DFD 1.0 Schedule Appointment (1.1 to 1.3); stores D1 Customers & Devices, D2 Appointments, D7 Staff & Stores.

Client validation: Not yet validated: new in Sprint 3. Free times are derived from store hours and booked appointments until the owner says how technician availability is set; who may reschedule is also open (FR01).

Normal flow of events:

- Front Desk selects the store and date; the system shows each technician's free times at that store: the store's business hours less the appointments already booked.

- Front Desk searches for the customer by phone number, or enters name, phone and email for a new customer.

- Front Desk selects a time and a technician.

- The system records the appointment as Booked and shows the confirmation.

- When the customer arrives, UC-01 pre-fills the repair job from the appointment and marks it Checked In.

Alternate/exceptional flows:

- 1a. No free time on the requested date: Front Desk offers another date, or the customer walks in without an appointment.

- 3a. Customer asks to reschedule: Front Desk opens the appointment and selects a new time; the system updates it.

- 3b. Customer cancels: Front Desk cancels the appointment; the system records it as Cancelled.

- 5a. Customer does not arrive: Front Desk marks the appointment No Show.

### 7. Status Reporting Use Case

The Sprint 3 review found that FR13, a Must, and DFD process 8.0 Report Repair Status had no use case. UC-13 covers both: the Owner’s overview of both stores and the Front Desk lookup when a customer calls to ask about a device. It only reads data.

#### UC-13 View Repair Status

Primary actor: Owner. Secondary actor: Front Desk. Priority: High (FR13 is a Must). Trigger: The Owner wants to see where repairs and parts stand at both stores, or a customer calls to ask about a device (external).

Stakeholders and interests: Owner wants one view of open repairs and parts availability at both stores. Front Desk wants to answer “where’s my phone?” while the customer is on the line. Customer wants a quick, accurate answer.

Brief description: The Owner views open repairs, jobs awaiting parts and low stock by store; Front Desk looks up one job’s status for a customer.

Relationships: Association: Owner, Front Desk.

Inputs: Store (one store or both); a status or figure to drill into; for a lookup, ticket number or customer phone.

Outputs: Two-store overview: open jobs by status, jobs Awaiting Parts and parts at or below their reorder point, for each store; the jobs or parts behind a figure; for a lookup, the job’s current status, assigned technician and when the status last changed.

Traces to: FR13, FR02, NFR01, NFR04. DFD 8.0 Report Repair Status; stores D1 Customers & Devices, D3 Repair Jobs, D4 Parts Inventory, D7 Staff & Stores.

Client validation: Proposed. The goal of one view across both stores comes from the Sprint 1 System Request; what the overview shows still needs the owner’s walkthrough.

Normal flow of events:

- Owner opens the repair status overview.

- The system shows, for each store, open jobs by status, jobs Awaiting Parts and parts at or below their reorder point.

- Owner selects a store, a status or the low-stock figure to see the jobs or parts behind it.

- Owner opens a job to see its status history.

Alternate/exceptional flows:

- 1a. A customer calls about a device: Front Desk searches by ticket number or phone; the system shows the job’s current status, assigned technician and when the status last changed.

- 1b. A Technician tries to open the overview: the system blocks it; technicians see only their own job queue (FR04, NFR01).

### 8. Open Items

Changed from Sprint 1 by the owner's confirmation:

- Store email is approved for notifications, which closes the story 13 open item.

- Quote at check-in, October 30: a quote (part cost plus the Owner’s labor charge) is built at check-in and approved once; approval is repeated only for an additional repair (UC-01 to UC-04). Technicians can check in, Managers and the Owner can repair, check-in picks the device from a list, and the Owner sets which roles open each screen (UC-11).

- Customer email is sent only when a repair is completed, not on every status change. Story 13 should be reworded to match.

- Purchase orders now need Owner approval. A new backlog story is needed for UC-09.

- Technicians cannot send customer email (UC-05).

Resolved by the Sprint 2 feedback:

- Appointment scheduling is in scope and optional; it is UC-12 and DFD process 1.0, and walk-ins skip it.

Client validation: The workflow order (#2) and the rules in confirmations #3 to #7 are validated by the client. The step-by-step flows of every use case, and all of UC-12, still need a walkthrough with the owner before Sprint 3 design sign-off; each use case’s Client validation line records its status. No use case is accepted because the AI catalogue suggested it.

Still to confirm with the owner:

- Payment is recorded in the system and taken at the existing register, since the system request rules out payment processing.

- Whether a diagnostic fee applies when a quote is declined or a device cannot be repaired.

- Who sets each part's reorder point for the low-stock list.

- Required intake fields in UC-01 have not been checked against how staff check in devices today.

- Whether labor is charged per part, per repair or per hour, and how a repair with no part is priced.

- Whether a Technician may see a customer’s phone and email while checking them in.

- Which roles may add a device to the check-in list, and who keeps the list tidy.

- Whether screen access should also be set per person or per action, not only per role.
