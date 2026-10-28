"""Extract readable Markdown text from .docx, .pptx and .xlsx files.

Standard library only, so it runs anywhere Python 3.9+ is installed.

Usage:
    python tools/extract_text.py                 # mirror docs/ into docs/_text/
    python tools/extract_text.py SRC_DIR OUT_DIR
    python tools/extract_text.py --stdout FILE  # used by git diff (see .gitattributes)

Each Office file becomes OUT_DIR/<same relative path>.md. Images, PDFs and
other files are skipped (agents can open PNG/PDF directly).
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
W = "{%s}" % NS["w"]


def cell_text(s):
    return " ".join(s.split()).replace("|", "\\|")


def md_table(rows):
    rows = [r for r in rows if any(c.strip() for c in r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(cell_text(c) for c in rows[0]) + " |",
           "|" + "---|" * width]
    out += ["| " + " | ".join(cell_text(c) for c in r) + " |" for r in rows[1:]]
    return "\n".join(out)


# ---------- docx ----------

def docx_para(p):
    text = "".join(
        t.text or "" if t.tag == W + "t" else ("\t" if t.tag == W + "tab" else "\n")
        for t in p.iter() if t.tag in (W + "t", W + "tab", W + "br")
    ).strip()
    if not text:
        return ""
    style = p.find("w:pPr/w:pStyle", NS)
    style = style.get(W + "val", "") if style is not None else ""
    m = re.match(r"(?i)heading\s*(\d)", style)
    if m:
        return "#" * min(int(m.group(1)) + 1, 6) + " " + text
    if style.lower() == "title":
        return "# " + text
    if p.find("w:pPr/w:numPr", NS) is not None or "list" in style.lower():
        return "- " + text
    return text


def docx_table(tbl):
    rows = []
    for tr in tbl.findall("w:tr", NS):
        rows.append([" ".join(filter(None, (docx_para(p) for p in tc.iter(W + "p"))))
                     for tc in tr.findall("w:tc", NS)])
    return md_table(rows)


def docx_to_md(path):
    with zipfile.ZipFile(path) as z:
        body = ET.fromstring(z.read("word/document.xml")).find("w:body", NS)
    blocks = []
    for el in body:
        if el.tag == W + "p":
            blocks.append(docx_para(el))
        elif el.tag == W + "tbl":
            blocks.append(docx_table(el))
    return "\n\n".join(b for b in blocks if b)


# ---------- pptx ----------

def slide_order(z):
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    targets = {r.get("Id"): r.get("Target") for r in rels.findall("rel:Relationship", NS)}
    return ["ppt/" + targets[s.get("{%s}id" % NS["r"])].lstrip("/").replace("ppt/", "")
            for s in pres.iterfind("p:sldIdLst/p:sldId", NS)]


def shape_text(root):
    lines = []
    for tbl in root.iter("{%s}tbl" % NS["a"]):
        rows = [[" ".join(t.text or "" for t in tc.iter("{%s}t" % NS["a"]))
                 for tc in tr.findall("a:tc", NS)] for tr in tbl.findall("a:tr", NS)]
        lines.append(md_table(rows))
        tbl.clear()  # keep table text out of the paragraph pass below
    for para in root.iter("{%s}p" % NS["a"]):
        t = "".join(x.text or "" for x in para.iter("{%s}t" % NS["a"])).strip()
        if t:
            lines.append(t)
    return lines


def pptx_to_md(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        for i, slide in enumerate(slide_order(z), 1):
            lines = shape_text(ET.fromstring(z.read(slide)))
            out.append(f"## Slide {i}\n\n" + ("\n\n".join(lines) if lines else "_(no text — image only)_"))
            rels_path = slide.replace("slides/", "slides/_rels/") + ".rels"
            if rels_path in names:
                rels = ET.fromstring(z.read(rels_path))
                for r in rels.findall("rel:Relationship", NS):
                    if r.get("Type", "").endswith("/notesSlide"):
                        notes_path = "ppt/notesSlides/" + Path(r.get("Target")).name
                        notes = [l for l in shape_text(ET.fromstring(z.read(notes_path)))
                                 if not l.isdigit()]
                        if notes:
                            out.append("**Speaker notes:**\n\n" + "\n\n".join(notes))
    return "\n\n".join(out)


# ---------- xlsx ----------

def col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def date_styles(z, names):
    """Indexes of cell styles that format a number as a date."""
    if "xl/styles.xml" not in names:
        return set()
    root = ET.fromstring(z.read("xl/styles.xml"))
    custom = {int(f.get("numFmtId")): f.get("formatCode", "")
              for f in root.iterfind("s:numFmts/s:numFmt", NS)}

    def is_date(fid):
        if 14 <= fid <= 22 or 45 <= fid <= 47:
            return True
        code = re.sub(r'"[^"]*"|\[[^\]]*\]', "", custom.get(fid, "")).lower()
        return bool(re.search(r"[dmy]", code))

    xfs = root.findall("s:cellXfs/s:xf", NS)
    return {i for i, xf in enumerate(xfs) if is_date(int(xf.get("numFmtId", 0)))}


def serial_to_date(v):
    from datetime import date, timedelta
    d = float(v)
    base = date(1899, 12, 30) + timedelta(days=int(d))
    return base.isoformat()


def xlsx_to_md(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        dates = date_styles(z, names)
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("s:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["s"])))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {r.get("Id"): r.get("Target") for r in rels.findall("rel:Relationship", NS)}
        for sheet in wb.iterfind("s:sheets/s:sheet", NS):
            target = targets[sheet.get("{%s}id" % NS["r"])].lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            root = ET.fromstring(z.read(target))
            rows = []
            for row in root.iterfind("s:sheetData/s:row", NS):
                cells = {}
                for c in row.findall("s:c", NS):
                    v = c.find("s:v", NS)
                    if c.get("t") == "s" and v is not None:
                        val = shared[int(v.text)]
                    elif c.get("t") == "inlineStr":
                        val = "".join(t.text or "" for t in c.iter("{%s}t" % NS["s"]))
                    elif v is not None and int(c.get("s", 0)) in dates:
                        val = serial_to_date(v.text)
                    else:
                        val = v.text if v is not None else ""
                    cells[col_index(c.get("r"))] = val or ""
                if cells:
                    rows.append([cells.get(i, "") for i in range(max(cells) + 1)])
            out.append(f"## Sheet: {sheet.get('name')}\n\n" + (md_table(rows) or "_(empty)_"))
    return "\n\n".join(out)


CONVERTERS = {".docx": docx_to_md, ".pptx": pptx_to_md, ".xlsx": xlsx_to_md}


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--stdout":  # git diff textconv
        f = Path(sys.argv[2])
        sys.stdout.reconfigure(encoding="utf-8")
        print(CONVERTERS[f.suffix.lower()](f))
        return
    root = Path(__file__).resolve().parent.parent
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "docs"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "docs" / "_text"
    for f in sorted(src.rglob("*")):
        conv = CONVERTERS.get(f.suffix.lower())
        if not conv or f.name.startswith("~$") or dst in f.parents:
            continue
        rel = f.relative_to(src)
        target = dst / (str(rel) + ".md")
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            body = conv(f)
        except Exception as e:  # keep going; one bad file shouldn't stop the rest
            body = f"_Extraction failed: {e}_"
        header = (f"<!-- Auto-generated from docs/{rel.as_posix()} by tools/extract_text.py. "
                  "Do not edit by hand; edit the original and re-run. -->\n\n"
                  f"# {f.stem}\n\n")
        with open(target, "w", encoding="utf-8", newline="\n") as out:
            out.write(header + body + "\n")
        print(f"{rel} -> {target.relative_to(dst.parent) if dst.parent in target.parents else target}")


if __name__ == "__main__":
    main()
