# Speaker-note (and slide text) edits for the Oct 23 logical DFD revision. Each old text must be found exactly once
# in the deck. Usage: python notes_edits.py <in.pptx> <out.pptx> slides|presentation
import os, sys, zipfile

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

EDITS = {
 'slides': [
  ('Context diagram: the system as one process and the five external entities. These flows match Level 0 exactly.',
   'Context diagram: the system as one process and the five external entities. These flows match Level 0 exactly. An entity is whoever gives data to the system or gets data from it: staff enter what customers tell them, and the Customer receives the claim ticket and the pickup notification directly.'),
  ('Part 3: completion notice and release, processes 5.0 and 6.0. 5.0 sends the one completion email from the store account; 6.0 releases a device only after payment is recorded.',
   'Part 3: pickup notification and release, processes 5.0 and 6.0. 5.0 sends the one pickup notification email from the store account; 6.0 releases a device only after payment is recorded.'),
  ('Part 4: back office and reporting, processes 7.0, 8.0 and 9.0. 8.0 is read-only and is not decomposed; UC-13 View Repair Status covers it.',
   'Part 4: back office and reporting, processes 7.0, 8.0 and 9.0. 8.0 is read-only and is not decomposed; UC-13 View Repair Status covers it. The Owner asks for the repair and inventory overview with an overview request.'),
  ('"Identify Customer" became Retrieve Customer Record and Save Customer Record, both system actions.',
   '"Identify Customer" became Retrieve Customer Record and Save Customer Record, both system actions: 2.1 finds a returning customer, 2.2 creates a new one or updates the one found. 2.5 prints the claim ticket for the Customer and the device tag for the Front Desk, with the store\'s contact details on the ticket.'),
  ('One completion email from the store account; Owner, Manager or Front Desk sends it, never a Technician.',
   'One pickup notification email from the store account; Owner, Manager or Front Desk sends it, never a Technician.'),
  ('the claim ticket and release receipt printouts, the completion notice email,',
   'the claim ticket (to the Customer), device tag and release receipt printouts, the pickup notification email,'),
 ],
 'presentation': [
  ('inside it are the web app and its database, and the Front Desk is outside.',
   'inside it are the web app and its database, and the Front Desk and the Customer are outside.'),
  ('the Claim Ticket Printout comes off the label printer,',
   'the Claim Ticket Printout comes off the label printer and goes to the Customer,'),
  ('Owner: staff-sent or automatic completion email (FR12)', 'Owner: staff-sent or automatic pickup notification email (FR12)'),
 ],
}

src, dst, which = sys.argv[1], sys.argv[2], sys.argv[3]
edits = EDITS[which]
zi = zipfile.ZipFile(src)
files = {n: zi.read(n) for n in zi.namelist()}
for old, new in edits:
    hits = 0
    for n in files:
        if not (n.startswith('ppt/notesSlides/') or n.startswith('ppt/slides/')) or not n.endswith('.xml'):
            continue
        x = files[n].decode('utf-8')
        for o in (esc(old), esc(old).replace("'", '&apos;'), esc(old).replace('"', '&quot;')):
            if o in x:
                hits += x.count(o); x = x.replace(o, esc(new)); break
        files[n] = x.encode('utf-8')
    if hits != 1:
        sys.exit('%d hits for: %s' % (hits, old[:70]))
tmp = dst + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        zo.writestr(item, files[item.filename])
os.replace(tmp, dst)
print('ok', len(edits))
