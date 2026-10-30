# Oct 23: the owner's clarifications and the Screen/Input Form names in the two decks.
#   Sprint 3 - Presentation.pptx: swaps every model picture (physical Level 0 part 1, ERD details) for its current render,
#     then edits slide text and speaker notes.
#   Sprint 3 - DFD and ERD Slides.pptx: speaker notes (pictures are refreshed by update_slides_pptx.py ... refresh).
# Run-aware edits with a count check for each; nothing is replaced until every check passes.
import os, re, shutil, sys, tempfile, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import new_png
from update_slides_pptx import fit_picture, write_out
from oct23_tech_text import edit_package

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PRES = os.path.join(REPO, 'docs', 'sprint-3', 'Sprint 3 - Presentation.pptx')
SLIDES = os.path.join(REPO, 'docs', 'sprint-3', 'drafts', 'Sprint 3 - DFD and ERD Slides.pptx')

SLIDES_EDITS = [
 ('Optional appointment booking. 2.0 pre-fills a job from a booked appointment; walk-ins need none.',
  'Optional appointment booking. 2.0 pre-fills a job from a booked appointment; walk-ins need none. The technician is optional: a technician may claim an unassigned appointment in 3.1 (owner, Oct 23).', 1),
 ("with the store's contact details on the ticket.",
  "with the store's contact details on the ticket. 2.4 takes an optional device passcode, needed only for camera repairs, and an optional technician (owner, Oct 23).", 1),
 ('Every quote goes to Awaiting Approval; no repair starts until 3.5 records the customer decision.',
  "3.1 lists the technician's jobs and the unassigned jobs and appointments they may claim (owner, Oct 23). Every quote goes to Awaiting Approval; no repair starts until 3.5 records the customer decision.", 1),
 ('Recording a part as used deducts stock automatically (client-confirmed); there is no reservation.',
  'Recording a part as used deducts stock automatically (client-confirmed); there is no reservation. A technician requests a missing part in 4.4; only a Manager orders it (owner, Oct 23).', 1),
 ('One pickup notification email from the store account; Owner, Manager or Front Desk sends it, never a Technician.',
  'One pickup notification email from the store account, sent only when someone clicks Send: Owner, Manager or Front Desk, or the Technician who finished the repair (owner, Oct 23; to confirm against the September 21 rule). The system fills in the address, so the Technician never sees it.', 1),
 ('A device is released only after payment is recorded; only the fact of the ID check is stored.',
  'A device is released only after payment is recorded, unless nothing is owed: a device that could not be repaired carries no diagnostic fee (owner, Oct 23). Only the fact of the ID check is stored.', 1),
 ('The Owner approves every purchase order before it is placed (client-confirmed).',
  "A Manager approves every purchase order before it is placed; the Owner no longer does (owner, Oct 23). 7.1 alerts the Manager when a part reaches its reorder point and lists the technicians' part requests; nothing is ordered automatically.", 1),
 ('Part 2: the repair bench, processes 3.0 and 4.0.',
  'Part 2: the repair bench, processes 3.0 and 4.0. Technicians claim unassigned jobs and appointments (D2) and request parts here.', 1),
 ('6.0 releases a device only after payment is recorded.',
  '6.0 releases a device only after payment is recorded, or when nothing is owed for a device that could not be repaired. A Technician may also send the notification (owner, Oct 23).', 1),
 ('Detail 1: customers, devices, appointments, staff and stores.',
  "Detail 1: customers, devices, appointments, staff and stores. An appointment's technician is optional, and device type and brand are optional (owner, Oct 23).", 1),
 ('which keeps it in 3NF.',
  'which keeps it in 3NF. The assigned technician may be empty until someone assigns or claims the job, and the optional device passcode is stored encrypted (owner, Oct 23).', 1),
 ('input and output forms,', 'input forms, screens,', 1),
 ('Input Form, Output Form, Printout,', 'Input Form (a form a person fills in), Screen (what the system shows a person), Printout,', 1),
 ('Purchase orders, the Owner’s approval queue, the status dashboard and the master records.',
  'Purchase orders, the Manager’s approval queue and low-stock alert, the Owner’s status dashboard and the master records.', 1),
 ('For presenting, use the three Level 0 parts.', 'For presenting, use the four Level 0 parts.', 1),
]

PRES_EDITS = [
 ('recorded every change, with its cause, in the Change Log.',
  'recorded every change, with its cause, in the Change Log. On October 23 the owner answered our open questions, and the physical DFDs and ERD you will see already include those answers.', 1),
 ('Data flow dictionary for all 165 logical flows (models document, Appendix B)', 'Data flow dictionary for all 171 logical flows (models document, Appendix B)', 1),
 ('Appendix B of the models document describes all 165 logical flows', 'Appendix B of the models document describes all 171 logical flows', 1),
 ('Browser on counter and bench devices: the existing laptop plus up to 3 more (est. $0–$2,400)',
  'Browser on the stores’ Lenovo ThinkPads; count to confirm (extra devices est. $0–$2,400)', 1),
 ('used through a browser on the counter and bench devices.', 'used through a browser on the stores’ Lenovo ThinkPads.', 1),
 ('an Input Form is a screen staff fill in, an Output Form is a screen the system shows,',
  'an Input Form is a form staff fill in on screen, a Screen is what the system shows them,', 1),
 ('so a customer can have zero or many devices, and each device belongs to exactly one customer.',
  "so a customer can have zero or many devices, and each device belongs to exactly one customer. An appointment's technician is now optional, because the owner says technicians may claim unassigned appointments.", 1),
 ('Columns that point to an employee record who did something, such as who sent the pickup notification or who decided a quote.',
  'Columns such as who sent the pickup notification or who decided a quote point to the employee who did it. The owner told us on October 23 that a passcode is optional and needed only for camera repairs, so the job has an optional device passcode, stored encrypted, and the assigned technician can be empty until someone assigns the job or a technician claims it.', 1),
 ("which supports the client's rule that the owner approves every purchase order before it is placed.",
  "which supports the owner's rule, confirmed on October 23, that a manager approves every purchase order before it is placed.", 1),
 ('Records device, serial or IMEI, condition and reported problem, then assigns a technician by open workload',
  'Records device, condition and reported problem; a technician is optional (assigned by hand or claimed later)', 1),
 ('The technician picker shows open jobs per tech to support FR04.',
  'The technician picker shows open jobs per tech to support FR04. The owner says assignment is by hand and optional, and technicians may claim jobs themselves, so this mockup will be updated.', 1),
 ('Shows only jobs assigned to the signed-in technician, using the confirmed job statuses',
  'Shows the technician’s jobs; unassigned jobs to claim will be added (owner, Oct 23)', 1),
 ('An out-of-stock part moves the job to Awaiting Parts and adds it to the low-stock list (alternate flow 3a)',
  'An out-of-stock part moves the job to Awaiting Parts and sends a part request to the Manager', 1),
 ('Technicians cannot send customer email or see contact details (UC-05 alternate flow 1a, NFR04).',
  'Technicians never see customer contact details (NFR04). The owner now says a technician may click Send on the pickup notification, which reverses the September 21 rule, so we are confirming it before changing UC-05.', 1),
 ('Every purchase order goes to the Owner for approval before it can be received',
  'Every purchase order needs a Manager’s approval before it can be received', 1),
 ('Submitting sets Pending Approval for the Owner (UC-09).',
  'Submitting sets Pending Approval for a Manager (UC-09; the owner confirmed on October 23 that managers approve). The system also alerts the Manager when a part reaches the reorder point the Manager sets.', 1),
 ('Store equipment and connectivity are unconfirmed', 'ThinkPads per store and connectivity unconfirmed', 1),
 ("Every purchase order waits on the owner's approval", 'Technician email: Oct 23 answer conflicts with Sept 21 rule', 1),
 ('Owner: staff-sent or automatic pickup notification email (FR12)', 'Owner: may a Technician send the pickup email (Sept 21 said no)?', 1),
 ('Owner: a PO spending threshold or urgent path (FR10)', 'Owner: may a Manager approve their own purchase order?', 1),
 ('we have not confirmed the equipment and internet connection at each store,',
  'we know the stores use Lenovo ThinkPads but not how many, or how reliable the internet connection is,', 1),
 ('Every purchase order waits on the owner, so orders could stall when the owner is busy.',
  "The owner's October 23 answers let a technician send the pickup email, which contradicts the September 21 rule, so we must confirm which holds.", 1),
 ('the owner has to choose whether staff send the pickup notification or the system sends it automatically, whether purchase orders need a spending threshold or an urgent path, and whether a manager covers one store or both.',
  'the owner has to confirm whether a technician may send the pickup email, whether a manager may approve an order they created, and whether a manager covers one store or both.', 1),
 ('Settle FR10, FR12 and Manager scope; update the catalog, use cases and models, and log each change',
  'Carry the owner’s Oct 23 answers into the catalog and use cases; confirm the Technician email rule', 1),
 ('Their answers will settle FR10, FR12 and the manager question, and we will update the catalog, use cases and models and log each change.',
  'The owner answered most of the open rules on October 23 and our models already show those answers; we will carry them into the catalog and use cases, confirm the technician email rule and the manager question, and log each change.', 1),
]


def swap_pres_pictures(src, dst):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    P = lambda *a: os.path.join(tmp, *a)
    pics = 0
    for f in os.listdir(P('ppt', 'slides')):
        if not f.endswith('.xml'):
            continue
        x = open(P('ppt', 'slides', f), encoding='utf-8').read()
        for descr in re.findall(r'descr="([^"]+_(?:Physical|Logical)\.png)"', x):
            png = new_png(os.path.basename(descr)[:-4])
            if not os.path.exists(png):
                sys.exit('no render for ' + descr)
            rid = re.search(r'descr="%s".*?r:embed="(rId\d+)"' % re.escape(descr), x, re.S).group(1)
            rels = open(P('ppt', 'slides', '_rels', f + '.rels'), encoding='utf-8').read()
            target = re.search(r'Id="%s"[^>]*Target="\.\./([^"]+)"' % rid, rels).group(1)
            shutil.copyfile(png, P('ppt', *target.split('/')))
            x = fit_picture(x, png, descr); pics += 1
        open(P('ppt', 'slides', f), 'w', encoding='utf-8').write(x)
    write_out(tmp, dst)
    print('presentation pictures swapped:', pics)


if __name__ == '__main__':
    for path in (PRES, SLIDES):
        lock = os.path.join(os.path.dirname(path), '~$' + os.path.basename(path)[2:])
        if os.path.exists(lock):
            sys.exit('close it in PowerPoint first: ' + path)
    staged = PRES + '.pics.pptx'
    swap_pres_pictures(PRES, staged)
    tmps = [(edit_package(staged, PRES_EDITS, 'pptx'), PRES), (edit_package(SLIDES, SLIDES_EDITS, 'pptx'), SLIDES)]
    for tmp, p in tmps:
        os.replace(tmp, p); print('edited', os.path.basename(p))
    os.remove(staged)
