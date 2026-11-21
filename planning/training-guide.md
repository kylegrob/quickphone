# Staff training guide

A session of about 60 minutes on the sample data. Start the application as described in [app/README.md](../app/README.md), reset the data with `seed_training --yes`, and open http://localhost:8000. Every person, phone number and address in the sample data is invented.

Every training account uses the password in `TRAINING_PASSWORD` in `app/shop/management/commands/seed_training.py`. Hand it out on paper during the session; it exists only for the sample data. Pickup emails are written to `app/sent_emails/` rather than sent, so trainees can open the file and read what the customer would receive.

| Sign in as | Role | Lands on |
|---|---|---|
| desk1@quickphone.test | Front Desk, Store 1 | Check in |
| sam@quickphone.test, jordan@quickphone.test | Technician, Store 1 | Technician jobs |
| manager1@quickphone.test | Manager, Store 1 | Inventory and POs |
| owner@quickphone.test | Owner, both stores | Dashboard |
| desk2@, alex@, manager2@quickphone.test | Store 2 staff | |

## Exercises

The sample data has one Store 1 job at every step of the workflow, so each exercise starts from a realistic state. Trainees work in pairs, one on a Front Desk screen and one on a Technician screen, and swap halfway.

| # | Exercise (role) | What to do | What the trainee should notice |
|---|---|---|---|
| 1 | Check in from an appointment (Front Desk) | Check in, today's 9:30 appointment, Start check-in. Pick the iPhone 13 on file, type the problem, Create job | Customer and technician come from the appointment; ticket and tag share one number |
| 2 | Walk-in with a new customer (Front Desk) | Search a phone number that does not exist, enter the new customer and device, leave the technician open | Searching by phone first stops duplicate customers; an open job waits for a technician to claim it |
| 3 | Book and reschedule (Front Desk) | Book appointment for tomorrow; then Reschedule it to a time Sam is already booked | Full slots and booked technicians cannot be picked |
| 4 | Claim and diagnose (Technician) | Claim the open Nintendo Switch job, Start diagnosis, tick parts, Send quote | The total builds as parts are ticked, with the Owner's labor added |
| 5 | Record the customer's answer (Front Desk) | Repair jobs, open the iPhone 12 job (Awaiting Approval), Customer approved | Repair cannot start before approval; the history records who recorded it |
| 6 | Repair and finish (Technician) | Open the iPhone 13 cracked screen job, check the parts list the quote filled in, add repair notes, Mark ready for pickup | The quote's parts come off stock when the job is marked ready; a job cannot be finished with more parts than are on hand |
| 7 | Order parts (Manager) | Inventory, Add to PO on the Galaxy S22 battery, link the waiting job, Submit; Approve; Mark as ordered; Receive delivery | Every order needs approval; receiving puts the waiting job back to In Repair |
| 8 | Pickup (Front Desk) | Open the Pixel 7 job (Ready for Pickup): Send pickup notification, try Release without paying, record payment, Print receipt and have it signed, tick Photo ID checked and Customer signed the receipt, Release | A repaired device is never released before payment; the email comes from the store's account |
| 9 | Return unrepaired (Front Desk) | Open the IdeaPad job (Returned Unrepaired) and print the receipt, have it signed, and release it with no payment | No fee is charged for a device that cannot be repaired |
| 10 | Both stores (Owner) | Dashboard; switch to Store 2 | Open repairs and low stock side by side |

Ask trainees to finish exercises 1, 4 and 8 without help; that is the acceptance check for usability (NFR03). Note anything that confused them, since it shows where the screens or the written manual need work.


## Correcting payments and reviewing security

Before release, open the job, find the mistaken payment, enter a reason and choose **Void payment**. The payment stays on the job marked Voided with the reason, person and time. It no longer counts toward the paid total or appears as a payment on the customer receipt; record the correct payment before releasing a repaired device. Closed jobs cannot be corrected this way. A Technician needs Owner-granted Repair jobs access to void a payment.

Managers may create and update Front Desk and Technician accounts at their home store. Ask the Owner to create or change another Manager account. A Manager may update their own profile, keeping their role and active status. Granting the Staff screen to another role does not grant account-management rights. The Owner opens **Audit records** to review security events; this page is read-only. A non-Owner granted Dashboard access sees only their home store.
