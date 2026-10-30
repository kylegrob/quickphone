# Oct 23: carry the owner's clarifications and the Screen/Input Form names into "Sprint 3 - DFD and ERD Models.docx":
# Appendix B (data flow dictionary) rows, Appendix A (physical data dictionary) cells, and the body text (Table 3.1,
# section 5, section 6, Tables 7.1 and 7.2, the appointment decision). Images are swapped separately
# (update_models_docx.py <docx> <docx> images). Edits the repo copy in place after every check passes.
import os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import replace_in_para, para_text, esc, html_unescape
from oct23_tech_text import edit_xml

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DOCX = os.path.join(REPO, 'docs', 'sprint-3', 'drafts', 'Sprint 3 - DFD and ERD Models.docx')
OWN = ' (owner, Oct 23)'

z = zipfile.ZipFile(DOCX)
d = z.read('word/document.xml').decode('utf-8')
z.close()
d = re.sub(r'<w:t xml:space="preserve"/>', '<w:t xml:space="preserve"></w:t>', d)


def cells_of(row):
    return re.findall(r'<w:tc>.*?</w:tc>', row, re.S)


def set_cell(cell, text):
    ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', cell))
    assert ts, 'cell without a run'
    out = cell[:ts[0].start()] + '<w:t xml:space="preserve">' + esc(text) + '</w:t>'
    for a, b in zip(ts, ts[1:]):
        out += cell[a.end():b.start()] + '<w:t xml:space="preserve"></w:t>'
    return out + cell[ts[-1].end():]


def set_row(row, values):
    cs = cells_of(row)
    for i, v in values.items():
        row = row.replace(cs[i], set_cell(cs[i], v), 1)
    return row


# ======================= Appendix A: physical data dictionary =======================
a0, a1 = d.find('Appendix A. Physical data dictionary'), d.find('Appendix B. Data flow dictionary')
A = d[a0:a1]


def table_after(label):
    i = A.find(label)
    assert i > 0, label
    m = re.compile(r'<w:tbl>.*?</w:tbl>', re.S).search(A, i)
    return m


def edit_column(table_label, column, values, insert_after=None):
    """values: {cell index: text}. Cells: 0 Key, 1 Column, 2 Type, 3 Null, 4 Default, 5 Valid values."""
    global A
    m = table_after(table_label)
    t = m.group(0)
    rows = re.findall(r'<w:tr[ >].*?</w:tr>', t, re.S)
    hit = [r for r in rows if para_text(cells_of(r)[1]).startswith(column + ' ')]
    assert len(hit) == 1, (table_label, column, len(hit))
    r = hit[0]
    if insert_after:   # clone this row as a new row after it
        t2 = t.replace(r, r + set_row(r, values), 1)
    else:
        t2 = t.replace(r, set_row(r, values), 1)
    A = A[:m.start()] + t2 + A[m.end():]


edit_column('(logical DEVICE;', 'device_type', {3: 'null', 5: 'optional' + OWN})
edit_column('(logical DEVICE;', 'brand', {3: 'null', 5: 'optional' + OWN})
edit_column('(logical APPOINTMENT;', 'technician_id', {3: 'null', 5: 'empty until assigned or claimed' + OWN})
edit_column('(logical REPAIR_JOB;', 'assigned_tech_id', {3: 'null', 5: 'empty until assigned or claimed' + OWN})
edit_column('(logical REPAIR_JOB;', 'reported_issue',
            {0: '', 1: 'device_passcode  (DevicePasscode)', 2: 'VARCHAR(255)', 3: 'null', 4: '',
             5: 'optional; stored encrypted; needed for camera replacements; authorized staff only' + OWN}, insert_after=True)
edit_column('(logical PURCHASE_ORDER;', 'approved_by_id', {5: 'a Manager' + OWN})
edit_column('(logical STORE_PART_STOCK;', 'reorder_point', {5: '>= 0; set by the Manager' + OWN})
edit_column('(logical JOB_PART;', 'part_status', {5: 'Needed (a part request), Used'})
d = d[:a0] + A + d[a1:]

# ======================= Appendix B: data flow dictionary =======================
start = d.find('Appendix B. Data flow dictionary')
head, tail = d[:start], d[start:]
tables = list(re.finditer(r'<w:tbl>.*?</w:tbl>', tail, re.S))
assert len(tables) == 9, len(tables)
TPL, data = {}, []
for t in tables:
    rows = re.findall(r'<w:tr[ >].*?</w:tr>', t.group(0), re.S)
    out = []
    for r in rows[1:]:
        cells = [para_text(c) for c in cells_of(r)]
        l0 = 'F2F6FA' in r
        TPL.setdefault(l0, r)
        out.append(dict(name=cells[0], ft=cells[1], lvl=cells[2], desc=cells[3], l0=l0))
    data.append(dict(hdr=rows[0], rows=out, xml=t.group(0)))


def tab(n): return data[n - 1]['rows']
def find(rows, name):
    m = [r for r in rows if r['name'] == name]
    assert len(m) == 1, (name, len(m)); return m[0]
def ren(rows, old, new, **kw):
    r = find(rows, old); r['name'] = new; r.update(kw); return r
def upd(rows, name, **kw):
    r = find(rows, name); r.update(kw); return r
def insert_after(rows, anchor, l0=False, **kw):
    kw.setdefault('lvl', 'Level 0 flow' if l0 else '')
    kw['l0'] = l0
    rows.insert(rows.index(find(rows, anchor)) + 1, kw)
def sub_all(old, new):
    n = 0
    for t in data:
        for r in t['rows']:
            for k in ('ft', 'lvl', 'desc'):
                if old in r[k]:
                    r[k] = r[k].replace(old, new); n += 1
    assert n, old


sub_all('3.1 Retrieve Assigned Jobs', '3.1 Select Repair Job')
sub_all('4.4 Record Parts Shortage', '4.4 Record Part Request')

# 1.0: the technician on an appointment is optional
t = tab(1)
upd(t, 'Chosen time slot', desc='ScheduledAt and StoreID of the slot the customer picked, with its TechnicianID if one was chosen.')
upd(t, 'Appointment booking', desc='New APPOINTMENT (CustomerID, StoreID, ScheduledAt, ApptStatus = Booked, and TechnicianID if one was chosen; '
    'otherwise a technician may claim it in 3.1).')

# 2.0: optional passcode, optional technician
t = tab(2)
upd(t, 'Check-in details', desc="Customer phone; new or changed customer details; the DeviceID of a device already on file, or a new device's "
    "Model (DeviceType, Brand and SerialOrIMEI optional); ReportedIssue and IntakeCondition; an optional device passcode; the "
    "assigned technician, if one is chosen. Splits into Customer phone number, Customer details, Device intake details, Device "
    "passcode, and Technician assignment.")
upd(t, 'New repair job', desc='New REPAIR_JOB (TicketNumber, DeviceID, StoreID, AppointmentID, AssignedTechID if one was chosen, ReportedIssue, '
    'DevicePasscode if given, encrypted, IntakeCondition, CheckInAt) and its first JOB_STATUS_HISTORY row (Status = Checked In).')
insert_after(t, 'Registered device', name='Device passcode', ft='Front Desk Staff → 2.4 Create Repair Job', lvl='Part of Check-in details',
             desc='DevicePasscode, optional: needed only for a camera replacement; stored encrypted and shown only to authorized staff' + OWN + '.')
upd(t, 'Technician assignment', desc='EmployeeID of the technician chosen for the job, if any. Staff or a Manager assign by hand, or a '
    'technician claims the job later in 3.1' + OWN + '.')

# 3.0: technicians claim unassigned jobs and appointments
t = tab(3)
upd(t, 'Diagnosis worklist', desc="The technician's job queue, with the unassigned jobs and appointments they may claim, and the stock of the "
    "parts needed. Splits into Job queue and Part availability.")
upd(t, 'Diagnosis details', desc='The job chosen or claimed, the DiagnosisNotes and the labor charge. Splits into Job to diagnose, Job claim, '
    'Diagnosis and Labor amount.')
upd(t, 'Diagnosis queue', desc="The technician's REPAIR_JOB rows, the unassigned ones at the store, and the QUOTE rows awaiting a decision. "
    "Splits into Own and unassigned jobs and Pending quote.")
upd(t, 'Diagnosis results', desc='The claim, DiagnosisNotes, parts needed, the new QUOTE, the recorded decision and each status change. Splits '
    'into Job claim record, Diagnosis findings, Needed part record, New quote, and Recorded quote decision.')
insert_after(t, 'Needed part details', l0=True, name='Unassigned appointments', ft='D2 Appointments → 3.0 Record Diagnosis',
             desc='APPOINTMENT rows at the store with ApptStatus = Booked and no TechnicianID (AppointmentID, ScheduledAt, CustomerID), '
                  'for a technician to claim' + OWN + '.')
insert_after(t, 'Unassigned appointments', l0=True, name='Appointment claim', ft='3.0 Record Diagnosis → D2 Appointments',
             desc='TechnicianID set on the APPOINTMENT the technician claims.')
insert_after(t, 'Job to diagnose', name='Job claim', ft='Repair Technician → 3.1 Select Repair Job', lvl='Part of Diagnosis details',
             desc='RepairJobID or AppointmentID of an unassigned job or appointment the technician takes on.')
ren(t, 'Assigned job queue', 'Job queue', lvl='Part of Diagnosis worklist',
    desc="The technician's own jobs, and the store's unassigned jobs and appointments, each with TicketNumber or ScheduledAt, device, "
         "ReportedIssue and current Status.")
ren(t, 'Assigned jobs', 'Own and unassigned jobs', lvl='Part of Diagnosis queue',
    desc='REPAIR_JOB rows where AssignedTechID is this technician or empty, with the latest JOB_STATUS_HISTORY Status.')
insert_after(t, 'Own and unassigned jobs', name='Job claim record', ft='3.1 Select Repair Job → D3 Repair Jobs', lvl='Part of Diagnosis results',
             desc='AssignedTechID set to the claiming technician on REPAIR_JOB.')

# 4.0: part requests
t = tab(4)
upd(t, 'Repair worklist', desc='The job being repaired and the confirmation of any part requested. Splits into Repair job details and Part '
    'request confirmation.')
upd(t, 'Repair work details', desc='The job chosen, each part and quantity used, any part requested, the RepairNotes and the completion. '
    'Splits into Job to repair, Parts used, Part request, and Repair completion.')
upd(t, 'Repair work record', desc='JOB_PART rows for parts used or requested, RepairNotes, CompletedAt and each status change. Splits into '
    'Parts-used record, Part request record, and Completed repair record.')
insert_after(t, 'Stock shortage', name='Part request', ft='Repair Technician → 4.4 Record Part Request', lvl='Part of Repair work details',
             desc='PartID and Quantity the technician asks for. Technicians request parts; only a Manager orders them' + OWN + '.')
ren(t, 'Parts shortage record', 'Part request record',
    desc="JOB_PART row (PartID, Quantity, PartStatus = Needed) for the part requested, and Status = Awaiting Parts; it appears in the "
         "Manager's low-stock alert (7.1).")
ren(t, 'Parts shortage notice', 'Part request confirmation', desc='PartName, Quantity requested and the job now Awaiting Parts.')

# 5.0: a Technician may send
t = tab(5)
insert_after(t, 'Notification preview', l0=True, name='Technician send request', ft='Repair Technician → 5.0 Send Pickup Notification',
             desc="RepairJobID of the completed job, the instruction to send and the technician's EmployeeID; it reaches 5.4 Send Email "
                  "Message. The system fills in the customer's address, so the technician never sees it" + OWN + '.')
upd(t, 'Send instruction', desc="Confirmation to send, with the sender's EmployeeID (Owner, Manager or Front Desk; a Technician sends "
    "through Technician send request). The email is never sent automatically" + OWN + '.')

# 6.0: no diagnostic fee for an unrepairable device
t = tab(6)
upd(t, 'Pickup record', desc='The PAYMENT row (none when nothing is owed), PickedUpAt, IDVerifiedFlag, SignatureFile and Status = Closed. '
    'Splits into Payment record and Job release record.')
ren(t, 'Paid job', 'Settled job', desc='RepairJobID with payment recorded, or with nothing owed: a device that could not be repaired carries '
    'no diagnostic fee' + OWN + '.')

# 7.0: low-stock alert, part requests, Manager approval
t = tab(7)
ren(t, 'Low-stock report', 'Low-stock alert',
    desc='Raised automatically when a part reaches the reorder point the Manager sets: parts at or below their reorder point per store, '
         'and the open part requests with their jobs' + OWN + '.')
upd(t, 'Purchase order status', desc="PurchaseOrderID, supplier, POStatus and dates, including the Manager's approval or rejection.")
upd(t, 'Purchase order approval', ft='Store Manager → 7.0 Process Purchase Orders',
    desc='PurchaseOrderID and Approved or Rejected, with RejectionReason when rejected. A Manager approves every order; the Owner no '
         'longer does' + OWN + '.')
upd(t, 'Purchase orders awaiting approval', ft='7.0 Process Purchase Orders → Store Manager')
upd(t, 'Jobs awaiting parts', desc='REPAIR_JOBs with Status = Awaiting Parts and their JOB_PART rows with PartStatus = Needed (the part '
    'requests). Splits into Open part requests (to 7.1) and Jobs waiting on this order (to 7.5).')
insert_after(t, 'Supplier details', name='Open part requests', ft='D3 Repair Jobs → 7.1 List Parts to Order', lvl='Part of Jobs awaiting parts',
             desc='JOB_PART rows with PartStatus = Needed and their REPAIR_JOBs: the technicians\' part requests, for the Manager to order.')

# write the tables back


def row_xml(r):
    x = TPL[r['l0']]
    ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', x))
    assert len(ts) == 4
    out, last = [], 0
    for m, v in zip(ts, [r['name'], r['ft'], r['lvl'], r['desc']]):
        out.append(x[last:m.start()]); out.append('<w:t xml:space="preserve">' + esc(v) + '</w:t>'); last = m.end()
    return ''.join(out) + x[last:]


for t in data:
    old = t['xml']
    tail = tail.replace(old, old[:old.find('<w:tr')] + t['hdr'] + ''.join(row_xml(r) for r in t['rows']) + '</w:tbl>', 1)


def set_para(xml, pred, newtext):
    for m in re.finditer(r'<w:p[ >].*?</w:p>', xml, re.S):
        if pred(para_text(m.group(0))):
            p = m.group(0)
            ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', p))
            q = p[:ts[0].start()] + '<w:t xml:space="preserve">' + esc(newtext) + '</w:t>'
            for a, b in zip(ts, ts[1:]):
                q += p[a.end():b.start()] + '<w:t xml:space="preserve"></w:t>'
            return xml[:m.start()] + q + p[ts[-1].end():] + xml[m.end():]
    sys.exit('paragraph not found')


heads = ['1.0 Schedule Appointment', '2.0 Register Repair Job', '3.0 Record Diagnosis', '4.0 Record Repair Work',
         '5.0 Send Pickup Notification', '6.0 Record Device Release', '7.0 Process Purchase Orders', '8.0 Report Repair Status',
         '9.0 Maintain Shop Records']
for nm, t in zip(heads, data):
    extra = '; no Level 1 diagram' if nm.startswith('8.0') else ''
    tail = set_para(tail, lambda s, nm=nm: s.startswith(nm + '   ('), '%s   (%d flows%s)' % (nm, len(t['rows']), extra))
L0n = sum(r['l0'] for t in data for r in t['rows']); L1n = sum(not r['l0'] for t in data for r in t['rows'])
intro = next(para_text(m.group(0)) for m in re.finditer(r'<w:p[ >].*?</w:p>', tail, re.S) if 'Level 0 flows and' in para_text(m.group(0)))
tail = set_para(tail, lambda s: 'Level 0 flows and' in s, re.sub(r'\d+ Level 0 flows and \d+ more', '%d Level 0 flows and %d more' % (L0n, L1n), intro))
d = head + tail
print('Appendix B:', L0n, 'Level 0 rows,', L1n, 'Level 1-only rows')

# ======================= body text =======================
PARA = r'<w:p[ >].*?</w:p>'
BODY = [
 ('creates the job with a ticket number (pre-filled from an appointment when one exists)',
  'creates the job with a ticket number, an optional device passcode and an optional technician (pre-filled from an appointment when one exists)', 1),
 ("Shows the technician's queue, records the diagnosis,",
  "Shows the technician's queue with the unassigned jobs and appointments they may claim, records the diagnosis,", 1),
 ('Records parts used (deducting stock), parts shortages (Awaiting Parts) and completion (Ready for Pickup).',
  'Records parts used (deducting stock), part requests (Awaiting Parts) and completion (Ready for Pickup).', 1),
 ('prepares and sends the pickup notification email from the store account and records the result on the job.',
  'prepares the pickup notification and sends it from the store account when staff or the Technician click Send (never automatically), and records the result on the job.', 1),
 ('and closes the job; refuses to close an unpaid job.',
  'and closes the job; refuses to close an unpaid job unless nothing is owed (no diagnostic fee for a device that cannot be repaired).', 1),
 ("Lists low stock and waiting jobs; records POs, the Owner's approval, placement and receipt (adding stock and releasing waiting jobs).",
  "Alerts the Manager when a part reaches its reorder point and lists part requests; records POs, a Manager's approval, placement and receipt (adding stock and releasing waiting jobs). Nothing is ordered automatically.", 1),
 ('“… Input Form” for a screen a person fills in, “… Output Form” for a screen the system shows,',
  '“… Input Form” for a form a person fills in on screen, “… Screen” for what the system shows a person (a list, an alert, a confirmation),', 1),
 ('used through a browser on the counter and bench devices in both stores', 'used through a browser on the stores’ Lenovo ThinkPads', 1),
 ('Daily backup (NFR06) is the managed database service’s automated backup.',
  'Daily backup (NFR06) is the managed database service’s automated backup. The physical diagrams also show the owner’s October 23 '
  'clarifications: a Technician may send the pickup notification, a Manager approves every purchase order, the system alerts the Manager '
  'when a part reaches its reorder point, technicians request parts and may claim unassigned jobs and appointments, a device that cannot '
  'be repaired owes no diagnostic fee, and an optional passcode is recorded at check-in (QuickPhone_Physical_DFD_Set.pdf, page 2). '
  'A Technician sending contradicts the September 21 confirmation #6 and is still to be confirmed with the owner.', 1),
 ('and whether a Manager covers one store or both is to be confirmed with the owner.',
  'and whether a Manager covers one store or both is to be confirmed with the owner. After the owner’s October 23 answers, '
  'repair_job.assigned_tech_id and appointment.technician_id may be empty until a job is assigned or claimed, device type and brand are '
  'optional, and repair_job.device_passcode holds the optional passcode, encrypted and shown only to authorized staff.', 1),
 ('pre-fills the customer and technician from it', 'pre-fills the customer and, if one was chosen, the technician from it', 1),
 ('The ERD reflects this with APPOINTMENT 0..1 per REPAIR_JOB.',
  'A technician may also claim an unassigned appointment or job in 3.1 (owner, October 23). The ERD reflects this with APPOINTMENT 0..1 '
  'per REPAIR_JOB and an optional TechnicianID.', 1),
 ('REPAIR_JOB.AssignedTechID, EMPLOYEE', 'REPAIR_JOB.AssignedTechID, APPOINTMENT.TechnicianID, EMPLOYEE', 1),
]
for old, new, want in BODY:
    d, n = edit_xml(d, old, new, PARA, para_text, replace_in_para)
    if n != want:
        sys.exit('%d of %d for: %s' % (n, want, old[:70]))


def row_cells(anchor_texts, old, new, want):
    """In the one table row whose cells include every anchor text, set each cell whose text is exactly `old`."""
    global d
    rows = [m for m in re.finditer(r'<w:tr[ >].*?</w:tr>', d, re.S)
            if all(a in [para_text(c).strip() for c in cells_of(m.group(0))] for a in anchor_texts)]
    assert len(rows) == 1, (anchor_texts, len(rows))
    r = rows[0].group(0); n = 0
    for c in cells_of(r):
        if para_text(c).strip() == old:
            r = r.replace(c, set_cell(c, new), 1); n += 1
    assert n == want, (anchor_texts, old, n)
    d = d[:rows[0].start()] + r + d[rows[0].end():]


row_cells(['3.0', 'Record Diagnosis'], 'D3, D4', 'D2, D3, D4', 1)                 # Table 3.1
row_cells(['D2', 'Appointments', 'APPOINTMENT'], '1.0, 2.0', '1.0, 2.0, 3.0', 2)  # Table 7.1
row_cells(['FR04 Assignment'], 'D3, D7', 'D2, D3, D7', 1)                          # Table 7.2

tmp = DOCX + '.tmp'
with zipfile.ZipFile(DOCX) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        zo.writestr(item, d.encode('utf-8') if item.filename == 'word/document.xml' else zi.read(item.filename))
os.replace(tmp, DOCX)
print('ok')
