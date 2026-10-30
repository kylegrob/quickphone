# Body-text edits to the models docx for the Oct 23 logical DFD revision (outside Appendix B).
# Usage: python body_edits.py <in.docx> <out.docx>
import os, re, sys, zipfile
sys.path.insert(0, r'C:\Users\Admin\Documents\Dev\Dev\QuickPhone\deliverables\Sprint3_models')
from update_models_docx import replace_in_para, para_text

src, dst = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src); d = z.read('word/document.xml').decode('utf-8')
stop = d.find('Appendix B. Data flow dictionary')

EDITS = [  # (old, new, expected count before Appendix B)
 ('(booking and check-in, repair bench, completion notice and release, back office)',
  '(booking and check-in, repair bench, pickup notification and release, back office)', 1),
 ('Figure 3.4 Level 0, part 3: front counter, completion notice and release (5.0, 6.0)',
  'Figure 3.4 Level 0, part 3: front counter, pickup notification and release (5.0, 6.0)', 1),
 ('and prints the claim ticket and tag.', 'and prints the claim ticket for the customer and the device tag.', 1),
 ('Send Completion Notice', 'Send Pickup Notification', 4),
 ('prepares and sends the completion email from the store account', 'prepares and sends the pickup notification email from the store account', 1),
 ("Answers status enquiries and produces the Owner's two-store overview.",
  "Answers status enquiries and, when the Owner asks, produces the repair and inventory overview of both stores.", 1),
 ('Figure 5.5 Physical Level 0, part 3: completion notice and release (5.0, 6.0)',
  'Figure 5.5 Physical Level 0, part 3: pickup notification and release (5.0, 6.0)', 1),
 ('Exactly one completion email per job', 'Exactly one pickup notification email per job', 1),
 ('Context diagram: the system boundary and five external entities.',
  'Context diagram: the system boundary and five external entities. The diagrams take the system’s viewpoint: an external entity is whoever gives data to the system or receives data from it. Staff enter what customers tell them, so the Customer appears only where it receives something from the system directly (the claim ticket and the pickup notification), and suppliers do not appear because purchase orders are placed with them outside the system.', 1),
]
for old, new, n in EDITS:
    done, pos = 0, 0
    while True:
        hit = None
        for m in re.finditer(r'<w:p[ >].*?</w:p>', d[:stop], re.S):
            if m.start() >= pos and old in para_text(m.group(0)):
                hit = m; break
        if not hit:
            break
        r = replace_in_para(hit.group(0), old, new)
        d = d[:hit.start()] + r + d[hit.end():]; stop += len(r) - len(hit.group(0)); done += 1
        pos = hit.start() + len(r)   # never revisit an edited paragraph (a new text may contain the old one)
    if done != n:
        sys.exit('%d of %d for: %s' % (done, n, old))
    print(done, old[:60])

tmp = dst + '.tmp'
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        b = zi.read(item.filename)
        if item.filename == 'word/document.xml':
            b = d.encode('utf-8')
        zo.writestr(item, b)
os.replace(tmp, dst)
print('ok')
