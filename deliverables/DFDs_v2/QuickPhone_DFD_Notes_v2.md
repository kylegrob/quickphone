# QuickPhone Logical DFDs v2: Build Notes

This set revises the Sep 28 DFDs against Dennis, Wixom & Roth, *Systems Analysis and Design* 8e, Chapter 4 (pp. 137–160). It follows the textbook's five steps (p. 144): (1) a context diagram, (2) a DFD fragment for each use case, (3) the fragments merged into Level 0, (4) a Level 1 DFD for each Level 0 process, built from the use case's steps, and (5) validation against the Figure 4-24 checklist. The diagrams use Gane and Sarson symbols and show external entities at every level, as the book does (p. 149). They are logical and technology-neutral. The Sep 28 files in `../DFDs/` are kept unchanged for comparison.

## What changed from the Sep 28 set, and why

| Change | Textbook basis |
|---|---|
| Every two-headed read/update arrow is split into two named one-way flows. For example, 6.5 ↔ D5 becomes *Ordered PO* in and *Receipt Status* out. | "This practice is incorrect… should always be shown as two separate data flows" (p. 139); Fig. 4-24 |
| Process names are now a single verb + noun with no "and". Examples: *Book & Check In Device* → **Check In Device**, *Purchase & Receive Parts* → **Replenish Parts**, *Send & Log Email* → **Send Completion Email** + **Record Notification Result** | Verb + noun; "avoid using the word 'and'" because a process performs one activity (pp. 137–138) |
| New **8.0 Maintain Shop Records**, which replaces *Manage Staff Accounts* and adds maintenance of stores, the parts catalog and suppliers | Every data store needs a process that adds and changes its data. "Administrative" processes are often overlooked (pp. 138, 157) |
| New input D1 → 5.3 *Customer Identity* | 5.3 can't match a photo ID without the customer's name: the "insufficient inputs" semantics error (p. 155) |
| New *Job Selection* inputs to 2.1, 3.1 and 4.1 | The *Selected Job* output needs a matching input, otherwise it is a partial "miracle" (p. 154) |
| 2.4 *Revise Repair Quote* → **Prepare Repair Quote**. Every quote now goes to Awaiting Approval, not just a higher revised quote | Matches catalog FR06/FR07 and the client-confirmed approval stage (fix made Sep 30 after the model-connection review) |
| *Final Cost & Send Approval* → *Job Selection, Final Cost & Send Instruction* | Consistent terminology (p. 156). "Approval" now means only the customer's quote approval and the owner's PO approval |
| Data flow names are unique across Level 0. Examples: *Stock Summary* (7.0) vs *Stock Levels* (6.0); *Current…* for reads vs *…Updates* for writes | "Every data flow has a unique name"; outputs are named differently from inputs (Fig. 4-24) |

## Use case fragments → Level 0 → Level 1

| Level 0 process | Built from | Level 1 processes |
|---|---|---|
| 1.0 Check In Device | UC-01, UC-11 | 1.1 Book Drop-off Appointment · 1.2 Identify Customer · 1.3 Record Device Intake · 1.4 Open Repair Job · 1.5 Produce Claim Documents |
| 2.0 Diagnose Device | UC-02, UC-03 | 2.1 Retrieve Assigned Job · 2.2 Record Diagnosis · 2.3 Check Part Availability · 2.4 Prepare Repair Quote · 2.5 Record Customer Quote Decision |
| 3.0 Repair Device | UC-04 | 3.1 Retrieve Repair Job · 3.2 Check Part Stock · 3.3 Record Part Usage · 3.4 Hold Job for Parts · 3.5 Complete Repair |
| 4.0 Notify Customer | UC-05 | 4.1 List Completed Jobs · 4.2 Confirm Final Cost · 4.3 Prepare Completion Email · 4.4 Send Completion Email · 4.5 Record Notification Result |
| 5.0 Release Device | UC-06 | 5.1 Find Pickup Job · 5.2 Record Payment · 5.3 Verify Customer Identity · 5.4 Close Repair Job |
| 6.0 Replenish Parts | UC-07, UC-08, UC-09 | 6.1 Identify Low Stock · 6.2 Prepare Purchase Order · 6.3 Approve Purchase Order · 6.4 Record Order Placement · 6.5 Receive Parts Delivery |
| 7.0 Report Repair Status | UC-10, UC-15 | Not decomposed (see below) |
| 8.0 Maintain Shop Records | UC-14, plus the catalog's information requirements FR 4.1, 4.6 and 4.7 | 8.1 Maintain Staff Accounts · 8.2 Maintain Store Details · 8.3 Maintain Parts Catalog · 8.4 Maintain Supplier Details |

Data stores: D1 Customers & Devices, D2 Repair Jobs, D3 Appointments, D4 Parts Inventory, D5 Purchase Orders & Suppliers, D6 Staff Accounts & Stores and D7 Notification Log.

**7.0 is left as a primitive.** It does only two things: answer a status enquiry and produce the two-store overview. The book advises against decomposing a process that yields only two children (p. 149), so 7.0 is covered by its process description instead:

> *7.0 Report Repair Status.* For a status enquiry, find the job by ticket number, phone or name in D1/D2. Return its status, last update, technician, promised date and whether the customer has been notified (D7). For the owner, summarise open jobs by status and store, overdue and aging jobs, jobs awaiting parts with the days waited, and low stock (D4). Read only: it writes to no store.

**Level 0 has eight processes.** The chapter text allows "no more than seven to nine" (p. 149). The Fig. 4-24 checklist says three to seven. If the instructor applies the checklist strictly, fold 7.0 into 8.0 as a "Maintain and Report Shop Records" group. That fix is weaker, because it brings back an "and" in the name.

## Validation (Fig. 4-24)

**Syntax.** Every process has a number, a verb-phrase name, at least one input and at least one output. There are no black holes or miracles. Every flow is one-way, has a noun name and touches a process. No flow runs directly between two entities, between two stores, or between an entity and a store. Each Level 1 diagram has 4–5 processes.

Every store has at least one input and one output somewhere in the set:

| Store | Written by | Read by |
|---|---|---|
| D1 | 1.2, 1.3 | 1.2, 4.3, 5.3, 7.0 |
| D2 | 1.4, 2.x, 3.x, 4.2, 5.2, 5.4 | 2.x, 3.1, 4.1, 5.1, 6.1, 6.5, 7.0 |
| D3 | 1.1 | 1.3 |
| D4 | 3.3, 6.5, 8.3 | 2.3, 3.2, 6.1, 7.0, 8.3 |
| D5 | 6.2–6.5, 8.4 | 6.2–6.5, 8.4 |
| D6 | 8.1, 8.2 | 1.4, 4.3, 8.1, 8.2 |
| D7 | 4.5 | 7.0 |

**Balance.** The context diagram and Level 0 share the same five entities and the same 24 external flows. Where a Level 0 flow is a bundle, its Level 1 parts are named on the child diagram. For example, *Job Selection, Final Cost & Send Instruction* splits into *Job Selection* (4.1), *Final Cost* (4.2) and *Send Instruction* (4.4). The book accepts this: balanced means "shown appropriately", not identical (p. 141).

**Semantics.** The viewpoint is the shop's throughout. Customer quote approval (2.5) and owner PO approval (6.3) are named separately everywhere. Alternative flows are explained in the diagram notes, as the book prescribes (p. 142): 2.5 sets In Repair when a quote is approved or Cancelled/Returned when it is declined, and 4.5 records sent or failed. The last check, a user walkthrough or role-play (p. 155), still has to be done with the owner.

## Client-confirmed rules shown

- A part is deducted automatically when it is recorded as used (3.3). There is no reservation step.
- Every PO needs owner approval (6.3). 6.4 accepts only approved POs.
- Customers get email only, and only when the repair is complete. The email is sent from the store's account (4.4).
- Only the Owner, Manager and Front Desk may give the Send Instruction. A Technician is refused.

## Deliberately left out

- **Supplier:** not an entity, because orders are placed outside the system.
- **Card machine:** not an entity, because only the paid flag is recorded.
- **UC-12, 13, 16, 17:** transfer, adjustment, initial load and the uncollected-device follow-up. UC-17 is temporal, and it would enter as a dashed control flow (p. 157).

## Walkthrough questions for the owner

- Who maintains store details (8.2)? Catalog FR11, FR12 and FR17 already give parts, suppliers and staff accounts to the Manager, but no requirement covers stores.
- Is the email sent by staff or automatically?
- How are customers with no email address handled?
- Can an unpaid device be released on a manager override?
- Is there an urgent path when the owner can't approve a PO?

Source: `dfd_source_v2.html?d=context|level0|l1_1…l1_6|l1_8`. To re-render the PNGs, run `render.ps1` (it uses headless Chrome).
