# Rebuilds Appendix B (data flow dictionary) of the models docx for the Oct 23 logical DFD revision:
# renames, Level 0 flows split into their named parts, new flows (claim ticket, device tag, store contact,
# notification preview, release authorization/confirmation, purchasing splits, overview request), fuller data
# elements for 1.1, 2.5, 3.3 and 3.4. Usage: python appb_rebuild.py <in.docx> <out.docx>
import re, sys, zipfile, shutil, os

src, dst = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src)
d = z.read('word/document.xml').decode('utf-8')

def unesc(s): return s.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&')
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def ptext(x): return ''.join(unesc(t) for t in re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', x))

start = d.find('Appendix B. Data flow dictionary')
assert start > 0
head, tail = d[:start], d[start:]

# ---------- parse tables ----------
tables = list(re.finditer(r'<w:tbl>.*?</w:tbl>', tail, re.S))
assert len(tables) == 9, len(tables)
TPL = {}
data = []
for t in tables:
    rows = re.findall(r'<w:tr[ >].*?</w:tr>', t.group(0), re.S)
    hdr, body = rows[0], rows[1:]
    out = []
    for r in body:
        cells = [ptext(c) for c in re.findall(r'<w:tc>.*?</w:tc>', r, re.S)]
        l0 = 'F2F6FA' in r
        TPL.setdefault(l0, r)
        out.append(dict(name=cells[0], ft=cells[1], lvl=cells[2], desc=cells[3], l0=l0))
    data.append(dict(hdr=hdr, rows=out, xml=t.group(0)))

def tab(n): return data[[1, 2, 3, 4, 5, 6, 7, 8, 9].index(n)]['rows']
def find(rows, name, lvl=None):
    m = [r for r in rows if r['name'] == name and (lvl is None or r['lvl'] == lvl)]
    assert len(m) == 1, (name, lvl, len(m)); return m[0]
def ren(rows, old, new, **kw):
    r = find(rows, old); r['name'] = new; r.update(kw); return r
def delete(rows, name, lvl):
    r = find(rows, name, lvl); rows.remove(r)
def insert_after(rows, anchor, **kw):
    i = rows.index(find(rows, anchor)); kw.setdefault('lvl', 'Level 0 flow'); kw.setdefault('l0', True)
    rows.insert(i + 1, kw)
def sub_all(old, new):  # in From -> To, Level and description cells of every table
    for t in data:
        for r in t['rows']:
            for k in ('ft', 'lvl', 'desc'):
                r[k] = r[k].replace(old, new)

# process renames
sub_all('5.0 Send Completion Notice', '5.0 Send Pickup Notification')
sub_all('5.3 Prepare Completion Email', '5.3 Prepare Pickup Notification')
sub_all('7.3 Record PO Approval', '7.3 Record Purchase Order Approval')

# 1.0
t = tab(1)
ren(t, 'Technician availability', 'Store schedule',
    desc="The store's opening hours and its active technicians (STORE StoreID, BusinessHours; EMPLOYEE EmployeeID, FirstName, LastName, Role = Technician, ActiveFlag). Free times are the business hours less the booked appointments.")
ren(t, 'Existing customer', 'Returning customer record')
ren(t, 'New customer', 'New customer record')

# 2.0
t = tab(2)
ren(t, 'Check-in results', 'Customer search results',
    desc='Customers matching the phone search (name, phone, email) and their devices, for the staff member to pick from.')
delete(t, 'Customer search results', 'Part of Check-in results')
insert_after(t, 'Customer search results', name='Device tag', ft='2.0 Register Repair Job → Front Desk Staff',
             desc='TicketNumber with the device Brand and Model, printed for the tag that stays with the device.')
insert_after(t, 'Device tag', name='Claim ticket', ft='2.0 Register Repair Job → Customer',
             desc="The customer's proof for pickup: TicketNumber, customer name, device, ReportedIssue, CheckInAt and the store's name, address and phone.")
ren(t, 'Checked In appointment', 'Checked-in appointment')
insert_after(t, 'Technician roster', name='Store contact details', ft='D7 Staff & Stores → 2.0 Register Repair Job',
             desc='STORE StoreName, Address and Phone, printed on the claim ticket.')
delete(t, 'Claim documents', 'Part of Check-in results')
find(t, 'Customer ID')['desc'] = "CustomerID with the customer's FirstName and LastName."
find(t, 'Registered device')['desc'] = 'CustomerID and customer name, DeviceID, Brand, Model, ReportedIssue and IntakeCondition.'
ren(t, 'Ticket number', 'Registered repair job',
    desc='RepairJobID, the generated TicketNumber, CheckInAt and StoreID, with the customer name, device Brand and Model and ReportedIssue passed on from 2.3: everything 2.5 prints except the store contact details.')
# the D7 read by 2.5 is the same flow as the Level 0 "Store contact details", listed once
t[:] = [r for r in t]

# 3.0
t = tab(3)
ren(t, 'Stock at this store', 'Needed part details',
    desc='For each part the diagnosis needs: the PART StandardCost and the quantity on hand at this store (derived from INVENTORY_TXN), so the quote can be priced and a shortage seen before the customer decides.')
find(t, 'Parts needed')['desc'] = 'RepairJobID, with PartID and Quantity for each part the repair needs.'
find(t, 'Part costs')['desc'] = 'RepairJobID, with PartID, Quantity and StandardCost of every part needed, in stock or not, used to price the quote.'

# 4.0
ren(tab(4), 'In Repair job', 'Job in repair')

# 5.0
t = tab(5)
sub_all('Part of Completion notice approval', 'Part of Notification approval')
sub_all('Part of Ready jobs', 'Part of Ready job records')
sub_all('Part of Completion record', 'Part of Notified job record')
ren(t, 'Completion notice approval', 'Notification approval',
    desc='The ready job chosen, the FinalCost confirmed and the instruction to send the pickup notification. Splits into Job to notify, Final cost and Send instruction.')
ren(t, 'Notification worklist', 'Pickup-ready job list',
    desc='TicketNumber, customer name, device and CompletedAt for each job ready for pickup whose customer has not yet been notified.')
delete(t, 'Ready-to-notify list', 'Part of Notification worklist')
insert_after(t, 'Pickup-ready job list', name='Notification preview', ft='5.0 Send Pickup Notification → Front Desk Staff',
             desc='The pickup notification exactly as it will be sent, for staff to check before sending.')
delete(t, 'Completion email draft', 'Part of Notification worklist')
ren(t, 'Completion email', 'Pickup notification',
    desc="Tells the customer the device is ready to collect: customer name, TicketNumber, device, FinalCost, store name, address and BusinessHours; sent once from the store's email account.")
ren(t, 'Ready jobs', 'Ready job records')
ren(t, 'Completion record', 'Notified job record',
    desc='FinalCost, EmailSentAt, EmailSentByID and EmailStatus on REPAIR_JOB: the confirmed cost, and who sent the pickup notification and when. Splits into Confirmed final cost and Notification record.')
ren(t, 'Customer email', 'Customer email address')
ren(t, 'Job ready for pickup', 'Confirmed ready job')
ren(t, 'Prepared email', 'Prepared notification')

# 6.0
t = tab(6)
ren(t, 'Pickup details', 'Pickup lookup', desc="TicketNumber, or the customer's phone number.")
delete(t, 'Pickup lookup', 'Part of Pickup details')
sub_all('Part of Pickup details', 'Part of Release authorization')
ren(t, 'Pickup results', 'Pickup job summary', desc='TicketNumber, customer name, device, tag number and FinalCost (the amount due).')
delete(t, 'Pickup job summary', 'Part of Pickup results')
insert_after(t, 'Pickup job summary', name='Release authorization', ft='Front Desk Staff → 6.0 Record Device Release',
             desc='What allows the device to leave: the photo-ID and tag check result, the payment amount and method, and the customer\'s signature. Splits into Identity check result, Payment details and Customer signature.')
insert_after(t, 'Release authorization', name='Release confirmation', ft='6.0 Record Device Release → Front Desk Staff',
             desc='TicketNumber, PickedUpAt and amount paid.')
delete(t, 'Release confirmation', 'Part of Pickup results')

# 7.0
t = tab(7)
ren(t, 'Purchasing details', 'Purchase order request', desc=find(t, 'PO request')['desc'])
delete(t, 'PO request', 'Part of Purchasing details')
insert_after(t, 'Purchase order request', name='Placed order details', ft='Store Manager → 7.0 Process Purchase Orders',
             desc='PurchaseOrderID confirmed as placed with the supplier outside the system, with the date placed.')
delete(t, 'Order placed confirmation', 'Part of Purchasing details')
insert_after(t, 'Placed order details', name='Received quantities', ft='Store Manager → 7.0 Process Purchase Orders',
             desc=find(t, 'Received quantities', 'Part of Purchasing details')['desc'])
delete(t, 'Received quantities', 'Part of Purchasing details')
ren(t, 'Purchasing status', 'Low-stock report', desc=find(t, 'Low-stock report', 'Part of Purchasing status')['desc'])
delete(t, 'Low-stock report', 'Part of Purchasing status')
insert_after(t, 'Low-stock report', name='Purchase order status', ft='7.0 Process Purchase Orders → Store Manager',
             desc="PurchaseOrderID, supplier, POStatus and dates, including the Owner's approval or rejection.")
delete(t, 'PO status', 'Part of Purchasing status')
insert_after(t, 'Purchase order status', name='Jobs released from Awaiting Parts', ft='7.0 Process Purchase Orders → Store Manager',
             desc=find(t, 'Jobs released from Awaiting Parts', 'Part of Purchasing status')['desc'])
delete(t, 'Jobs released from Awaiting Parts', 'Part of Purchasing status')
ren(t, 'PO approval decision', 'Purchase order approval')
ren(t, 'POs awaiting approval', 'Purchase orders awaiting approval')
ren(t, 'PO decision', 'Purchase order decision record')
ren(t, 'Ordered PO lines', 'Ordered purchase order lines')
sub_all('Ordered PO lines.', 'Ordered purchase order lines.')
sub_all('Submitted purchase order, PO decision,', 'Submitted purchase order, Purchase order decision record,')

# 8.0
t = tab(8)
ren(t, 'Two-store status overview', 'Repair and inventory overview',
    desc='Open jobs by Status for each store, jobs Awaiting Parts and parts at or below their reorder point; the jobs or parts behind a figure when the Owner opens it.')
insert_after(t, 'Job status', name='Overview request', ft='Store Owner → 8.0 Report Repair Status',
             desc='The store to show (or both), and any figure the Owner opens to see the jobs or parts behind it.')

# 9.0
t = tab(9)
sub_all('Part of Shop record changes', 'Part of Staff, store, part and supplier changes')
sub_all('Part of Record update confirmation', 'Part of Change confirmations')
ren(t, 'Shop record changes', 'Staff, store, part and supplier changes')
ren(t, 'Record update confirmation', 'Change confirmations')

# ---------- write tables back ----------
def row_xml(r):
    x = TPL[r['l0']]
    ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', x))
    assert len(ts) == 4
    vals = [r['name'], r['ft'], r['lvl'], r['desc']]
    out, last = [], 0
    for m, v in zip(ts, vals):
        out.append(x[last:m.start()]); out.append('<w:t xml:space="preserve">' + esc(v) + '</w:t>'); last = m.end()
    out.append(x[last:])
    return ''.join(out)

new_tail = tail
for t in data:
    old = t['xml']
    pre = old[:old.find('<w:tr')]
    new = pre + t['hdr'] + ''.join(row_xml(r) for r in t['rows']) + '</w:tbl>'
    new_tail = new_tail.replace(old, new, 1)

# headings "N.N Name   (X flows)" and the intro counts
names = ['1.0 Schedule Appointment', '2.0 Register Repair Job', '3.0 Record Diagnosis', '4.0 Record Repair Work',
         '5.0 Send Completion Notice', '6.0 Record Device Release', '7.0 Process Purchase Orders', '8.0 Report Repair Status',
         '9.0 Maintain Shop Records']
def fix_para(xml, pred, newtext):
    for m in re.finditer(r'<w:p[ >].*?</w:p>', xml, re.S):
        if pred(ptext(m.group(0))):
            p = m.group(0)
            ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', p))
            q = p[:ts[0].start()] + '<w:t xml:space="preserve">' + esc(newtext) + '</w:t>'
            for a, b in zip(ts, ts[1:]):
                q += p[a.end():b.start()] + '<w:t xml:space="preserve"></w:t>'
            q += p[ts[-1].end():]
            return xml[:m.start()] + q + xml[m.end():]
    sys.exit('heading not found')
for nm, t in zip(names, data):
    n = len(t['rows'])
    label = nm.replace('5.0 Send Completion Notice', '5.0 Send Pickup Notification')
    extra = '; no Level 1 diagram' if nm.startswith('8.0') else ''
    new_tail = fix_para(new_tail, lambda s, nm=nm: s.startswith(nm + '   ('), '%s   (%d flows%s)' % (label, n, extra))
L0n = sum(r['l0'] for t in data for r in t['rows']); L1n = sum(not r['l0'] for t in data for r in t['rows'])
intro = [ptext(m.group(0)) for m in re.finditer(r'<w:p[ >].*?</w:p>', new_tail, re.S) if 'Level 0 flows and' in ptext(m.group(0))][0]
new_intro = re.sub(r'\d+ Level 0 flows and \d+ more', '%d Level 0 flows and %d more' % (L0n, L1n), intro)
new_tail = fix_para(new_tail, lambda s: 'Level 0 flows and' in s, new_intro)
print('Level 0 rows', L0n, 'Level 1-only rows', L1n)

d2 = head + new_tail
tmp = dst + '.tmp'
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        data_ = zi.read(item.filename)
        if item.filename == 'word/document.xml':
            data_ = d2.encode('utf-8')
        zo.writestr(item, data_)
os.replace(tmp, dst)
print('ok')
