# QuickPhone Physical DFDs and Physical ERD: Build Notes

These models convert the Sprint 2 logical set (DFD v3.1 and the 22-entity ERD) into physical form. They follow the textbook's logical-to-physical steps: add implementation references, draw the human–machine boundary, add system-related processes and stores, restate the data elements on flows, and name stores by their tables. Gane and Sarson symbols are used. **Every external entity and every data store appears exactly once per diagram**; no duplicate symbols are used. Two drawing devices make that possible:

- **Orthogonal routes:** for example, the Owner's flows into 6.0 and 7.0 on Level 0.
- **One converging flow:** 9.0's nightly backup reads every store once, drawn as joined lines into a single arrow.

## Implementation decisions shown

Sprint 2 did not choose a technology, so the models carry forward the Sprint 1 PSPI recommendation: a custom web application used at the counter and bench PCs in both stores, backed by one shared relational database. **Confirm this with the owner before the models go out.** Everything else traces to Sprint 2:

- Claim ticket and device tag print to a label printer at each counter (FR03, UC-01).
- The completion email is a staff click, sent from the store's own email account (FR12, NFR05; client-confirmed #5–#7).
- The card machine is not linked. Staff take payment on it or in cash (manual process 5.5), then key the amount and method into the system (FR08).
- The photo-ID check is manual (5.2). Only an ID-checked flag is stored.
- Orders are placed with suppliers by phone, email or website, outside the system; the Manager then clicks "Mark placed" (UC-10).
- Starting inventory is loaded from a CSV file (new batch process 8.5; FR11, UC-07 2a).
- Part usage is a single database transaction that deducts stock, with a CHECK constraint that blocks negative stock (FR07).
- New process **9.0 Run System Services** covers sign-in, role checks on every request, idle-session expiry and nightly backup (NFR01, NFR05, NFR06). Two new stores support it: D8 Sessions and D9 Backup Copies.

## Files

| File | Content |
|---|---|
| `QuickPhone_PDFD_0_Context.png` | Physical context diagram (adds the All Staff sign-in flows) |
| `QuickPhone_PDFD_1_Level0.png` | Physical Level 0: 9 processes, boundary, stores with table names |
| `QuickPhone_PDFD_2…8_*.png` | Physical Level 1 for 1.0–6.0 and 8.0 (7.0 stays a primitive) |
| `QuickPhone_PDFD_9_Level1_P9_SystemServices.png` | New Level 1 for 9.0, with timer triggers as dashed control flows |
| `QuickPhone_Physical_ERD.png` | 24 tables, ANSI SQL types, keys, NOT NULL, notation and design decisions |

## ERD changes from the logical model

The logical model's 22 entities become 24 tables, adding `user_session` and `backup_log`. Other changes:

- `password_hash` and `last_login_at` added to employee.
- `email_address` added to store, as the sending account.
- `intake_condition` moved from device to repair_job, because condition is recorded at every visit.
- purchase_order gains `submitted_at`, `placed_at` and `rejection_reason`.
- Three stored derived values are kept deliberately: quote total, PO total and the job's current status.

The CHECK constraints and indexes are listed on the diagram. FK lines to store and employee are omitted for readability; the key column names the table each one references.

## Open items carried forward

1. The delivery route (custom web app vs subscription) is assumed, not decided.
2. On-screen signature: FR08 still asks whether the customer signs at all. `signature_file` is nullable so it can be dropped.
3. PO approval threshold or urgent path: if adopted, it becomes a rule inside 6.3.
4. Fallback for customers with no email: modelled as Failed plus a logged phone call.

Re-render with `render.ps1` (headless Chrome). Sources: `physical_dfd_source.html?d=context|level0|l1_1…l1_6|l1_8|l1_9` and `physical_erd_source.html`.
