<!-- Auto-generated from docs/sprint-3/Sprint 3 - Presentation.pptx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - Presentation

## Slide 1

Sprint 3 Presentation

**Speaker notes:**

Good afternoon. We are Team 4: Bara, Ehsanullah, Kyle and Leonard, and our client is Quick Phone Repair, a phone repair business with two stores. In Sprint 3 we moved from analysis into design. We will cover what changed since Sprint 2 and what we fixed after checking our work against the textbook, then walk through the physical data flow diagram and the physical ERD, show three interface prototypes, and finish with our limitations, risks, open decisions and next steps. We will ask for your feedback at the end.

## Slide 2

What changed since Sprint 2

Modified logical DFDs naming to reflect what the system does (Record Diagnosis, Record Repair Work, etc.)

Appointment scheduling is in scope, walk-ins skip it.

ERD simplified from 22 to 16 entities

DFDs and ERD aligned: 7 data stores hold the 16 entities, each entity in one data store.

Built physical DFDs & ERDs

Built three new prototypes

**Speaker notes:**

This slide answers the Sprint 2 feedback point by point. First, process names. The old diagrams named people's work, like Diagnose Device and Repair Device. Every process now names what the system does, such as Record Diagnosis and Record Repair Work. Second, appointments. Scheduling is in scope but optional: it has its own process, 1.0, and its own use case, UC-12, and walk-ins skip it. Third, the ERD was too hard to read, so we cut it from 22 entities to 16 and redrew every diagram at slide size. Fourth, the DFDs and the ERD now line up: seven data stores hold the sixteen entities, and each entity sits in exactly one store. We also added the context diagram you asked for, built the physical DFDs and physical ERD, and built three interface prototypes. And we revised the Sprint 1 System Request and Feasibility Analysis and recorded every change, with its cause, in the Change Log. On October 23 the owner answered our open questions, and the physical DFDs and ERD you will see already include those answers.

## Slide 3

What we fixed after the textbook review

Logical ERD in third normal form; derived values kept only in the physical ERD, marked

Every ERD relationship named both ways (employs / is employed by)

Every data flow has a unique name; each Level 1 DFD balances with Level 0

Data flow dictionary for all 171 logical flows (models document, Appendix B)

New use case UC-13 View Repair Status covers FR13 and DFD process 8.0

FR08 (release after payment) marked proposed: our decision, not client-confirmed

**Speaker notes:**

After building the models, we checked every Sprint 1 to 3 deliverable against the textbook, Dennis, Wixom and Roth, and against your feedback, and fixed what we found. The logical ERD is now in third normal form. Values we can calculate, such as a job's current status and a quote total, are left out of the logical model; the physical model stores them on purpose, for speed, and marks them as derived. Every relationship line on the ERD is now named in both directions, as in the textbook's physical ERD: a store employs employees, and an employee is employed by a store. On the DFDs, every data flow name is now unique, and each Level 1 diagram balances with its Level 0 parent. Appendix B of the models document describes all 171 logical flows and the data each one carries. We added use case UC-13, View Repair Status, because the status report requirement had a process but no use case. And we marked FR08, release only after payment, as proposed, because it is our decision, not something the client has confirmed yet.

## Slide 4

| Criterion | Weight | Custom: Django + PostgreSQL | Repair-shop subscription | Shared spreadsheet |
|---|---|---|---|---|
| Fit to the confirmed rules | 25 | 125 (5) | 75 (3) | 50 (2) |
| Access control and record integrity | 15 | 60 (4) | 75 (5) | 15 (1) |
| One view of both stores | 10 | 50 (5) | 50 (5) | 30 (3) |
| Annual cost to QuickPhone (est.) | 20 | 80 (4) | 40 (2) | 100 (5) |
| Support after December 9 | 15 | 30 (2) | 75 (5) | 45 (3) |
| Delivers the MOU deliverables | 10 | 50 (5) | 20 (2) | 30 (3) |
| Adoption by staff used to paper | 5 | 20 (4) | 15 (3) | 15 (3) |
| Total (of 500) | 100 | 415 | 350 | 285 |

Acquisition and technical approach

Hardware and software (Ch. 7)

Three-tier thin client–server, hosted offsite (Fig. 7-2)

Browser on the stores’ Lenovo ThinkPads; count to confirm (extra devices est. $0–$2,400)

Python 3.12, Django 5.2 LTS (security fixes to April 2028)

PostgreSQL 16+, managed, daily backup (NFR06)

Email through the store’s own mailbox (client #7); one label printer per store (est. $0–$400)

Hosting est. $0–$450 a year

What reverses it: a vendor demo proving full rule fit only narrows the gap (415 vs 400). If nobody will support the system after December 9 (support weighted 30, fit 10), the subscription wins, 380 vs 370. Scores 1–5 in brackets; SAD 8e Fig. 6-6.

**Speaker notes:**

Our acquisition and technical approach. Using the textbook’s weighted alternative matrix, we compared three routes: building a custom system, subscribing to a product made for repair shops, and a shared spreadsheet. The weights come from what the owner has told us matters. Fit to the seven rules the owner confirmed counts most, then the yearly cost, support after we hand over on December 9, and the deliverables in our MOU. The custom build scores 415 out of 500, the subscription 350 and the spreadsheet 285. Custom wins on fit and on the MOU. The subscription wins on support, but at about 140 to 150 dollars per store per month it costs more than twice our likely yearly estimate. The result is not safe: if the owner cannot name anyone to look after the system after December 9, the subscription comes out ahead, and we will tell the owner so. On the right is the technical approach: a three-tier web application in Python with the Django framework and a PostgreSQL database, hosted offsite and used through a browser on the stores’ Lenovo ThinkPads. Every cost here is an estimate from our feasibility study, and the choice stays provisional until the owner confirms it.

## Slide 5

_(no text — image only)_

**Speaker notes:**

This is part 1 of the physical Level 0 DFD, the front counter at booking and check-in: 1.0 Schedule Appointment and 2.0 Register Repair Job. Physical means it shows how each step is carried out. The band at the bottom of each process says how, for example Django and a label printer for check-in. Each data store lists the database tables it holds, and those are the same tables you will see on the ERD. The dashed red line is the human-machine boundary. As in the textbook, it goes around each person who uses the system’s screens, here the Front Desk. The Customer has no line, because they only receive the printed claim ticket and never use the screens. Each line is one data flow, and its name says how the data travels, as in the textbook's physical DFDs: an Input Form is a form staff fill in on screen, a Screen is what the system shows them, the Claim Ticket Printout comes off the label printer and goes to the Customer, and a PostgreSQL Record line reads or writes the tables of the store it touches. The other three Level 0 parts, the complete Level 0, every Level 1 diagram and the logical versions are in the models document, the DFD and ERD slide deck, and the physical DFD set PDF.

## Slide 6

Physical ERD

**Speaker notes:**

This is the physical ERD, detail 1 of 3: customers, devices, appointments, staff and stores. Each table shows its keys, data types and required columns, and the colored header names the DFD data store that holds it, so you can match it to the data flow diagrams. Each line is named both ways: the first name reads from the one side to the many side, the second reads back. A store employs employees and schedules appointments, a technician handles appointments, and a customer owns devices and books appointments; read back, an employee is employed by a store and an appointment is booked by a customer. The crow's foot marks give cardinality and modality, so a customer can have zero or many devices, and each device belongs to exactly one customer. An appointment's technician is now optional, because the owner says technicians may claim unassigned appointments. The note at the bottom is an assumption the owner must confirm: each employee has a home store, and we do not yet know whether a manager covers one store or both.

## Slide 7

_(no text — image only)_

**Speaker notes:**

Detail 2 is the repair job, the center of the system. A repair job tracks its status history, generates quotes, receives payment and uses parts. The status history always has at least one row, because every job starts as Checked In. Two columns are derived and stored on purpose, and they are marked: the current status, which is the latest history row, and the quote total, which is labor plus parts. We store them so the job queues load quickly and an approved quote cannot change afterwards; the logical ERD leaves them out to stay in third normal form. Columns such as who sent the pickup notification or who decided a quote point to the employee who did it. The owner told us on October 23 that a passcode is optional and needed only for camera repairs, so the job has an optional device passcode, stored encrypted, and the assigned technician can be empty until someone assigns the job or a technician claims it.

## Slide 8

_(no text — image only)_

**Speaker notes:**

Detail 3 covers parts, purchasing and suppliers. A part appears in each store's stock, and every change to that stock is logged as an inventory transaction: a part used, received or adjusted. Quantity on hand is the sum of those transactions; like the status on the last slide, the physical model also stores it so stock checks are instant. A supplier fulfills purchase orders and is the default source for parts. A purchase order contains its lines, and a part can appear on many order lines. Created-by and approved-by link each purchase order to the employees involved, which supports the owner's rule, confirmed on October 23, that a manager approves every purchase order before it is placed.

## Slide 9

INTERFACE 1 · FRONT DESK

Check In Device

Starts from a booked appointment or a walk-in, then searches by phone so a returning customer is not entered twice

Records device, condition and reported problem; a technician is optional (assigned by hand or claimed later)

Creates the job as Checked In and prints a matching claim ticket and device tag

Flags a customer with no email so staff call at completion (alternate flow 2a)

TRACES TO

Use case

UC-01 Check In Device

DFD process

2.0 Register Repair Job

Requirements

FR01 to FR04, FR06, NFR03

Data stores

D1, D2, D3, D7

Quick Phone Repair Management · Sprint 3 interface prototypes · Screens use sample data

**Speaker notes:**

Front Desk view for UC-01. Show how check-in can start from a booked appointment (FR01, FR02) or a walk-in. Phone search comes first so we do not create duplicate customers. The technician picker shows open jobs per tech to support FR04. The owner says assignment is by hand and optional, and technicians may claim jobs themselves, so this mockup will be updated. On save the job is created as Checked In and the claim ticket and device tag print with the same number (FR03). Mention the no-email flag, which covers alternate flow 2a.

## Slide 10

INTERFACE 2 · TECHNICIAN

Diagnose, Quote and Repair

Shows the technician’s jobs; unassigned jobs to claim will be added (owner, Oct 23)

Technician picks parts against live store stock and the quote totals automatically

An out-of-stock part moves the job to Awaiting Parts and sends a part request to the Manager

Repair view records parts used and deducts stock; customer contact and email are hidden from this role

TRACES TO

Use cases

UC-02, UC-04

DFD process

3.0 Record Diagnosis,4.0 Record Repair Work

Requirements

FR04 to FR07, NFR01, NFR02, NFR04

Data stores

D3, D4

Quick Phone Repair Management · Sprint 3 interface prototypes · Screens use sample data

**Speaker notes:**

Technician view for UC-02 and UC-04. The left list is the assigned job queue from FR04. The selected job is in diagnosis: the tech checks the parts needed, sees stock at this store, enters labor, and the system totals the quote before setting Awaiting Approval (FR05, FR07). Picking an out-of-stock part switches the job to Awaiting Parts. Once the customer approves, the same screen switches to the repair view where parts used are recorded and deducted, and entries that would take stock below zero are blocked (NFR02). Technicians never see customer contact details (NFR04). The owner now says a technician may click Send on the pickup notification, which reverses the September 21 rule, so we are confirming it before changing UC-05.

## Slide 11

INTERFACE 3 · MANAGER

Parts Inventory and Purchase Orders

Stock for each store, with low stock defined as at or below the reorder point

Add to PO builds a one-supplier draft and links the jobs waiting on those parts

Every purchase order needs a Manager’s approval before it can be received

Receiving updates stock, supports partial delivery and returns linked jobs to Diagnosing or In Repair

TRACES TO

Use cases

UC-07, UC-08, UC-10

DFD process

7.0 Process Purchase Orders,9.0 Maintain Shop Records

Requirements

FR06, FR09 to FR11, NFR01, NFR02

Data stores

D3, D4, D5, D6

Quick Phone Repair Management · Sprint 3 interface prototypes · Screens use sample data

**Speaker notes:**

Manager view for UC-07, UC-08 and UC-10, matching DFD processes 7.0 Process Purchase Orders and 9.0 Maintain Shop Records. The tiles and the Low status use the reorder point rule from UC-07, and Import CSV covers FR11. Add to PO starts a draft for one supplier and links jobs that are Awaiting Parts (UC-08 step 3). Submitting sets Pending Approval for a Manager (UC-09; the owner confirmed on October 23 that managers approve). The system also alerts the Manager when a part reaches the reorder point the Manager sets. Receiving is only allowed on an approved order, handles partial delivery, and moves linked jobs back to Diagnosing or In Repair (UC-10).

## Slide 12

Limitations, risks and decisions needed

Limitations

ThinkPads per store and connectivity unconfirmed

Use cases not yet walked through with the owner

Technology chosen provisionally; the owner’s support answer can reverse it

Prototype screenshots predate the owner’s Oct 23 answers

Risks

No one named to support the system after the December 9 handoff

Technician email: Oct 23 answer conflicts with Sept 21 rule

Staff may skip new check-in and release steps when the counter is busy

Models are AI-assisted; every member must be able to explain them

Decisions needed

Owner: may a Technician send the pickup email (Sept 21 said no)?

Owner: may a Manager approve their own purchase order?

Owner: does a Manager cover one store or both?

Professor: are nine Level 0 processes and the derived physical columns acceptable?

**Speaker notes:**

Now our reflection, starting with what is still open. Limitations: we know the stores use Lenovo ThinkPads but not how many, or how reliable the internet connection is, we have not yet walked the owner through the use cases step by step, the technology choice in our alternative matrix is provisional until the owner tells us who will support the system, and the prototype slides you just saw still cite the Sprint 2 process numbers. We will update them. Risks: the biggest is that nobody is named to support the system after we hand it over on December 9, which is also the largest unknown in the yearly cost. The owner's October 23 answers let a technician send the pickup email, which contradicts the September 21 rule, so we must confirm which holds. Staff may skip the new check-in and release steps on a busy day. And our models were built with AI help, so each of us has to be able to explain them. Decisions needed: the owner has to confirm whether a technician may send the pickup email, whether a manager may approve an order they created, and whether a manager covers one store or both. From you, we would like feedback on two modelling choices: keeping nine processes on Level 0, and storing derived columns in the physical ERD.

## Slide 13

Uncertainty and next steps

Uncertainty

Benefits are estimates: about 6 staff hours a week, $8,952 a year and a $17,100 three-year NPV (likely case)

They rest on assumed volumes and national wage rates until the owner gives real baselines

Django and PostgreSQL chosen provisionally; the subscription wins if nobody will support the system after December 9

Free appointment times assume store hours less bookings until the owner says how availability is set

Next steps

Owner walkthrough before November 2: use cases, the three interface alternatives, equipment and open rules

Carry the owner’s Oct 23 answers into the catalog and use cases; confirm the Technician email rule

Re-score the alternative matrix with the owner’s answers

Regenerate prototype screenshots for the Oct 23 answers

Team walkthrough of the DFDs and ERD; decide the pending AI log rows

Start the Sprint 4 build and specification

**Speaker notes:**

Uncertainty and next steps. Our benefit figures are estimates: about six staff hours a week, roughly 8,952 dollars a year, and a three-year net present value of about 17,100 dollars in the likely case. They rest on assumed repair volumes and national wage rates, and they will change once the owner gives us real numbers. The technology is chosen only provisionally: a custom Django and PostgreSQL web app scored highest in our alternative matrix, but if the owner cannot name anyone to support it after December 9, a repair-shop subscription comes out ahead. And free appointment times assume store hours minus existing bookings until the owner tells us how availability is really set. Next steps: we will walk the owner through the use cases, the three interface alternatives, the equipment and the open business rules before November 2. The owner answered most of the open rules on October 23 and our models already show those answers; we will carry them into the catalog and use cases, confirm the technician email rule and the manager question, and log each change. We will re-score the alternative matrix with the owner’s answers, regenerate the prototype screenshots, walk the whole team through the DFDs and ERD, and then start the Sprint 4 build and specification.

## Slide 14

Thank you

**Speaker notes:**

Thank you. To sum up: the models now answer your Sprint 2 feedback and match the textbook, and our main open items are the owner's decisions and the walkthrough before November 2. We would welcome your feedback on the nine-process Level 0 and the derived physical columns, and we are happy to take questions. Every AI contribution is in our AI Decision Log, and any of us can walk you through a model or a decision.
