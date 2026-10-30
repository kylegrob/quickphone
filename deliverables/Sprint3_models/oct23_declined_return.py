# Oct 23: a declined quote sets Returned Unrepaired (UC-03, Appendix B 3.5), and UC-06 gains flow 4b so a job with
# nothing owed can be released without a payment. Replaces the earlier same-day change to Closed.
# Usage: python oct23_declined_return.py <use_cases.docx> <models.docx>   (both edited in place)
import os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import replace_in_para, para_text

UC_EDITS = [
 ('the recorded decision and who recorded it; status In Repair or Closed.',
  'the recorded decision and who recorded it; status In Repair or Returned Unrepaired.'),
 ('3a. Customer declines: Front Desk records the decline and the system sets status to Closed with no repair charge.',
  '3a. Customer declines: Front Desk records the decline and the system sets status to Returned Unrepaired with no repair charge.'),
]
UC_4A = '4a. Customer cannot pay: Front Desk does not release the device, and the job stays open until payment is recorded.'
UC_4B = ('4b. Nothing is owed (quote declined or device not repairable): Front Desk skips the payment step and goes to the '
         'signature; the system sets status to Closed. If the owner sets a diagnostic fee (open question, FR05), it is taken '
         'here as a normal payment.')
MODEL_EDITS = [('(In Repair if approved, Closed if declined)', '(In Repair if approved, Returned Unrepaired if declined)')]


def paras(d):
    return list(re.finditer(r'<w:p[ >].*?</w:p>', d, re.S))


def edit(d, old, new):
    hits = [m for m in paras(d) if old in para_text(m.group(0))]
    if len(hits) != 1:
        sys.exit('%d hits for: %s' % (len(hits), old[:60]))
    m = hits[0]
    return d[:m.start()] + replace_in_para(m.group(0), old, new) + d[m.end():]


def rewrite(path, fn):
    d = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
    d = fn(d)
    tmp = path + '.tmp'
    with zipfile.ZipFile(path) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for item in zi.infolist():
            zo.writestr(item, d.encode('utf-8') if item.filename == 'word/document.xml' else zi.read(item.filename))
    os.replace(tmp, path)


def uc(d):
    for old, new in UC_EDITS:
        d = edit(d, old, new)
    if UC_4B[:20] in d:
        sys.exit('4b already present')
    hits = [m for m in paras(d) if para_text(m.group(0)).strip() == UC_4A]
    if len(hits) != 1:
        sys.exit('%d hits for 4a' % len(hits))
    m = hits[0]
    return d[:m.end()] + replace_in_para(m.group(0), UC_4A, UC_4B) + d[m.end():]


def models(d):
    for old, new in MODEL_EDITS:
        d = edit(d, old, new)
    return d


rewrite(sys.argv[1], uc); rewrite(sys.argv[2], models); print('ok')
