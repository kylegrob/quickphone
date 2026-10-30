# Builds the two physical-model submission PDFs from the rendered diagrams:
#   submission/QuickPhone_Physical_DFD_Set.pdf  front matter + context + complete Level 0 + eight Level 1 diagrams
#   submission/QuickPhone_Physical_ERD_Full.pdf     complete physical ERD + notes
# Run render_slides.ps1 first. Usage: python build_submission.py
import html, os, subprocess, sys
from pypdf import PdfWriter, PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
PHYS = os.path.join(HERE, 'slides', 'physical')
OUT = os.path.join(HERE, 'submission')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# Level 0 flow -> the Level 1 flows it is made of (SAD 8e Ch. 4 balancing). "=" means the same flow appears on
# the Level 1 under the same name. 8.0 is a primitive with no Level 1.
COMPOSITION = [
 ('1.0 Schedule Appointment', [
  ('Appointment Request Input Form', 'Date Picker Input Form; Booking Input Form; Appointment Change Input Form'),
  ('Appointment Schedule Output Form', 'Available Times Output Form; Booking Confirmation Output Form; Change Confirmation Output Form'),
  ('DB Record: Store Hours and Technicians', '='), ('DB Record: Existing Customer', '='), ('DB Record: New Customer', '='),
  ('DB Record Update: Appointment', 'DB Record: New Appointment; DB Record Update: Appointment Change'),
  ('DB Record: Booked Appointments', '= ; DB Record: Appointment to Change')]),
 ('2.0 Register Repair Job', [
  ('Check-In Input Form', 'Phone Search Input Form; Customer Details Input Form; Device Intake Input Form; Technician Assignment Input Form'),
  ('Customer Match Output Form', '='), ('Device Tag Printout', '='), ('Claim Ticket Printout', '= (to the Customer)'),
  ('DB Record: Matching Customers', '='), ('DB Record Update: Customer and Device', 'DB Record Update: Customer; DB Record: New Device'),
  ("DB Record: Today's Appointment", '='), ('DB Record Update: Appointment Checked In', '='),
  ('DB Record: Technician Roster', '='), ('DB Record: Store Contact', '='), ('DB Record: New Repair Job', '=')]),
 ('3.0 Record Diagnosis', [
  ('Diagnosis Input Form', 'Diagnosis Job Selection Input Form; Diagnosis Findings Input Form; Labor Amount Input Form'),
  ('Diagnosis Output Form', 'Assigned Jobs Output Form; Part Availability Output Form'),
  ('Quote Decision Input Form', '='), ('Pending Quotes Output Form', '='),
  ('DB Record: Diagnosis Queue', 'DB Record: Assigned Jobs; DB Record: Pending Quote'),
  ('DB Record Update: Diagnosis and Quote', 'DB Record Update: Diagnosis Findings; DB Record: Part Needed; DB Record: New Quote; DB Record Update: Quote Decision'),
  ('DB Record: Part Availability', '=')]),
 ('4.0 Record Repair Work', [
  ('Repair Work Input Form', 'Repair Job Selection Input Form; Parts Used Input Form; Repair Completion Input Form'),
  ('Repair Work Output Form', 'Repair Job Output Form; Parts Shortage Output Form'),
  ('DB Record: Job in Repair', '='), ('DB Record Update: Repair Work', 'DB Record: Parts Used; DB Record: Parts Shortage; DB Record Update: Repair Completion'),
  ('DB Record: Stock on Hand', '='), ('DB Record Update: Stock Deduction', '=')]),
 ('5.0 Send Pickup Notification', [
  ('Pickup Notification Input Form', 'Ready Job Selection Input Form; Final Cost Input Form; Send Approval Input Form (open question FR12: removed if the email is automatic)'),
  ('Ready Jobs Output Form', '='), ('Email Preview Output Form', '='), ('Pickup Notification Email', '='),
  ('DB Record: Ready Jobs', 'DB Record: Unnotified Ready Jobs; DB Record: Approved Quote Total'),
  ('DB Record Update: Notice Sent', 'DB Record Update: Final Cost; DB Record Update: Email Sent'),
  ('DB Record: Customer Email Address', '='), ('DB Record: Store Pickup Details', '=')]),
 ('6.0 Record Device Release', [
  ('Ticket Lookup Input Form', '='),
  ('Release Input Form', 'Photo ID and Claim Ticket (to manual 6.5, which gives ID Check Input Form); Payment Input Form (from manual 6.6); Signature Input Form'),
  ('Pickup Job Output Form', '= ; Pickup Identity Output Form and Amount Due Output Form (read by staff doing 6.5 and 6.6)'),
  ('Release Receipt Printout', '='), ('DB Record: Customer Name', '='), ('DB Record: Job Awaiting Pickup', '='),
  ('DB Record Update: Payment and Release', 'DB Record: New Payment; DB Record Update: Job Released')]),
 ('7.0 Process Purchase Orders', [
  ('PO Request Input Form', '='), ('Order Placed Input Form', '='), ('Receiving Input Form', '='),
  ('Low-Stock Output Form', '='), ('PO Status Output Form', '='), ('Released Jobs Output Form', '='),
  ('PO Approval Input Form', '='), ('Pending POs Output Form', '='),
  ('DB Record: Jobs Awaiting Parts', '= ; DB Record: Jobs Waiting on PO'),
  ('DB Record Update: Awaiting-Parts Jobs', 'DB Record Update: Job Part Order; DB Record Update: Jobs Released'),
  ('DB Record: Low-Stock Parts', '='), ('DB Record Update: Stock Received', '='),
  ('DB Record: Open Purchase Orders', 'DB Record: POs Pending Approval; DB Record: Approved POs; DB Record: Ordered PO Lines'),
  ('DB Record Update: Purchase Order', 'DB Record: New Purchase Order; DB Record Update: PO Decision; DB Record Update: PO Placed; DB Record Update: PO Received'),
  ('DB Record: Supplier for Order', '=')]),
 ('9.0 Maintain Shop Records', [
  ('Shop Records Input Form', 'Staff Account Input Form; Store Details Input Form; Part Catalog Input Form; Supplier Input Form'),
  ('Shop Records Output Form', 'Staff Account Output Form; Store Details Output Form; Part Catalog Output Form; Supplier Output Form'),
  ('Inventory Import File', '='), ('Import Error Report', '='),
  ('DB Record: Staff and Stores', 'DB Record: Staff Accounts; DB Record: Store Details'),
  ('DB Record Update: Staff and Stores', 'DB Record Update: Staff Account; DB Record Update: Store Details'),
  ('DB Record: Parts Catalog', '= ; DB Record: Existing Part Names'), ('DB Record Update: Parts Catalog', '= ; DB Record: Imported Stock'),
  ('DB Record: Supplier List', '= ; DB Record: Supplier Names'), ('DB Record Update: Supplier List', '=')]),
]

CSS = """@page{size:11in 8.5in;margin:0.55in 0.6in}
body{font-family:'Segoe UI',Arial,sans-serif;color:#222;font-size:10.5pt;line-height:1.38}
h1{color:#1f4e79;font-size:20pt;margin:0 0 2pt}h2{color:#1f4e79;font-size:13pt;margin:14pt 0 4pt}
.sub{color:#555;margin:0 0 10pt}p{margin:0 0 6pt}
table{border-collapse:collapse;width:100%;font-size:9pt}td,th{border:1px solid #c9d3de;padding:3pt 5pt;vertical-align:top;text-align:left}
th{background:#1f4e79;color:#fff}td.p{background:#eef3f8;font-weight:700;color:#1f4e79}
.cols{display:flex;gap:22pt}.cols>div{flex:1}.brk{page-break-before:always}ol{margin:0 0 6pt 16pt;padding:0}li{margin:0 0 2pt}
code{font-family:Consolas,monospace;font-size:9.5pt}"""


def print_pdf(html_text, out_pdf):
    tmp = out_pdf.replace('.pdf', '.html')
    open(tmp, 'w', encoding='utf-8').write(html_text)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                    '--print-to-pdf=' + out_pdf, 'file:///' + tmp.replace('\\', '/')], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)


def dfd_front():
    e = html.escape
    rows = []
    for proc, flows in COMPOSITION:
        rows.append('<tr><td class="p" colspan="2">%s</td></tr>' % e(proc))
        for l0, l1 in flows:
            l1 = l1.replace('= ;', 'Same name on Level 1; also').replace('=', 'Same name on Level 1') if l1.startswith('=') else l1
            rows.append('<tr><td>%s</td><td>%s</td></tr>' % (e(l0), e(l1)))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<h1>QuickPhone Repair Tracking System: Physical Data Flow Diagrams</h1>
<p class="sub">MIS 4173 Sprint 3 · Team 4 · Method: Dennis, Wixom, Roth &amp; Haley, <i>Systems Analysis and Design</i>, 8th ed., Ch. 4 and Ch. 9</p>
<div class="cols"><div>
<h2>Contents</h2><ol>
<li>Context diagram: the whole system as process 0 and its five external entities.</li>
<li>Level 0 diagram, complete: nine processes, seven data stores, five entities, each drawn once.</li>
<li>Level 1 diagrams for 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0 and 9.0. Process 8.0 Report Repair Status is a read-only primitive with no Level 1.</li>
</ol>
<p>The slide deck shows the same Level 0 in four slide-sized parts; they contain no flows that are not on the complete diagram.</p>
<h2>How the logical DFDs were made physical (Fig. 9-1)</h2>
<ol>
<li><b>Implementation references.</b> Each process names how it runs (bottom band, e.g. "Django · bench PC"). Each data store is a group of tables in the PostgreSQL database, named "PostgreSQL: …" with its tables listed. Each data flow names its medium.</li>
<li><b>Human–machine boundary.</b> As in Figs. 9-2 and 9-4, a dashed red line around each person who uses the system's screens: Front Desk, Technician, Manager and Owner. The two manual steps in 6.0 (check photo ID, take payment on the unlinked card machine) are human action and sit inside the Front Desk's line. The Customer has no line: like the Customer Service Department in Fig. 9-2, the customer only receives a printout and an email and never uses the system's screens.</li>
<li><b>System-related components.</b> 9.5 Import Inventory File (one-time CSV load) with its import file and error report; audit tables job_status_history and inventory_txn inside D3 and D4.</li>
<li><b>Data elements.</b> Each flow carries the elements listed for its logical counterpart in the data flow dictionary (models document, Appendix B), under the physical field names of the ERD, plus system fields such as time stamps and who made the change.</li>
</ol>
</div><div>
<h2>How to read a flow name</h2>
<p>Following Figs. 9-2 and 9-4, every line is one data flow with one noun name that says what it is and how it travels:</p>
<table><tr><th>Name pattern</th><th>Meaning</th></tr>
<tr><td><code>… Input Form</code></td><td>A screen a person fills in; data goes into the system.</td></tr>
<tr><td><code>… Output Form</code></td><td>A screen the system shows a person.</td></tr>
<tr><td><code>… Printout</code>, <code>… Email</code>, <code>… File</code>, <code>… Report</code></td><td>Printed paper, the email sent from the store's account, an uploaded file, a generated report.</td></tr>
<tr><td><code>PostgreSQL Record: …</code></td><td>Rows read from, or a new row added to, the store the line touches.</td></tr>
<tr><td><code>PostgreSQL Record Update: …</code></td><td>Existing rows changed in the store the line touches.</td></tr></table>
<p style="margin-top:6pt">A Level 0 flow that groups several screens (for example <i>Check-In Input Form</i>) splits into named parts on its Level 1; the table that follows lists every split, so each Level 1 balances with Level 0. Lines run only horizontally and vertically and cross at right angles (Ch. 4).</p>
<h2>Assumptions and open items</h2>
<p>The implementation is a Django (Python) web application with one PostgreSQL database for both stores, chosen provisionally in the Sprint 3 alternative matrix (415 of 500, against 350 for a repair-shop subscription); the choice reverses if nobody will support the system after December 9. Whether the pickup notification email is sent by staff or automatically (FR12) is open; 5.0 is drawn staff-sent.</p>
</div></div>
<div class="brk"></div>
<h1>Balancing: Level 0 flows and their Level 1 parts</h1>
<p class="sub">Every flow into or out of a Level 0 process appears on its Level 1 diagram, under the same name or split into the named parts below (SAD 8e Ch. 4, balancing).</p>
<table><tr><th style="width:34%">Level 0 flow</th><th>Level 1 flows</th></tr>{''.join(rows)}</table>
</body></html>"""


def erd_notes():
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<h1>QuickPhone Repair Tracking System: Physical ERD notes</h1>
<p class="sub">MIS 4173 Sprint 3 · Team 4 · Method: Dennis, Wixom, Roth &amp; Haley, <i>Systems Analysis and Design</i>, 8th ed., Ch. 5 and Ch. 10</p>
<div class="cols"><div>
<h2>Logical to physical (Fig. 10-7)</h2><ol>
<li><b>Entities to tables.</b> Sixteen tables in snake_case; each header names the DFD data store (D1–D7) that holds it, so the ERD and the DFDs stay balanced.</li>
<li><b>Attributes to fields.</b> Each field has a data type and size (VARCHAR, INTEGER, DECIMAL, TIMESTAMP, BOOLEAN), NN for not null, and CK where only listed values are allowed (statuses, roles, payment method). Each field's default and valid values (Fig. 10-9) are in the models document, Appendix A.</li>
<li><b>Primary keys.</b> Every table has one (PK); store_part_stock uses the pair store_id + part_id.</li>
<li><b>Foreign keys.</b> Every relationship is a foreign key in the child table (FK, with the parent table named). Every foreign key is drawn as a line with crow's-foot cardinality, and each line is named both ways, as in Fig. 10-8 ("Places / Is Placed By"): the first name reads from the "one" side to the "many" side, the second reads back (Ch. 5).</li>
<li><b>System-related components.</b> Each field the physical DFD adds is stored where its flow writes it: password_hash by 9.1 Maintain Staff Accounts (Staff Account Input Form); ticket_number by 2.4 Create Repair Job, printed by 2.5 on the Claim Ticket and Device Tag Printouts; email_sent_at, email_sent_by_id and email_status by 5.5 Record Notification Result (Email Send Result); id_verified_flag by 6.2 Record Identity Check (ID Check Input Form); signature_file and picked_up_at by 6.4 Close Repair Job (Signature Input Form). The audit tables take a row from every status change (job_status_history) and from 4.3, 7.5, 9.3 and the 9.5 Inventory Import File batch (inventory_txn); created_at and the other time stamps are set by the application on save. The Import Error Report goes back to the Manager and is not stored.</li>
</ol></div><div>
<h2>Documented denormalizations</h2>
<p>The logical ERD is in third normal form. Three fields marked <i>derived</i> are stored on purpose for speed and are kept correct by the program (Ch. 10, optimizing storage):</p>
<ul><li><code>repair_job.status</code>: the latest row of job_status_history.</li>
<li><code>quote.total_amount</code>: labor_amount + parts_amount.</li>
<li><code>store_part_stock.quantity_on_hand</code>: the sum of inventory_txn.quantity_change.</li></ul>
<h2>Assumptions</h2>
<p>Types are standard SQL, all valid in PostgreSQL, the chosen DBMS. DEVICE stays its own table inside D1: storage is optimized table by table (no repeated customer data, few nulls; Ch. 10), so a separate data store would save nothing. EMPLOYEE.store_id is a home store; the Owner sees both stores. Photo ID numbers are never stored, only that the check was done.</p>
</div></div></body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    front = os.path.join(OUT, '_front.pdf'); print_pdf(dfd_front(), front)
    notes = os.path.join(OUT, '_erd_notes.pdf'); print_pdf(erd_notes(), notes)
    dfd = [front] + [os.path.join(PHYS, f) for f in sorted(os.listdir(PHYS))
                     if f.endswith('.pdf') and (f.startswith(('01_', '02_')) or '_Level1_' in f)]
    for parts, name in ((dfd, 'QuickPhone_Physical_DFD_Set.pdf'),
                        ([os.path.join(PHYS, 'ERD_Full_Physical.pdf'), notes], 'QuickPhone_Physical_ERD_Full.pdf')):
        w = PdfWriter()
        for p in parts:
            for page in PdfReader(p).pages: w.add_page(page)
        w.write(os.path.join(OUT, name))
        print(name, len(w.pages), 'pages:', ', '.join(os.path.basename(p) for p in parts))
    os.remove(front); os.remove(notes)


if __name__ == '__main__':
    main()
