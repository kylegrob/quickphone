# Oct 23: bring the physical DFD/ERD front matter in build_submission.py in line with the owner's clarifications,
# and finish the Oct 23 PostgreSQL relabel there (the balancing table still said "DB Record").
import pathlib, sys

p = pathlib.Path(__file__).with_name('build_submission.py')
s = p.read_text(encoding='utf-8')


def sub(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f'expected {n}, found {c}: {old[:90]!r}')
    s = s.replace(old, new)


# balancing table: the diagrams say PostgreSQL since the Oct 23 relabel
head, sep, tail = s.partition('CSS = """')
head = head.replace('DB Record', 'PostgreSQL Record')
s = head + sep + tail

sub("  ('Check-In Input Form', 'Phone Search Input Form; Customer Details Input Form; Device Intake Input Form; Technician Assignment Input Form'),",
    "  ('Check-In Input Form', 'Phone Search Input Form; Customer Details Input Form; Device Intake Input Form; Passcode Input Form; Technician Assignment Input Form'),")
sub("  ('Diagnosis Input Form', 'Diagnosis Job Selection Input Form; Diagnosis Findings Input Form; Labor Amount Input Form'),\n"
    "  ('Diagnosis Output Form', 'Assigned Jobs Output Form; Part Availability Output Form'),",
    "  ('Diagnosis Input Form', 'Diagnosis Job Selection Input Form; Job Claim Input Form; Diagnosis Findings Input Form; Labor Amount Input Form'),\n"
    "  ('Diagnosis Output Form', 'Job Queue Output Form; Part Availability Output Form'),")
sub("  ('PostgreSQL Record: Diagnosis Queue', 'PostgreSQL Record: Assigned Jobs; PostgreSQL Record: Pending Quote'),\n"
    "  ('PostgreSQL Record Update: Diagnosis and Quote', 'PostgreSQL Record Update: Diagnosis Findings; PostgreSQL Record: Part Needed; PostgreSQL Record: New Quote; PostgreSQL Record Update: Quote Decision'),",
    "  ('PostgreSQL Record: Diagnosis Queue', 'PostgreSQL Record: Open Jobs; PostgreSQL Record: Pending Quote'),\n"
    "  ('PostgreSQL Record Update: Diagnosis and Quote', 'PostgreSQL Record Update: Job Claimed; PostgreSQL Record Update: Diagnosis Findings; PostgreSQL Record: Part Needed; PostgreSQL Record: New Quote; PostgreSQL Record Update: Quote Decision'),\n"
    "  ('PostgreSQL Record: Unassigned Appointments', '='), ('PostgreSQL Record Update: Appointment Claimed', '='),")
sub("  ('Repair Work Input Form', 'Repair Job Selection Input Form; Parts Used Input Form; Repair Completion Input Form'),\n"
    "  ('Repair Work Output Form', 'Repair Job Output Form; Parts Shortage Output Form'),\n"
    "  ('PostgreSQL Record: Job in Repair', '='), ('PostgreSQL Record Update: Repair Work', 'PostgreSQL Record: Parts Used; PostgreSQL Record: Parts Shortage; PostgreSQL Record Update: Repair Completion'),",
    "  ('Repair Work Input Form', 'Repair Job Selection Input Form; Parts Used Input Form; Part Request Input Form; Repair Completion Input Form'),\n"
    "  ('Repair Work Output Form', 'Repair Job Output Form; Part Request Output Form'),\n"
    "  ('PostgreSQL Record: Job in Repair', '='), ('PostgreSQL Record Update: Repair Work', 'PostgreSQL Record: Parts Used; PostgreSQL Record: Part Request; PostgreSQL Record Update: Repair Completion'),")
sub("  ('Pickup Notification Input Form', 'Ready Job Selection Input Form; Final Cost Input Form; Send Approval Input Form (open question FR12: removed if the email is automatic)'),",
    "  ('Pickup Notification Input Form', 'Ready Job Selection Input Form; Final Cost Input Form; Send Approval Input Form'),\n"
    "  ('Send Notification Input Form', '= (from the Repair Technician, to 5.4)'),")
sub("  ('Low-Stock Output Form', '='),", "  ('Low-Stock Alert Output Form', '='),")
sub("  ('PostgreSQL Record: Jobs Awaiting Parts', '= ; PostgreSQL Record: Jobs Waiting on PO'),",
    "  ('PostgreSQL Record: Jobs Awaiting Parts', 'PostgreSQL Record: Open Part Requests; PostgreSQL Record: Jobs Waiting on PO'),")
sub("  ('PostgreSQL Record Update: Diagnosis and Quote'", "  ('PostgreSQL Record Update: Diagnosis and Quote'")  # sanity: still one

# DFD front matter
sub('(bottom band, e.g. "Django · bench PC")', '(bottom band, e.g. "Django · bench ThinkPad")')
sub("<p>The implementation is a Django (Python) web application with one PostgreSQL database for both stores, chosen provisionally in the Sprint 3 alternative matrix (415 of 500, against 350 for a repair-shop subscription); the choice reverses if nobody will support the system after December 9. Whether the pickup notification email is sent by staff or automatically (FR12) is open; 5.0 is drawn staff-sent.</p>",
    "<p>The implementation is a Django (Python) web application with one PostgreSQL database for both stores, run in a browser on the stores' Lenovo ThinkPads, chosen provisionally in the Sprint 3 alternative matrix (415 of 500, against 350 for a repair-shop subscription); the choice reverses if nobody will support the system after December 9.</p>\n"
    "<p><b>Owner clarifications (October 23) drawn here.</b> The pickup notification is never automatic: staff or the Technician click Send (5.4; the system fills in the address, so the Technician never sees it). A Manager approves every purchase order (7.3); the Owner no longer does. The system alerts the Manager when a part reaches the reorder point the Manager sets (7.1, 9.3); Technicians request parts (4.4) but never order, and nothing is ordered automatically. Technicians may claim an unassigned job or appointment (3.1); assignment at check-in is optional, and the assignment screens are also open to Manager accounts. A device that could not be repaired owes no diagnostic fee and is settled without a payment (6.3). The optional device passcode (2.4) is needed only for camera repairs.</p>\n"
    "<p><b>To confirm with the owner.</b> Technician sending contradicts the September 21 confirmation #6 (Technicians may not send email); the newer instruction is drawn. Whether a Manager may approve an order they created, and who may see a passcode.</p>")

# ERD notes
sub("signature_file and picked_up_at by 6.4 Close Repair Job (Signature Input Form).",
    "signature_file and picked_up_at by 6.4 Close Repair Job (Signature Input Form); device_passcode by 2.4 Create Repair Job (Passcode Input Form), encrypted before it is stored; assigned_tech_id by 2.4 or, when a technician claims the job, 3.1 Select Repair Job (Job Claim Input Form), which also sets appointment.technician_id.")
sub("EMPLOYEE.store_id is a home store; the Owner sees both stores. Photo ID numbers are never stored, only that the check was done.</p>",
    "EMPLOYEE.store_id is a home store; the Owner sees both stores. Photo ID numbers are never stored, only that the check was done.</p>\n"
    "<h2>Owner clarifications (October 23)</h2>\n"
    "<p>Front desk records the customer's name and phone, the device model and the issue, so device.device_type and brand may be empty. "
    "repair_job.assigned_tech_id and appointment.technician_id may be empty until someone assigns the job or a technician claims it (zero-or-one on the EMPLOYEE side). "
    "repair_job.device_passcode is optional, needed only for camera repairs, stored encrypted and shown only to authorized staff (proposed: the assigned technician, Manager and Owner). "
    "purchase_order.approved_by_id now names a Manager. A job returned unrepaired has no payment row, since there is no diagnostic fee. "
    "store_part_stock.reorder_point is set by the Manager; a low-stock alert is raised when quantity_on_hand reaches it. A part request is a job_part row with part_status Needed.</p>")

p.write_text(s, encoding='utf-8')
print('ok')
