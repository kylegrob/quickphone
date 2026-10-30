# Use Cases docx: trace lines that name DFD processes renamed on Oct 23. Usage: python uc_edits.py <in> <out>
import os, re, sys, zipfile
sys.path.insert(0, r'C:\Users\Admin\Documents\Dev\Dev\QuickPhone\deliverables\Sprint3_models')
from update_models_docx import replace_in_para, para_text

EDITS = [('DFD 5.0 Send Completion Notice (5.1 to 5.5)', 'DFD 5.0 Send Pickup Notification (5.1 to 5.5)'),
         ('DFD 7.3 Record PO Approval;', 'DFD 7.3 Record Purchase Order Approval;')]
src, dst = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src); d = z.read('word/document.xml').decode('utf-8')
for old, new in EDITS:
    hits = [m for m in re.finditer(r'<w:p[ >].*?</w:p>', d, re.S) if old in para_text(m.group(0))]
    if len(hits) != 1:
        sys.exit('%d hits: %s' % (len(hits), old))
    m = hits[0]; d = d[:m.start()] + replace_in_para(m.group(0), old, new) + d[m.end():]
tmp = dst + '.tmp'
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        b = zi.read(item.filename)
        zo.writestr(item, d.encode('utf-8') if item.filename == 'word/document.xml' else b)
os.replace(tmp, dst); print('ok')
