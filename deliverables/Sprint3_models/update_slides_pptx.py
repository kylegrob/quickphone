# Updates "Sprint 3 - DFD and ERD Slides.pptx" to the right-angle diagram set (Oct 22 relabel):
#   - swaps every diagram picture for its new render, matched by the source path stored in the picture's descr,
#     fitting the new aspect ratio inside the old picture box
#   - adds a "Level 0 part 4" slide after each "part 3" slide (logical and physical), cloned from the part 3 slide
#   - rewrites the speaker notes that described three Level 0 parts
# Usage: python update_slides_pptx.py <in.pptx> <out.pptx> [full|refresh]   (refresh = pictures only)
import os, re, shutil, sys, tempfile, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_models_docx import new_png, png_size, esc

NOTES = {  # slide file -> new speaker notes (old text is replaced whole)
 'slide5.xml': 'Level 0 is shown in four parts so every flow name is readable. Part 1: booking and check-in, processes 1.0 and 2.0. The complete Level 0 is in the appendix and the PDF.',
 'slide7.xml': 'Part 3: completion notice and release, processes 5.0 and 6.0. 5.0 sends the one completion email from the store account; 6.0 releases a device only after payment is recorded.',
 'NEW_LOG': 'Part 4: back office and reporting, processes 7.0, 8.0 and 9.0. 8.0 is read-only and is not decomposed; UC-13 View Repair Status covers it.',
 'slide22.xml': 'Physical context: the same boundary and entities, with every flow named for its medium: input and output forms, the claim ticket and release receipt printouts, the completion notice email, and the inventory import file and error report. Each line is one flow and matches a Level 0 flow exactly.',
 'slide23.xml':'Each process shows how it is implemented; stores show their table names; the dashed red line is the human–machine boundary. Flow names state their medium, as in the textbook’s physical DFDs (SAD 8e Figs. 9-2, 9-4): Input Form, Output Form, Printout, Email, File, and DB Record or DB Record Update for rows read from or written to a store.',
 'NEW_PHYS': 'Part 4: back office and reporting. Purchase orders, the Owner’s approval queue, the status dashboard and the master records.',
}


def set_notes(xml, text):
    """Puts text in the notes body placeholder: first <a:t> of the body shape gets it, the others in it are emptied."""
    m = re.search(r'(<p:sp>(?:(?!</p:sp>).)*?<p:ph type="body"[^>]*/>.*?</p:sp>)', xml, re.S)
    if not m:
        return xml
    sp = m.group(1)
    ts = list(re.finditer(r'<a:t>[^<]*</a:t>', sp))
    if ts:
        new = sp[:ts[0].start()] + '<a:t>' + esc(text) + '</a:t>' + re.sub(r'<a:t>[^<]*</a:t>', '<a:t></a:t>', sp[ts[0].end():])
    else:
        new = sp.replace('</p:txBody>', '<a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>%s</a:t></a:r></a:p></p:txBody>' % esc(text))
        new = new.replace('<a:p/></p:txBody>', '</p:txBody>') if '<a:p/>' in new else new
    return xml.replace(sp, new)


def fit_picture(xml, png, descr_old):
    """Swaps the descr path and refits the picture's ext/off to the new aspect, centred in the old box."""
    w, h = png_size(png)
    def fix(m):
        pic = m.group(0)
        if descr_old not in pic:
            return pic
        pic = pic.replace(descr_old, png)
        off = re.search(r'<a:off x="(\d+)" y="(\d+)"/>', pic); ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>', pic)
        x, y, cx, cy = map(int, (off.group(1), off.group(2), ext.group(1), ext.group(2)))
        s = min(cx / w, cy / h); ncx, ncy = int(w * s), int(h * s)
        nx, ny = x + (cx - ncx) // 2, y + (cy - ncy) // 2
        pic = pic.replace(off.group(0), '<a:off x="%d" y="%d"/>' % (nx, ny)).replace(ext.group(0), '<a:ext cx="%d" cy="%d"/>' % (ncx, ncy))
        return pic
    return re.sub(r'<p:pic>.*?</p:pic>', fix, xml, flags=re.S)


def write_out(tmp, dst):
    """Re-zips the unpacked deck, [Content_Types].xml first."""
    out = dst + '.tmp'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(tmp, '[Content_Types].xml'), '[Content_Types].xml')
        for root, _, files in os.walk(tmp):
            for f in files:
                arc = os.path.relpath(os.path.join(root, f), tmp).replace('\\', '/')
                if arc != '[Content_Types].xml':
                    z.write(os.path.join(root, f), arc)
    os.replace(out, dst); shutil.rmtree(tmp); print('ok (pictures refreshed)')


def main(src, dst, mode='full'):
    """mode 'full': the Oct 22 restructuring (run once); 'refresh': only swap pictures for their current renders."""
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    P = lambda *a: os.path.join(tmp, *a)
    rd = lambda p: open(p, encoding='utf-8').read()
    def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

    # 1. swap pictures
    for f in sorted(os.listdir(P('ppt', 'slides'))):
        if not f.endswith('.xml'):
            continue
        x = rd(P('ppt', 'slides', f))
        for descr in re.findall(r'descr="([^"]+\.png)"', x):
            png = new_png(os.path.basename(descr)[:-4])
            if not os.path.exists(png):
                sys.exit('no render for ' + descr)
            rid = re.search(r'descr="%s".*?r:embed="(rId\d+)"' % re.escape(descr), x, re.S).group(1)
            rels = rd(P('ppt', 'slides', '_rels', f + '.rels'))
            target = re.search(r'Id="%s"[^>]*Target="\.\./([^"]+)"' % rid, rels).group(1)
            shutil.copyfile(png, P('ppt', *target.split('/')))
            x = fit_picture(x, png, descr)
        wr(P('ppt', 'slides', f), x)
    if mode == 'refresh':
        return write_out(tmp, dst)

    # 2. notes of existing slides
    def notes_of(slide):
        r = rd(P('ppt', 'slides', '_rels', slide + '.rels'))
        m = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', r)
        return m.group(1) if m else None
    for s, text in NOTES.items():
        if s.startswith('slide'):
            n = notes_of(s); wr(P('ppt', 'notesSlides', n), set_notes(rd(P('ppt', 'notesSlides', n)), text))

    # 3. new slides cloned from the part 3 slides
    pres = rd(P('ppt', 'presentation.xml')); prels = rd(P('ppt', '_rels', 'presentation.xml.rels')); ct = rd(P('[Content_Types].xml'))
    nslides = len([f for f in os.listdir(P('ppt', 'slides')) if f.endswith('.xml')])
    for base, view, notes_key in (('slide25.xml', 'physical', 'NEW_PHYS'), ('slide7.xml', 'logical', 'NEW_LOG')):
        nslides += 1; new = 'slide%d.xml' % nslides; newn = 'notesSlide%d.xml' % nslides
        png = os.path.join(os.path.dirname(new_png('x_Logical')), '..', view, '06_DFD_Level0_Part4_BackOffice_%s.png' % view.capitalize())
        png = os.path.normpath(png)
        media = 'image-%d-1.png' % nslides
        shutil.copyfile(png, P('ppt', 'media', media))
        x = rd(P('ppt', 'slides', base))
        old_descr = re.search(r'descr="([^"]+\.png)"', x).group(1)
        x = fit_picture(x.replace(old_descr, old_descr), png, old_descr)
        wr(P('ppt', 'slides', new), x)
        r = rd(P('ppt', 'slides', '_rels', base + '.rels'))
        r = re.sub(r'\.\./media/[^"]+', '../media/' + media, r)
        r = re.sub(r'\.\./notesSlides/notesSlide\d+\.xml', '../notesSlides/' + newn, r)
        wr(P('ppt', 'slides', '_rels', new + '.rels'), r)
        on = notes_of(base)
        nx = set_notes(rd(P('ppt', 'notesSlides', on)), NOTES[notes_key])
        wr(P('ppt', 'notesSlides', newn), nx)
        nr = rd(P('ppt', 'notesSlides', '_rels', on + '.rels'))
        nr = re.sub(r'\.\./slides/slide\d+\.xml', '../slides/' + new, nr)
        wr(P('ppt', 'notesSlides', '_rels', newn + '.rels'), nr)
        ct = ct.replace('</Types>', '<Override PartName="/ppt/slides/%s" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                        '<Override PartName="/ppt/notesSlides/%s" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/></Types>' % (new, newn))
        rid = 'rId%d' % (max(int(i) for i in re.findall(r'Id="rId(\d+)"', prels)) + 1)
        prels = prels.replace('</Relationships>', '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/%s"/></Relationships>' % (rid, new))
        base_rid = re.search(r'Id="(rId\d+)"[^>]*Target="slides/%s"' % base, prels).group(1)
        sid = max(int(i) for i in re.findall(r'<p:sldId id="(\d+)"', pres)) + 1
        anchor = re.search(r'<p:sldId id="\d+" r:id="%s"/>' % base_rid, pres).group(0)
        pres = pres.replace(anchor, anchor + '<p:sldId id="%d" r:id="%s"/>' % (sid, rid))
    wr(P('ppt', 'presentation.xml'), pres); wr(P('ppt', '_rels', 'presentation.xml.rels'), prels); wr(P('[Content_Types].xml'), ct)
    app = P('docProps', 'app.xml')
    if os.path.exists(app):
        a = rd(app); a = re.sub(r'<Slides>\d+</Slides>', '<Slides>%d</Slides>' % nslides, a); a = re.sub(r'<Notes>\d+</Notes>', '<Notes>%d</Notes>' % nslides, a); wr(app, a)

    out = dst + '.tmp'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(P('[Content_Types].xml'), '[Content_Types].xml')
        for root, _, files in os.walk(tmp):
            for f in files:
                arc = os.path.relpath(os.path.join(root, f), tmp).replace('\\', '/')
                if arc != '[Content_Types].xml':
                    z.write(os.path.join(root, f), arc)
    os.replace(out, dst); shutil.rmtree(tmp); print('ok', nslides, 'slides')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
