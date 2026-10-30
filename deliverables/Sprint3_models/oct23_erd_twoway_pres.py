# Team deck "Sprint 3 - Presentation.pptx", Oct 23 ERD pass: swaps the three physical ERD detail pictures for their
# new renders (relationship names in both directions) and rewrites the slide text and speaker notes that described
# one verb per line.
# Usage: python oct23_erd_twoway_pres.py <in.pptx> <out.pptx>
import os, re, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import new_png, esc
from update_slides_pptx import fit_picture, write_out
import zipfile

EDITS = [  # (old, new, expected count across slides and notes)
 ('Every ERD relationship labeled with a verb (a STORE employs EMPLOYEEs)',
  'Every ERD relationship named both ways (employs / is employed by)', 1),
 ('Every relationship line on the ERD now carries a verb, read from the one side to the many side, so for example a store employs employees.',
  "Every relationship line on the ERD is now named in both directions, as in the textbook's physical ERD: a store employs employees, and an employee is employed by a store.", 1),
 ('Read each line with its verb: a store employs employees and schedules appointments, a technician handles appointments, and a customer owns devices and books appointments.',
  'Each line is named both ways: the first name reads from the one side to the many side, the second reads back. A store employs employees and schedules appointments, a technician handles appointments, and a customer owns devices and books appointments; read back, an employee is employed by a store and an appointment is booked by a customer.', 1),
]


def main(src, dst):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    P = lambda *a: os.path.join(tmp, *a)
    pics = 0
    for f in os.listdir(P('ppt', 'slides')):
        if not f.endswith('.xml'):
            continue
        x = open(P('ppt', 'slides', f), encoding='utf-8').read()
        for descr in re.findall(r'descr="([^"]+_ERD_[^"]+\.png)"', x):
            png = new_png(os.path.basename(descr)[:-4])
            rid = re.search(r'descr="%s".*?r:embed="(rId\d+)"' % re.escape(descr), x, re.S).group(1)
            rels = open(P('ppt', 'slides', '_rels', f + '.rels'), encoding='utf-8').read()
            target = re.search(r'Id="%s"[^>]*Target="\.\./([^"]+)"' % rid, rels).group(1)
            shutil.copyfile(png, P('ppt', *target.split('/')))
            x = fit_picture(x, png, descr); pics += 1
        open(P('ppt', 'slides', f), 'w', encoding='utf-8').write(x)
    for old, new, n in EDITS:
        done = 0
        for d in ('slides', 'notesSlides'):
            for f in os.listdir(P('ppt', d)):
                if not f.endswith('.xml'):
                    continue
                p = P('ppt', d, f); x = open(p, encoding='utf-8').read()
                for o in {esc(old), esc(old).replace("'", '&apos;')}:
                    if o in x:
                        x = x.replace(o, esc(new)); done += 1
                open(p, 'w', encoding='utf-8').write(x)
        if done != n:
            sys.exit('%d of %d for: %s' % (done, n, old[:60]))
    write_out(tmp, dst)
    print('ok:', pics, 'pictures,', len(EDITS), 'text edits')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
