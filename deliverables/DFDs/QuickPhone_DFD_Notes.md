# QuickPhone Logical DFDs: Build Notes

These notes follow the lecture's process: context diagram, then a fragment for each use case, then fragments merged into Level 0, then each Level 0 process decomposed into Level 1, then validation. The diagrams are logical and technology-neutral. They show what happens to data, not the devices, screens or files that do it. They replace the Sep 14 context and Level 0 diagrams, which came before the client-confirmed requirements. Those diagrams still showed part reservation, alerts on every status change, a CSV import, and purchase orders with no owner approval.

## Use case fragments → Level 0 processes

| Process | Built from | Level 1 |
|---|---|---|
| 1.0 Book & Check In Device | UC-01, UC-11 | 1.1–1.4 |
| 2.0 Diagnose & Quote Repair | UC-02, UC-03 | 2.1–2.3 |
| 3.0 Repair Device & Record Parts Used | UC-04 | 3.1–3.5 |
| 4.0 Notify Customer Repair Complete | UC-05 | 4.1–4.4 |
| 5.0 Release Device at Pickup | UC-06 | 5.1–5.4 |
| 6.0 Purchase & Receive Parts | UC-07, UC-08, UC-09 | 6.1–6.5 |
| 7.0 Report Job & Store Status | UC-10, UC-15 | primitive (lookup only) |
| 8.0 Manage Staff Accounts | UC-14 | primitive (lookup only) |

Data stores: D1 Customers & Devices, D2 Repair Jobs, D3 Appointments, D4 Parts Inventory, D5 Purchase Orders & Suppliers, D6 Staff Accounts & Stores, and D7 Notification Log. D7 is new. It comes from the confirmed requirement to log each notification's sender, time and result.

## Balancing and validation

Every external-entity flow on the context diagram appears unchanged on Level 0. Every Level 0 flow into or out of a process appears again on its Level 1 diagram. A few flows split into named parts at Level 1. For example, "Intake Details & Technician Assignment" becomes Customer Details, Device/Condition/Fault Details and Technician Assignment. Level 0 read-and-update pairs are drawn as two-way arrows to reduce clutter. At Level 1 they are drawn as separate, named flows.

Syntax check: every process has a verb-phrase name and at least one input and one output. Every data store has at least one input and one output across the set. Every entity has at least one flow, and no flow runs directly between two entities or two stores.

Semantic check: all names are written from the shop's point of view. Customer approval of a quote (2.3) and owner approval of a purchase order (6.3) are named separately throughout.

## Client-confirmed rules shown

- Part deduction happens automatically when a part is recorded as used (3.3). There is no reservation step.
- Every purchase order needs owner approval (6.3). Step 6.4 accepts only approved purchase orders.
- Customers are notified by email only, and only when a repair is complete. The email is sent from the store's account (4.4).
- Only the Owner, Manager and Front Desk may send customer email. A Technician is refused.

## Deliberately left out

- The supplier is not an entity, because orders are placed outside the system.
- The card machine is not an entity, because the system records only the paid flag.
- Supporting cases UC-12, UC-13, UC-16 and UC-17 are left out. These are stock transfer, stock adjustment, initial inventory load and uncollected-device follow-up. Add them to 6.0 and 7.0 if the owner confirms them.

## Walkthrough questions for the owner

- Is email sent by staff or automatically?
- How are customers without an email address handled?
- Can a manager override release of an unpaid device?
- Is there an urgent path when the owner can't approve a purchase order?

Source: `dfd_source.html`. Open it with `?d=level0`, `?d=l1_3`, etc. to redraw a diagram.
