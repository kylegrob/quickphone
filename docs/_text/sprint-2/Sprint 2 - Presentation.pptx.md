<!-- Auto-generated from docs/sprint-2/Sprint 2 - Presentation.pptx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 2 - Presentation

## Slide 1

Sprint 2 Presentation

By: Kyle Robertson, Leonard Mann,

Bara Abusamhan, Ehsanullah Pardisi

**Speaker notes:**

The Sprint 2 Presentation going over: requirements, use cases, and logical diagrams

## Slide 2

The Problem

Staff cannot see in one place where each repair stands and which parts it needs.

Customers call to ask where their device is

Jobs stall waiting on parts

Devices can be lost or released to the wrong person

**Speaker notes:**

Bara

## Slide 3

What Changed Since Sprint 1

**Speaker notes:**

Every PO now waits for the Owner; Reservation is gone: part leaves stock when the technician logs the repair; one completion email from the store's account automatically sent when job is complete

## Slide 4

Requirements

## Slide 5

Use Cases

4 actors in the system: Owner, Manager, Technician and Front Desk. Customers and suppliers sit outside it

UC-01 to UC-06 follow a repair from check-in to pickup matching the job statuses

UC-07 to UC-10 keep parts stocked at both stores, with every purchase order going through the owner

UC-11 controls accounts so each person only sees what their role allows

Each use case maps to a story in our backlog

The use cases shows what every person does in the system. The diagrams take those same steps and display how the data moves between them

## Slide 6

_(no text — image only)_

**Speaker notes:**

This is our Level 0 logical DFD. It shows eight major processes of our system:

Processes 1.0, 2.0, 3.0 and 5.0, down the left side: follow one repair from start to finish.Check In opens the repair job. Diagnose produces the quote and records whether the customer approves it. Repair logs the parts used, and those parts come off inventory automatically. Release handles the ID check and payment, then closes the job. Notify Customer sends the completion email in between.

The right side supports that repair work. Replenish Parts handles reorders, and the owner approves each purchase order. Report Repair Status answers status questions and gives the owner a view across both stores. Maintain Shop Records keeps the reference data current.

Repair Jobs is the central data store, and almost every process reads from it or writes to it. That’s what links the eight processes into one system.

1.0 Check In: writes to D1 (customers and devices) and D2(repair jobs), creating CUSTOMER, DEVICE and a new REPAIR_JOB

2.0 Diagnose: reads stock from D4 (INVENTORY) and saves the QUOTE in D2 (repair jobs)

3.0 Repair: logs JOB_PART in D2 (repair jobs) and deducts INVENTORY in D4 (parts inventory)

4.0 Notify: reads the CUSTOMER email from D1(customers and devices) and records a NOTIFICATION in D7 (notification log)

5.0 Release: saves the PAYMENT and closes the REPAIR_JOB in D2 (repair jobs)

6.0 Replenish: the Owner-approved PURCHASE_ORDER in D5(purchae orders & suppliers) restocks INVENTORY and releases waiting jobs

## Slide 7

ERD

## Slide 8

Questions for Sprint 3

**Speaker notes:**

1. PO spending limit“The client confirmed that every purchase order needs the Owner’s approval. We still need to know whether small orders can skip that step, and what happens when the Owner isn’t available. That decides how the approval process works.”

2. Intake fields“We drafted the check-in form from our own assumptions: customer details, the device model and IMEI, its condition, and any accessories. We need the client to confirm it matches what the front desk records today, and whether they store passcodes.”

3. Diagnostic fee“When a device goes back unrepaired, we don’t know whether the shop charges for the diagnosis. Until the client tells us, that part of the payment process stays blank.”

## Slide 9

Thank you
