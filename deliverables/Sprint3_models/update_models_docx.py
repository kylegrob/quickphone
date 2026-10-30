# Updates "Sprint 3 - DFD and ERD Models.docx" to the right-angle diagram set (Oct 22 relabel):
#   - swaps every embedded diagram for its new render (matched by the source name stored in wp:docPr/@name),
#     resizing the height to the new aspect ratio
#   - inserts Figure 3.5 / 5.6 (Level 0 part 4, logical and physical) and Figure 6.9 (complete physical ERD)
#   - renumbers the physical Level 1 figures and edits the text that described three Level 0 parts
# Usage: python update_models_docx.py <in.docx> <out.docx> [full|refresh]   (refresh = images + Appendix B renames)
import os, re, shutil, struct, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(HERE, 'slides')

RENAME = {'03_DFD_Level0_Part1_Counter': '03_DFD_Level0_Part1_Booking_CheckIn',
          '05_DFD_Level0_Part3_BackOffice': '05_DFD_Level0_Part3_Notice_Release',
          '14_ERD_Overview': '15_ERD_Overview', '15_ERD_Detail1': '16_ERD_Detail1',
          '16_ERD_Detail2': '17_ERD_Detail2', '17_ERD_Detail3': '18_ERD_Detail3'}
for i, n in enumerate(['1.0_ScheduleAppointment', '2.0_RegisterRepairJob', '3.0_RecordDiagnosis', '4.0_RecordRepairWork',
                       '5.0_SendCompletionNotice', '6.0_RecordDeviceRelease', '7.0_ProcessPurchaseOrders', '9.0_MaintainShopRecords']):
    RENAME['%02d_DFD_Level1_%s' % (6 + i, n)] = '%02d_DFD_Level1_%s' % (7 + i, n)


def new_png(old_name):
    if old_name in ('18_DFD_ERD_Alignment', '19_DFD_ERD_Alignment'):
        return os.path.join(SLIDES, '19_DFD_ERD_Alignment.png')
    view = 'logical' if old_name.endswith('_Logical') else 'physical'
    base, suffix = old_name.rsplit('_', 1)
    return os.path.join(SLIDES, view, RENAME.get(base, base) + '_' + suffix + '.png')


def png_size(path):
    with open(path, 'rb') as f:
        f.read(16); return struct.unpack('>II', f.read(8))


def para_text(p):
    return ''.join(html_unescape(t) for t in re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p))


def html_unescape(s):
    return s.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&')


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def replace_in_para(p, old, new):
    """Replaces text that may span several runs: the new text goes into the first run touched."""
    ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', p))
    texts = [html_unescape(m.group(2)) for m in ts]
    full = ''.join(texts)
    k = full.find(old)
    if k < 0:
        return None
    end = k + len(old); pos = 0; out = []; placed = False
    for m, t in zip(ts, texts):
        a, b = pos, pos + len(t); pos = b
        if b <= k or a >= end:
            out.append(t); continue
        keep_l = t[:max(0, k - a)]; keep_r = t[max(0, end - a):] if end < b else ''
        out.append(keep_l + ('' if placed else new) + keep_r); placed = True
    res, last = [], 0
    for m, t in zip(ts, out):
        res.append(p[last:m.start()]); res.append('<w:t xml:space="preserve">' + esc(t) + '</w:t>'); last = m.end()
    res.append(p[last:])
    return ''.join(res)


def main(src, dst, mode='full'):
    """mode 'full': the Oct 22 restructuring (run once); 'refresh': swap images and apply logical_renames to Appendix B."""
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp); names = z.namelist()
    doc_p = os.path.join(tmp, 'word', 'document.xml'); rel_p = os.path.join(tmp, 'word', '_rels', 'document.xml.rels')
    d = open(doc_p, encoding='utf-8').read(); rels = open(rel_p, encoding='utf-8').read()
    relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    EMU_W = 8686800

    # 1. swap images
    def swap(m):
        x = m.group(0)
        name = re.search(r'name="([^"]+)"', x).group(1)
        png = new_png(name)
        if not os.path.exists(png):
            sys.exit('no render for ' + name + ' -> ' + png)
        rid = re.search(r'r:embed="(rId\d+)"', x).group(1)
        shutil.copyfile(png, os.path.join(tmp, 'word', relmap[rid]))
        w, h = png_size(png)
        cx = int(re.search(r'<wp:extent cx="(\d+)"', x).group(1))
        if w / h > 1.8 or cx < EMU_W:   # posters: full text width
            cx = EMU_W
        cy = int(cx * h / w)
        x = re.sub(r'cx="\d+" cy="\d+"', 'cx="%d" cy="%d"' % (cx, cy), x)
        return x.replace('name="%s"' % name, 'name="%s"' % os.path.basename(png)[:-4])
    d = re.sub(r'<w:drawing>.*?</w:drawing>', swap, d, flags=re.S)

    # 2. paragraphs: list of (start, end, xml)
    def paras():
        return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r'<w:p[ >].*?</w:p>', d, re.S)]

    def find_para(text):
        for s, e, p in paras():
            if para_text(p).strip() == text:
                return s, e, p
        sys.exit('paragraph not found: ' + text)

    next_rid = max(int(r[3:]) for r in relmap) + 1

    def insert_figure_after(caption_old, png, caption_new, page_break=True):
        nonlocal d, rels, next_rid
        s, e, cap = find_para(caption_old)
        # the image paragraph is the paragraph just before the caption
        prev = [p for p in paras() if p[1] <= s][-1]
        img = prev[2]
        rid = 'rId%d' % next_rid; next_rid += 1
        media = 'media/%s.png' % os.path.basename(png)[:-4].replace('.', '_')
        shutil.copyfile(png, os.path.join(tmp, 'word', media))
        rels = rels.replace('</Relationships>', '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="%s"/></Relationships>' % (rid, media))
        w, h = png_size(png); cx = EMU_W; cy = int(cx * h / w)
        img = re.sub(r'r:embed="rId\d+"', 'r:embed="%s"' % rid, img)
        img = re.sub(r'cx="\d+" cy="\d+"', 'cx="%d" cy="%d"' % (cx, cy), img)
        img = re.sub(r'name="[^"]+"', 'name="%s"' % os.path.basename(png)[:-4], img, count=1)
        img = re.sub(r'(descr|title)="[^"]*"', lambda m: '%s="%s"' % (m.group(1), esc(caption_new)), img)
        if not page_break:
            img = img.replace('<w:pageBreakBefore/>', '')
        cap2 = replace_in_para(cap, caption_old, caption_new)
        d = d[:e] + img + cap2 + d[e:]

    def retext(old, new, whole=False):
        nonlocal d
        for s, e, p in paras():
            t = para_text(p)
            if (t.strip() == old) if whole else (old in t):
                r = replace_in_para(p, old, new)
                d = d[:s] + r + d[e:]
                return
        sys.exit('text not found: ' + old)

    if mode == 'refresh':
        from logical_renames import RENAMES
        start = d.find('Appendix B. Data flow dictionary')
        if start < 0:
            sys.exit('Appendix B not found')
        start = d.rfind('<w:p', 0, start)
        head, tail = d[:start], d[start:]
        count = 0
        for old, new in sorted(RENAMES, key=lambda r: -len(r[0])):
            while True:
                m = None
                for pm in re.finditer(r'<w:p[ >].*?</w:p>', tail, re.S):
                    if old in para_text(pm.group(0)):
                        m = pm; break
                if not m:
                    break
                tail = tail[:m.start()] + replace_in_para(m.group(0), old, new) + tail[m.end():]; count += 1
        d = head + tail
        print('Appendix B replacements:', count)
    if mode == 'full':  # the one-time restructuring; already applied to the repo copy
        retext('Figure 3.2 Level 0, part 1: front counter (1.0, 2.0, 5.0, 6.0)', 'Figure 3.2 Level 0, part 1: front counter, booking and check-in (1.0, 2.0)')
        retext('Figure 3.4 Level 0, part 3: back office and reporting (7.0, 8.0, 9.0)', 'Figure 3.4 Level 0, part 3: front counter, completion notice and release (5.0, 6.0)')
        insert_figure_after('Figure 3.4 Level 0, part 3: front counter, completion notice and release (5.0, 6.0)',
                            os.path.join(SLIDES, 'logical', '06_DFD_Level0_Part4_BackOffice_Logical.png'),
                            'Figure 3.5 Level 0, part 4: back office and reporting (7.0, 8.0, 9.0)')
        for n in range(13, 5, -1):
            retext('Figure 5.%d Physical Level 1' % n, 'Figure 5.%d Physical Level 1' % (n + 1))
        retext('Figure 5.3 Physical Level 0, part 1', 'Figure 5.3 Physical Level 0, part 1: booking and check-in (1.0, 2.0)', whole=True)
        retext('Figure 5.4 Physical Level 0, part 2', 'Figure 5.4 Physical Level 0, part 2: repair bench (3.0, 4.0)', whole=True)
        retext('Figure 5.5 Physical Level 0, part 3', 'Figure 5.5 Physical Level 0, part 3: completion notice and release (5.0, 6.0)', whole=True)
        insert_figure_after('Figure 5.5 Physical Level 0, part 3: completion notice and release (5.0, 6.0)',
                            os.path.join(SLIDES, 'physical', '06_DFD_Level0_Part4_BackOffice_Physical.png'),
                            'Figure 5.6 Physical Level 0, part 4: back office and reporting (7.0, 8.0, 9.0)')
        insert_figure_after('Figure 6.8 Physical detail 3', os.path.join(SLIDES, 'physical', 'ERD_Full_Physical.png'),
                            'Figure 6.9 Complete physical ERD: every table, key and relationship (full size in QuickPhone_Physical_ERD_Full.pdf)')
        # body text
        retext('shown complete and in three readable parts (front counter, repair bench, back office)',
               'shown complete and in four slide-sized parts (booking and check-in, repair bench, completion notice and release, back office)')
        retext('so Level 0 keeps nine processes and is read in three parts.', 'so Level 0 keeps nine processes and is read in four parts.')
        retext('The complete Level 0 is shown first for reference; the three parts that follow show the same flows at a size that can be read on a slide or page.',
               'The complete Level 0 is shown first for reference; the four parts that follow show the same flows at a size that can be read on a slide or page. Every line runs horizontally or vertically, so lines that must cross do so at right angles (SAD 8e Ch. 4).')
        retext("The physical set applies the textbook's logical-to-physical steps. Each process carries an implementation band, a dashed human–machine boundary encloses the web app and its database, stores list their tables, and flows name their medium (screen, printed label, SMTP email, CSV file).",
               "The physical set applies the textbook's logical-to-physical steps (SAD 8e Ch. 9, Fig. 9-1). Each process carries an implementation band, a dashed human–machine boundary encloses the web app and its database, and each store is a group of tables in that database, named “DB: …” with its tables listed. Following Figs. 9-2 and 9-4, each flow has one noun name that states its medium: “… Input Form” for a screen a person fills in, “… Output Form” for a screen the system shows, “… Printout”, “… Email” and “… File” for paper, the store’s email and an uploaded file, and “DB Record: …” or “DB Record Update: …” for rows read from or written to a store. A Level 0 flow that groups several screens splits into named parts on its Level 1; the full-size set (QuickPhone_Physical_DFD_Set.pdf) lists every split.")
        retext('are listed as foreign keys on the detail diagrams rather than drawn as lines.',
               'are listed as foreign keys on the detail diagrams rather than drawn as lines; the complete physical ERD (Figure 6.9) draws every foreign key as a line (SAD 8e Ch. 10, Step 4).')

    # alt text of each figure = its caption (the paragraph after the image)
    ps = paras()
    for i in range(len(ps) - 1, -1, -1):
        s, e, p = ps[i]
        if '<w:drawing>' in p and i + 1 < len(ps):
            cap = esc(para_text(ps[i + 1][2]).strip())
            if cap.startswith('Figure'):
                p2 = re.sub(r'(descr|title)="[^"]*"', lambda m: '%s="%s"' % (m.group(1), cap), p)
                d = d[:s] + p2 + d[e:]

    # unique drawing ids
    n = [0]
    def did(m):
        n[0] += 1; return '<wp:docPr id="%d"' % n[0]
    d = re.sub(r'<wp:docPr id="\d+"', did, d)
    open(doc_p, 'w', encoding='utf-8').write(d); open(rel_p, 'w', encoding='utf-8').write(rels)
    out = dst + '.tmp'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(tmp, '[Content_Types].xml'), '[Content_Types].xml')
        for root, _, files in os.walk(tmp):
            for f in files:
                full = os.path.join(root, f); arc = os.path.relpath(full, tmp).replace('\\', '/')
                if arc != '[Content_Types].xml':
                    z.write(full, arc)
    os.replace(out, dst)
    shutil.rmtree(tmp)
    print('ok', n[0], 'images')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
