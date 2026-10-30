# Oct 23 (user): "Output Form" read as if alerts and confirmations were forms, and some names did not say what the
# data is ("Part Request Output Form" was the confirmation). New rule for physical flows to and from people:
#   ... Input Form  = a form a person fills in on screen (data goes into the system)
#   ... Screen      = something the system shows a person (data comes out)
# Every name says what the data is; "purchase order" is spelled out. Printout, Email, File, Report and the
# PostgreSQL Record names are unchanged. Applies to dfd_slides.html (physical view) and build_submission.py.
import pathlib, sys

RENAME = {
 # system shows a person -> Screen
 'Amount Due Output Form': 'Amount Due Screen',
 'Appointment Schedule Output Form': 'Appointment Schedule Screen',
 'Available Times Output Form': 'Available Times Screen',
 'Booking Confirmation Output Form': 'Booking Confirmation Screen',
 'Change Confirmation Output Form': 'Change Confirmation Screen',
 'Customer Match Output Form': 'Matching Customers Screen',
 'Diagnosis Output Form': 'Diagnosis Worklist Screen',
 'Email Preview Output Form': 'Email Preview Screen',
 'Job Queue Output Form': 'Job Queue Screen',
 'Job Status Output Form': 'Job Status Screen',
 'Low-Stock Alert Output Form': 'Low-Stock Alert Screen',
 'PO Status Output Form': 'Purchase Order Status Screen',
 'Part Availability Output Form': 'Part Availability Screen',
 'Part Catalog Output Form': 'Part Catalog Confirmation Screen',
 'Part Request Output Form': 'Part Request Confirmation Screen',
 'Pending POs Output Form': 'Pending Purchase Orders Screen',
 'Pending Quotes Output Form': 'Pending Quotes Screen',
 'Pickup Identity Output Form': 'Customer Identity Screen',
 'Pickup Job Output Form': 'Pickup Job Screen',
 'Ready Jobs Output Form': 'Ready Jobs Screen',
 'Released Jobs Output Form': 'Released Jobs Screen',
 'Repair Job Output Form': 'Repair Job Details Screen',
 'Repair Work Output Form': 'Repair Worklist Screen',
 'Shop Records Output Form': 'Shop Record Confirmation Screen',
 'Staff Account Output Form': 'Staff Account Confirmation Screen',
 'Status Dashboard Output Form': 'Status Dashboard Screen',
 'Store Details Output Form': 'Store Details Confirmation Screen',
 'Supplier Output Form': 'Supplier Confirmation Screen',
 # person fills in -> Input Form, renamed where the name did not say what the data is
 'Date Picker Input Form': 'Requested Date Input Form',
 'Diagnosis Input Form': 'Diagnosis Details Input Form',
 'Pickup Notification Input Form': 'Notification Approval Input Form',
 'Release Input Form': 'Release Authorization Input Form',
 'Receiving Input Form': 'Received Quantities Input Form',
 'PO Request Input Form': 'Purchase Order Request Input Form',
 'PO Approval Input Form': 'Purchase Order Approval Input Form',
}

here = pathlib.Path(__file__).parent

# diagrams: names sit in quotes in the flow definitions
p = here / 'dfd_slides.html'
s = p.read_text(encoding='utf-8')
for old, new in RENAME.items():
    c = s.count(f"'{old}'")
    if c == 0:
        sys.exit(f'not in dfd_slides.html: {old}')
    s = s.replace(f"'{old}'", f"'{new}'")
p.write_text(s, encoding='utf-8')

# PDF front matter: balancing table, reading guide, clarifications page. Longest names first so a name that
# contains another ("Diagnosis Input Form" inside nothing, but be safe) is replaced whole.
p = here / 'build_submission.py'
s = p.read_text(encoding='utf-8')
for old in sorted(RENAME, key=len, reverse=True):
    s = s.replace(old, RENAME[old])
for old, new in [
    ("<tr><td><code>… Input Form</code></td><td>A screen a person fills in; data goes into the system.</td></tr>\n"
     "<tr><td><code>… Output Form</code></td><td>A screen the system shows a person.</td></tr>",
     "<tr><td><code>… Input Form</code></td><td>A form on screen that a person fills in; data goes into the system.</td></tr>\n"
     "<tr><td><code>… Screen</code></td><td>Something the system shows a person: a list, an alert, a confirmation; data comes out of the system.</td></tr>"),
    ("(for example <i>Check-In Input Form</i>)", "(for example <i>Check-In Input Form</i> or <i>Diagnosis Worklist Screen</i>)"),
]:
    if s.count(old) != 1:
        sys.exit(f'front matter: {old[:60]!r}')
    s = s.replace(old, new)
left = [o for o in RENAME if o in s]
if 'Output Form' in s or left:
    sys.exit(f'left in build_submission.py: {left} / Output Form x{s.count("Output Form")}')
p.write_text(s, encoding='utf-8')
print(len(RENAME), 'names renamed')
