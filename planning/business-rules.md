# Business rules decided with the owner

These are the decisions that shape how the application behaves. Each is either direction the owner gave or a team decision made while building, marked "to confirm" until the owner agrees. The requirements catalogue ([requirements-catalog.docx](requirements-catalog.docx)) lists the same decisions against each requirement.

## Owner direction, October 30

- **The quote is shown at check-in.** It is the part cost plus the labor the Owner sets for each part (Inventory, edit a part; only the Owner can change it). Clicking Create job approves the quote, so repair needs no second approval. Leave the parts blank when the device needs diagnosis first, and the technician quotes as before.
- **Only an additional repair is re-approved.** From Diagnosing or In Repair the technician sends an additional repair; Front Desk records the answer. A declined additional repair leaves the approved repair going. The approved total is the sum of the approved quotes.
- **Technicians can check in customers** and print the claim ticket, but cannot open the job list, payment or release.
- **Managers and the Owner can repair devices.** They can be assigned a job, claim an open one and use the same repair screen ("My repair jobs").
- **Brand and model come from a list.** Check-in picks the device from a list grouped by brand. "Device not on the list? Add it" adds a new type, brand and model for everyone, and a model added with different capitalization is matched to the existing one. The starter list is in `app/shop/device_catalog.py`.
- **The Owner sets screen access by role.** The Access screen (Owner only) is a table of seven screens by four roles; the defaults are the earlier fixed rules and only changed boxes are stored. It controls which screens a role can open, not the rules inside a screen: only a Manager or the Owner approves a purchase order, technicians work only on their own jobs, and only the Owner can give the Owner role. Opening Staff, suppliers and stores does not grant account-management rights: only the Owner and Managers may create or edit accounts. Managers manage Front Desk and Technician accounts in their home store; only the Owner creates or edits another Manager or an Owner account. Managers may update their own profile without changing role or deactivating themselves.

## Team decisions, October 28 (to confirm)

- **Technicians may send the pickup notification** (owner answer #1, October 23) but never see the customer's address.
- **Quoted parts are stored in a QUOTE_LINE table**, so the technician sees them again after approval. A JOB_PART "Needed" row keeps its meaning: a part the job is waiting for.
- **A declined quote returns the device unrepaired.** Front Desk may record a fee, but none is required to release it.
- **The passcode** is visible to the assigned technician, Managers and the Owner.
- **Managers work only in their home store**; only the Owner switches stores.
- **A Manager may approve an order they created**, and history keeps both names. Set `ALLOW_SELF_APPROVAL_OF_PO` in `app/shop/permissions.py` to change this.
- **PART has a SKU.**

## Team decisions, November 2 to 20 (to confirm)

- **Technicians see customer phone and email** on the check-in screen, because they check customers in.
- **Parts come off stock when a job is marked ready**, in one step, and a shortfall blocks completion.
- **Appointment length depends on the repair type.** Book appointment first asks for the repair type; the time slots then show only start times where that length fits. A booking holds its technician for its whole length, and one that would run past closing (the last slot plus one slot) cannot be picked. The Owner or a Manager changes the lengths, in 15-minute steps, under Staff, stores and suppliers. A booking keeps the length it was made with if the type changes later.
- **Approvers are emailed when an order is submitted.** The store's Managers and the Owner (not the person who submitted it) get an email from the store account; a failed email does not undo the submission.
- **A payment recorded by mistake can be voided** from the job page until the device is released. A reason is required. The original payment remains with its amount, method and payment time, plus who voided it and when. Voids are excluded from the paid total and receipt; job history and security audit records retain the correction. Technicians may void payments when the Owner grants Repair jobs access (Kyle, Nov 20).
- **The technician bench shows whether the pickup notification was sent**, on the job and in the job list, with the Send button beside it.
- **New customers need a phone number**; email is optional, and the send button for the pickup notification appears only when the customer has an email on file.
- **A locked account cannot be unlocked early.** It unlocks itself after 15 minutes.

## Still to confirm with the owner

Store hours and the slot grid (placeholders in `app/quickphone/settings.py`), the minutes for each repair type (placeholders in `app/shop/repair_types.py`), ticket printers, and how labor is charged for a repair with no part (today a zero-cost "service" part is used, because labor is charged per part times quantity).


## Security changes, November 20 (Kyle; team direction)

The dashboard remains Owner-only by default. If the Owner grants it to another role, it shows only that user's home store, regardless of a selected store in the session. The Owner still sees both stores. Technician access to customer contact details, shared customer lookup and assigned-job passcodes remains available; purchase-order approval and self-approval remain with Managers and the Owner.

The Owner's Audit records page lists sign-ins and failures, sign-outs, staff changes and password-reset indicators, role/screen-access changes, passcode views, payment voids and shop-reference edits. It records the person, time, store, target and outcome without copying credentials or device passcodes. Failed sign-ins retain a hash of the supplied login for correlation. Events have no edit/delete interface, and application model/queryset updates and deletes are refused; database administrators still have direct database authority. Account, permission and payment changes are committed with their audit entries. Concurrent payment recording, voiding and release lock the job row before checking its current state.
