<!-- Auto-generated from docs/sprint-3/Quick Phone Sprint 3 Prototypes.pptx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Quick Phone Sprint 3 Prototypes

## Slide 1

Book Appointments · Front Desk

PROTOTYPE A · WORKSPACE · 1 OF 4

Pick a date, time slot and technician

Full slots and booked technicians are blocked

Reschedule updates the same appointment

TRACES TO SPRINT 3 MODELS

Use case

UC-12 Schedule Appointment

DFD process

1.0 Schedule Appointment

Requirements

FR01, NFR01, NFR02

Data stores

D1, D2, D7

Inputs

Appointment request

Outputs

Appointment schedule

**Speaker notes:**

Prototype A, Workspace: a desktop web app with forms and job details side by side. Best for staff at a desk computer who want everything about one job on one screen. Trade-off: it needs a computer at the counter and the bench, and pages are denser to scan. This slide covers FR01: Front Desk books or reschedules a drop-off appointment and selects an available technician. Here Maria Santos is being moved to 1:30 PM. The 11:00 AM slot is full, and Sam is already booked at 1:30, so the system blocks saving until Front Desk picks Jordan or another time. Appointments are stored in D2 Appointments, and the screen carries the Appointment request and Appointment schedule flows of DFD process 1.0 Schedule Appointment (UC-12).

## Slide 2

Check In Device · Front Desk

PROTOTYPE A · WORKSPACE · 2 OF 4

Starts from a booked appointment or a walk-in

Phone search prevents duplicate customers

Ticket and device tag share one job number

TRACES TO SPRINT 3 MODELS

Use case

UC-01 Check In Device

DFD process

2.0 Register Repair Job

Requirements

FR01 to FR04, FR06, NFR03

Data stores

D1, D2, D3, D7

Inputs

Check-in details

Outputs

Customer search results,claim ticket, device tag

**Speaker notes:**

Prototype A, Workspace: a desktop web app with forms and job details side by side. Best for staff at a desk computer who want everything about one job on one screen. Trade-off: it needs a computer at the counter and the bench, and pages are denser to scan. This screen covers UC-01. Check-in starts from a booked appointment (FR01) or a walk-in found by phone search (FR02), the technician is assigned (FR04), and the claim ticket and device tag print with the same number (FR03). Booking and rescheduling appointments (FR01) is on the previous slide.

## Slide 3

Diagnose, Quote and Repair · Technician

PROTOTYPE A · WORKSPACE · 3 OF 4

Shows only jobs assigned to this technician

Quote totals from parts and labor as you go

Stock comes off only when parts are used

TRACES TO SPRINT 3 MODELS

Use cases

UC-02, UC-04

DFD process

3.0 Record Diagnosis,4.0 Record Repair Work

Requirements

FR04 to FR07, NFR01, NFR02, NFR04

Data stores

D3, D4

Inputs

Diagnosis details, repair work details

Outputs

Diagnosis worklist, repair worklist

**Speaker notes:**

Technician screen for UC-02 and UC-04. The job list is the assigned queue from FR04. Diagnosis, parts and labor build the quote, which moves the job to Awaiting Approval. An out-of-stock part sets Awaiting Parts. After approval the same screen switches to recording parts used, and stock is deducted only then, as the client confirmed. Customer contact details and email are hidden from technicians (NFR04).

## Slide 4

Inventory and Purchase Orders · Manager

PROTOTYPE A · WORKSPACE · 4 OF 4

Low means at or below the reorder point

One supplier per PO, linked to waiting jobs

A Manager approves every PO before receiving

TRACES TO SPRINT 3 MODELS

Use cases

UC-07, UC-08, UC-10

DFD process

7.0 Process Purchase Orders,9.0 Maintain Shop Records

Requirements

FR06, FR09 to FR11, NFR01, NFR02

Data stores

D3, D4, D5, D6

Inputs

Purchase order request, received quantities, part catalog changes

Outputs

Low-stock alert, purchase order status, jobs released from Awaiting Parts

**Speaker notes:**

Manager screen for UC-07, UC-08 and UC-10, following DFD processes 7.0 Process Purchase Orders and 9.0 Maintain Shop Records. Stock is per store, Import CSV covers FR11, and Add to PO builds a one-supplier draft linked to jobs Awaiting Parts. Submitting sets it to Pending Approval for a Manager, who the owner confirmed on October 23 must approve every PO. Receiving is allowed only on approved orders, handles partial delivery and returns linked jobs to Diagnosing or In Repair (UC-10).

## Slide 5

Book Appointments · Front Desk

PROTOTYPE B · GUIDED COUNTER · 1 OF 4

Dates on the left, large time tiles on the right

Full slots and booked technicians are blocked

Change updates the same appointment

TRACES TO SPRINT 3 MODELS

Use case

UC-12 Schedule Appointment

DFD process

1.0 Schedule Appointment

Requirements

FR01, NFR01, NFR02

Data stores

D1, D2, D7

Inputs

Appointment request

Outputs

Appointment schedule

**Speaker notes:**

Prototype B, Guided Counter: a tablet app that guides staff through one task at a time, with large touch targets and a font chosen for legibility, so it is the strongest accessibility option. Best for new or less technical staff and touch use at the counter and bench. Trade-off: more taps per job and less overview of the whole shop. This slide covers FR01. Front Desk switches to Appointments, picks a date on the left, then taps a time and an available technician. Full slots and booked technicians cannot be chosen, which keeps the schedule free of double bookings (NFR02).

## Slide 6

Check-in Wizard · Front Desk

PROTOTYPE B · GUIDED COUNTER · 2 OF 4

Four steps, one question per screen

Large tiles and chips instead of typing

Review step shows the ticket before printing

TRACES TO SPRINT 3 MODELS

Use case

UC-01 Check In Device

DFD process

2.0 Register Repair Job

Requirements

FR01 to FR04, FR06, NFR03

Data stores

D1, D2, D3, D7

Inputs

Check-in details

Outputs

Customer search results,claim ticket, device tag

**Speaker notes:**

Prototype B, Guided Counter: a tablet app that guides staff through one task at a time, with large touch targets and a font chosen for legibility, so it is the strongest accessibility option. Best for new or less technical staff and touch use at the counter and bench. Trade-off: more taps per job and less overview of the whole shop. The wizard collects the same UC-01 fields as the other prototypes: customer, device and problem, technician, then review and print.

## Slide 7

Bench · Technician

PROTOTYPE B · GUIDED COUNTER · 3 OF 4

Tap part tiles to build the quote

Plus and minus buttons for labor and parts

Out-of-stock pick sets Awaiting Parts

TRACES TO SPRINT 3 MODELS

Use cases

UC-02, UC-04

DFD process

3.0 Record Diagnosis,4.0 Record Repair Work

Requirements

FR04 to FR07, NFR01, NFR02, NFR04

Data stores

D3, D4

Inputs

Diagnosis details, repair work details

Outputs

Diagnosis worklist, repair worklist

**Speaker notes:**

Technician bench for UC-02 and UC-04. Job chips across the top replace the job list. The technician taps part tiles that show stock at this store, sets labor with plus and minus buttons, and sends the quote. In repair mode, parts used are counted with the same buttons and test results are large toggles. Stock is deducted only when parts are recorded as used, and customer contact details stay hidden.

## Slide 8

Stock and Orders · Manager

PROTOTYPE B · GUIDED COUNTER · 4 OF 4

Part cards show stock and reorder point

Add to order fills a one-supplier cart

Receive view handles partial deliveries

TRACES TO SPRINT 3 MODELS

Use cases

UC-07, UC-08, UC-10

DFD process

7.0 Process Purchase Orders,9.0 Maintain Shop Records

Requirements

FR06, FR09 to FR11, NFR01, NFR02

Data stores

D3, D4, D5, D6

Inputs

Purchase order request, received quantities, part catalog changes

Outputs

Low-stock alert, purchase order status, jobs released from Awaiting Parts

**Speaker notes:**

Manager stock view for UC-07, UC-08 and UC-10. Each part card shows on-hand quantity against its reorder point. Add to order fills a cart limited to one supplier, links jobs waiting on those parts, and sends the order to a Manager for approval. The Receive delivery view counts what arrived with plus and minus buttons and shows whether the order will be Received or Partially Received.

## Slide 9

Book Appointments · Front Desk

PROTOTYPE C · OPERATIONS BOARD · 1 OF 4

Appointments open in the side panel

Full slots and booked technicians are blocked

The job board stays visible while booking

TRACES TO SPRINT 3 MODELS

Use case

UC-12 Schedule Appointment

DFD process

1.0 Schedule Appointment

Requirements

FR01, NFR01, NFR02

Data stores

D1, D2, D7

Inputs

Appointment request

Outputs

Appointment schedule

**Speaker notes:**

Prototype C, Operations Board: a dark desktop status board where work opens in side panels. Best for experienced staff handling many jobs who want speed and keyboard shortcuts. Trade-off: more on screen to learn, and a dark theme can be harder to read in a bright shop. This slide covers FR01. The Appointments tab in the side panel lists bookings by date with a Reschedule action, and a compact form to book a new drop-off with an available technician. The picture is zoomed in on the panel so it is readable.

## Slide 10

Front Desk Board and Check-in

PROTOTYPE C · OPERATIONS BOARD · 2 OF 4

Every job visible in its status column

Check-in opens in a side panel

Keyboard shortcuts for fast data entry

TRACES TO SPRINT 3 MODELS

Use case

UC-01 Check In Device

DFD process

2.0 Register Repair Job

Requirements

FR01 to FR04, FR06, NFR03

Data stores

D1, D2, D3, D7

Inputs

Check-in details

Outputs

Customer search results,claim ticket, device tag

**Speaker notes:**

Prototype C, Operations Board: a dark desktop status board where work opens in side panels. Every open job sits in a column for its status, so Front Desk can see where any repair stands at a glance (FR06 open repairs view). Best for experienced staff handling many jobs who want speed and keyboard shortcuts. Trade-off: more on screen to learn, and a dark theme can be harder to read in a bright shop. Check-in collects the same UC-01 fields in a compact side panel and adds the new job to the Checked In column.

## Slide 11

Technician Board

PROTOTYPE C · OPERATIONS BOARD · 3 OF 4

Technician’s jobs grouped by status

Diagnose, Repair and History tabs

History shows each status change and who made it

TRACES TO SPRINT 3 MODELS

Use cases

UC-02, UC-04

DFD process

3.0 Record Diagnosis,4.0 Record Repair Work

Requirements

FR04 to FR07, NFR01, NFR02, NFR04

Data stores

D3, D4

Inputs

Diagnosis details, repair work details

Outputs

Diagnosis worklist, repair worklist

**Speaker notes:**

Technician board for UC-02 and UC-04. The technician’s own jobs sit in status columns, and selecting one opens a detail panel. Diagnose and quote uses a compact parts table with stock on hand. Repair records quantities used, which is when stock is deducted. History lists each status change with time and user, which supports the audit history backlog story. Customer contact details are hidden for this role.

## Slide 12

Parts and Purchase Orders · Manager

PROTOTYPE C · OPERATIONS BOARD · 4 OF 4

Edit stock and reorder points in place

Selected parts become one PO per supplier

Tabs for parts, orders and receiving

TRACES TO SPRINT 3 MODELS

Use cases

UC-07, UC-08, UC-10

DFD process

7.0 Process Purchase Orders,9.0 Maintain Shop Records

Requirements

FR06, FR09 to FR11, NFR01, NFR02

Data stores

D3, D4, D5, D6

Inputs

Purchase order request, received quantities, part catalog changes

Outputs

Low-stock alert, purchase order status, jobs released from Awaiting Parts

**Speaker notes:**

Manager view for UC-07, UC-08 and UC-10. The parts table can be edited in place, with count changes needing a reason (UC-07 alternate flow 2b). Selecting low parts creates one draft PO per supplier and links waiting jobs. The Purchase orders tab shows drafts, orders waiting on a Manager’s approval, approved orders ready to receive, and rejected orders returned with a reason. Receiving works only on approved orders.
