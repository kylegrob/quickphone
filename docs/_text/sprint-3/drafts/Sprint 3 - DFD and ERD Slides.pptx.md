<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - DFD and ERD Slides.pptx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - DFD and ERD Slides

## Slide 1

Quick Phone Repair Management System

Sprint 3 data flow diagrams and entity relationship diagrams

MIS 4173 · Team 4: Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann

## Slide 2

What changed after the Sprint 2 feedback

Context diagram added, logical and physical.

Every process is named for what the system does: Record Diagnosis, Record Repair Work, Retrieve Customer Record…

No repeated symbols: every entity and data store appears once per diagram.

Appointment scheduling is in scope and optional: process 1.0, use case UC-12; walk-ins skip it.

ERD simplified from 22 to 16 entities and drawn for slides: an overview plus three readable detail slides.

DFDs and ERD aligned: 7 data stores hold the 16 entities, each entity in exactly one store (alignment slide).

**Speaker notes:**

Walk the instructor through each feedback point and where it is answered. The alignment slide is the direct answer to the DFD/ERD consistency point.

## Slide 3

Logical models

What the system does and stores, independent of technology

## Slide 4

_(no text — image only)_

**Speaker notes:**

Context diagram: the system as one process and the five external entities. These flows match Level 0 exactly. An entity is whoever gives data to the system or gets data from it: staff enter what customers tell them, and the Customer receives the claim ticket and the pickup notification directly.

## Slide 5

_(no text — image only)_

**Speaker notes:**

Level 0 is shown in four parts so every flow name is readable. Part 1: booking and check-in, processes 1.0 and 2.0. The complete Level 0 is in the appendix and the PDF.

## Slide 6

_(no text — image only)_

**Speaker notes:**

Part 2: the repair bench, processes 3.0 and 4.0. Technicians claim unassigned jobs and appointments (D2) and request parts here.

## Slide 7

_(no text — image only)_

**Speaker notes:**

Part 3: pickup notification and release, processes 5.0 and 6.0. 5.0 sends the one pickup notification email from the store account; 6.0 releases a device only after payment is recorded, or when nothing is owed for a device that could not be repaired. A Technician may also send the notification (owner, Oct 23).

## Slide 8

_(no text — image only)_

**Speaker notes:**

Part 4: back office and reporting, processes 7.0, 8.0 and 9.0. 8.0 is read-only and is not decomposed; UC-13 View Repair Status covers it. The Owner asks for the repair and inventory overview with an overview request.

## Slide 9

_(no text — image only)_

**Speaker notes:**

Optional appointment booking. 2.0 pre-fills a job from a booked appointment; walk-ins need none. The technician is optional: a technician may claim an unassigned appointment in 3.1 (owner, Oct 23).

## Slide 10

_(no text — image only)_

**Speaker notes:**

"Identify Customer" became Retrieve Customer Record and Save Customer Record, both system actions: 2.1 finds a returning customer, 2.2 creates a new one or updates the one found. 2.5 prints the claim ticket for the Customer and the device tag for the Front Desk, with the store's contact details on the ticket. 2.4 takes an optional device passcode, needed only for camera repairs, and an optional technician (owner, Oct 23).

## Slide 11

_(no text — image only)_

**Speaker notes:**

3.1 lists the technician's jobs and the unassigned jobs and appointments they may claim (owner, Oct 23). Every quote goes to Awaiting Approval; no repair starts until 3.5 records the customer decision.

## Slide 12

_(no text — image only)_

**Speaker notes:**

Recording a part as used deducts stock automatically (client-confirmed); there is no reservation. A technician requests a missing part in 4.4; only a Manager orders it (owner, Oct 23).

## Slide 13

_(no text — image only)_

**Speaker notes:**

One pickup notification email from the store account, sent only when someone clicks Send: Owner, Manager or Front Desk, or the Technician who finished the repair (owner, Oct 23; to confirm against the September 21 rule). The system fills in the address, so the Technician never sees it.

## Slide 14

_(no text — image only)_

**Speaker notes:**

A device is released only after payment is recorded, unless nothing is owed: a device that could not be repaired carries no diagnostic fee (owner, Oct 23). Only the fact of the ID check is stored.

## Slide 15

_(no text — image only)_

**Speaker notes:**

A Manager approves every purchase order before it is placed; the Owner no longer does (owner, Oct 23). 7.1 alerts the Manager when a part reaches its reorder point and lists the technicians' part requests; nothing is ordered automatically.

## Slide 16

_(no text — image only)_

**Speaker notes:**

Each master-data store has a process that creates and changes it.

## Slide 17

_(no text — image only)_

**Speaker notes:**

Each dashed box is a DFD data store, and the entities inside it are exactly what that store holds. This is how the ERD and DFDs line up.

## Slide 18

_(no text — image only)_

**Speaker notes:**

Detail 1: customers, devices, appointments, staff and stores. An appointment's technician is optional, and device type and brand are optional (owner, Oct 23).

## Slide 19

_(no text — image only)_

**Speaker notes:**

Detail 2: the repair job and what hangs off it: status history, quotes, payment and parts. The logical model leaves out the current status and the quote total because both are derived, which keeps it in 3NF. The assigned technician may be empty until someone assigns or claims the job, and the optional device passcode is stored encrypted (owner, Oct 23).

## Slide 20

_(no text — image only)_

**Speaker notes:**

Detail 3: parts inventory, purchase orders and suppliers.

## Slide 21

_(no text — image only)_

**Speaker notes:**

Answers feedback point 7 directly: 16 entities in 7 stores, each exactly once, and every store is created and read by some process.

## Slide 22

Physical models

How the design is implemented: Django (Python) web app and one PostgreSQL database, chosen provisionally in the alternative matrix

## Slide 23

_(no text — image only)_

**Speaker notes:**

Physical context: the same boundary and entities, with every flow named for its medium: input forms, screens, the claim ticket (to the Customer), device tag and release receipt printouts, the pickup notification email, and the inventory import file and error report. Each line is one flow and matches a Level 0 flow exactly.

## Slide 24

_(no text — image only)_

**Speaker notes:**

Each process shows how it is implemented; stores show their table names; the dashed red lines are the human–machine boundary, drawn around each person who uses the system’s screens (SAD 8e Figs. 9-2, 9-4); the Customer has none because they only receive a printout and an email. Flow names state their medium, as in the textbook’s physical DFDs (SAD 8e Figs. 9-2, 9-4): Input Form (a form a person fills in), the plain data name (what the system shows a person; lists end in “List”), Printout, Email, File, and PostgreSQL Record or PostgreSQL Record Update for rows read from or written to a store.

## Slide 25

_(no text — image only)_

## Slide 26

_(no text — image only)_

## Slide 27

_(no text — image only)_

**Speaker notes:**

Part 4: back office and reporting. Purchase orders, the Manager’s approval queue and low-stock alert, the Owner’s status dashboard and the master records.

## Slide 28

_(no text — image only)_

## Slide 29

_(no text — image only)_

## Slide 30

_(no text — image only)_

## Slide 31

_(no text — image only)_

## Slide 32

_(no text — image only)_

## Slide 33

_(no text — image only)_

**Speaker notes:**

The photo-ID check and taking payment stay manual (6.5, 6.6); the card machine is not linked to the system.

## Slide 34

_(no text — image only)_

## Slide 35

_(no text — image only)_

**Speaker notes:**

9.5 Import Inventory File is the one-time CSV load of starting stock (FR11).

## Slide 36

_(no text — image only)_

**Speaker notes:**

Physical ERD: 16 tables, same structure, plus SQL types, checked value lists and three derived columns stored for speed (status, total_amount, quantity_on_hand), each marked on the detail slides.

## Slide 37

_(no text — image only)_

## Slide 38

_(no text — image only)_

## Slide 39

_(no text — image only)_

## Slide 40

Appendix

Complete Level 0 diagrams (zoom in, or open the PDF)

## Slide 41

_(no text — image only)_

**Speaker notes:**

All nine processes on one diagram for reference. Nine is within the textbook’s seven-to-nine limit (SAD 8e Ch. 4, p. 149). For presenting, use the four Level 0 parts.

## Slide 42

_(no text — image only)_
