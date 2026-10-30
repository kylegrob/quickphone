# Oct 23: FR12 and UC-05 renamed from "completion email" to "pickup notification" (Kyle Robertson's decision), in
# the catalog, use cases (text and diagram), models document and team presentation. Each old text must be found the
# stated number of times. Usage: python oct23_pickup_notification.py   (edits the files in docs/ in place)
import os, re, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from update_models_docx import replace_in_para, para_text, esc

DOCS = os.path.normpath(os.path.join(HERE, '..', '..', 'docs'))
D = os.path.join(DOCS, 'sprint-3', 'drafts')

DOCX = {
 os.path.join(D, 'Sprint 3 - Requirements Catalog and Memo.docx'): [
  ('Customers receive one completion email from the store’s account (FR12)', 'Customers receive one pickup notification email from the store’s account (FR12)', 1),
  ('Customer email', 'Pickup notification', 1, 'FR12Customer email'),   # label is "FR12", a line break, "Customer email"
  ('can send the customer a completion email from the store’s email account;',
   'can send the customer a pickup notification email from the store’s email account, telling them the device is ready to collect;', 1),
  ('A Technician attempts to send a completion email and is blocked.', 'A Technician attempts to send a pickup notification and is blocked.', 1),
  ('Is the completion email sent by staff or automatically', 'Is the pickup notification sent by staff or automatically', 1),
 ],
 os.path.join(D, 'Sprint 3 - Use Cases.docx'): [
  ('Send Repair Completion Email', 'Send Pickup Notification', 2),
  ('can all send the completion email.', 'can all send the pickup notification.', 1),
  ('no completion email can be sent.', 'no pickup notification can be sent.', 1),
  ('sends the customer a completion email from the store mailbox.',
   'sends the customer a pickup notification email from the store mailbox, telling them the device is ready to collect.', 1),
  ('Ready-to-notify list; email preview; completion email to the customer',
   'Pickup-ready job list; notification preview; pickup notification to the customer', 1),
 ],
 os.path.join(D, 'Sprint 3 - DFD and ERD Models.docx'): [
  ('FR12 Customer email', 'FR12 Pickup notification', 1),
  ('sends the completion email,', 'sends the pickup notification,', 1),
 ],
}
PPTX = {
 os.path.join(DOCS, 'sprint-3', 'Sprint 3 - Presentation.pptx'): [
  ('who sent the completion email', 'who sent the pickup notification', 1),
  ('whether staff send the completion email or', 'whether staff send the pickup notification or', 1),
 ],
}
UC_PNG = os.path.join(HERE, 'QuickPhone_Use_Case_Diagram.png')


def rezip(path, files, order):
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for item in order:
            zo.writestr(item, files[item.filename])
    os.replace(tmp, path)


for path, edits in DOCX.items():
    zi = zipfile.ZipFile(path); order = zi.infolist(); files = {i.filename: zi.read(i.filename) for i in order}; zi.close()
    d = files['word/document.xml'].decode('utf-8')
    for old, new, n, *within in edits:   # optional 4th item: the paragraph's whole text must equal it
        done, pos = 0, 0
        ok = lambda t: old in t and (not within or t == within[0])
        while True:
            hit = next((m for m in re.finditer(r'<w:p[ >].*?</w:p>', d, re.S) if m.start() >= pos and ok(para_text(m.group(0)))), None)
            if not hit:
                break
            r = replace_in_para(hit.group(0), old, new)
            d = d[:hit.start()] + r + d[hit.end():]; pos = hit.start() + len(r); done += 1
        if done != n:
            sys.exit('%s: %d of %d for %s' % (os.path.basename(path), done, n, old))
    files['word/document.xml'] = d.encode('utf-8')
    if path.endswith('Use Cases.docx'):
        files['word/media/image1.png'] = open(UC_PNG, 'rb').read()   # same 1330x1180 layout, so the frame size holds
    rezip(path, files, order); print('ok', os.path.basename(path))

for path, edits in PPTX.items():
    zi = zipfile.ZipFile(path); order = zi.infolist(); files = {i.filename: zi.read(i.filename) for i in order}; zi.close()
    for old, new, n in edits:
        hits = 0
        for k in files:
            if k.endswith('.xml') and (k.startswith('ppt/notesSlides/') or k.startswith('ppt/slides/')):
                x = files[k].decode('utf-8'); c = x.count(esc(old))
                if c:
                    hits += c; files[k] = x.replace(esc(old), esc(new)).encode('utf-8')
        if hits != n:
            sys.exit('%s: %d of %d for %s' % (os.path.basename(path), hits, n, old))
    rezip(path, files, order); print('ok', os.path.basename(path))
