# Project context

The facts and decisions every deliverable must agree with. Update this file when the client confirms something or the team decides something; cite the source and date. Last updated 2026-10-22 (start of Sprint 3).

## Client and scope

Quick Phone Repair & Designs, Raleigh, NC, repairs phones, tablets, laptops and game consoles at **two stores**. Owner and sponsor: Ashiqullah Pardisi. Today the shop runs on paper and memory, with **Lenovo ThinkPad computers (how many per store is unconfirmed; owner, Oct 23) and a card machine**; nothing else (printers, other devices, internet reliability, existing records) is confirmed, so staff devices are the most likely real cost. The problem: no shared view of repair jobs and parts, so customers call for status, jobs stall waiting on parts that were not reordered, and devices risk being lost or released to the wrong person.

The MOU deliverables, due **December 9, 2026**, are a working prototype, interface designs, a technical specification, and a training session with a written user manual. The Sprint 3 alternative matrix (Oct 23, SAD 8e Ch. 6–7) chose, **provisionally**, a custom web application in Python/Django 5.2 with one PostgreSQL database for both stores, hosted offsite as a three-tier thin client–server system. It scored 415 of 500 against 350 for a repair-shop subscription (RepairDesk and RepairShopr list about $140–150 per store per month, Oct 23) and 285 for a shared spreadsheet. **The result reverses if nobody will support the system after December 9**, so the owner's answer on support decides the route. Team members have used Python (Kyle, Oct 23; each member to confirm).

## Client-confirmed requirements (September 21 correspondence)

1. Four roles use the system: Owner, Manager, Technician, Front Desk. Customers and suppliers are external.
2. Workflow: intake → diagnosis → approval → repair → notification → payment → closure.
3. Parts are deducted from a store's stock automatically when a technician records them as used. **No reservation step.**
4. **Every purchase order needs the Owner's approval** (PO statuses: Draft, Pending Approval, Approved, Ordered, Received).
5. Customers are notified **by email only, once, when the repair is complete**. Other status emails and SMS are out of scope.
6. Owner, Manager and Front Desk may send the email; Technicians may not, and cannot see customer contact details.
7. The email goes from the store's own email account.

## Owner clarifications (October 23)

The owner answered eight open points. They supersede #4 above and conflict with #6:

1. Staff or the Technician click a button to send the pickup notification; it is never automatic. **This conflicts with #6** (Technicians may not send email). It is drawn in the physical DFDs and is still to confirm with the owner.
2. A **Manager** approves every purchase order. No Owner approval is needed, so #4 is superseded.
3. The system alerts staff automatically when stock reaches the minimum level. Technicians request parts in the system. Managers review the requests and order from outside suppliers (Amazon, eBay, MobileSentrix and others). Technicians never purchase, and nothing is ordered automatically.
4. Assignment is manual: Managers or authorized staff assign appointments, and technicians may assign themselves to available ones. There is no automatic assignment.
5. No diagnostic fee is charged when a device cannot be repaired.
6. Managers set and update each part's reorder point. A low-stock notice is raised automatically when stock reaches it.
7. Front desk records the customer's full name and phone, the device model and the issue. A passcode is optional and needed only for camera replacements; any passcode collected is stored securely and is visible only to authorized staff.
8. The stores use Lenovo ThinkPad computers only.

Applied (Oct 23) to the physical DFD and ERD PDFs, the DFD and ERD Models document (all images, Appendices A and B, now 171 flows), the DFD and ERD Slides deck and the Sprint 3 Presentation. Still to do: the catalog, the use cases, the prototype screenshots, the Owner Design Review Packet and the hardware/software specification. Physical DFD flows to and from people use "… Input Form" for a form a person fills in and "… Screen" for what the system shows them.

## Team decisions since then

- Drop-off appointments are **optional**; walk-ins need none (Sprint 2 feedback; UC-12, FR01).
- A device is released **only after payment is recorded**; no manager override. The system records the fact of payment (amount, method, status, time); it does not take payments.
- At release, staff tick an ID-checked flag; the ID number and type are never stored.
- Each store's stock is tracked separately; transfers between stores are out of scope.
- Job statuses (master list): Checked In, Diagnosing, Awaiting Approval, In Repair, Awaiting Parts, Ready for Pickup, Returned Unrepaired, Closed.
- Existing inventory can be imported from CSV at launch.

## Sprint 4 build decisions (Kyle, October 28)

Made while building the working system in `app/` (Prototype A, Curation Memo Oct 24). Each answers an open question for the build; those marked *owner* still need the owner's confirmation. The documents named in "Documents to update" below do not yet reflect them.

- Technicians **may** send the pickup notification (owner answer #1), without seeing the customer's address. Supersedes confirmation #6 and NFR05.
- Technicians **see customer phone and email** on every screen other roles do, because they check customers in (Kyle, Nov 2). Supersedes the rest of confirmation #6 and the Sprint 4 draft NFR04 (*owner*).
- The parts on a quote are stored in a new **QUOTE_LINE** table (D3: quote_id, part_id, quantity, unit_cost); ERD goes to 17 entities. JOB_PART "Needed" keeps its meaning of a part request.
- A declined quote sets Returned Unrepaired; Front Desk **may** record a fee, but none is required for release (*owner*).
- The passcode is visible to the assigned technician, Managers and the Owner (*owner*: who counts as "authorized staff").
- A Manager works in their **home store only**; only the Owner sees both stores (*owner*).
- A Manager **may** approve a purchase order they created (*owner*).
- PART gains a unique **sku** column, as Prototype A shows.
- PostgreSQL is installed locally for the build. SQLite is used only for automated tests.
- Placeholders still to confirm: store hours and 30-minute appointment slots (9:00–17:00).

## Documents to update after the Sprint 4 build

QUOTE_LINE and PART.sku in the logical and physical ERD and Appendix A; the QUOTE_LINE store reads and writes in DFD 3.0 (3.3 quote) and 4.0; NFR05 and UC-05 for Technician-sent email; UC-03 and UC-06 for the optional fee on a declined quote; NFR04 and UC-01 for passcode visibility; FR10 and UC-09 (Manager approves, self-approval allowed); FR13 and FR14 for store scope; the Prototype A screenshots (still show Owner approval and no passcode). Each change needs a Change Log row when the document was already submitted.

## Current models (Sprint 3, revision 2)

Requirements catalog: **14 functional (FR01–FR14) and 6 nonfunctional (NFR01–NFR06)**, nine client-confirmed (FR08 is proposed: its pickup step is confirmed, but release only after payment is a team decision); NFR05 = technicians cannot send email, NFR06 = daily backup. Use cases UC-01 to UC-13 (UC-09 Approve Purchase Order, UC-12 Schedule Appointment, UC-13 View Repair Status for FR13 and DFD 8.0). A booked appointment pre-fills the customer and technician, not the device; free times are store hours less booked appointments.

ERD: **16 entities in 7 DFD data stores**, each entity in exactly one store. The logical ERD is in 3NF with no derived attributes; the physical ERD stores repair_job.status, quote.total_amount and store_part_stock.quantity_on_hand as marked denormalizations (Oct 22). Assumption: EMPLOYEE.StoreID is a home store and the Owner sees both stores. D1 Customers & Devices (CUSTOMER, DEVICE); D2 Appointments; D3 Repair Jobs (REPAIR_JOB, JOB_STATUS_HISTORY, QUOTE, PAYMENT, JOB_PART); D4 Parts Inventory (PART, STORE_PART_STOCK, INVENTORY_TXN); D5 Purchase Orders (PURCHASE_ORDER, PO_LINE); D6 Suppliers; D7 Staff & Stores (STORE, EMPLOYEE).

DFD processes: 1.0 Schedule Appointment, 2.0 Register Repair Job, 3.0 Record Diagnosis, 4.0 Record Repair Work, 5.0 Send Pickup Notification, 6.0 Record Device Release, 7.0 Process Purchase Orders, 8.0 Report Repair Status, 9.0 Maintain Shop Records. Nine Level 0 processes is a deliberate choice, within SAD 8e's "seven to nine" (Ch. 4, p. 149); every Level 1 has three to seven. Physical flow names follow SAD 8e Figs. 9-2 and 9-4: "… Input Form", "… Output Form", "… Printout", "… Email", "… File" for people, and "DB Record: …" / "DB Record Update: …" for stores; one idea per name, with Level 0 groups split on the Level 1s (balancing table in the physical DFD PDF). All DFDs use right-angle lines; the slide view of Level 0 has four parts (Oct 22). Oct 23 validation pass: every Level 0 flow name says what the data is (vague groups such as "Check-in results" split into named flows), the claim ticket goes to the Customer, the Owner sends an overview request to 8.0, and the customer email is called the **pickup notification** everywhere (FR12, UC-05 Send Pickup Notification, DFD 5.0). Viewpoint: an external entity is whoever gives data to the system or receives data from it. Oct 23 physical relabel (SAD 8e Ch. 9 Steps 1–2, Figs. 9-2 and 9-4): stores are "PostgreSQL: …", store flows "PostgreSQL Record: …" / "PostgreSQL Record Update: …", process bands name Django. The human–machine boundary is a dashed line around each person who uses the system's screens (Front Desk with the manual steps 6.5 and 6.6, Technician, Manager, Owner). The Customer has none, because they only receive a printout and an email, like the Customer Service Department in Fig. 9-2. DEVICE stays a table in D1: storage is optimized table by table (Ch. 10), so a separate store would save nothing.

## Estimates (all preliminary, pending the owner's own figures)

About 6 staff hours a week saved (~315 hrs/yr, ~$8,952/yr at BLS May 2025 national wage rates). Cost ranges low / likely / high: one-time $100 / $1,550 / $5,350; annual $80 / $1,460 / $3,765. Likely case: three-year NPV about $17,100, payback about 2.5 months. The 104 technician hours recovered could also fund ~100 more repairs (~$12,000 at an assumed $120 average repair). That is the same hours valued a second way and must never be added to the savings figure. Call and job volumes are analyst assumptions.

## Open questions for the client

- Raised by the Oct 23 answers: does the Technician's right to send the pickup email override confirmation #6 and NFR05? May a Manager approve a purchase order they created? Who counts as "authorized staff" (for assignment and for seeing passcodes)? When does the system learn that a repair is a camera replacement? Should intake still collect the customer's email address, which the pickup notification needs? Can a technician request a part that is not for a job? How many ThinkPads does each store have?
- Does the customer sign at pickup (FR08)? How is technician availability set, and who may reschedule (FR01)? Is there a fee when the customer declines a quote (the Oct 23 answer covers only unrepairable devices)? Does a Manager cover one store or both?
- Equipment, connectivity and records inventory; who supports the system after the December 9 handoff (top organizational risk, and the answer that decides custom build vs subscription in the alternative matrix); a vendor demo of whether a subscription product enforces Owner approval of every PO and hides contact details from technicians.
- A walkthrough of every use case with the owner.

## Known inconsistencies to fix

- **Two Sprint 2 catalog versions.** The OneDrive copy in `docs/sprint-2/` is the September 25 draft: 5 NFRs, an "NRF06" typo, and FR07 still describes part reservation. The October 8 rebuild (revised Oct 19, in `docs/sprint-3/drafts/`) is current. The Sprint 2 use cases also still reserve parts (UC-02, UC-03).
- **Sprint 2 ERD** (24 entities, including REPAIR_APPROVAL and QuantityReserved) is superseded by the 16-entity model in the Sprint 3 drafts.
- **Project name** varies: "Quick Phone Repair Management System" (MOU, Sprint 1 System Request, catalog) vs "QuickPhone Repair Tracking System" (revised System Requests). Agree on one before the technical specification.
- `Quick Phone Sprint 3 Prototypes.pptx` is now the 12-slide, three-alternative deck (A Workspace, B Guided Counter, C Operations Board). Its trace panels and the presentation's were re-traced to the rev 2 DFDs, Table 7.1 stores, the catalog and the use cases on Oct 23; traces cite Level 0 flow names. The screenshots still need regenerating: the Manager screens say "Submit/Send to Owner for approval" (a Manager approves since Oct 23), check-in has no optional passcode, and the appointment screens show a device and problem although an appointment holds no device (UC-12). The presentation's older Technician screenshot still says checked parts are reserved, which contradicts confirmation #3. Slide 7's notes mention test results, which no use case or DFD flow records.
- Feasibility v2.2 section 3.10 puts a subscription at $1,200–$2,400 a year; the Oct 23 list prices are about $3,400–$3,600 a year for two stores. Update 3.10 to match the alternative matrix.
- The Sprint 3 Change Log's file table refers to Kyle's local working folders (`deliverables/...`); in this repo those files are in `docs/sprint-3/drafts/`.
