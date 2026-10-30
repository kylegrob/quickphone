# Oct 24 (user): "Screen" is a medium, not part of what the data is. Physical flows the system shows a person now carry
# only the data name; lists end in "List" where the data is a list. Applies to dfd_slides.html and build_submission.py.
import pathlib, sys

RENAME = {
 'Appointment Schedule Screen': 'Appointment Schedule',
 'Available Times Screen': 'Available Times',
 'Booking Confirmation Screen': 'Booking Confirmation',
 'Change Confirmation Screen': 'Change Confirmation',
 'Matching Customers Screen': 'Matching Customers',
 'Pending Quotes Screen': 'Pending Quotes List',
 'Diagnosis Worklist Screen': 'Diagnosis Worklist',
 'Job Queue Screen': 'Job Queue',
 'Part Availability Screen': 'Part Availability',
 'Repair Worklist Screen': 'Repair Worklist',
 'Repair Job Details Screen': 'Repair Job Details',
 'Part Request Confirmation Screen': 'Part Request Confirmation',
 'Ready Jobs Screen': 'Ready Jobs List',
 'Email Preview Screen': 'Email Preview',
 'Pickup Job Screen': 'Pickup Jobs List',
 'Customer Identity Screen': 'Customer Identity',
 'Amount Due Screen': 'Amount Due',
 'Job Status Screen': 'Job Status List',
 'Status Dashboard Screen': 'Status List',
 'Low-Stock Alert Screen': 'Low Stock Alert List',
 'Purchase Order Status Screen': 'Purchase Order Status List',
 'Released Jobs Screen': 'Released Jobs List',
 'Pending Purchase Orders Screen': 'Pending Purchase Orders List',
 'Shop Record Confirmation Screen': 'Shop Record Confirmation',
 'Staff Account Confirmation Screen': 'Staff Account Confirmation',
 'Store Details Confirmation Screen': 'Store Details Confirmation',
 'Part Catalog Confirmation Screen': 'Part Catalog Confirmation',
 'Supplier Confirmation Screen': 'Supplier Confirmation',
}
here = pathlib.Path(__file__).parent
for fn in ('dfd_slides.html', 'build_submission.py'):
    p = here / fn; s = p.read_text(encoding='utf-8')
    for old in sorted(RENAME, key=len, reverse=True):
        s = s.replace(old, RENAME[old])
    p.write_text(s, encoding='utf-8')
    print(fn, [l for l in s.splitlines() if 'Screen' in l][:8])
