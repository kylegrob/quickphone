# Updates the team deck "Sprint 3 - Presentation.pptx" for the Oct 22 relabel: the physical Level 0 picture
# (now part 1 of 4: 1.0 and 2.0) and the speaker-note sentences that described the old part 1.
# Usage: python update_presentation_pptx.py <in.pptx> <out.pptx>
import os, re, shutil, sys, tempfile, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import new_png, esc
from update_slides_pptx import fit_picture

NOTE_EDITS = [
 ('inside it are the web app and its database, and the Front Desk and the Customer are outside.',
  'inside it are the web app and its database, and the Front Desk is outside.'),
 ('This is the physical Level 0 DFD for the front counter: 1.0 Schedule Appointment, 2.0 Register Repair Job, 5.0 Send Completion Notice and 6.0 Record Device Release.',
  'This is part 1 of the physical Level 0 DFD, the front counter at booking and check-in: 1.0 Schedule Appointment and 2.0 Register Repair Job.'),
 ('Flows name their medium, such as the printed ticket and tag, or the completion email sent from the store\'s own account.',
  'Each line is one data flow, and its name says how the data travels, as in the textbook\'s physical DFDs: an Input Form is a screen staff fill in, an Output Form is a screen the system shows, the Claim Ticket Printout comes off the label printer, and a DB Record line reads or writes the tables of the store it touches.'),
 ('The other two Level 0 parts, every Level 1 diagram and the logical versions are in the models document and the DFD and ERD slide deck.',
  'The other three Level 0 parts, the complete Level 0, every Level 1 diagram and the logical versions are in the models document, the DFD and ERD slide deck, and the physical DFD set PDF.'),
]


def main(src, dst):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    P = lambda *a: os.path.join(tmp, *a)
    done = 0
    for f in os.listdir(P('ppt', 'slides')):
        if not f.endswith('.xml'):
            continue
        x = open(P('ppt', 'slides', f), encoding='utf-8').read()
        for descr in re.findall(r'descr="([^"]+_Physical\.png)"', x):
            if 'Level0_Part1' not in descr:
                continue
            png = new_png(os.path.basename(descr)[:-4])
            rid = re.search(r'descr="%s".*?r:embed="(rId\d+)"' % re.escape(descr), x, re.S).group(1)
            rels = open(P('ppt', 'slides', '_rels', f + '.rels'), encoding='utf-8').read()
            target = re.search(r'Id="%s"[^>]*Target="\.\./([^"]+)"' % rid, rels).group(1)
            shutil.copyfile(png, P('ppt', *target.split('/')))
            x = fit_picture(x, png, descr); done += 1
            open(P('ppt', 'slides', f), 'w', encoding='utf-8').write(x)
    for f in os.listdir(P('ppt', 'notesSlides')):
        if not f.endswith('.xml'):
            continue
        p = P('ppt', 'notesSlides', f); x = open(p, encoding='utf-8').read(); y = x
        for old, new in NOTE_EDITS:
            y = y.replace(esc(old).replace("'", '&apos;'), esc(new)).replace(esc(old), esc(new))
        if y != x:
            open(p, 'w', encoding='utf-8').write(y); done += 1
    out = dst + '.tmp'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(P('[Content_Types].xml'), '[Content_Types].xml')
        for root, _, files in os.walk(tmp):
            for f in files:
                arc = os.path.relpath(os.path.join(root, f), tmp).replace('\\', '/')
                if arc != '[Content_Types].xml':
                    z.write(os.path.join(root, f), arc)
    os.replace(out, dst); shutil.rmtree(tmp); print('ok, parts changed:', done)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
