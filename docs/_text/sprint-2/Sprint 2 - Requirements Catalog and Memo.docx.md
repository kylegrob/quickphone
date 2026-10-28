<!-- Auto-generated from docs/sprint-2/Sprint 2 - Requirements Catalog and Memo.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 2 - Requirements Catalog and Memo

# Quick Phone Repair Management System Requirements Catalogue and Memo

MIS 4173 | Sprint 2 | Fall 2026

## Memo

To: Ashiqullah Pardisi, Quick Phone; Dr. John Drake

From: Kyle Robertson, Ehsanullah Pardisi, Bara Abusamhan, and Leonard Mann

Date: September 25, 2026

Subject: Proposed requirements for scheduling repair and parts inventory

## The requirements catalogue holds 14 functional and 4 nonfunctional requirements, 11 of them confirmed in the client's September 21 correspondence. The AI catalogue, generated from the same notes, holds 31 requirements (Appendix A). We judged 7 spurious, 10 salient and 3 in conflict with what the client told us; the other 11 restate items we already had. Three of the salient items exposed gaps, which we have added to our catalogue

## Using the Student Consulting MOU and the process diagram from our Sprint 1 presentation, our team created the requirements for Quick Phone’s web-based repair system. The process diagram includes scheduling drop-off appointments, checking in devices, assigning technicians, completing repairs, sending customer email updates, handling pickup, managing parts and purchases, and using a dashboard to track everything.

## Before we finalize the use cases, process models, and data models, we still need to confirm a few details with Quick Phone. These include how quote approvals will work, how technician availability will be handled, when parts should be reserved, how payment status will be recorded, and when customer emails should be sent. The project is still expected to include a prototype, interface designs, technical specifications, and training materials by December 9, 2026.

## Requirements catalogue

Priority is our initial assessment: Must support the core workflow; Should can follow if time permits. All items remain proposed until the client confirms them. Each test describes a practical acceptance check for the prototype.

### Functional requirements

| ID | Area | Prio. | Requirement and acceptance check |
|---|---|---|---|
| FR01 | Appointments | Must | Front desk staff can book or change a drop-off appointment and select an available technician. Check: Book and reschedule a sample appointment; verify the assigned technician and time. |
| FR02 | Intake | Must | At check-in, staff can link a customer and device to a new repair job and record the reported issue. Check: Create a job from an appointment and retrieve its customer and device details. |
| FR03 | Claim ticket | Should | The system can produce a claim ticket and device tag with a job identifier. Check: Generate both items for a sample intake and match them to the job. |
| FR04 | Assignment | Must | Staff can assign a repair to a technician, who can see an assigned job queue. Check: Assign a job and verify it appears in the technician’s view. |
| FR05 | Diagnosis and quote | Must | A technician can record a diagnosis and quote; staff can record the customer quote decision. Check: Save a diagnosis, quote, and approval decision on one job. |
| FR06 | Job status | Must | Authorized staff can update a job from intake through repair, ready for pickup, and release. Check: Update a job and verify its status in the open repairs view. |
| FR07 | Parts usage | Must | A technician can see parts availability, reserve a part for a job, and record actual usage. Check: Reserve and use a sample part; verify job detail and available stock. |
| FR08 | Pickup | Must | Front desk staff can verify pickup and record payment status before releasing a device. Check: Complete a sample pickup and verify the job is closed. |
| FR09 | Inventory | Must | A store manager can add parts and record stock received, used, or corrected. Check: Post each transaction and verify the resulting quantity. |
| FR10 | Purchasing | Should | A store manager can maintain suppliers and purchase orders and review low-stock items. Check: Create a purchase order and verify its status and linked supplier. |
| FR11 | Inventory import | Should | A store manager can import a CSV of part records with validation feedback. Check: Import a valid file and reject a malformed row without silent data loss. |
| FR12 | Customer alerts | Should | The system can email a customer when an agreed job status change occurs. Check: Trigger a test status change and verify an email to the linked address. |
| FR13 | Dashboard | Must | The store owner can view open repairs and current parts availability together. Check: Compare dashboard totals with sample job and inventory records. |
| FR14 | Users and locations | Should | A store manager can maintain staff accounts, roles, and locations. Check: Assign a role and location and verify the resulting access. |

### Nonfunctional requirements

| ID | Area | Prio. | Requirement and acceptance check |
|---|---|---|---|
| NFR01 | Authorization | Must | Staff access to customer, job, inventory, and purchasing records follows approved roles. Check: Verify that a user cannot perform an unauthorized action. |
| NFR02 | Data accuracy | Must | Appointment, job, stock, and payment status changes persist without creating contradictory records. Check: Save, refresh, and reconcile a sample transaction across views. |
| NFR03 | Usability | Should | Front desk and technician tasks use clear forms and readable queues. Check: Have a representative user complete intake and status update with the prototype. |
| NFR04 | Privacy | Must | Customer contact and device information is visible only to staff with an operational need. Check: Review role access and visible fields with the client. |
| NRF06 | Backup | Should | Job, customer and inventory records are backed up daily and can be restored Check: Restore a backup to a test copy; verify a sample job and stock level match. |

## Questions for client confirmation

- Which status changes should trigger email, and who approves the message text?

- How is technician availability determined, and who may assign or reschedule jobs?

- When are parts reserved versus deducted, and how are shortages handled?

- Who approves a quote, and what proof of payment or pickup must be recorded?

- Are purchasing, CSV import, and multiple locations within the December prototype scope?
