<!-- Auto-generated from docs/sprint-2/Sprint 2 - Use Cases.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 2 - Use Cases

## Sprint 2 Use Cases: Quick Phone Repair Management System

Eleven core use cases cover the repair workflow, parts inventory, purchasing and user access, built from the requirements the owner confirmed for Sprint 2.

| Item | Detail |
|---|---|
| Client | Quick Phone Repair & Designs, Raleigh, NC |
| Project sponsor | Ashiqullah Pardisi, Owner |
| Course | MIS 4173 Systems Analysis & Design |
| Team | Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann |
| Sprint | Sprint 2 |

### 1. Actors

Four roles use the system. Customers and suppliers are outside it: customers receive email, and suppliers receive purchase orders sent outside the system.

| Actor | Responsibilities in the system | Sends customer email |
|---|---|---|
| Owner | Approves purchase orders, manages user accounts, sees all activity at both stores | Yes |
| Manager | Maintains parts inventory, creates and receives purchase orders, manages staff accounts | Yes |
| Technician | Diagnoses devices, prepares quotes, performs repairs, records parts used | No |
| Front Desk | Checks in devices, records customer approval, notifies customers, releases devices and records payment | Yes |

### 2. Use Case Summary

| ID | Use case | Primary actor | Backlog stories |
|---|---|---|---|
| UC-01 | Check In Device | Front Desk | 2, 3, 4 |
| UC-02 | Diagnose Device and Prepare Quote | Technician | 5, 6, 10 |
| UC-03 | Record Customer Approval | Front Desk | 4 |
| UC-04 | Repair Device and Record Parts Used | Technician | 6, 10 |
| UC-05 | Send Repair Completion Email | Front Desk (also Manager, Owner) | 13 |
| UC-06 | Release Device and Record Payment | Front Desk | 7 |
| UC-07 | Maintain Parts Inventory | Manager | 8, 9, 11 |
| UC-08 | Create Purchase Order | Manager | 12 |
| UC-09 | Approve Purchase Order | Owner | New in Sprint 2 |
| UC-10 | Receive Purchase Order | Manager | 12 |
| UC-11 | Manage User Accounts | Manager (also Owner) | 1 |

Backlog stories 14 to 17 (audit history, dashboard, appointments, search) support these use cases and are not modeled separately.

### 3. Use Case Diagram

use case diagram · 4 actors, 11 use cases

Front Desk and Technician carry the repair workflow. Manager, Owner and Front Desk can all send the completion email, and UC-09 (highlighted) is new in Sprint 2.

### 4. Repair Workflow Use Cases

UC-01 to UC-06 take a job from intake to closure. Job statuses follow the confirmed workflow: Checked In, Diagnosing, Awaiting Approval, In Repair, Awaiting Parts, Ready for Pickup, Closed.

#### UC-01 Check In Device

Primary actor: Front Desk. Priority: High. Trigger: A customer brings a device to the counter (external).

Stakeholders and interests: Customer wants the device logged and a claim ticket. Technician needs complete intake details. Owner wants no lost devices.

Brief description: Front Desk records the customer and device, creates a repair job, assigns a technician and prints the claim ticket and device tag.

Relationships: Association: Front Desk.

Normal flow of events:

- Front Desk searches for the customer by phone number.

- Front Desk selects the existing customer or enters name, phone and email.

- Front Desk enters the device type, brand, model, serial or IMEI, condition and reported problem.

- Front Desk assigns a technician.

- The system creates the job with status Checked In and generates a ticket number.

- The system prints the claim ticket for the customer and the tag label for the device.

Alternate/exceptional flows:

- 2a. Customer has no email address: Front Desk saves the record and the system flags that no completion email can be sent.

- 6a. Printer fails: Front Desk reprints from the job record before the device leaves the counter.

#### UC-02 Diagnose Device and Prepare Quote

Primary actor: Technician. Priority: High. Trigger: A job is assigned to the technician (external).

Stakeholders and interests: Technician wants a clear record of findings. Customer wants an accurate price before work starts.

Brief description: Technician records the diagnosis, checks parts availability, reserves parts and enters a quote for approval.

Relationships: Association: Technician.

Normal flow of events:

- Technician opens the assigned job and sets status to Diagnosing.

- Technician records the diagnosis.

- Technician selects the parts needed and the system shows stock at that store.

- The system reserves the selected parts for the job.

- Technician enters labor and parts cost; the system totals the quote.

- The system sets status to Awaiting Approval.

Alternate/exceptional flows:

- 3a. Part is out of stock: the system marks the job Awaiting Parts and adds the part to the low-stock list for the Manager.

- 2a. Device cannot be repaired: Technician records the finding and the job moves to "Return unrepaired” with no repair charge.

#### UC-03 Record Customer Approval

Primary actor: Front Desk. Priority: High. Trigger: A job reaches Awaiting Approval (temporal).

Stakeholders and interests: Customer wants to approve cost before work begins. Owner wants approval recorded before labor is spent.

Brief description: Front Desk contacts the customer with the quote and records the decision.

Relationships: Association: Front Desk.

Normal flow of events:

- Front Desk opens the list of jobs Awaiting Approval.

- Front Desk contacts the customer and gives the quote.

- Front Desk records the approval, the date and who approved.

- The system sets status to In Repair and notifies the technician in the system.

Alternate/exceptional flows:

- 3a. Customer declines: Front Desk records the decline, the system releases reserved parts and the job moves to Ready for Pickup with no repair charge.

- 2a. Customer cannot be reached: the job stays Awaiting Approval and Front Desk logs the attempt.

#### UC-04 Repair Device and Record Parts Used

Primary actor: Technician. Priority: High. Trigger: A job reaches In Repair (temporal).

Stakeholders and interests: Technician wants to log work quickly at the bench. Manager needs stock counts to stay accurate.

Brief description: Technician completes the repair and records the parts used; the system deducts them from inventory automatically.

Relationships: Association: Technician.

Normal flow of events:

- Technician opens the job and performs the repair.

- Technician records each part used and its quantity.

- The system deducts the quantities from that store's stock and clears the reservation.

- Technician records repair notes and marks the repair complete.

- The system sets status to Ready for Pickup and adds the job to the notification list.

Alternate/exceptional flows:

- 2a. A different or extra part is needed: Technician records it; if the price changes, the job returns to Awaiting Approval (UC-03).

- 3a. Deduction would take stock below zero: the system blocks the entry and alerts the Manager to correct the count.

#### UC-05 Send Repair Completion Email

Primary actor: Front Desk. Secondary actors: Manager, Owner. Priority: High. Trigger: A job reaches Ready for Pickup (temporal).

Stakeholders and interests: Customer wants to know the device is ready without calling. Owner wants fewer status calls.

Brief description: An authorized user sends the customer a completion email from the store mailbox. Technicians cannot send email.

Relationships: Association: Front Desk, Manager, Owner.

Normal flow of events:

- User opens the list of jobs Ready for Pickup that have not been notified.

- User selects a job and reviews the prefilled email with ticket number, final cost and pickup hours.

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

Normal flow of events:

- Front Desk looks up the job by ticket number.

- Front Desk matches the device tag to the ticket.

- Front Desk checks the customer's photo ID and marks it verified; the ID number is not stored.

- Front Desk records the final cost, payment method and paid status.

- The customer signs for the device and the system stores the signature.

- The system sets status to Closed and records who released the device.

Alternate/exceptional flows:

- 1a. Customer has no ticket: Front Desk finds the job by phone number and requires photo ID before release.

- 3a. ID does not match the customer record: Front Desk does not release the device and notifies the Manager.

### 5. Inventory, Purchasing and Account Use Cases

UC-07 to UC-10 keep parts in stock at both stores, with the Owner approving every purchase order. UC-11 controls who can do what.

#### UC-07 Maintain Parts Inventory

Primary actor: Manager. Priority: High. Trigger: A part is added, changed or counted, or the low-stock list needs review (external).

Stakeholders and interests: Technicians need accurate stock to quote and repair. Owner wants fewer jobs waiting on parts.

Brief description: Manager adds and edits parts, imports the starting inventory and reviews the low-stock list.

Relationships: Association: Manager.

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

Normal flow of events:

- Manager selects the supplier.

- Manager adds parts, quantities and unit costs; the system totals the order.

- Manager links any jobs Awaiting Parts to the order.

- Manager submits the order; the system sets status to Pending Approval and notifies the Owner in the system.

Alternate/exceptional flows:

- 4a. Manager saves without submitting: the order stays in Draft and can be edited.

#### UC-09 Approve Purchase Order

Primary actor: Owner. Priority: High. Trigger: A purchase order reaches Pending Approval (temporal).

Stakeholders and interests: Owner wants to approve all spending. Manager needs a fast decision to keep repairs moving.

Brief description: Owner reviews a submitted purchase order and approves or rejects it.

Relationships: Association: Owner.

Normal flow of events:

- Owner opens the list of orders Pending Approval.

- Owner reviews supplier, parts, total cost and linked jobs.

- Owner approves the order.

- The system sets status to Approved, records the Owner and date, and notifies the Manager in the system.

Alternate/exceptional flows:

- 3a. Owner rejects the order: Owner enters a reason and the system returns it to Draft for the Manager.

#### UC-10 Receive Purchase Order

Primary actor: Manager. Priority: High. Trigger: A supplier delivery arrives at the store (external).

Stakeholders and interests: Manager wants stock updated on arrival. Technicians waiting on parts want to resume work.

Brief description: Manager records what arrived against an approved order and the system adds it to stock.

Relationships: Association: Manager.

Normal flow of events:

- Manager opens the approved purchase order.

- Manager enters the quantity received for each part.

- The system adds the quantities to that store's stock.

- The system moves each linked job out of Awaiting Parts, back to In Repair, so it appears in the assigned technician's queue

- The system sets the order to Received.

Alternate/exceptional flows:

- 2a. Partial delivery: the system sets the order to Partially Received and keeps the rest open.

- 1a. Order is not approved: the system blocks receiving.

#### UC-11 Manage User Accounts

Primary actor: Manager. Secondary actor: Owner. Priority: High. Trigger: A staff member joins, leaves or changes role (external).

Stakeholders and interests: Owner wants each person limited to their role. Staff need working logins.

Brief description: Manager or Owner creates, edits and deactivates accounts and assigns each one a role and store.

Relationships: Association: Manager, Owner.

Normal flow of events:

- User opens account management.

- User enters the staff member's name and email.

- User assigns a role (Owner, Manager, Technician or Front Desk) and a store location.

- The system creates the account and applies that role's permissions.

Alternate/exceptional flows:

- 1a. Staff member leaves: User deactivates the account; the system keeps their history on past jobs.

- 3a. Manager tries to assign the Owner role: the system blocks it; only the Owner can.

### 6. Open Items

Changed from Sprint 1 by the owner's confirmation:

- Store email is approved for notifications, which closes the story 13 open item.

- Customer email is sent only when a repair is completed, not on every status change. Story 13 should be reworded to match.

- Purchase orders now need Owner approval. A new backlog story is needed for UC-09.

- Technicians cannot send customer email (UC-05).

Still to confirm with the owner:

- Payment is recorded in the system and taken at the existing register, since the system request rules out payment processing.

- Whether a diagnostic fee applies when a quote is declined or a device cannot be repaired.

- Who sets each part's reorder point for the low-stock list.

- Required intake fields in UC-01 have not been checked against how staff check in devices today.
