# Oct 23 (second pass): "completion email" -> "pickup notification" in the System Request v1.2, Feasibility Analysis
# v2.2 and Product Backlog, at Kyle Robertson's direction. The backlog's "Sprint 3 Changes" sheet is a history of
# past edits and is left as written. Each old text must be found the stated number of times.
# Usage: python oct23_pickup_notification_2.py   (edits the files in docs/sprint-3/drafts in place)
import os, re, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from update_models_docx import replace_in_para, para_text, esc

D = os.path.normpath(os.path.join(HERE, '..', '..', 'docs', 'sprint-3', 'drafts'))
DOCX = {
 'Sprint 3 - Systems Request v1.2.docx': [
  ('one completion email to the customer from the store’s account', 'one pickup notification email to the customer from the store’s account', 1),
  ('completion emails are sent from the store’s account', 'pickup notification emails are sent from the store’s account', 1),
  ('customers receive a completion email when their device is ready', 'customers receive a pickup notification when their device is ready', 1),
  ('status emails other than the repair completion email', 'status emails other than the pickup notification', 1),
  ('Send the customer one completion email from the store’s account when the repair is done',
   'Send the customer one pickup notification email from the store’s account when the device is ready to collect', 1),
  ('Is the completion email sent by staff', 'Is the pickup notification sent by staff', 1),
 ],
 'Sprint 3 - Feasibility Analysis v2.2.docx': [
  ('the completion email from the store’s account was approved', 'the pickup notification email from the store’s account was approved', 1),
  ('Whether the completion email is sent', 'Whether the pickup notification is sent', 1),
 ],
}
XLSX = {
 'Sprint 3 - Product Backlog.xlsx': [
  ('one completion email from the store account', 'one pickup notification email from the store account', 1),
  ('Send completion email', 'Send pickup notification', 1),
  ("send the customer one completion email from the store's email account when the repair is done",
   "send the customer one pickup notification email from the store's email account when the device is ready for pickup", 1),
  ('one completion email per job, and no email for any other status', 'one pickup notification per job, and no email for any other status', 1),
  ('client confirmed one completion email only, no other status emails', 'client confirmed one pickup notification email only, no other status emails', 1),
  ('One completion email per job, sent by staff', 'One pickup notification email per job, sent by staff', 1),
  ('pickup, completion email.', 'pickup, pickup notification.', 1),
 ],
}


def load(path):
    zi = zipfile.ZipFile(path); order = zi.infolist(); files = {i.filename: zi.read(i.filename) for i in order}; zi.close()
    return order, files


def save(path, order, files):
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for item in order:
            zo.writestr(item, files[item.filename])
    os.replace(tmp, path)


for name, edits in DOCX.items():
    path = os.path.join(D, name); order, files = load(path)
    d = files['word/document.xml'].decode('utf-8')
    for old, new, n in edits:
        done, pos = 0, 0
        while True:
            hit = next((m for m in re.finditer(r'<w:p[ >].*?</w:p>', d, re.S) if m.start() >= pos and old in para_text(m.group(0))), None)
            if not hit:
                break
            r = replace_in_para(hit.group(0), old, new)
            d = d[:hit.start()] + r + d[hit.end():]; pos = hit.start() + len(r); done += 1
        if done != n:
            sys.exit('%s: %d of %d for %s' % (name, done, n, old))
    files['word/document.xml'] = d.encode('utf-8'); save(path, order, files); print('ok', name)

for name, edits in XLSX.items():
    path = os.path.join(D, name); order, files = load(path)
    parts = [k for k in files if k == 'xl/sharedStrings.xml' or (k.startswith('xl/worksheets/') and k.endswith('.xml'))]
    for old, new, n in edits:
        hits = 0
        for k in parts:
            x = files[k].decode('utf-8')
            for o, nw in ((esc(old), esc(new)), (esc(old).replace("'", '&apos;'), esc(new).replace("'", '&apos;'))):
                c = x.count(o)
                if c:
                    hits += c; x = x.replace(o, nw); break
            files[k] = x.encode('utf-8')
        if hits != n:
            sys.exit('%s: %d of %d for %s' % (name, hits, n, old))
    save(path, order, files); print('ok', name)
