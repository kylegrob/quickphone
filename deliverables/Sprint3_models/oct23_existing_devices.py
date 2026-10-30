# Oct 23: a customer may own several devices. Appendix B now says how 2.3 reuses a device already on file, and UC-01
# gets the matching normal-flow wording and a "more than one device" alternate flow (Kyle Robertson's request).
# Usage: python oct23_existing_devices.py   (edits the files in docs/sprint-3/drafts in place)
import os, re, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from update_models_docx import replace_in_para, para_text

D = os.path.normpath(os.path.join(HERE, '..', '..', 'docs', 'sprint-3', 'drafts'))
EDITS = {
 'Sprint 3 - DFD and ERD Models.docx': [
  ('DeviceType, Brand, Model, SerialOrIMEI; ReportedIssue and IntakeCondition;',
   "the DeviceID of a device already on file, or a new device's DeviceType, Brand, Model and SerialOrIMEI; ReportedIssue and IntakeCondition;"),
  ('DeviceType, Brand, Model, SerialOrIMEI, IntakeCondition and ReportedIssue.',
   "The DeviceID of a device already on file, picked from the customer search results, or a new device's DeviceType, Brand, Model and SerialOrIMEI; with this visit's IntakeCondition and ReportedIssue. When a customer brings several devices, 2.3 to 2.5 run once per device."),
  ('DEVICE row created or reused (DeviceID, CustomerID, DeviceType, Brand, Model, SerialOrIMEI).',
   "A DEVICE row for a new device (DeviceID, CustomerID, DeviceType, Brand, Model, SerialOrIMEI); a device picked from the customer's records is reused, not written again."),
 ],
 'Sprint 3 - Use Cases.docx': [
  ('device type, brand, model, serial or IMEI, condition and reported problem; technician choice;',
   "a device already on file, or a new device's type, brand, model and serial or IMEI; its condition and reported problem; technician choice;"),
  ('Front Desk enters the device type, brand, model, serial or IMEI, condition and reported problem.',
   "Front Desk selects one of the customer's devices already on file or enters a new device's type, brand, model and serial or IMEI, then records its condition and reported problem."),
 ],
}
# new alternate flow, inserted after the paragraph that starts with the anchor (a copy of it, so the list style holds)
INSERT = ('Sprint 3 - Use Cases.docx', '2a. Customer has no email address:',
          '3a. Customer brings more than one device: the customer is saved once, then steps 3 to 6 repeat for each device, so every device gets its own repair job, ticket number, claim ticket and tag.')

for name, edits in EDITS.items():
    path = os.path.join(D, name)
    zi = zipfile.ZipFile(path); order = zi.infolist(); files = {i.filename: zi.read(i.filename) for i in order}; zi.close()
    d = files['word/document.xml'].decode('utf-8')
    for old, new in edits:
        hits = [m for m in re.finditer(r'<w:p[ >].*?</w:p>', d, re.S) if old in para_text(m.group(0))]
        if len(hits) != 1:
            sys.exit('%s: %d hits for %s' % (name, len(hits), old))
        m = hits[0]; d = d[:m.start()] + replace_in_para(m.group(0), old, new) + d[m.end():]
    if name == INSERT[0]:
        hits = [m for m in re.finditer(r'<w:p[ >].*?</w:p>', d, re.S) if para_text(m.group(0)).strip().startswith(INSERT[1])]
        if len(hits) != 1:
            sys.exit('anchor hits %d' % len(hits))
        m = hits[0]; p = m.group(0)
        clone = replace_in_para(p, para_text(p), INSERT[2])
        clone = re.sub(r' w14:paraId="[0-9A-F]+"', '', clone); clone = re.sub(r' w14:textId="[0-9A-F]+"', '', clone)
        d = d[:m.end()] + clone + d[m.end():]
    files['word/document.xml'] = d.encode('utf-8')
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for item in order:
            zo.writestr(item, files[item.filename])
    os.replace(tmp, path); print('ok', name)
