# Oct 23: UC-03 declined quote ends the job as Closed, matching Appendix B flow "Recorded quote decision" (3.5).
# Usage: python oct23_uc03_closed.py <in.docx> <out.docx>
import os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import replace_in_para, para_text

EDITS = [
 ('the recorded decision and who recorded it; status In Repair or Returned Unrepaired.',
  'the recorded decision and who recorded it; status In Repair or Closed.'),
 ('3a. Customer declines: Front Desk records the decline and the system sets status to Returned Unrepaired with no repair charge.',
  '3a. Customer declines: Front Desk records the decline and the system sets status to Closed with no repair charge.'),
]
src, dst = sys.argv[1], sys.argv[2]
d = zipfile.ZipFile(src).read('word/document.xml').decode('utf-8')
for old, new in EDITS:
    hits = [m for m in re.finditer(r'<w:p[ >].*?</w:p>', d, re.S) if old in para_text(m.group(0))]
    if len(hits) != 1:
        sys.exit('%d hits for: %s' % (len(hits), old[:60]))
    m = hits[0]; d = d[:m.start()] + replace_in_para(m.group(0), old, new) + d[m.end():]
tmp = dst + '.tmp'
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        zo.writestr(item, d.encode('utf-8') if item.filename == 'word/document.xml' else zi.read(item.filename))
os.replace(tmp, dst)
print('ok', len(EDITS))
