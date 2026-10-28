<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - Systems Request v1.2.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - Systems Request v1.2

SYSTEMS ANALYSIS & DESIGN PROJECT

QuickPhone Repair Tracking System

Systems Request

Project sponsor: Dr. Ashiqullah Pardisi, owner, Quick Phone Repair & Designs, Raleigh, NC

Prepared by: Project team – Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann

Submitted: Sprint 1 – September 14–20, 2026

Version: 1.2 – revised October 19, 2026 for the client’s September 21 confirmations and the Sprint 2 requirements (see the Sprint 3 change log); economic figures as in Feasibility Analysis v2.2

System request at a glance

| Item | Summary |
|---|---|
| Project name | QuickPhone Repair Tracking System |
| Project sponsor | Dr. Ashiqullah Pardisi, owner, Quick Phone Repair & Designs, Raleigh, NC |
| Business need | Give staff at both stores one shared view of every open repair and the parts it needs, so fewer customers call for status updates, fewer jobs stall waiting on parts, and no device is lost or released to the wrong person. |
| Business requirements | Optional appointment scheduling and intake of repair jobs; status tracking from check-in to customer pickup; parts inventory with automatic deduction when parts are used; purchase orders approved by the owner before they are placed; one pickup notification email to the customer from the store’s account; access by four roles: front desk, technician, manager and owner. |
| Business value | Estimated tangible benefit of $8,952 per year from staff time saved and fewer lost-device incidents, against an estimated $1,550 one-time and $1,460 per year in cost. Estimated 3-year net present value of about $17,100 with a payback of about 2.5 months. All figures are preliminary estimates. Intangible: better customer experience, accountability and control across two stores. |
| Special issues or constraints | The system records whether a job has been paid rather than taking payment, so QuickPhone's existing payment process is unchanged; staff at both stores must work from the same information; four-student team with final handoff on December 9, 2026; pickup notification emails are sent from the store’s account, approved by the owner on September 21. |

Contents

1. Organization and Application Overview	4

1.1 The Organization and Its Core Business	4

1.2 The Application	4

2. Existing Systems and Processes	4

2.1 Current Repair Process	4

2.2 Existing Tools	5

2.3 Limitations of the Current Situation	5

3. Problem Description	6

3.1 Problem Statement	6

3.2 PIECES Problem Analysis	6

4. Product Vision	6

4.1 Goals	6

4.2 Non-Goals	7

5. Core Functionality to Be Added	7

6. Expected Value	8

6.1 Tangible Benefits	8

6.2 Intangible Benefits	8

6.3 Success Measures	9

7. Issues and Constraints	9

7.1 Constraints	9

7.2 Issues Requiring Owner Decisions	10

7.3 Assumptions	10

8. Approval	10

## 1. Organization and Application Overview

### 1.1 The Organization and Its Core Business

QuickPhone is an independent electronics repair business with two store locations. Its core business is diagnosing and repairing customer devices: phones, tablets, laptops, game consoles and other consumer electronics. A typical repair follows the same path at both stores: the customer drops off the device, a technician diagnoses the fault, the customer approves a quote, parts are taken from stock or ordered from a supplier, the repair is completed and tested, and the customer collects the device.

Revenue depends on how many repairs the stores can finish, how quickly they turn devices around, and whether customers trust QuickPhone with their devices. Parts are a key input: each store keeps its own stock of screens, batteries and other components, and the store manager reorders from suppliers.

| Role | Responsibilities in the repair business |
|---|---|
| Store owner | Oversees both stores, sets priorities, approves every purchase order and sponsors this project |
| Store manager | Creates purchase orders for the owner’s approval, receives parts and manages staff accounts |
| Front desk staff | Check devices in, book drop-offs, communicate quotes and status to customers, release devices at pickup |
| Repair technicians | Diagnose faults, prepare quotes, record the parts they use and complete repairs; they cannot email customers |
| Customers | Drop off and collect devices, approve quotes; they do not use the system directly |
| Suppliers | Supply replacement parts; orders are placed outside the system and tracked in it |

### 1.2 The Application

The QuickPhone Repair Tracking System will be used by staff at both stores. It will record every repair job from check-in to customer pickup, schedule optional drop-off appointments and technician work, manage parts inventory and purchase orders, and give everyone a single, shared view of open repairs and parts availability. Staff at both stores will work from the same information, and the system will record whether a job has been paid rather than taking payment, so QuickPhone's existing payment process is unaffected. How the system is delivered has not yet been decided; the Sprint 3 physical design assumes a web application with one shared database, which the owner has still to confirm.

## 2. Existing Systems and Processes

### 2.1 Current Repair Process

Today, each repair moves through these steps. The workflow is the same one the owner wants the new system to follow; what is missing is a shared record of where each job and part stands.

| Step | What happens today | Who |
|---|---|---|
| 1. Drop-off | Customer walks in or arranges a drop-off; details of the customer, device and fault are recorded | Front desk |
| 2. Diagnosis and quote | Technician inspects the device and prepares a quote; the customer is contacted if the quote changes | Technician, front desk |
| 3. Parts | Staff check whether the part is in stock at the store; if not, the manager orders it from a supplier | Technician, manager |
| 4. Repair and testing | Technician completes and tests the repair | Technician |
| 5. Ready and pickup | Customer is told the device is ready, pays at the counter and collects the device | Front desk |

### 2.2 Existing Tools

QuickPhone has no single system shared by both stores that shows repair status and parts availability together. The specific tools currently used for each activity have not yet been documented; they will be confirmed in the owner interview (Sprint 1 task S1-02) and recorded in the table below.

| Activity | Current tool or method | Status |
|---|---|---|
| Recording customer, device and fault at intake | To be confirmed (for example paper ticket, spreadsheet or POS notes) | Confirm with owner |
| Tracking repair status | To be confirmed | Confirm with owner |
| Tracking parts stock at each store | To be confirmed | Confirm with owner |
| Tracking supplier orders and deliveries | To be confirmed | Confirm with owner |
| Telling customers their device is ready | Staff contact customers directly (email alerts are wanted) | Owner requirement |
| Taking payment | Existing payment process stays in place; the new system only records a paid flag | Owner decision |

### 2.3 Limitations of the Current Situation

| Limitation | Effect on the business | Source |
|---|---|---|
| No shared, real-time view of repair status | Customers call to ask where their device is; staff must stop work to find the answer | Owner goal: fewer "where's my phone?" calls |
| Parts stock and supplier orders not linked to jobs | Jobs sit waiting on parts that were not reordered in time | Owner goal: fewer jobs stuck waiting on parts |
| No consistent device tagging and release check | Devices can be misplaced or released to the wrong person | Owner goal: no lost devices |
| Information separated between two stores | Staff cannot see stock or jobs at the other store | Analyst finding from two-store operation |
| No history of who changed a job and when | Disputes about approvals or pickups are hard to resolve | Analyst finding |

## 3. Problem Description

### 3.1 Problem Statement

QuickPhone staff do not have a single, shared view of repair jobs and parts inventory across both stores. As a result, customers call to ask where their device is, jobs sit waiting on parts that were not reordered in time, and devices are at risk of being misplaced or released to the wrong person.

### 3.2 PIECES Problem Analysis

The PIECES framework groups the problems by Performance, Information, Economics, Control, Efficiency and Service.

| Category | Problem at QuickPhone |
|---|---|
| Performance | Repairs take longer when jobs wait on parts that are not in stock or not yet ordered. |
| Information | Staff cannot see, in one place, each job's status, the parts it needs and stock at both stores. |
| Economics | Staff time is spent answering status calls and chasing parts instead of completing repairs; lost devices create replacement and goodwill costs. |
| Control | No reliable record of who checked a device in, approved a quote, used a part or released a device. |
| Efficiency | The same information is asked for and repeated between customers, front desk, technicians and the manager. |
| Service | Customers must call for updates and may wait longer than necessary for their device. |

## 4. Product Vision

For QuickPhone's front desk staff, repair technicians, store manager and owner who need to know where every repair and every part stands at both stores, the QuickPhone Repair Tracking System is a repair and parts inventory tracker that follows each device from check-in to customer pickup and gives everyone one shared view of open repairs and parts availability. Unlike off-the-shelf repair shop subscriptions that bundle point-of-sale and payment features QuickPhone does not want, our product is built around QuickPhone's own workflow and keeps the business in control of its data.

In one sentence: every device tracked, every part accounted for, one view for both stores.

### 4.1 Goals

- Fewer "where's my phone?" calls, because staff can answer instantly and customers receive a pickup notification when their device is ready.

- Fewer jobs stuck waiting on parts, because low stock and waiting jobs are visible before they become delays.

- No lost devices, because every device is tagged at check-in and released only after ticket, ID and signature checks.

### 4.2 Non-Goals

- Taking or processing payments.

- A customer self-service portal or online booking.

- SMS messaging, and status emails other than the pickup notification.

- Reporting and analytics (planned for a later release).

## 5. Core Functionality to Be Added

| Capability | What it adds | Main users | Priority |
|---|---|---|---|
| Customer and device intake | Find or create the customer, record the device (phone, tablet, laptop, console, other), condition and accessories, create the job with a ticket number, print a claim ticket and device tag label | Front desk | Must |
| Repair job workflow | Move jobs through the agreed statuses with a full history; record diagnosis, quotes, customer approval, final cost and a paid Yes/No flag | Technicians, front desk | Must |
| Technician assignment and scheduling | Assign jobs to technicians with a personal job queue; book, reschedule or cancel optional drop-off appointments by store and time slot (walk-ins need none) | Front desk, manager | Must (assignment) / Should (appointments) |
| Parts on jobs | Record the parts used on a job, which deducts them from the store’s stock automatically (client-confirmed; no reservation step), and flag jobs awaiting parts | Technicians | Must |
| Parts inventory | Parts catalog with cost, supplier, device model and grade; stock per store; availability lookup; low-stock list; a way to load existing inventory if it is carried across at launch | Manager, technicians | Must |
| Purchasing and receiving | Create purchase orders, which the owner approves before they are placed (client-confirmed), and receive deliveries against them so stock and waiting jobs update | Manager | Must |
| Pickup and release | Verify the ticket number, check photo ID, capture the customer’s signature and record the payment; release only once payment is recorded | Front desk | Must |
| Open repairs dashboard | One view of open jobs by status, overdue jobs, jobs awaiting parts and low stock at both stores; quick job lookup | All staff, owner | Must |
| Customer email alerts | Send the customer one pickup notification email from the store’s account when the device is ready to collect; owner, manager or front desk send it, technicians cannot (client-confirmed) | Front desk, manager, owner | Must |
| Users, roles and locations | Staff accounts and role-based access for Front Desk, Technician, Manager and Owner at two stores | Manager | Must |

The prioritized product backlog (QuickPhone_Product_Backlog.xlsx) breaks these capabilities into user stories with acceptance criteria. The Sprint 2 requirements catalog (14 functional and 6 nonfunctional requirements) and twelve use cases now specify them, and the Sprint 3 DFDs and ERD model them.

## 6. Expected Value

### 6.1 Tangible Benefits

The estimates below come from the cost-benefit model in the Feasibility Analysis (v2.1) and are preliminary. Wage rates are national averages from the U.S. Bureau of Labor Statistics (May 2025); the technician rate in particular is likely above what QuickPhone actually pays, so this estimate may fall once payroll figures are available. Call volumes, incident counts and reduction percentages are analyst assumptions that will be replaced with QuickPhone's own baseline figures.

| Benefit | Estimated value per year | Basis |
|---|---|---|
| Fewer status-enquiry calls | $1,866 | Stores x calls x reduction x minutes per call / 60 x front desk wage x 52 |
| Less time chasing jobs waiting on parts | $3,724 | Stores x waiting jobs x hours per job x reduction x technician wage x 52 |
| Less inventory administration | $2,912 | Stores x manager hours x reduction x manager wage x 52 |
| Fewer lost or wrongly released devices | $450 | Incidents x cost per incident x reduction |
| Total estimated tangible benefit per year | $8,952 | Sum of the rows above |

| Measure (3-year horizon, estimated) | Result |
|---|---|
| Estimated one-time cost to QuickPhone (Year 0) | $1,550 (range $100 - $5,350) |
| Estimated recurring cost per year | $1,460 (range $80 - $3,765) |
| Estimated net benefit per year | $7,492 |
| Estimated net present value at 10% discount rate | about $17,100 |
| Estimated return on investment (3 years) | about 353% |
| Estimated payback period | about 2.5 months |

All figures above are preliminary estimates taken from the Feasibility Analysis (v2.1). They are shown as ranges where the underlying facts are not yet established. The two largest unknowns are what computing equipment QuickPhone needs to buy, since the stores currently run on one laptop, and who is responsible for the system after handoff; the second of these is also the largest single swing item in the annual cost. Development labor is provided by the student team as a course project and is not a cash cost to QuickPhone, and the Feasibility Analysis also shows the result if that labor had to be paid for.

### 6.2 Intangible Benefits

- Better customer experience: customers are told when their device is ready instead of having to call.

- Greater trust and accountability: every check-in, approval, part used and release is recorded with the staff member and time.

- Consistent process at both stores, making it easier to train new staff and move staff between stores.

- Better purchasing decisions from visible stock levels and parts needed by waiting jobs.

- A foundation for later reporting on turnaround times, parts usage and technician workload.

### 6.3 Success Measures

| Objective | Measure | Proposed target |
|---|---|---|
| Fewer "where's my phone?" calls | Status-enquiry calls per week, per store | 50% fewer within 60 days of go-live |
| Fewer jobs stuck waiting on parts | Jobs in Awaiting Parts for more than 5 days | 50% fewer within 60 days of go-live |
| No lost devices | Devices misplaced or released to the wrong person | Zero per quarter |

## 7. Issues and Constraints

### 7.1 Constraints

| Type | Constraint | Implication |
|---|---|---|
| Scope | No payment collection; prices recorded for reference only (quote, final cost, paid flag) | Existing payment process stays in place |
| Scope | Customers do not use the system directly | No customer portal; customers are contacted by email only |
| Technical | Staff at both stores must work from the same information | Must be usable at the counter and at the repair bench in both stores |
| Technical | Email-only customer alerts | Sent from the store’s email account, approved by the owner on September 21 |
| Schedule | Fixed course calendar: six sprints, final deliverables due December 9, 2026 | MVP must be demonstrated in Sprint 4 (Nov 2-8); scope must be frozen early |
| Resources | Four-student team working part time | Must items are prioritized; Should items built only if capacity allows |
| Budget | No budget stated | Cash costs are limited to hosting, a domain and in-store hardware |
| Privacy | System stores customer contact details and signatures | Role-based access; customer information protected in storage and in transit; no ID numbers stored |

### 7.2 Issues Requiring Owner Decisions

| Issue | Why it matters | Decide by |
|---|---|---|
| What tools are used today for intake, status and parts tracking, and what baseline figures exist? | Confirms the as-is process and the value estimates | Still open; Sprint 3 |
| May alerts be emailed from the shop’s existing mailbox? Resolved September 21: yes, from the store’s account. | Email alerts depend on it | Resolved |
| Where will the system be hosted, and who supports it after December 9? | Affects cost, reliability and handoff | Sprint 3 |
| Which label printer and label size will be used? | Needed to design the device tag label | Sprint 3 |
| Should device passcodes be recorded, and how? | Privacy and security design | Sprint 3 |
| Can unpaid repairs be released, and what happens to uncollected devices? Sprint 2 proposes no release until payment is recorded; uncollected devices are still open. | Pickup rules and claim ticket terms | Sprint 3 |
| Is the pickup notification sent by staff or automatically when a repair is marked complete? | Who can trigger it (technicians may not) and how the pickup screens work | Sprint 3 |
| Is there a purchase-order spending threshold, or an urgent path when the owner is unavailable? | Every order now waits on the owner’s approval | Sprint 3 |

### 7.3 Assumptions

- Each store keeps its own stock levels; moving parts between stores is out of scope for the December prototype.

- Supplier orders are placed outside the system and recorded in it by the store manager.

- Photo ID is checked visually at pickup; only an ID-checked flag is stored.

- What computing equipment is available at each store has not yet been confirmed; some additional equipment may be required.

## 8. Approval

By signing below, the project sponsor approves this systems request and authorizes the team to proceed to requirements analysis in Sprint 2.

| Name | Role | Signature | Date |
|---|---|---|---|
|  | Project sponsor (store owner) |  |  |
|  | Store manager |  |  |
|  | Project team Scrum Master |  |  |
