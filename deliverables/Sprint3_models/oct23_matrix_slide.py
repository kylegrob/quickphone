# Oct 23: adds the "Acquisition and technical approach" slide (alternative matrix + hardware/software specification)
# to the Sprint 3 presentation, after "What we fixed after the textbook review", with speaker notes. Styling copies the
# deck's two-panel slides (slide13.xml: F2F2F2 / EAF3E6 panels, 1F4E79 headings). Scores come from build_acquisition_doc.py.
import os, re, shutil, sys, tempfile, zipfile
from xml.sax.saxutils import escape as esc

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PPTX = os.path.join(REPO, 'docs', 'sprint-3', 'Sprint 3 - Presentation.pptx')
AFTER_SLDID = '281'   # "What we fixed after the textbook review"

C = [('Fit to the confirmed rules', 25, 5, 3, 2), ('Access control and record integrity', 15, 4, 5, 1),
     ('One view of both stores', 10, 5, 5, 3), ('Annual cost to QuickPhone (est.)', 20, 4, 2, 5),
     ('Support after December 9', 15, 2, 5, 3), ('Delivers the MOU deliverables', 10, 5, 2, 3),
     ('Adoption by staff used to paper', 5, 4, 3, 3)]
TOT = [sum(c[1] * c[2 + k] for c in C) for k in range(3)]
assert TOT == [415, 350, 285], TOT

NOTES = ('Our acquisition and technical approach. Using the textbook’s weighted alternative matrix, we compared three '
         'routes: building a custom system, subscribing to a product made for repair shops, and a shared spreadsheet. The '
         'weights come from what the owner has told us matters. Fit to the seven rules the owner confirmed counts most, then '
         'the yearly cost, support after we hand over on December 9, and the deliverables in our MOU. The custom build scores '
         '415 out of 500, the subscription 350 and the spreadsheet 285. Custom wins on fit and on the MOU. The subscription '
         'wins on support, but at about 140 to 150 dollars per store per month it costs more than twice our likely yearly '
         'estimate. The result is not safe: if the owner cannot name anyone to look after the system after December 9, the '
         'subscription comes out ahead, and we will tell the owner so. On the right is the technical approach: a three-tier web '
         'application in Python with the Django framework and a PostgreSQL database, hosted offsite and used through a browser '
         'on the counter and bench devices. Every cost here is an estimate from our feasibility study, and the choice stays '
         'provisional until the owner confirms it.')

NAVY, INK = '1F4E79', '222222'


def run(t, sz, b=False, color=INK):
    return ('<a:r><a:rPr lang="en-US" sz="%d"%s dirty="0"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:rPr>'
            '<a:t>%s</a:t></a:r>' % (sz, ' b="1"' if b else '', color, esc(t)))


def cell(runs, fill=None, algn='l', b_color='BFBFBF'):
    lines = ''.join('<a:ln%s w="9525"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln%s>' % (s, b_color, s) for s in 'LRTB')
    return ('<a:tc><a:txBody><a:bodyPr/><a:lstStyle/><a:p><a:pPr algn="%s"/>%s</a:p></a:txBody>'
            '<a:tcPr marL="68580" marR="68580" marT="45720" marB="45720" anchor="ctr">%s%s</a:tcPr></a:tc>'
            % (algn, runs, lines, '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % fill if fill else '<a:noFill/>'))


def table(x, y, w):
    cols = [2650000, 700000, 1050000, 1050000, 1050000]
    assert sum(cols) == w
    rh = 400000
    head = ['Criterion', 'Weight', 'Custom: Django + PostgreSQL', 'Repair-shop subscription', 'Shared spreadsheet']
    rows = ['<a:tr h="%d">%s</a:tr>' % (520000, ''.join(cell(run(h, 1200, True, 'FFFFFF'), NAVY, 'l' if i == 0 else 'ctr') for i, h in enumerate(head)))]
    for name, wt, *sc in C:
        cs = [cell(run(name, 1300)), cell(run(str(wt), 1300), algn='ctr')]
        for k, s in enumerate(sc):
            cs.append(cell(run(str(wt * s), 1300, k == 0) + run('  (%d)' % s, 1100, False, '666666'),
                           'EAF3E6' if k == 0 else None, 'ctr'))
        rows.append('<a:tr h="%d">%s</a:tr>' % (rh, ''.join(cs)))
    rows.append('<a:tr h="%d">%s</a:tr>' % (rh, ''.join(
        [cell(run('Total (of 500)', 1300, True), 'D9E2F3'), cell(run('100', 1300, True), 'D9E2F3', 'ctr')] +
        [cell(run(str(t), 1400, True, NAVY), 'C6E0B4' if k == 0 else 'D9E2F3', 'ctr') for k, t in enumerate(TOT)])))
    h = 520000 + rh * (len(C) + 1)
    grid = ''.join('<a:gridCol w="%d"/>' % c for c in cols)
    return ('<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="3" name="Alternative matrix"/><p:cNvGraphicFramePr>'
            '<a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
            '<p:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></p:xfrm><a:graphic>'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table"><a:tbl><a:tblPr firstRow="1"/>'
            '<a:tblGrid>%s</a:tblGrid>%s</a:tbl></a:graphicData></a:graphic></p:graphicFrame>' % (x, y, w, h, grid, ''.join(rows))), h


def panel(id_, name, x, y, w, h, fill, heading, bullets, sz=1400, bullet=True):
    paras = ['<a:p><a:pPr algn="l"><a:spcAft><a:spcPts val="600"/></a:spcAft></a:pPr>%s</a:p>' % run(heading, 2000, True, NAVY)] if heading else []
    for b in bullets:
        paras.append(('<a:p><a:pPr algn="l" marL="228600" indent="-228600"><a:spcAft><a:spcPts val="500"/></a:spcAft>'
                     '<a:buFont typeface="Arial"/><a:buChar char="•"/></a:pPr>%s</a:p>' if bullet else '<a:p><a:pPr algn="l"/>%s</a:p>') % ''.join(run(*r) if isinstance(r, tuple) else run(r, sz) for r in (b if isinstance(b, list) else [b])))
    return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/>'
            '<a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="%s"/>'
            '</a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr rtlCol="0" anchor="t" wrap="square" '
            'lIns="182880" rIns="182880" tIns="118872" bIns="91440"><a:normAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody></p:sp>'
            % (id_, name, x, y, w, h, fill, ''.join(paras)))


def slide_xml():
    top, L = 1508760, 548640
    tbl, th = table(L, top, 6500000)
    spec = panel(4, 'Hardware and software', 7231380, top, 4411980, th, 'EAF3E6', 'Hardware and software (Ch. 7)', [
        'Three-tier thin client–server, hosted offsite (Fig. 7-2)',
        'Browser on counter and bench devices: the existing laptop plus up to 3 more (est. $0–$2,400)',
        'Python 3.12, Django 5.2 LTS (security fixes to April 2028)',
        'PostgreSQL 16+, managed, daily backup (NFR06)',
        'Email through the store’s own mailbox (client #7); one label printer per store (est. $0–$400)',
        'Hosting est. $0–$450 a year'], sz=1400)
    note = panel(5, 'Sensitivity', L, top + th + 150000, 11094720, 640080, 'F2F2F2', None, [[
        ('What reverses it: ', 1400, True, NAVY),
        ('a vendor demo proving full rule fit only narrows the gap (415 vs 400). If nobody will support the system after '
         'December 9 (support weighted 30, fit 10), the subscription wins, 380 vs 370. Scores 1–5 in brackets; SAD 8e Fig. 6-6.', 1400)]], bullet=False)
    title = ('<p:sp><p:nvSpPr><p:cNvPr id="2" name="Title 1"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="title"/>'
             '</p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" dirty="0"/>'
             '<a:t>Acquisition and technical approach</a:t></a:r></a:p></p:txBody></p:sp>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>%s%s%s%s'
            '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>' % (title, tbl, spec, note))


def main():
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(PPTX) as z:
        z.extractall(tmp); order = z.namelist()
    P = lambda *a: os.path.join(tmp, *a)
    rd = lambda p: open(p, encoding='utf-8').read()
    def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
    pres = rd(P('ppt', 'presentation.xml'))
    if 'Acquisition and technical approach' in ''.join(rd(P('ppt', 'slides', f)) for f in os.listdir(P('ppt', 'slides')) if f.endswith('.xml')):
        sys.exit('slide already present')
    n = max(int(m) for m in re.findall(r'slide(\d+)\.xml', ' '.join(os.listdir(P('ppt', 'slides'))))) + 1
    nn = max(int(m) for m in re.findall(r'notesSlide(\d+)\.xml', ' '.join(os.listdir(P('ppt', 'notesSlides'))))) + 1
    wr(P('ppt', 'slides', 'slide%d.xml' % n), slide_xml())
    wr(P('ppt', 'slides', '_rels', 'slide%d.xml.rels' % n),
       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout2.xml"/>'
       '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide%d.xml"/></Relationships>' % nn)
    notes = rd(P('ppt', 'notesSlides', 'notesSlide12.xml'))
    notes = re.sub(r'(<p:ph type="body"[^>]*/>.*?<a:p>).*?(</a:p>)', lambda m: m.group(1) + '<a:r><a:rPr lang="en-US" dirty="0"/><a:t>%s</a:t></a:r>' % esc(NOTES) + m.group(2), notes, count=1, flags=re.S)
    assert esc(NOTES) in notes
    wr(P('ppt', 'notesSlides', 'notesSlide%d.xml' % nn), notes)
    wr(P('ppt', 'notesSlides', '_rels', 'notesSlide%d.xml.rels' % nn),
       rd(P('ppt', 'notesSlides', '_rels', 'notesSlide12.xml.rels')).replace('../slides/slide13.xml', '../slides/slide%d.xml' % n))
    ct = rd(P('[Content_Types].xml'))
    ct = ct.replace('</Types>', '<Override PartName="/ppt/slides/slide%d.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                    '<Override PartName="/ppt/notesSlides/notesSlide%d.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/></Types>' % (n, nn))
    wr(P('[Content_Types].xml'), ct)
    prel = rd(P('ppt', '_rels', 'presentation.xml.rels'))
    rid = 'rId%d' % (max(int(r) for r in re.findall(r'Id="rId(\d+)"', prel)) + 1)
    wr(P('ppt', '_rels', 'presentation.xml.rels'), prel.replace('</Relationships>',
       '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide%d.xml"/></Relationships>' % (rid, n)))
    sid = max(int(s) for s in re.findall(r'<p:sldId id="(\d+)"', pres)) + 1
    anchor = re.search(r'<p:sldId id="%s" r:id="rId\d+"/>' % AFTER_SLDID, pres).group(0)
    wr(P('ppt', 'presentation.xml'), pres.replace(anchor, anchor + '<p:sldId id="%d" r:id="%s"/>' % (sid, rid)))
    out = PPTX + '.tmp'
    new = ['ppt/slides/slide%d.xml' % n, 'ppt/slides/_rels/slide%d.xml.rels' % n, 'ppt/notesSlides/notesSlide%d.xml' % nn,
           'ppt/notesSlides/_rels/notesSlide%d.xml.rels' % nn]
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for arc in order + new:
            z.write(P(*arc.split('/')), arc)
    os.replace(out, PPTX); shutil.rmtree(tmp)
    print('added slide%d.xml (notesSlide%d) after sldId %s' % (n, nn, AFTER_SLDID))


if __name__ == '__main__':
    main()
