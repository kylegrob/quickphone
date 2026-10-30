# Oct 23: text edits for the technology choice (Django + PostgreSQL) and the textbook-style human-machine boundary,
# in the models docx, the DFD/ERD slide deck and the Sprint 3 presentation. Run-aware: a phrase may span several runs.
# Usage: python oct23_tech_text.py   (edits the repo copies in docs/sprint-3 in place, after checking every count)
import os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import replace_in_para, para_text, esc, html_unescape

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DRAFTS = os.path.join(REPO, 'docs', 'sprint-3', 'drafts')

BOUNDARY_DOC = ('a dashed human–machine boundary is drawn around each person who uses the system’s screens (Front Desk, '
                'Technician, Manager, Owner), as in Figs. 9-2 and 9-4, and each store is a group of tables in the PostgreSQL '
                'database, named “PostgreSQL: …” with its tables listed.')
DOCX_EDITS = [
 ('a dashed human–machine boundary encloses the web app and its database, and each store is a group of tables in that database, named “DB: …” with its tables listed.', BOUNDARY_DOC, 1),
 ('and “DB Record: …” or “DB Record Update: …” for rows', 'and “PostgreSQL Record: …” or “PostgreSQL Record Update: …” for rows', 1),
 ('Manual steps (the photo-ID check and taking payment on the unlinked card machine) are manual processes outside the boundary, and 9.5 Import Inventory File is a batch process.',
  'The manual steps (the photo-ID check and taking payment on the unlinked card machine) are manual processes inside the Front Desk’s boundary, on the human side. The Customer has no boundary: like the Customer Service Department in Fig. 9-2, the customer only receives a printout and an email and never uses the system’s screens. 9.5 Import Inventory File is a batch process.', 1),
 ('The implementation assumed is the Sprint 1 recommendation: a custom web application at the counter and bench PCs in both stores, with one shared relational database. Sprint 2 did not choose a technology, so this is still to be confirmed with the owner. Daily backup (NFR06) is assumed to be a hosting-platform service.',
  'The implementation is the route chosen, provisionally, in the Sprint 3 alternative matrix: a custom web application built with Django (Python) and a PostgreSQL database, hosted offsite as a three-tier thin client–server system and used through a browser on the counter and bench devices in both stores (SAD 8e Fig. 7-2). It scored 415 of a possible 500 against 350 for a repair-shop subscription, and the result reverses if nobody will support the system after handoff, which the owner has still to answer. Daily backup (NFR06) is the managed database service’s automated backup.', 1),
 ('ANSI SQL types (DBMS not yet chosen);', 'ANSI SQL types, all valid in PostgreSQL, the chosen DBMS;', 1),
]
SLIDES_EDITS = [
 ('How the design is implemented: assumed web app with one shared database (to confirm with the owner)',
  'How the design is implemented: Django (Python) web app and one PostgreSQL database, chosen provisionally in the alternative matrix', 1),
 ('the dashed red line is the human–machine boundary.', 'the dashed red lines are the human–machine boundary, drawn around each person who uses the system’s screens (SAD 8e Figs. 9-2, 9-4); the Customer has none because they only receive a printout and an email.', 1),
 ('and DB Record or DB Record Update for rows', 'and PostgreSQL Record or PostgreSQL Record Update for rows', 1),
]
PRES_EDITS = [
 ('for example the web app and a label printer for check-in.', 'for example Django and a label printer for check-in.', 1),
 ('The dashed red line is the human-machine boundary: inside it are the web app and its database, and the Front Desk and the Customer are outside.',
  'The dashed red line is the human-machine boundary. As in the textbook, it goes around each person who uses the system’s screens, here the Front Desk. The Customer has no line, because they only receive the printed claim ticket and never use the screens.', 1),
 ('and a DB Record line reads or writes the tables of the store it touches.', 'and a PostgreSQL Record line reads or writes the tables of the store it touches.', 1),
 ('Alternative matrix and hardware/software specification still to finish', 'Technology chosen provisionally; the owner’s support answer can reverse it', 1),
 ('the alternative matrix and the hardware and software specification are still being finished,',
  'the technology choice in our alternative matrix is provisional until the owner tells us who will support the system,', 1),
 ('The custom web app with one shared database is assumed from Sprint 1, not yet confirmed',
  'Django and PostgreSQL chosen provisionally; the subscription wins if nobody will support the system after December 9', 1),
 ('The design also assumes a custom web application with one shared database, which came from our Sprint 1 recommendation and is not confirmed.',
  'The technology is chosen only provisionally: a custom Django and PostgreSQL web app scored highest in our alternative matrix, but if the owner cannot name anyone to support it after December 9, a repair-shop subscription comes out ahead.', 1),
 ('Finish the alternative matrix and hardware/software specification', 'Re-score the alternative matrix with the owner’s answers', 1),
 ('We will finish the alternative matrix and the hardware and software specification, update the prototype traces,',
  'We will re-score the alternative matrix with the owner’s answers, update the prototype traces,', 1),
]


def a_replace(p, old, new):
    """replace_in_para for DrawingML paragraphs (<a:t> runs)."""
    ts = list(re.finditer(r'(<a:t>)([^<]*)(</a:t>)', p))
    texts = [html_unescape(m.group(2)) for m in ts]
    full = ''.join(texts); k = full.find(old)
    if k < 0:
        return None
    end = k + len(old); pos = 0; out = []; placed = False
    for t in texts:
        a, b = pos, pos + len(t); pos = b
        if b <= k or a >= end:
            out.append(t); continue
        out.append(t[:max(0, k - a)] + ('' if placed else new) + (t[max(0, end - a):] if end < b else '')); placed = True
    res, last = [], 0
    for m, t in zip(ts, out):
        res.append(p[last:m.start()]); res.append('<a:t>' + esc(t) + '</a:t>'); last = m.end()
    res.append(p[last:])
    return ''.join(res)


def a_text(p):
    return ''.join(html_unescape(t) for t in re.findall(r'<a:t>([^<]*)</a:t>', p))


def edit_xml(x, old, new, para_re, text_of, repl):
    n, pos = 0, 0
    while True:
        hit = next((m for m in re.finditer(para_re, x, re.S) if m.start() >= pos and old in text_of(m.group(0))), None)
        if not hit:
            return x, n
        r = repl(hit.group(0), old, new)
        x = x[:hit.start()] + r + x[hit.end():]; n += 1; pos = hit.start() + len(r)


def edit_package(path, edits, kind):
    with zipfile.ZipFile(path) as z:
        parts = {i.filename: z.read(i.filename) for i in z.infolist()}; infos = z.infolist()
    if kind == 'docx':
        targets = ['word/document.xml']; para_re, text_of, repl = r'<w:p[ >].*?</w:p>', para_text, replace_in_para
    else:
        targets = sorted(f for f in parts if re.match(r'ppt/(slides/slide|notesSlides/notesSlide)\d+\.xml$', f))
        para_re, text_of, repl = r'<a:p>.*?</a:p>', a_text, a_replace
    xml = {f: parts[f].decode('utf-8') for f in targets}
    for old, new, want in edits:
        got = 0
        for f in targets:
            xml[f], n = edit_xml(xml[f], old, new, para_re, text_of, repl); got += n
        if got != want:
            sys.exit('%s: %d of %d for: %s' % (os.path.basename(path), got, want, old))
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
        for i in infos:
            zo.writestr(i, xml[i.filename].encode('utf-8') if i.filename in xml else parts[i.filename])
    return tmp


if __name__ == '__main__':
    jobs = [(os.path.join(DRAFTS, 'Sprint 3 - DFD and ERD Models.docx'), DOCX_EDITS, 'docx'),
            (os.path.join(DRAFTS, 'Sprint 3 - DFD and ERD Slides.pptx'), SLIDES_EDITS, 'pptx'),
            (os.path.join(REPO, 'docs', 'sprint-3', 'Sprint 3 - Presentation.pptx'), PRES_EDITS, 'pptx')]
    for path, _, _ in jobs:
        lock = os.path.join(os.path.dirname(path), '~$' + os.path.basename(path)[2:])
        if os.path.exists(lock):
            sys.exit('close it in Office first: ' + path)
    tmps = [(edit_package(p, e, k), p) for p, e, k in jobs]   # all checks pass before anything is replaced
    for tmp, p in tmps:
        os.replace(tmp, p); print('edited', os.path.basename(p))
