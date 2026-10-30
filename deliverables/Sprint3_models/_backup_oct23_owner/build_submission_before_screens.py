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
  ('PostgreSQL Record: Store Hours and Technicians', '='), ('PostgreSQL Record: Existing Customer', '='), ('PostgreSQL Record: New Customer', '='),
  ('PostgreSQL Record Update: Appointment', 'PostgreSQL Record: New Appointment; PostgreSQL Record Update: Appointment Change'),
  ('PostgreSQL Record: Booked Appointments', '= ; PostgreSQL Record: Appointment to Change')]),
 ('2.0 Register Repair Job', [
  ('Check-In Input Form', 'Phone Search Input Form; Customer Details Input Form; Device Intake Input Form; Passcode Input Form; Technician Assignment Input Form'),
  ('Customer Match Output Form', '='), ('Device Tag Printout', '='), ('Claim Ticket Printout', '= (to the Customer)'),
  ('PostgreSQL Record: Matching Customers', '='), ('PostgreSQL Record Update: Customer and Device', 'PostgreSQL Record Update: Customer; PostgreSQL Record: New Device'),
  ("PostgreSQL Record: Today's Appointment", '='), ('PostgreSQL Record Update: Appointment Checked In', '='),
  ('PostgreSQL Record: Technician Roster', '='), ('PostgreSQL Record: Store Contact', '='), ('PostgreSQL Record: New Repair Job', '=')]),
 ('3.0 Record Diagnosis', [
  ('Diagnosis Input Form', 'Diagnosis Job Selection Input Form; Job Claim Input Form; Diagnosis Findings Input Form; Labor Amount Input Form'),
  ('Diagnosis Output Form', 'Job Queue Output Form; Part Availability Output Form'),
  ('Quote Decision Input Form', '='), ('Pending Quotes Output Form', '='),
  ('PostgreSQL Record: Diagnosis Queue', 'PostgreSQL Record: Open Jobs; PostgreSQL Record: Pending Quote'),
  ('PostgreSQL Record Update: Diagnosis and Quote', 'PostgreSQL Record Update: Job Claimed; PostgreSQL Record Update: Diagnosis Findings; PostgreSQL Record: Part Needed; PostgreSQL Record: New Quote; PostgreSQL Record Update: Quote Decision'),
  ('PostgreSQL Record: Unassigned Appointments', '='), ('PostgreSQL Record Update: Appointment Claimed', '='),
  ('PostgreSQL Record: Part Availability', '=')]),
 ('4.0 Record Repair Work', [
  ('Repair Work Input Form', 'Repair Job Selection Input Form; Parts Used Input Form; Part Request Input Form; Repair Completion Input Form'),
  ('Repair Work Output Form', 'Repair Job Output Form; Part Request Output Form'),
  ('PostgreSQL Record: Job in Repair', '='), ('PostgreSQL Record Update: Repair Work', 'PostgreSQL Record: Parts Used; PostgreSQL Record: Part Request; PostgreSQL Record Update: Repair Completion'),
  ('PostgreSQL Record: Stock on Hand', '='), ('PostgreSQL Record Update: Stock Deduction', '=')]),
 ('5.0 Send Pickup Notification', [
  ('Pickup Notification Input Form', 'Ready Job Selection Input Form; Final Cost Input Form; Send Approval Input Form'),
  ('Send Notification Input Form', '= (from the Repair Technician, to 5.4)'),
  ('Ready Jobs Output Form', '='), ('Email Preview Output Form', '='), ('Pickup Notification Email', '='),
  ('PostgreSQL Record: Ready Jobs', 'PostgreSQL Record: Unnotified Ready Jobs; PostgreSQL Record: Approved Quote Total'),
  ('PostgreSQL Record Update: Notice Sent', 'PostgreSQL Record Update: Final Cost; PostgreSQL Record Update: Email Sent'),
  ('PostgreSQL Record: Customer Email Address', '='), ('PostgreSQL Record: Store Pickup Details', '=')]),
 ('6.0 Record Device Release', [
  ('Ticket Lookup Input Form', '='),
  ('Release Input Form', 'Photo ID and Claim Ticket (to manual 6.5, which gives ID Check Input Form); Payment Input Form (from manual 6.6); Signature Input Form'),
  ('Pickup Job Output Form', '= ; Pickup Identity Output Form and Amount Due Output Form (read by staff doing 6.5 and 6.6)'),
  ('Release Receipt Printout', '='), ('PostgreSQL Record: Customer Name', '='), ('PostgreSQL Record: Job Awaiting Pickup', '='),
  ('PostgreSQL Record Update: Payment and Release', 'PostgreSQL Record: New Payment; PostgreSQL Record Update: Job Released')]),
 ('7.0 Process Purchase Orders', [
  ('PO Request Input Form', '='), ('Order Placed Input Form', '='), ('Receiving Input Form', '='),
  ('Low-Stock Alert Output Form', '='), ('PO Status Output Form', '='), ('Released Jobs Output Form', '='),
  ('PO Approval Input Form', '='), ('Pending POs Output Form', '='),
  ('PostgreSQL Record: Jobs Awaiting Parts', 'PostgreSQL Record: Open Part Requests; PostgreSQL Record: Jobs Waiting on PO'),
  ('PostgreSQL Record Update: Awaiting-Parts Jobs', 'PostgreSQL Record Update: Job Part Order; PostgreSQL Record Update: Jobs Released'),
  ('PostgreSQL Record: Low-Stock Parts', '='), ('PostgreSQL Record Update: Stock Received', '='),
  ('PostgreSQL Record: Open Purchase Orders', 'PostgreSQL Record: POs Pending Approval; PostgreSQL Record: Approved POs; PostgreSQL Record: Ordered PO Lines'),
  ('PostgreSQL Record Update: Purchase Order', 'PostgreSQL Record: New Purchase Order; PostgreSQL Record Update: PO Decision; PostgreSQL Record Update: PO Placed; PostgreSQL Record Update: PO Received'),
  ('PostgreSQL Record: Supplier for Order', '=')]),
 ('9.0 Maintain Shop Records', [
  ('Shop Records Input Form', 'Staff Account Input Form; Store Details Input Form; Part Catalog Input Form; Supplier Input Form'),
  ('Shop Records Output Form', 'Staff Account Output Form; Store Details Output Form; Part Catalog Output Form; Supplier Output Form'),
  ('Inventory Import File', '='), ('Import Error Report', '='),
  ('PostgreSQL Record: Staff and Stores', 'PostgreSQL Record: Staff Accounts; PostgreSQL Record: Store Details'),
  ('PostgreSQL Record Update: Staff and Stores', 'PostgreSQL Record Update: Staff Account; PostgreSQL Record Update: Store Details'),
  ('PostgreSQL Record: Parts Catalog', '= ; PostgreSQL Record: Existing Part Names'), ('PostgreSQL Record Update: Parts Catalog', '= ; PostgreSQL Record: Imported Stock'),
  ('PostgreSQL Record: Supplier List', '= ; PostgreSQL Record: Supplier Names'), ('PostgreSQL Record Update: Supplier List', '=')]),
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
<li><b>Implementation references.</b> Each process names how it runs (bottom band, e.g. "Django · bench ThinkPad"). Each data store is a group of tables in the PostgreSQL database, named "PostgreSQL: …" with its tables listed. Each data flow names its medium.</li>
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
<p>The implementation is a Django (Python) web application with one PostgreSQL database for both stores, run in a browser on the stores' Lenovo ThinkPads, chosen provisionally in the Sprint 3 alternative matrix (415 of 500, against 350 for a repair-shop subscription); the choice reverses if nobody will support the system after December 9.</p>
<p>The owner's clarifications of October 23 are drawn; the next page lists where each one appears.</p>
</div></div>
<div class="brk"></div>
<h1>Owner clarifications of October 23: where they are drawn</h1>
<p class="sub">Each answer from the owner, and the processes and flows that changed because of it.</p>
<table><tr><th style="width:30%">Owner's answer</th><th>Where it is drawn</th></tr>
<tr><td>1. Pickup notification is sent by a click from the Technician or authorized staff, never automatically</td><td>5.4 Send Email Message takes Send Approval Input Form (Front Desk, Manager, Owner) or Send Notification Input Form (Repair Technician, new on the context, the complete Level 0 and Level 0 part 3). The system fills in the customer's address from D1, so the Technician never sees it. <b>To confirm:</b> this reverses the September 21 confirmation #6 (Technicians may not send email); the newer instruction is drawn.</td></tr>
<tr><td>2. A Manager approves every purchase order; no Owner approval</td><td>7.3 Record Purchase Order Approval: Pending POs Output Form and PO Approval Input Form now go to and from the Store Manager; the Store Owner keeps only 8.0. <b>To confirm:</b> whether a Manager may approve an order they created.</td></tr>
<tr><td>3. Low-stock alerts, technician part requests, Manager-only purchasing, no automatic ordering</td><td>7.1 List Parts to Order sends the Low-Stock Alert Output Form with the open part requests; 4.4 Record Part Request takes a Part Request Input Form from the Technician. Orders are placed off-system by the Manager (7.4); no process orders automatically and no Technician flow reaches 7.0.</td></tr>
<tr><td>4. Manual assignment; technicians may assign themselves</td><td>3.1 Select Repair Job lists the technician's jobs with the unassigned jobs and appointments (D2, new on 3.0) and takes a Job Claim Input Form. The Technician Assignment Input Form at 2.4 is optional; the Front Desk assignment screens are also open to Manager accounts.</td></tr>
<tr><td>5. No diagnostic fee when a device cannot be repaired</td><td>6.3 Record Payment passes a Returned Unrepaired job on as a Settled Job with no payment row.</td></tr>
<tr><td>6. Managers set each part's reorder point</td><td>Unchanged: the Part Catalog Input Form at 9.3 carries the reorder point per store; 7.1 alerts when stock reaches it.</td></tr>
<tr><td>7. Intake fields; optional passcode, needed only for camera repairs, stored securely</td><td>2.4 Create Repair Job takes an optional Passcode Input Form and stores it encrypted with the job. <b>To confirm:</b> who may see a passcode.</td></tr>
<tr><td>8. Stores use Lenovo ThinkPad computers</td><td>Context and bench process bands name the stores' ThinkPads.</td></tr>
<tr><td>Fixed at the same time</td><td>4.0: the Stock Shortage line from 4.2 now ends on 4.4 (it ended on 4.3). The balancing table that follows now uses the PostgreSQL flow names shown on the diagrams.</td></tr>
</table>
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
<li><b>Attributes to fields.</b> Each field has a data type and size (VARCHAR, INTEGER, DECIMAL, TIMESTAMP, BOOLEAN), NN for not null, and CK where only listed values are allowed. Defaults and valid values (Fig. 10-9) are in the models document, Appendix A.</li>
<li><b>Primary keys.</b> Every table has one (PK); store_part_stock uses the pair store_id + part_id.</li>
<li><b>Foreign keys.</b> Every relationship is a foreign key in the child table (FK, with the parent table named). Every foreign key is drawn as a line with crow's-foot cardinality, and each line is named both ways, as in Fig. 10-8 ("Places / Is Placed By"): the first name reads from the "one" side to the "many" side, the second reads back (Ch. 5).</li>
<li><b>System-related components.</b> Each field the physical DFD adds is stored where its flow writes it: password_hash by 9.1 Maintain Staff Accounts (Staff Account Input Form); ticket_number by 2.4 Create Repair Job, printed by 2.5 on the Claim Ticket and Device Tag Printouts; email_sent_at, email_sent_by_id and email_status by 5.5 Record Notification Result (Email Send Result); id_verified_flag by 6.2 Record Identity Check (ID Check Input Form); signature_file and picked_up_at by 6.4 Close Repair Job (Signature Input Form); device_passcode, encrypted, by 2.4 (Passcode Input Form); assigned_tech_id by 2.4 or by a claim at 3.1 (Job Claim Input Form). The audit tables take a row from every status change (job_status_history) and from 4.3, 7.5, 9.3 and the 9.5 Inventory Import File batch (inventory_txn); time stamps are set on save. The Import Error Report is not stored.</li>
</ol></div><div>
<h2>Documented denormalizations</h2>
<p>The logical ERD is in third normal form. Three fields marked <i>derived</i> are stored on purpose for speed and are kept correct by the program (Ch. 10, optimizing storage):</p>
<ul><li><code>repair_job.status</code>: the latest row of job_status_history.</li>
<li><code>quote.total_amount</code>: labor_amount + parts_amount.</li>
<li><code>store_part_stock.quantity_on_hand</code>: the sum of inventory_txn.quantity_change.</li></ul>
<h2>Assumptions</h2>
<p>Types are standard SQL, all valid in PostgreSQL, the chosen DBMS. DEVICE stays its own table inside D1: storage is optimized table by table (no repeated customer data, few nulls; Ch. 10), so a separate data store would save nothing. EMPLOYEE.store_id is a home store; the Owner sees both stores. Photo ID numbers are never stored, only that the check was done.</p>
<h2>Owner clarifications (October 23)</h2>
<p>device_type and brand are optional (intake records name, phone, model and issue). assigned_tech_id and appointment.technician_id stay empty until a job is assigned or claimed. device_passcode is optional, encrypted, for authorized staff only (proposed: assigned technician, Manager, Owner). approved_by_id names a Manager. An unrepaired job has no payment row (no diagnostic fee). The Manager sets reorder_point; a part request is a job_part row with part_status Needed.</p>
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
