<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - DFD and ERD Models.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - DFD and ERD Models

Quick Phone Repair Management System

Data Flow Diagrams and Entity Relationship Diagrams (revision 2)

MIS 4173 | Sprint 3 | Fall 2026 | Team 4: Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann | October 20, 2026

## How this revision answers the Sprint 2 feedback

The requirements, use cases, DFDs and ERD now describe the same system, and every diagram is drawn to be read on a 16:9 slide. The matching slide deck (QuickPhone_Sprint3_DFD_ERD_Slides.pptx) and a PDF of every diagram are in the slides folder beside this document.

| Feedback | What changed | Where |
|---|---|---|
| Missing context diagram | Logical and physical context diagrams: the system, Customer, Front Desk, Technician, Store Manager and Store Owner, with their major flows. | Sections 2, 6 |
| Process names describe people's work | Every process names what the information system does, e.g. Record Diagnosis, Record Repair Work, Retrieve Customer Record (Table 8.1). | Sections 3–5, 8 |
| Repeated entities and data stores | Every external entity and every data store is drawn once per diagram, at every level, logical and physical. | All DFDs |
| Appointment scheduling unclear | In scope and optional: process 1.0 Schedule Appointment with its own Level 1, use case UC-12, and APPOINTMENT 0..1 per job. Walk-ins skip it. | Sections 3, 4.1, 7 |
| ERD unreadable | ERD simplified from 22 to 16 entities and drawn for 16:9 slides: an overview plus three detail diagrams with all keys and attributes. Slide deck and PDFs supplied. | Section 6 |
| DFDs and ERD inconsistent | 7 data stores hold the 16 entities, each entity in exactly one store. Each store lists its entities on every DFD, and the ERD overview draws each store as a box around its entities. | Section 7 |

## 1. Model set at a glance

- Context diagram: the system boundary and five external entities. The diagrams take the system’s viewpoint: an external entity is whoever gives data to the system or receives data from it. Staff enter what customers tell them, so the Customer appears only where it receives something from the system directly (the claim ticket and the pickup notification), and suppliers do not appear because purchase orders are placed with them outside the system.

- Level 0: nine processes and seven data stores; shown complete and in four slide-sized parts (booking and check-in, repair bench, pickup notification and release, back office). Nine is within the textbook’s limit: Dennis, Wixom and Roth advise at least three and “no more than seven to nine” processes per DFD (SAD 8e Ch. 4, p. 149), and every Level 1 meets the stricter three-to-seven of the Fig. 4-24 checklist. Getting Level 0 down to seven would mean merging unrelated work or rejoining appointments and release, which the Sprint 2 feedback asked us to model separately, so Level 0 keeps nine processes and is read in four parts.

- Level 1: one diagram for each process except 8.0, a read-only primitive described in Table 3.1.

- ERD: 16 entities (logical) and 16 tables (physical), each held by exactly one of the seven data stores.

- Notation: Gane and Sarson DFDs and crow's foot ERDs (Dennis, Wixom and Roth, SAD 8e). Every entity and store is drawn once per diagram.

## 2. Context diagram

Figure 2.1 Logical context diagram

## 3. Level 0 DFD

The complete Level 0 is shown first for reference; the four parts that follow show the same flows at a size that can be read on a slide or page. Every line runs horizontally or vertically, so lines that must cross do so at right angles (SAD 8e Ch. 4). Each part draws every store and entity its processes use, once.

Figure 3.1 Complete logical Level 0 (full resolution in slides/logical/02_DFD_Level0_Complete_Logical.pdf)

Figure 3.2 Level 0, part 1: front counter, booking and check-in (1.0, 2.0)

Figure 3.3 Level 0, part 2: repair bench (3.0, 4.0)

Figure 3.4 Level 0, part 3: front counter, pickup notification and release (5.0, 6.0)

Figure 3.5 Level 0, part 4: back office and reporting (7.0, 8.0, 9.0)

### Table 3.1 Level 0 process descriptions

| No. | Process | What the system does | Use case | Requirements | Stores |
|---|---|---|---|---|---|
| 1.0 | Schedule Appointment | Lists free times (store hours less booked appointments), records a booking against a customer, and records reschedules and cancellations. Optional: walk-ins skip it. | UC-12 | FR01 | D1, D2, D7 |
| 2.0 | Register Repair Job | Retrieves or saves the customer, records the device, creates the job with a ticket number, an optional device passcode and an optional technician (pre-filled from an appointment when one exists) and prints the claim ticket for the customer and the device tag. | UC-01 | FR02–FR04, FR06 | D1, D2, D3, D7 |
| 3.0 | Record Diagnosis | Shows the technician's queue with the unassigned jobs and appointments they may claim, records the diagnosis, checks stock, records the quote and the customer's decision. | UC-02, UC-03 | FR05–FR07 | D2, D3, D4 |
| 4.0 | Record Repair Work | Records parts used (deducting stock), part requests (Awaiting Parts) and completion (Ready for Pickup). | UC-04 | FR06, FR07 | D3, D4 |
| 5.0 | Send Pickup Notification | Lists jobs ready for pickup, confirms the final cost, prepares the pickup notification and sends it from the store account when staff or the Technician click Send (never automatically), and records the result on the job. | UC-05 | FR12, NFR05 | D1, D3, D7 |
| 6.0 | Record Device Release | Retrieves the pickup job, records the ID check and payment, and closes the job; refuses to close an unpaid job unless nothing is owed (no diagnostic fee for a device that cannot be repaired). | UC-06 | FR08 | D1, D3 |
| 7.0 | Process Purchase Orders | Alerts the Manager when a part reaches its reorder point and lists part requests; records POs, a Manager's approval, placement and receipt (adding stock and releasing waiting jobs). Nothing is ordered automatically. | UC-08–UC-10 | FR09, FR10 | D3, D4, D5, D6 |
| 8.0 | Report Repair Status | Answers status enquiries and, when the Owner asks, produces the repair and inventory overview of both stores. Read only; a primitive with no Level 1. | UC-13 | FR13 | D1, D3, D4, D7 |
| 9.0 | Maintain Shop Records | Maintains staff accounts, store details, the parts catalog (adjustments, starting import) and suppliers. | UC-07, UC-11 | FR09, FR11, FR14 | D4, D6, D7 |

## 4. Level 1 DFDs (logical)

Each Level 1 balances with its parent (SAD 8e Ch. 4, Fig. 4-24): every Level 0 flow into or out of a process appears on its Level 1, either under the same name or split into named parts, and no Level 1 adds an input or output that its parent lacks. Every flow name is used once across the whole set, and each name is a noun. Appendix B lists every logical flow with the data elements it carries and, for a Level 1 flow, the Level 0 flow it belongs to.

Figure 4.1 Level 1: 1.0 Schedule Appointment

Figure 4.2 Level 1: 2.0 Register Repair Job

Figure 4.3 Level 1: 3.0 Record Diagnosis

Figure 4.4 Level 1: 4.0 Record Repair Work

Figure 4.5 Level 1: 5.0 Send Pickup Notification

Figure 4.6 Level 1: 6.0 Record Device Release

Figure 4.7 Level 1: 7.0 Process Purchase Orders

Figure 4.8 Level 1: 9.0 Maintain Shop Records

## 5. Physical DFDs

The physical set applies the textbook's logical-to-physical steps (SAD 8e Ch. 9, Fig. 9-1). Each process carries an implementation band, a dashed human–machine boundary is drawn around each person who uses the system’s screens (Front Desk, Technician, Manager, Owner), as in Figs. 9-2 and 9-4, and each store is a group of tables in the PostgreSQL database, named “PostgreSQL: …” with its tables listed. Following Figs. 9-2 and 9-4, each flow has one noun name that states its medium: “… Input Form” for a form a person fills in on screen, the plain data name for what the system shows a person (a list, an alert, a confirmation; lists end in “List”), “… Printout”, “… Email” and “… File” for paper, the store’s email and an uploaded file, and “PostgreSQL Record: …” or “PostgreSQL Record Update: …” for rows read from or written to a store. A Level 0 flow that groups several screens splits into named parts on its Level 1; the full-size set (QuickPhone_Physical_DFD_Set.pdf) lists every split. The manual steps (the photo-ID check and taking payment on the unlinked card machine) are manual processes inside the Front Desk’s boundary, on the human side. The Customer has no boundary: like the Customer Service Department in Fig. 9-2, the customer only receives a printout and an email and never uses the system’s screens. 9.5 Import Inventory File is a batch process.

The implementation is the route chosen, provisionally, in the Sprint 3 alternative matrix: a custom web application built with Django (Python) and a PostgreSQL database, hosted offsite as a three-tier thin client–server system and used through a browser on the stores’ Lenovo ThinkPads (SAD 8e Fig. 7-2). It scored 415 of a possible 500 against 350 for a repair-shop subscription, and the result reverses if nobody will support the system after handoff, which the owner has still to answer. Daily backup (NFR06) is the managed database service’s automated backup. The physical diagrams also show the owner’s October 23 clarifications: a Technician may send the pickup notification, a Manager approves every purchase order, the system alerts the Manager when a part reaches its reorder point, technicians request parts and may claim unassigned jobs and appointments, a device that cannot be repaired owes no diagnostic fee, and an optional passcode is recorded at check-in (QuickPhone_Physical_DFD_Set.pdf, page 2). A Technician sending contradicts the September 21 confirmation #6 and is still to be confirmed with the owner.

Figure 5.1 Physical context diagram

Figure 5.2 Complete physical Level 0

Figure 5.3 Physical Level 0, part 1: booking and check-in (1.0, 2.0)

Figure 5.4 Physical Level 0, part 2: repair bench (3.0, 4.0)

Figure 5.5 Physical Level 0, part 3: pickup notification and release (5.0, 6.0)

Figure 5.6 Physical Level 0, part 4: back office and reporting (7.0, 8.0, 9.0)

Figure 5.7 Physical Level 1: 1.0 Schedule Appointment

Figure 5.8 Physical Level 1: 2.0 Register Repair Job

Figure 5.9 Physical Level 1: 3.0 Record Diagnosis

Figure 5.10 Physical Level 1: 4.0 Record Repair Work

Figure 5.11 Physical Level 1: 5.0 Send Pickup Notification

Figure 5.12 Physical Level 1: 6.0 Record Device Release

Figure 5.13 Physical Level 1: 7.0 Process Purchase Orders

Figure 5.14 Physical Level 1: 9.0 Maintain Shop Records

## 6. Entity relationship diagrams

The overview draws each DFD data store as a dashed box around the entities it holds, so the ERD and the DFDs can be read against each other. The three detail diagrams show every attribute and key. Each relationship line is named in both directions, as in the textbook's physical ERD (SAD 8e Fig. 10-8, "Places / Is Placed By"): the upper or left name reads from the "one" side to the "many" side and the lower or right name reads back, so the line between STORE and EMPLOYEE reads "a STORE employs EMPLOYEEs" and "an EMPLOYEE is employed by a STORE". Crow's foot marks give its cardinality and modality (SAD 8e Ch. 5, Step 3). Links to EMPLOYEE that only record who did something (changes a status, decides a quote, sends the pickup notification, records an inventory transaction, creates or approves a purchase order) are listed as foreign keys on the detail diagrams rather than drawn as lines; the complete physical ERD (Figure 6.9) draws every foreign key as a line (SAD 8e Ch. 10, Step 4).

Figure 6.1 Logical ERD overview: 16 entities in 7 data stores

Figure 6.2 Detail 1: customers, devices, appointments, staff and stores

Figure 6.3 Detail 2: repair jobs

Figure 6.4 Detail 3: parts, purchasing and suppliers

Figure 6.5 Physical ERD overview: 16 tables

Figure 6.6 Physical detail 1

Figure 6.7 Physical detail 2

Figure 6.8 Physical detail 3

Figure 6.9 Complete physical ERD: every table, key and relationship (full size in QuickPhone_Physical_ERD_Full.pdf)

### Table 6.1 Simplification from the Sprint 2 ERD (22 → 16 entities)

| Change | Reason |
|---|---|
| ROLE → EMPLOYEE.Role (checked value list) | The four roles are fixed by the client (#1); a lookup table added an entity without adding information. |
| JOB_STATUS → checked JOB_STATUS_HISTORY.Status (copied to repair_job.status in the physical model) | The eight statuses are fixed (FR06); the history table still records every change, who made it and when. |
| NOTIFICATION → REPAIR_JOB email fields (EmailSentAt, EmailSentByID, EmailStatus) | Exactly one pickup notification email per job (client-confirmed #5). |
| JOB_NOTE → REPAIR_JOB.DiagnosisNotes and RepairNotes | The use cases record one diagnosis and one set of repair notes per job; contact attempts go in the status history note. |
| PO_JOB_LINK → JOB_PART.PurchaseOrderID | A waiting job is linked to the order for the part it needs; the extra link table is not needed. |
| EMAIL_TEMPLATE removed | Judged spurious in the catalog memo (no client source); the email has one fixed format. |
| backup_log removed (physical) | Daily backup (NFR06) is a hosting-platform service, not application data. |
| Kept: QUOTE and PAYMENT as entities | A job can be re-quoted (UC-04 2a) and each approval must be kept; a payment is its own record with method and status. |
| Audit FKs reduced | Who changed a status lives in JOB_STATUS_HISTORY, so REPAIR_JOB no longer repeats intake and release employee FKs. |

Physical design decisions: ANSI SQL types, all valid in PostgreSQL, the chosen DBMS; CHECK constraints for the value lists (role, status, decision, payment method, PO status, transaction type) and for quantity_on_hand >= 0 (FR07); unique keys on ticket_number, appointment_id and employee email; composite key on store_part_stock (store_id, part_id). The logical ERD is in third normal form. It shows identifiers and keys only, and it leaves out three derived attributes that SAD 8e Appendix 5A removes at 3NF: a job’s current status (the latest JOB_STATUS_HISTORY row), a quote’s total (labor plus parts) and a part’s quantity on hand (the sum of its INVENTORY_TXN rows). The physical model stores all three as documented denormalizations, marked “derived” on the detail slides: repair_job.status and store_part_stock.quantity_on_hand make queues and stock checks instant, and quote.total_amount keeps an approved figure from drifting. The application writes each one in the same transaction as the row it summarizes. EMPLOYEE.StoreID is each employee’s home store; the Owner role sees both stores, and whether a Manager covers one store or both is to be confirmed with the owner. After the owner’s October 23 answers, repair_job.assigned_tech_id and appointment.technician_id may be empty until a job is assigned or claimed, device type and brand are optional, and repair_job.device_passcode holds the optional passcode, encrypted and shown only to authorized staff.

## 7. DFD and ERD alignment

Figure 7.1 Each store holds a fixed set of entities; the grid shows which processes create, read and update each store

### Table 7.1 Data store to entity matrix

| Store | Name | ERD entities held | Created / updated by | Read by |
|---|---|---|---|---|
| D1 | Customers & Devices | CUSTOMER, DEVICE | 1.0, 2.0 | 1.0, 2.0, 5.0, 6.0, 8.0 |
| D2 | Appointments | APPOINTMENT | 1.0, 2.0, 3.0 | 1.0, 2.0, 3.0 |
| D3 | Repair Jobs | REPAIR_JOB, JOB_STATUS_HISTORY, QUOTE, PAYMENT, JOB_PART | 2.0, 3.0, 4.0, 5.0, 6.0, 7.0 | 3.0, 4.0, 5.0, 6.0, 7.0, 8.0 |
| D4 | Parts Inventory | PART, STORE_PART_STOCK, INVENTORY_TXN | 4.0, 7.0, 9.0 | 3.0, 4.0, 7.0, 8.0, 9.0 |
| D5 | Purchase Orders | PURCHASE_ORDER, PO_LINE | 7.0 | 7.0 |
| D6 | Suppliers | SUPPLIER | 9.0 | 7.0, 9.0 |
| D7 | Staff & Stores | STORE, EMPLOYEE | 9.0 | 1.0, 2.0, 5.0, 8.0, 9.0 |

### Table 7.2 Requirement → use case → DFD process → store → entity

| Requirement | Use case | DFD processes | Stores | Entities / attributes |
|---|---|---|---|---|
| FR01 Appointments | UC-12 | 1.1–1.3; 2.4 (pre-fill) | D2, D1, D7 | APPOINTMENT |
| FR02 Intake and lookup | UC-01, UC-06, UC-13 | 2.1–2.4, 6.1 | D1, D3 | CUSTOMER, DEVICE, REPAIR_JOB |
| FR03 Claim ticket | UC-01 | 2.4, 2.5 | D3 | REPAIR_JOB.TicketNumber |
| FR04 Assignment | UC-01, UC-02 | 2.4, 3.1 | D2, D3, D7 | REPAIR_JOB.AssignedTechID, APPOINTMENT.TechnicianID, EMPLOYEE |
| FR05 Diagnosis and quote | UC-02, UC-03 | 3.2–3.5 | D3, D4 | REPAIR_JOB.DiagnosisNotes, QUOTE |
| FR06 Job status | UC-01–06, UC-10 | 2.4, 3.2–3.5, 4.3–4.5, 6.4, 7.5 | D3 | JOB_STATUS_HISTORY (stored as repair_job.status in the physical model) |
| FR07 Parts usage | UC-02, UC-04 | 3.3, 4.2–4.4 | D4, D3 | JOB_PART, STORE_PART_STOCK, INVENTORY_TXN |
| FR08 Pickup and payment | UC-06 | 6.1–6.4 | D3, D1 | PAYMENT, REPAIR_JOB release fields |
| FR09 Inventory | UC-07, UC-10 | 9.3, 7.5 | D4, D5 | PART, STORE_PART_STOCK, INVENTORY_TXN, PO_LINE |
| FR10 Purchasing | UC-07–UC-10 | 7.1–7.5, 9.4 | D5, D6, D4, D3 | PURCHASE_ORDER, PO_LINE, SUPPLIER, JOB_PART.PurchaseOrderID |
| FR11 Inventory import | UC-07 | 9.3 (logical) / 9.5 (physical) | D4 | PART, STORE_PART_STOCK, INVENTORY_TXN |
| FR12 Pickup notification | UC-05 | 5.1–5.5 | D3, D1, D7 | REPAIR_JOB email fields, STORE.EmailAddress |
| FR13 Dashboard | UC-13 | 8.0 | D1, D3, D4, D7 | read only |
| FR14 Users and locations | UC-11 | 9.1, 9.2 | D7 | EMPLOYEE.Role, STORE |
| NFR01 Authorization | All | every process (role check) | D7 | EMPLOYEE.Role |
| NFR02 Data accuracy | All | status and stock writes | D3, D4 | JOB_STATUS_HISTORY, INVENTORY_TXN |
| NFR05 Notification permission | UC-05 | 5.1, 5.4 | D7 | EMPLOYEE.Role |
| NFR06 Backup | — | not modelled | — | hosting platform backup (physical design note) |

### Appointment scheduling decision

In scope and optional. The Front Desk may book, reschedule or cancel an appointment (1.0, UC-12, FR01); a walk-in customer needs none. When one exists, 2.4 Create Repair Job pre-fills the customer and, if one was chosen, the technician from it and marks it Checked In; the device is recorded at check-in. Free times are the store’s business hours less booked appointments until the owner says how technician availability is set. A technician may also claim an unassigned appointment or job in 3.1 (owner, October 23). The ERD reflects this with APPOINTMENT 0..1 per REPAIR_JOB and an optional TechnicianID.

## 8. Changes from the Sprint 2 models

| Sprint 2 | Sprint 3 | Why |
|---|---|---|
| 1.0 Check In Device | 2.0 Register Repair Job | Names the system activity, not the counter task. |
| 1.1 Book Drop-off Appointment | 1.0 Schedule Appointment (1.1–1.3) | Appointments are a distinct, optional workflow (FR01, UC-12). |
| 1.2 Identify Customer | 2.1 Retrieve Customer Record + 2.2 Save Customer Record | "Identify" was a user goal; the system retrieves, creates or updates a record. |
| 2.0 Diagnose Device | 3.0 Record Diagnosis | The system records a diagnosis; the technician diagnoses. |
| 3.0 Repair Device | 4.0 Record Repair Work | The system records parts usage and completion. |
| 4.0 Notify Customer | 5.0 Send Pickup Notification | Names the single confirmed notification. |
| 5.0 Release Device | 6.0 Record Device Release | Staff release the device; the system records it. |
| 6.0 Replenish Parts | 7.0 Process Purchase Orders | Describes the PO life cycle the system processes. |
| D1–D7 (Sprint 2: Customers & Devices, Repair Jobs, Appointments, Parts Inventory, POs & Suppliers, Staff & Stores, Notification Log) | D1 Customers & Devices, D2 Appointments, D3 Repair Jobs, D4 Parts Inventory, D5 Purchase Orders, D6 Suppliers, D7 Staff & Stores | Each store now maps to one ERD subject area; suppliers split from orders; notifications fold into Repair Jobs. |

## Appendix A. Physical data dictionary

Every table in the physical ERD with its keys, SQL types and nullability; the logical name of each column is shown in brackets. CK marks a column limited to a checked value list. password_hash appears only in the physical model. As in SAD 8e Fig. 10-9, each column also gives its default, the value stored when a row is saved without one (identity means PostgreSQL generates the key), and its valid values: the checked list for a CK column or a range rule. The lists come from the catalog and Appendix B.

store   (logical STORE; data store D7)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | store_id (StoreID) | INTEGER | NOT NULL | identity |  |
| UK | store_name (StoreName) | VARCHAR(60) | NOT NULL |  |  |
|  | address (Address) | VARCHAR(200) | NOT NULL |  |  |
|  | phone (Phone) | VARCHAR(20) | NOT NULL |  |  |
|  | email_address (EmailAddress) | VARCHAR(120) | NOT NULL |  | email address format |
|  | business_hours (BusinessHours) | VARCHAR(120) | null |  |  |

employee   (logical EMPLOYEE; data store D7)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | employee_id (EmployeeID) | INTEGER | NOT NULL | identity |  |
| FK store | store_id (StoreID) | INTEGER | NOT NULL |  |  |
|  | first_name (FirstName) | VARCHAR(40) | NOT NULL |  |  |
|  | last_name (LastName) | VARCHAR(40) | NOT NULL |  |  |
| UK | email (Email) | VARCHAR(120) | NOT NULL |  | email address format |
| CK | role (Role) | VARCHAR(12) | NOT NULL |  | Owner, Manager, Technician, Front Desk (client-confirmed #1) |
|  | password_hash (PasswordHash) | VARCHAR(255) | NOT NULL |  |  |
|  | active_flag (ActiveFlag) | BOOLEAN | NOT NULL | TRUE |  |

customer   (logical CUSTOMER; data store D1)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | customer_id (CustomerID) | INTEGER | NOT NULL | identity |  |
|  | first_name (FirstName) | VARCHAR(40) | NOT NULL |  |  |
|  | last_name (LastName) | VARCHAR(40) | NOT NULL |  |  |
| IX | phone (Phone) | VARCHAR(20) | NOT NULL |  |  |
|  | email (Email) | VARCHAR(120) | null |  | email address format |
|  | created_at (CreatedAt) | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP |  |

device   (logical DEVICE; data store D1)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | device_id (DeviceID) | INTEGER | NOT NULL | identity |  |
| FK customer | customer_id (CustomerID) | INTEGER | NOT NULL |  |  |
|  | device_type (DeviceType) | VARCHAR(20) | null |  | optional (owner, Oct 23) |
|  | brand (Brand) | VARCHAR(40) | null |  | optional (owner, Oct 23) |
|  | model (Model) | VARCHAR(60) | NOT NULL |  |  |
| IX | serial_or_imei (SerialOrIMEI) | VARCHAR(40) | null |  |  |

appointment   (logical APPOINTMENT; data store D2)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | appointment_id (AppointmentID) | INTEGER | NOT NULL | identity |  |
| FK customer | customer_id (CustomerID) | INTEGER | NOT NULL |  |  |
| FK store | store_id (StoreID) | INTEGER | NOT NULL |  |  |
| FK employee | technician_id (TechnicianID) | INTEGER | null |  | empty until assigned or claimed (owner, Oct 23) |
|  | scheduled_at (ScheduledAt) | TIMESTAMP | NOT NULL |  |  |
| CK | appt_status (ApptStatus) | VARCHAR(12) | NOT NULL | 'Booked' | Booked, Checked In, Cancelled |

repair_job   (logical REPAIR_JOB; data store D3)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | repair_job_id (RepairJobID) | INTEGER | NOT NULL | identity |  |
| UK | ticket_number (TicketNumber) | VARCHAR(12) | NOT NULL | generated by 2.4 |  |
| FK device | device_id (DeviceID) | INTEGER | NOT NULL |  |  |
| FK store | store_id (StoreID) | INTEGER | NOT NULL |  |  |
| FK,UK appt. | appointment_id (AppointmentID) | INTEGER | null |  |  |
| FK employee | assigned_tech_id (AssignedTechID) | INTEGER | null |  | empty until assigned or claimed (owner, Oct 23) |
| CK | status (Status) | VARCHAR(20) | NOT NULL | 'Checked In' | Checked In, Diagnosing, Awaiting Approval, In Repair, Awaiting Parts, Ready for Pickup, Returned Unrepaired, Closed (FR06, client-confirmed #2) |
|  | reported_issue (ReportedIssue) | VARCHAR(500) | NOT NULL |  |  |
|  | device_passcode (DevicePasscode) | VARCHAR(255) | null |  | optional; stored encrypted; needed for camera replacements; authorized staff only (owner, Oct 23) |
|  | intake_condition (IntakeCondition) | VARCHAR(500) | null |  |  |
|  | diagnosis_notes (DiagnosisNotes) | VARCHAR(2000) | null |  |  |
|  | repair_notes (RepairNotes) | VARCHAR(2000) | null |  |  |
|  | check_in_at (CheckInAt) | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP |  |
|  | completed_at (CompletedAt) | TIMESTAMP | null |  |  |
|  | final_cost (FinalCost) | DECIMAL(10,2) | null |  | >= 0 |
|  | email_sent_at (EmailSentAt) | TIMESTAMP | null |  |  |
| FK employee | email_sent_by_id (EmailSentByID) | INTEGER | null |  |  |
| CK | email_status (EmailStatus) | VARCHAR(10) | null |  | Sent, Failed |
|  | picked_up_at (PickedUpAt) | TIMESTAMP | null |  |  |
|  | id_verified_flag (IDVerifiedFlag) | BOOLEAN | NOT NULL | FALSE | TRUE before picked_up_at is set (FR08) |
|  | signature_file (SignatureFile) | VARCHAR(255) | null |  |  |

job_status_history   (logical JOB_STATUS_HISTORY; data store D3)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | history_id (HistoryID) | BIGINT | NOT NULL | identity |  |
| FK repair_job | repair_job_id (RepairJobID) | INTEGER | NOT NULL |  |  |
| CK | status (Status) | VARCHAR(20) | NOT NULL |  | Checked In, Diagnosing, Awaiting Approval, In Repair, Awaiting Parts, Ready for Pickup, Returned Unrepaired, Closed (FR06, client-confirmed #2) |
| FK employee | changed_by_id (ChangedByID) | INTEGER | NOT NULL |  |  |
|  | changed_at (ChangedAt) | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP |  |
|  | note (Note) | VARCHAR(300) | null |  |  |

quote   (logical QUOTE; data store D3)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | quote_id (QuoteID) | INTEGER | NOT NULL | identity |  |
| FK repair_job | repair_job_id (RepairJobID) | INTEGER | NOT NULL |  |  |
|  | labor_amount (LaborAmount) | DECIMAL(10,2) | NOT NULL |  | >= 0 |
|  | parts_amount (PartsAmount) | DECIMAL(10,2) | NOT NULL |  | >= 0 |
|  | total_amount (TotalAmount) | DECIMAL(10,2) | NOT NULL |  | = labor_amount + parts_amount |
| CK | decision (Decision) | VARCHAR(10) | NOT NULL | 'Pending' | Pending, Approved, Declined |
|  | decision_at (DecisionAt) | TIMESTAMP | null |  |  |
| FK employee | decision_by_id (DecisionByID) | INTEGER | null |  |  |

payment   (logical PAYMENT; data store D3)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | payment_id (PaymentID) | INTEGER | NOT NULL | identity |  |
| FK repair_job | repair_job_id (RepairJobID) | INTEGER | NOT NULL |  |  |
|  | amount (Amount) | DECIMAL(10,2) | NOT NULL |  | > 0 |
| CK | method (Method) | VARCHAR(12) | NOT NULL |  | Card, Cash |
| CK | payment_status (PaymentStatus) | VARCHAR(10) | NOT NULL | 'Paid' | Paid (no other value defined yet) |
|  | paid_at (PaidAt) | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP |  |

job_part   (logical JOB_PART; data store D3)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | job_part_id (JobPartID) | INTEGER | NOT NULL | identity |  |
| FK repair_job | repair_job_id (RepairJobID) | INTEGER | NOT NULL |  |  |
| FK part | part_id (PartID) | INTEGER | NOT NULL |  |  |
| FK purch._order | purchase_order_id (PurchaseOrderID) | INTEGER | null |  |  |
|  | quantity (Quantity) | INTEGER | NOT NULL |  | > 0 |
| CK | part_status (PartStatus) | VARCHAR(8) | NOT NULL |  | Needed (a part request), Used |
|  | recorded_at (RecordedAt) | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP |  |

part   (logical PART; data store D4)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | part_id (PartID) | INTEGER | NOT NULL | identity |  |
| FK supplier | default_supplier_id (DefaultSupplierID) | INTEGER | null |  |  |
|  | part_name (PartName) | VARCHAR(100) | NOT NULL |  |  |
|  | device_model (DeviceModel) | VARCHAR(60) | null |  |  |
|  | grade (Grade) | VARCHAR(20) | null |  |  |
|  | standard_cost (StandardCost) | DECIMAL(10,2) | NOT NULL |  | >= 0 |
|  | active_flag (ActiveFlag) | BOOLEAN | NOT NULL | TRUE |  |

store_part_stock   (logical STORE_PART_STOCK; data store D4)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK,FK store | store_id (StoreID) | INTEGER | NOT NULL |  |  |
| PK,FK part | part_id (PartID) | INTEGER | NOT NULL |  |  |
| CK | quantity_on_hand (QuantityOnHand) | INTEGER | NOT NULL | 0 | >= 0 (FR07) |
|  | reorder_point (ReorderPoint) | INTEGER | NOT NULL | 0 | >= 0; set by the Manager (owner, Oct 23) |

inventory_txn   (logical INVENTORY_TXN; data store D4)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | inventory_txn_id (InventoryTxnID) | BIGINT | NOT NULL | identity |  |
| FK stock | store_id (StoreID) | INTEGER | NOT NULL |  |  |
| FK stock | part_id (PartID) | INTEGER | NOT NULL |  |  |
| FK employee | recorded_by_id (RecordedByID) | INTEGER | NOT NULL |  |  |
| CK | txn_type (TxnType) | VARCHAR(12) | NOT NULL |  | Used, Received, Adjustment, Import (9.5; proposed) |
|  | quantity_change (QuantityChange) | INTEGER | NOT NULL |  | not 0; negative for Used |
|  | reason (Reason) | VARCHAR(200) | null |  |  |
|  | txn_at (TxnAt) | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP |  |

supplier   (logical SUPPLIER; data store D6)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | supplier_id (SupplierID) | INTEGER | NOT NULL | identity |  |
| UK | supplier_name (SupplierName) | VARCHAR(100) | NOT NULL |  |  |
|  | contact_name (ContactName) | VARCHAR(80) | null |  |  |
|  | phone (Phone) | VARCHAR(20) | null |  |  |
|  | email (Email) | VARCHAR(120) | null |  | email address format |
|  | active_flag (ActiveFlag) | BOOLEAN | NOT NULL | TRUE |  |

purchase_order   (logical PURCHASE_ORDER; data store D5)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | purchase_order_id (PurchaseOrderID) | INTEGER | NOT NULL | identity |  |
| FK store | store_id (StoreID) | INTEGER | NOT NULL |  |  |
| FK supplier | supplier_id (SupplierID) | INTEGER | NOT NULL |  |  |
| FK employee | created_by_id (CreatedByID) | INTEGER | NOT NULL |  |  |
| FK employee | approved_by_id (ApprovedByID) | INTEGER | null |  | a Manager (owner, Oct 23) |
| CK | po_status (POStatus) | VARCHAR(20) | NOT NULL | 'Pending Approval' | Draft, Pending Approval, Approved, Ordered, Received |
|  | created_at (CreatedAt) | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP |  |
|  | approved_at (ApprovedAt) | TIMESTAMP | null |  |  |
|  | placed_at (PlacedAt) | TIMESTAMP | null |  |  |
|  | rejection_reason (RejectionReason) | VARCHAR(300) | null |  | required when returned to Draft |

po_line   (logical PO_LINE; data store D5)

| Key | Column (logical name) | Type | Null | Default | Valid values |
|---|---|---|---|---|---|
| PK | po_line_id (POLineID) | INTEGER | NOT NULL | identity |  |
| FK purch._order | purchase_order_id (PurchaseOrderID) | INTEGER | NOT NULL |  |  |
| FK part | part_id (PartID) | INTEGER | NOT NULL |  |  |
|  | quantity_ordered (QuantityOrdered) | INTEGER | NOT NULL |  | > 0 |
|  | quantity_received (QuantityReceived) | INTEGER | NOT NULL | 0 | 0 to quantity_ordered |
|  | unit_cost (UnitCost) | DECIMAL(10,2) | NOT NULL |  | >= 0 |

## Appendix B. Data flow dictionary

Every logical data flow on the context, Level 0 and Level 1 diagrams: 80 Level 0 flows and 91 more that appear only on a Level 1, grouped by process. Each has a unique noun name and lists the data it carries, using the logical ERD attribute names (SAD 8e Ch. 4). Shaded rows are Level 0 flows; the description of a composite Level 0 flow names the Level 1 flows it splits into. A Level 1 flow is either part of a Level 0 flow, which keeps the diagrams balanced, or internal to its process. A Level 1 flow with the same name as a Level 0 flow is the same flow and is listed once. Quantity on hand is derived from INVENTORY_TXN in the logical model.

1.0 Schedule Appointment   (17 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Appointment request | Front Desk Staff → 1.0 Schedule Appointment | Level 0 flow | Requested date and store; the customer's name, phone and email; the chosen time; or a reschedule or cancel request. Splits into Requested date, Booking request, and Appointment change request. |
| Appointment schedule | 1.0 Schedule Appointment → Front Desk Staff | Level 0 flow | Open time slots for the requested date and store, then the booking or change confirmation (AppointmentID, ScheduledAt, store). Splits into Available times, Booking confirmation and Change confirmation. |
| Store schedule | D7 Staff & Stores → 1.0 Schedule Appointment | Level 0 flow | The store's opening hours and its active technicians (STORE StoreID, BusinessHours; EMPLOYEE EmployeeID, FirstName, LastName, Role = Technician, ActiveFlag). Free times are the business hours less the booked appointments. |
| Returning customer record | D1 Customers & Devices → 1.0 Schedule Appointment | Level 0 flow | CUSTOMER rows matching the phone number entered (CustomerID, FirstName, LastName, Phone, Email). |
| New customer record | 1.0 Schedule Appointment → D1 Customers & Devices | Level 0 flow | A CUSTOMER created at booking when none matched (FirstName, LastName, Phone, Email, CreatedAt). |
| Appointment updates | 1.0 Schedule Appointment → D2 Appointments | Level 0 flow | New, rescheduled or cancelled APPOINTMENT rows. Splits into Appointment booking and Changed appointment. |
| Booked appointments | D2 Appointments → 1.0 Schedule Appointment | Level 0 flow | APPOINTMENT rows for the date and store, used to find free slots and the appointment to change (AppointmentID, ScheduledAt, TechnicianID, ApptStatus). |
| Requested date | Front Desk Staff → 1.1 List Available Times | Part of Appointment request | Requested date and StoreID. |
| Available times | 1.1 List Available Times → Front Desk Staff | Part of Appointment schedule | Free time slots for the date and store, each with an available technician. |
| Chosen time slot | 1.1 List Available Times → 1.2 Record Appointment Booking | Internal to 1.0 | ScheduledAt and StoreID of the slot the customer picked, with its TechnicianID if one was chosen. |
| Booking request | Front Desk Staff → 1.2 Record Appointment Booking | Part of Appointment request | Customer phone, FirstName, LastName and Email, with the confirmed slot. |
| Booking confirmation | 1.2 Record Appointment Booking → Front Desk Staff | Part of Appointment schedule | AppointmentID, ScheduledAt, store name and the customer's name. |
| Appointment booking | 1.2 Record Appointment Booking → D2 Appointments | Part of Appointment updates | New APPOINTMENT (CustomerID, StoreID, ScheduledAt, ApptStatus = Booked, and TechnicianID if one was chosen; otherwise a technician may claim it in 3.1). |
| Appointment change request | Front Desk Staff → 1.3 Record Appointment Change | Part of Appointment request | AppointmentID, with a new ScheduledAt or the instruction to cancel. |
| Change confirmation | 1.3 Record Appointment Change → Front Desk Staff | Part of Appointment schedule | AppointmentID with its new ScheduledAt, or notice that it is cancelled. |
| Appointment to change | D2 Appointments → 1.3 Record Appointment Change | Part of Booked appointments | The APPOINTMENT row being rescheduled or cancelled (AppointmentID, ScheduledAt, ApptStatus). |
| Changed appointment | 1.3 Record Appointment Change → D2 Appointments | Part of Appointment updates | Updated ScheduledAt, or ApptStatus = Cancelled. |

2.0 Register Repair Job   (22 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Check-in details | Front Desk Staff → 2.0 Register Repair Job | Level 0 flow | Customer phone; new or changed customer details; the DeviceID of a device already on file, or a new device's Model (DeviceType, Brand and SerialOrIMEI optional); ReportedIssue and IntakeCondition; an optional device passcode; the assigned technician, if one is chosen. Splits into Customer phone number, Customer details, Device intake details, Device passcode, and Technician assignment. |
| Customer search results | 2.0 Register Repair Job → Front Desk Staff | Level 0 flow | Customers matching the phone search (name, phone, email) and their devices, for the staff member to pick from. |
| Device tag | 2.0 Register Repair Job → Front Desk Staff | Level 0 flow | TicketNumber with the device Brand and Model, printed for the tag that stays with the device. |
| Claim ticket | 2.0 Register Repair Job → Customer | Level 0 flow | The customer's proof for pickup: TicketNumber, customer name, device, ReportedIssue, CheckInAt and the store's name, address and phone. |
| Matching customer records | D1 Customers & Devices → 2.0 Register Repair Job | Level 0 flow | CUSTOMER rows matching the phone number, with their DEVICE rows (CustomerID, FirstName, LastName, Phone, Email; DeviceID, Brand, Model). |
| Intake records | 2.0 Register Repair Job → D1 Customers & Devices | Level 0 flow | New or updated CUSTOMER and DEVICE rows. Splits into Customer record and Device record. |
| Today's appointment | D2 Appointments → 2.0 Register Repair Job | Level 0 flow | The APPOINTMENT booked for this customer today, if any (AppointmentID, TechnicianID, ApptStatus); pre-fills the job. |
| Checked-in appointment | 2.0 Register Repair Job → D2 Appointments | Level 0 flow | ApptStatus = Checked In for the appointment that became a job. |
| Technician roster | D7 Staff & Stores → 2.0 Register Repair Job | Level 0 flow | Active technicians at the store, for assigning the job (EmployeeID, FirstName, LastName). |
| Store contact details | D7 Staff & Stores → 2.0 Register Repair Job | Level 0 flow | STORE StoreName, Address and Phone, printed on the claim ticket. |
| New repair job | 2.0 Register Repair Job → D3 Repair Jobs | Level 0 flow | New REPAIR_JOB (TicketNumber, DeviceID, StoreID, AppointmentID, AssignedTechID if one was chosen, ReportedIssue, DevicePasscode if given, encrypted, IntakeCondition, CheckInAt) and its first JOB_STATUS_HISTORY row (Status = Checked In). |
| Customer phone number | Front Desk Staff → 2.1 Retrieve Customer Record | Part of Check-in details | Phone, the search key. |
| Selected customer | 2.1 Retrieve Customer Record → 2.2 Save Customer Record | Internal to 2.0 | CustomerID of the customer picked, or none for a new customer. |
| Customer details | Front Desk Staff → 2.2 Save Customer Record | Part of Check-in details | FirstName, LastName, Phone, Email. |
| Customer record | 2.2 Save Customer Record → D1 Customers & Devices | Part of Intake records | CUSTOMER row created or updated (CustomerID, FirstName, LastName, Phone, Email, CreatedAt). |
| Customer ID | 2.2 Save Customer Record → 2.3 Record Device Details | Internal to 2.0 | CustomerID with the customer's FirstName and LastName. |
| Device intake details | Front Desk Staff → 2.3 Record Device Details | Part of Check-in details | The DeviceID of a device already on file, picked from the customer search results, or a new device's DeviceType, Brand, Model and SerialOrIMEI; with this visit's IntakeCondition and ReportedIssue. When a customer brings several devices, 2.3 to 2.5 run once per device. |
| Device record | 2.3 Record Device Details → D1 Customers & Devices | Part of Intake records | A DEVICE row for a new device (DeviceID, CustomerID, DeviceType, Brand, Model, SerialOrIMEI); a device picked from the customer's records is reused, not written again. |
| Registered device | 2.3 Record Device Details → 2.4 Create Repair Job | Internal to 2.0 | CustomerID and customer name, DeviceID, Brand, Model, ReportedIssue and IntakeCondition. |
| Device passcode | Front Desk Staff → 2.4 Create Repair Job | Part of Check-in details | DevicePasscode, optional: needed only for a camera replacement; stored encrypted and shown only to authorized staff (owner, Oct 23). |
| Technician assignment | Front Desk Staff → 2.4 Create Repair Job | Part of Check-in details | EmployeeID of the technician chosen for the job, if any. Staff or a Manager assign by hand, or a technician claims the job later in 3.1 (owner, Oct 23). |
| Registered repair job | 2.4 Create Repair Job → 2.5 Print Claim Documents | Internal to 2.0 | RepairJobID, the generated TicketNumber, CheckInAt and StoreID, with the customer name, device Brand and Model and ReportedIssue passed on from 2.3: everything 2.5 prints except the store contact details. |

3.0 Record Diagnosis   (25 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Customer quote decision | Front Desk Staff → 3.0 Record Diagnosis | Level 0 flow | QuoteID and Decision (Approved or Declined), entered after the customer is called. |
| Quotes awaiting decision | 3.0 Record Diagnosis → Front Desk Staff | Level 0 flow | Quotes with no decision yet: TicketNumber, customer name and phone, LaborAmount, PartsAmount. |
| Diagnosis worklist | 3.0 Record Diagnosis → Repair Technician | Level 0 flow | The technician's job queue, with the unassigned jobs and appointments they may claim, and the stock of the parts needed. Splits into Job queue and Part availability. |
| Diagnosis details | Repair Technician → 3.0 Record Diagnosis | Level 0 flow | The job chosen or claimed, the DiagnosisNotes and the labor charge. Splits into Job to diagnose, Job claim, Diagnosis and Labor amount. |
| Diagnosis queue | D3 Repair Jobs → 3.0 Record Diagnosis | Level 0 flow | The technician's REPAIR_JOB rows, the unassigned ones at the store, and the QUOTE rows awaiting a decision. Splits into Own and unassigned jobs and Pending quote. |
| Diagnosis results | 3.0 Record Diagnosis → D3 Repair Jobs | Level 0 flow | The claim, DiagnosisNotes, parts needed, the new QUOTE, the recorded decision and each status change. Splits into Job claim record, Diagnosis findings, Needed part record, New quote, and Recorded quote decision. |
| Needed part details | D4 Parts Inventory → 3.0 Record Diagnosis | Level 0 flow | For each part the diagnosis needs: the PART StandardCost and the quantity on hand at this store (derived from INVENTORY_TXN), so the quote can be priced and a shortage seen before the customer decides. |
| Unassigned appointments | D2 Appointments → 3.0 Record Diagnosis | Level 0 flow | APPOINTMENT rows at the store with ApptStatus = Booked and no TechnicianID (AppointmentID, ScheduledAt, CustomerID), for a technician to claim (owner, Oct 23). |
| Appointment claim | 3.0 Record Diagnosis → D2 Appointments | Level 0 flow | TechnicianID set on the APPOINTMENT the technician claims. |
| Job to diagnose | Repair Technician → 3.1 Select Repair Job | Part of Diagnosis details | RepairJobID chosen from the queue. |
| Job claim | Repair Technician → 3.1 Select Repair Job | Part of Diagnosis details | RepairJobID or AppointmentID of an unassigned job or appointment the technician takes on. |
| Job queue | 3.1 Select Repair Job → Repair Technician | Part of Diagnosis worklist | The technician's own jobs, and the store's unassigned jobs and appointments, each with TicketNumber or ScheduledAt, device, ReportedIssue and current Status. |
| Own and unassigned jobs | D3 Repair Jobs → 3.1 Select Repair Job | Part of Diagnosis queue | REPAIR_JOB rows where AssignedTechID is this technician or empty, with the latest JOB_STATUS_HISTORY Status. |
| Job claim record | 3.1 Select Repair Job → D3 Repair Jobs | Part of Diagnosis results | AssignedTechID set to the claiming technician on REPAIR_JOB. |
| Job under diagnosis | 3.1 Select Repair Job → 3.2 Record Diagnosis Findings | Internal to 3.0 | RepairJobID of the job being diagnosed. |
| Diagnosis | Repair Technician → 3.2 Record Diagnosis Findings | Part of Diagnosis details | DiagnosisNotes and the parts the repair needs (PartID, Quantity). |
| Diagnosis findings | 3.2 Record Diagnosis Findings → D3 Repair Jobs | Part of Diagnosis results | DiagnosisNotes on REPAIR_JOB and a JOB_STATUS_HISTORY row (Status = Diagnosing, ChangedByID, ChangedAt). |
| Parts needed | 3.2 Record Diagnosis Findings → 3.3 Check Part Stock | Internal to 3.0 | RepairJobID, with PartID and Quantity for each part the repair needs. |
| Part availability | 3.3 Check Part Stock → Repair Technician | Part of Diagnosis worklist | For each part needed: PartName and quantity on hand at this store. |
| Needed part record | 3.3 Check Part Stock → D3 Repair Jobs | Part of Diagnosis results | JOB_PART row (PartID, Quantity, PartStatus = Needed) for a part not in stock, and Status = Awaiting Parts. |
| Part costs | 3.3 Check Part Stock → 3.4 Record Repair Quote | Internal to 3.0 | RepairJobID, with PartID, Quantity and StandardCost of every part needed, in stock or not, used to price the quote. |
| Labor amount | Repair Technician → 3.4 Record Repair Quote | Part of Diagnosis details | LaborAmount for the quote. |
| New quote | 3.4 Record Repair Quote → D3 Repair Jobs | Part of Diagnosis results | New QUOTE (RepairJobID, LaborAmount, PartsAmount, Decision = Pending) and Status = Awaiting Approval. |
| Pending quote | D3 Repair Jobs → 3.5 Record Quote Decision | Part of Diagnosis queue | QUOTE row awaiting a decision (QuoteID, RepairJobID, LaborAmount, PartsAmount). |
| Recorded quote decision | 3.5 Record Quote Decision → D3 Repair Jobs | Part of Diagnosis results | Decision, DecisionAt and DecisionByID on QUOTE, and the new Status (In Repair if approved, Returned Unrepaired if declined). |

4.0 Record Repair Work   (17 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Repair worklist | 4.0 Record Repair Work → Repair Technician | Level 0 flow | The job being repaired and the confirmation of any part requested. Splits into Repair job details and Part request confirmation. |
| Repair work details | Repair Technician → 4.0 Record Repair Work | Level 0 flow | The job chosen, each part and quantity used, any part requested, the RepairNotes and the completion. Splits into Job to repair, Parts used, Part request, and Repair completion. |
| Job in repair | D3 Repair Jobs → 4.0 Record Repair Work | Level 0 flow | REPAIR_JOB with Status = In Repair (RepairJobID, TicketNumber, device, DiagnosisNotes, approved QUOTE). |
| Repair work record | 4.0 Record Repair Work → D3 Repair Jobs | Level 0 flow | JOB_PART rows for parts used or requested, RepairNotes, CompletedAt and each status change. Splits into Parts-used record, Part request record, and Completed repair record. |
| On-hand stock | D4 Parts Inventory → 4.0 Record Repair Work | Level 0 flow | Quantity on hand of a part at this store (StoreID, PartID; derived from INVENTORY_TXN). |
| Stock deduction | 4.0 Record Repair Work → D4 Parts Inventory | Level 0 flow | INVENTORY_TXN row (StoreID, PartID, RecordedByID, TxnType = Used, QuantityChange negative, TxnAt). |
| Job to repair | Repair Technician → 4.1 Retrieve Repair Job | Part of Repair work details | RepairJobID chosen from the technician's In Repair jobs. |
| Repair job details | 4.1 Retrieve Repair Job → Repair Technician | Part of Repair worklist | TicketNumber, device, DiagnosisNotes and the approved parts and labor. |
| Parts used | Repair Technician → 4.2 Verify Part Stock | Part of Repair work details | PartID and Quantity used. |
| Verified parts used | 4.2 Verify Part Stock → 4.3 Record Parts Usage | Internal to 4.0 | PartID and Quantity confirmed as in stock. |
| Stock shortage | 4.2 Verify Part Stock → 4.4 Record Part Request | Internal to 4.0 | PartID, Quantity wanted and quantity on hand when stock is short. |
| Part request | Repair Technician → 4.4 Record Part Request | Part of Repair work details | PartID and Quantity the technician asks for. Technicians request parts; only a Manager orders them (owner, Oct 23). |
| Parts-used record | 4.3 Record Parts Usage → D3 Repair Jobs | Part of Repair work record | JOB_PART row (RepairJobID, PartID, Quantity, PartStatus = Used, RecordedAt). |
| Part request record | 4.4 Record Part Request → D3 Repair Jobs | Part of Repair work record | JOB_PART row (PartID, Quantity, PartStatus = Needed) for the part requested, and Status = Awaiting Parts; it appears in the Manager's low-stock alert (7.1). |
| Part request confirmation | 4.4 Record Part Request → Repair Technician | Part of Repair worklist | PartName, Quantity requested and the job now Awaiting Parts. |
| Repair completion | Repair Technician → 4.5 Record Repair Completion | Part of Repair work details | RepairNotes and the instruction that the repair is complete. |
| Completed repair record | 4.5 Record Repair Completion → D3 Repair Jobs | Part of Repair work record | RepairNotes and CompletedAt on REPAIR_JOB, and Status = Ready for Pickup. |

5.0 Send Pickup Notification   (20 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Notification approval | Front Desk Staff → 5.0 Send Pickup Notification | Level 0 flow | The ready job chosen, the FinalCost confirmed and the instruction to send the pickup notification. Splits into Job to notify, Final cost and Send instruction. |
| Pickup-ready job list | 5.0 Send Pickup Notification → Front Desk Staff | Level 0 flow | TicketNumber, customer name, device and CompletedAt for each job ready for pickup whose customer has not yet been notified. |
| Notification preview | 5.0 Send Pickup Notification → Front Desk Staff | Level 0 flow | The pickup notification exactly as it will be sent, for staff to check before sending. |
| Technician send request | Repair Technician → 5.0 Send Pickup Notification | Level 0 flow | RepairJobID of the completed job, the instruction to send and the technician's EmployeeID; it reaches 5.4 Send Email Message. The system fills in the customer's address, so the technician never sees it (owner, Oct 23). |
| Pickup notification | 5.0 Send Pickup Notification → Customer | Level 0 flow | Tells the customer the device is ready to collect: customer name, TicketNumber, device, FinalCost, store name, address and BusinessHours; sent once from the store's email account. |
| Ready job records | D3 Repair Jobs → 5.0 Send Pickup Notification | Level 0 flow | REPAIR_JOB rows with Status = Ready for Pickup and no EmailSentAt, and each approved QUOTE total. Splits into Ready jobs not yet notified and Approved quote total. |
| Notified job record | 5.0 Send Pickup Notification → D3 Repair Jobs | Level 0 flow | FinalCost, EmailSentAt, EmailSentByID and EmailStatus on REPAIR_JOB: the confirmed cost, and who sent the pickup notification and when. Splits into Confirmed final cost and Notification record. |
| Customer email address | D1 Customers & Devices → 5.0 Send Pickup Notification | Level 0 flow | CUSTOMER FirstName, LastName and Email. |
| Store pickup details | D7 Staff & Stores → 5.0 Send Pickup Notification | Level 0 flow | STORE StoreName, Address, Phone, BusinessHours and EmailAddress (the sending account). |
| Job to notify | Front Desk Staff → 5.1 List Jobs Ready for Pickup | Part of Notification approval | RepairJobID chosen from the ready list. |
| Ready jobs not yet notified | D3 Repair Jobs → 5.1 List Jobs Ready for Pickup | Part of Ready job records | REPAIR_JOB rows with Status = Ready for Pickup and EmailSentAt empty. |
| Job awaiting final cost | 5.1 List Jobs Ready for Pickup → 5.2 Confirm Final Cost | Internal to 5.0 | RepairJobID of the job chosen. |
| Final cost | Front Desk Staff → 5.2 Confirm Final Cost | Part of Notification approval | FinalCost entered or confirmed by staff. |
| Approved quote total | D3 Repair Jobs → 5.2 Confirm Final Cost | Part of Ready job records | LaborAmount + PartsAmount of the approved QUOTE, shown as the default final cost. |
| Confirmed final cost | 5.2 Confirm Final Cost → D3 Repair Jobs | Part of Notified job record | FinalCost written to REPAIR_JOB. |
| Confirmed ready job | 5.2 Confirm Final Cost → 5.3 Prepare Pickup Notification | Internal to 5.0 | RepairJobID, CustomerID, StoreID and FinalCost. |
| Prepared notification | 5.3 Prepare Pickup Notification → 5.4 Send Email Message | Internal to 5.0 | Recipient Email, subject and body. |
| Send instruction | Front Desk Staff → 5.4 Send Email Message | Part of Notification approval | Confirmation to send, with the sender's EmployeeID (Owner, Manager or Front Desk; a Technician sends through Technician send request). The email is never sent automatically (owner, Oct 23). |
| Send result | 5.4 Send Email Message → 5.5 Record Notification Result | Internal to 5.0 | Sent or failed, sender EmployeeID and time. |
| Notification record | 5.5 Record Notification Result → D3 Repair Jobs | Part of Notified job record | EmailSentAt, EmailSentByID and EmailStatus on REPAIR_JOB. |

6.0 Record Device Release   (15 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Pickup lookup | Front Desk Staff → 6.0 Record Device Release | Level 0 flow | TicketNumber, or the customer's phone number. |
| Pickup job summary | 6.0 Record Device Release → Front Desk Staff | Level 0 flow | TicketNumber, customer name, device, tag number and FinalCost (the amount due). |
| Release authorization | Front Desk Staff → 6.0 Record Device Release | Level 0 flow | What allows the device to leave: the photo-ID and tag check result, the payment amount and method, and the customer's signature. Splits into Identity check result, Payment details and Customer signature. |
| Release confirmation | 6.0 Record Device Release → Front Desk Staff | Level 0 flow | TicketNumber, PickedUpAt and amount paid. |
| Job awaiting pickup | D3 Repair Jobs → 6.0 Record Device Release | Level 0 flow | REPAIR_JOB ready for pickup (RepairJobID, TicketNumber, FinalCost, device) and any PAYMENT already recorded. |
| Pickup record | 6.0 Record Device Release → D3 Repair Jobs | Level 0 flow | The PAYMENT row (none when nothing is owed), PickedUpAt, IDVerifiedFlag, SignatureFile and Status = Closed. Splits into Payment record and Job release record. |
| Customer identity | D1 Customers & Devices → 6.0 Record Device Release | Level 0 flow | CUSTOMER FirstName and LastName, to compare with the photo ID. |
| Job for pickup | 6.1 Retrieve Pickup Job → 6.2 Record Identity Check | Internal to 6.0 | RepairJobID and the customer name to check. |
| Identity check result | Front Desk Staff → 6.2 Record Identity Check | Part of Release authorization | Whether the photo ID and the device tag matched (yes or no). The ID itself is not stored. |
| Verified job | 6.2 Record Identity Check → 6.3 Record Payment | Internal to 6.0 | RepairJobID with IDVerifiedFlag = true. |
| Payment details | Front Desk Staff → 6.3 Record Payment | Part of Release authorization | Amount and Method (card or cash) taken at the counter. |
| Payment record | 6.3 Record Payment → D3 Repair Jobs | Part of Pickup record | PAYMENT row (RepairJobID, Amount, Method, PaymentStatus = Paid, PaidAt). |
| Settled job | 6.3 Record Payment → 6.4 Close Repair Job | Internal to 6.0 | RepairJobID with payment recorded, or with nothing owed: a device that could not be repaired carries no diagnostic fee (owner, Oct 23). |
| Customer signature | Front Desk Staff → 6.4 Close Repair Job | Part of Release authorization | Signature captured on screen at release. |
| Job release record | 6.4 Close Repair Job → D3 Repair Jobs | Part of Pickup record | PickedUpAt, IDVerifiedFlag and SignatureFile on REPAIR_JOB, and Status = Closed. |

7.0 Process Purchase Orders   (26 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Purchase order request | Store Manager → 7.0 Process Purchase Orders | Level 0 flow | StoreID, SupplierID and lines (PartID, QuantityOrdered, UnitCost), with the jobs the order is for. |
| Placed order details | Store Manager → 7.0 Process Purchase Orders | Level 0 flow | PurchaseOrderID confirmed as placed with the supplier outside the system, with the date placed. |
| Received quantities | Store Manager → 7.0 Process Purchase Orders | Level 0 flow | POLineID and quantity received for each line. |
| Low-stock alert | 7.0 Process Purchase Orders → Store Manager | Level 0 flow | Raised automatically when a part reaches the reorder point the Manager sets: parts at or below their reorder point per store, and the open part requests with their jobs (owner, Oct 23). |
| Purchase order status | 7.0 Process Purchase Orders → Store Manager | Level 0 flow | PurchaseOrderID, supplier, POStatus and dates, including the Manager's approval or rejection. |
| Jobs released from Awaiting Parts | 7.0 Process Purchase Orders → Store Manager | Level 0 flow | TicketNumber and new Status of each job whose parts arrived. |
| Purchase order approval | Store Manager → 7.0 Process Purchase Orders | Level 0 flow | PurchaseOrderID and Approved or Rejected, with RejectionReason when rejected. A Manager approves every order; the Owner no longer does (owner, Oct 23). |
| Purchase orders awaiting approval | 7.0 Process Purchase Orders → Store Manager | Level 0 flow | PURCHASE_ORDERs with POStatus = Pending Approval: supplier, store, lines and total. |
| Jobs awaiting parts | D3 Repair Jobs → 7.0 Process Purchase Orders | Level 0 flow | REPAIR_JOBs with Status = Awaiting Parts and their JOB_PART rows with PartStatus = Needed (the part requests). Splits into Open part requests (to 7.1) and Jobs waiting on this order (to 7.5). |
| Awaiting-parts job updates | 7.0 Process Purchase Orders → D3 Repair Jobs | Level 0 flow | The PurchaseOrderID set on waiting JOB_PART rows, and the status change for jobs whose parts arrived. Splits into Jobs linked to the order and Released job status. |
| Stock levels | D4 Parts Inventory → 7.0 Process Purchase Orders | Level 0 flow | STORE_PART_STOCK rows at or below ReorderPoint (StoreID, PartID, quantity on hand, ReorderPoint). |
| Stock received | 7.0 Process Purchase Orders → D4 Parts Inventory | Level 0 flow | INVENTORY_TXN row (StoreID, PartID, RecordedByID, TxnType = Received, QuantityChange positive, TxnAt). |
| Open purchase orders | D5 Purchase Orders → 7.0 Process Purchase Orders | Level 0 flow | PURCHASE_ORDER and PO_LINE rows not yet received. Splits into Pending purchase orders, Approved purchase orders and Ordered purchase order lines. |
| Purchase order records | 7.0 Process Purchase Orders → D5 Purchase Orders | Level 0 flow | New and updated PURCHASE_ORDER and PO_LINE rows. Splits into Submitted purchase order, Purchase order decision record, Ordered status and Receipt status. |
| Supplier details | D6 Suppliers → 7.0 Process Purchase Orders | Level 0 flow | SUPPLIER rows for choosing the supplier (SupplierID, SupplierName, ContactName, Phone, Email). |
| Open part requests | D3 Repair Jobs → 7.1 List Parts to Order | Part of Jobs awaiting parts | JOB_PART rows with PartStatus = Needed and their REPAIR_JOBs: the technicians' part requests, for the Manager to order. |
| Submitted purchase order | 7.2 Record Purchase Order → D5 Purchase Orders | Part of Purchase order records | PURCHASE_ORDER (StoreID, SupplierID, CreatedByID, POStatus = Pending Approval, CreatedAt) and its PO_LINE rows. |
| Jobs linked to the order | 7.2 Record Purchase Order → D3 Repair Jobs | Part of Awaiting-parts job updates | PurchaseOrderID set on the waiting JOB_PART rows. |
| Pending purchase orders | D5 Purchase Orders → 7.3 Record Purchase Order Approval | Part of Open purchase orders | PURCHASE_ORDER rows with POStatus = Pending Approval, with their lines. |
| Purchase order decision record | 7.3 Record Purchase Order Approval → D5 Purchase Orders | Part of Purchase order records | POStatus = Approved, ApprovedByID and ApprovedAt; or POStatus = Draft with RejectionReason. |
| Approved purchase orders | D5 Purchase Orders → 7.4 Record Order Placement | Part of Open purchase orders | PURCHASE_ORDER rows with POStatus = Approved. |
| Ordered status | 7.4 Record Order Placement → D5 Purchase Orders | Part of Purchase order records | POStatus = Ordered and PlacedAt. |
| Ordered purchase order lines | D5 Purchase Orders → 7.5 Record Parts Receipt | Part of Open purchase orders | PO_LINE rows of ordered POs (POLineID, PartID, QuantityOrdered, QuantityReceived). |
| Receipt status | 7.5 Record Parts Receipt → D5 Purchase Orders | Part of Purchase order records | QuantityReceived on each PO_LINE, and POStatus = Received when all lines arrive. |
| Jobs waiting on this order | D3 Repair Jobs → 7.5 Record Parts Receipt | Part of Jobs awaiting parts | JOB_PART rows linked to the PO, with their RepairJobID. |
| Released job status | 7.5 Record Parts Receipt → D3 Repair Jobs | Part of Awaiting-parts job updates | JOB_STATUS_HISTORY row returning each released job to Diagnosing (quote not yet approved) or In Repair (approved). |

8.0 Report Repair Status   (8 flows; no Level 1 diagram)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Status enquiry | Front Desk Staff → 8.0 Report Repair Status | Level 0 flow | TicketNumber, or customer phone or name. |
| Job status | 8.0 Report Repair Status → Front Desk Staff | Level 0 flow | TicketNumber, device, current Status with its date, and FinalCost when known. |
| Overview request | Store Owner → 8.0 Report Repair Status | Level 0 flow | The store to show (or both), and any figure the Owner opens to see the jobs or parts behind it. |
| Repair and inventory overview | 8.0 Report Repair Status → Store Owner | Level 0 flow | Open jobs by Status for each store, jobs Awaiting Parts and parts at or below their reorder point; the jobs or parts behind a figure when the Owner opens it. |
| Job status history | D3 Repair Jobs → 8.0 Report Repair Status | Level 0 flow | REPAIR_JOB rows and their JOB_STATUS_HISTORY rows (Status, ChangedAt). |
| Customer lookup | D1 Customers & Devices → 8.0 Report Repair Status | Level 0 flow | CUSTOMER FirstName, LastName and Phone, to find a job by customer. |
| Stock summary | D4 Parts Inventory → 8.0 Report Repair Status | Level 0 flow | Quantity on hand and ReorderPoint by store and part. |
| Store list | D7 Staff & Stores → 8.0 Report Repair Status | Level 0 flow | StoreID and StoreName, to report by store. |

9.0 Maintain Shop Records   (21 flows)

| Data flow | From → To | Level | Data elements (description) |
|---|---|---|---|
| Staff, store, part and supplier changes | Store Manager → 9.0 Maintain Shop Records | Level 0 flow | New or changed staff accounts, store details, parts and stock adjustments, and suppliers. Splits into Staff account details, Store details, Part catalog changes, and Supplier changes. |
| Change confirmations | 9.0 Maintain Shop Records → Store Manager | Level 0 flow | Confirmation of each record saved, or the reason it was refused. Splits into Account confirmation, Store confirmation, Catalog confirmation and Supplier confirmation. |
| Current organization records | D7 Staff & Stores → 9.0 Maintain Shop Records | Level 0 flow | EMPLOYEE and STORE rows. Splits into Current staff accounts and Current store records. |
| Organization record updates | 9.0 Maintain Shop Records → D7 Staff & Stores | Level 0 flow | Created or changed EMPLOYEE and STORE rows. Splits into Staff account updates and Store updates. |
| Current part catalog | D4 Parts Inventory → 9.0 Maintain Shop Records | Level 0 flow | PART rows and STORE_PART_STOCK rows (ReorderPoint, quantity on hand). |
| Part catalog updates | 9.0 Maintain Shop Records → D4 Parts Inventory | Level 0 flow | Created or changed PART and STORE_PART_STOCK rows, and an INVENTORY_TXN row (TxnType = Adjustment, Reason) for each stock adjustment. |
| Current supplier records | D6 Suppliers → 9.0 Maintain Shop Records | Level 0 flow | SUPPLIER rows. Splits into Current supplier records (to 9.4) and Supplier list (to 9.3). |
| Supplier updates | 9.0 Maintain Shop Records → D6 Suppliers | Level 0 flow | Created or changed SUPPLIER rows (SupplierName, ContactName, Phone, Email, ActiveFlag). |
| Staff account details | Store Manager → 9.1 Maintain Staff Accounts | Part of Staff, store, part and supplier changes | FirstName, LastName, Email, Role, StoreID, ActiveFlag and an initial password. |
| Account confirmation | 9.1 Maintain Staff Accounts → Store Manager | Part of Change confirmations | Saved EMPLOYEE, or blocked when a Manager tries to create an Owner account. |
| Current staff accounts | D7 Staff & Stores → 9.1 Maintain Staff Accounts | Part of Current organization records | EMPLOYEE rows (EmployeeID, name, Email, Role, StoreID, ActiveFlag). |
| Staff account updates | 9.1 Maintain Staff Accounts → D7 Staff & Stores | Part of Organization record updates | Created or changed EMPLOYEE row. |
| Store details | Store Manager → 9.2 Maintain Store Details | Part of Staff, store, part and supplier changes | StoreName, Address, Phone, EmailAddress, BusinessHours. |
| Store confirmation | 9.2 Maintain Store Details → Store Manager | Part of Change confirmations | Saved STORE. |
| Current store records | D7 Staff & Stores → 9.2 Maintain Store Details | Part of Current organization records | STORE rows. |
| Store updates | 9.2 Maintain Store Details → D7 Staff & Stores | Part of Organization record updates | Created or changed STORE row. |
| Part catalog changes | Store Manager → 9.3 Maintain Parts Catalog | Part of Staff, store, part and supplier changes | PartName, DeviceModel, Grade, StandardCost, DefaultSupplierID, ActiveFlag; ReorderPoint per store; stock adjustments (StoreID, PartID, QuantityChange, Reason). |
| Catalog confirmation | 9.3 Maintain Parts Catalog → Store Manager | Part of Change confirmations | Saved PART, stock settings and adjustments. |
| Supplier list | D6 Suppliers → 9.3 Maintain Parts Catalog | Part of Current supplier records | SupplierID and SupplierName, to set a part's DefaultSupplierID. |
| Supplier changes | Store Manager → 9.4 Maintain Supplier Details | Part of Staff, store, part and supplier changes | SupplierName, ContactName, Phone, Email, ActiveFlag. |
| Supplier confirmation | 9.4 Maintain Supplier Details → Store Manager | Part of Change confirmations | Saved SUPPLIER. |
