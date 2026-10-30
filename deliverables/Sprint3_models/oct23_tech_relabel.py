# Oct 23: name the implementation on the physical DFDs (SAD 8e Ch. 9, Step 1; Figs. 9-2 and 9-4).
# Stores become "PostgreSQL: <store>", store flows "PostgreSQL Record: ..." / "PostgreSQL Record Update: ...",
# process bands name Django (Python) instead of "Web app". Basis: Sprint 3 alternative matrix and hw/sw specification.
import pathlib, re, sys

p = pathlib.Path(__file__).with_name('dfd_slides.html')
s = p.read_text(encoding='utf-8')
n0 = len(s)

def sub(old, new, count_expected=None):
    global s
    c = s.count(old)
    if c == 0:
        sys.exit(f'not found: {old!r}')
    if count_expected is not None and c != count_expected:
        sys.exit(f'{old!r}: expected {count_expected}, found {c}')
    s = s.replace(old, new)
    return c

# Data store names, shrunk to fit the box (never below 19 px) when the longer prefix overflows.
sub("    // Physical store names say how the store is implemented (SAD 8e Ch. 9 Step 1): tables in the shared database\n"
    "    txt(n.x-hw+78,ty,PHYS?'DB: '+n.label:n.label,{fs:22,fw:700,anchor:'start',fill:'#1a1a1a'});",
    "    // Physical store names say how the store is implemented (SAD 8e Ch. 9 Step 1): tables in the PostgreSQL database\n"
    "    const sn=txt(n.x-hw+78,ty,PHYS?'PostgreSQL: '+n.label:n.label,{fs:22,fw:700,anchor:'start',fill:'#1a1a1a'});\n"
    "    if(PHYS){const av=n.w-78-10,len=sn.getComputedTextLength();if(len>av)sn.setAttribute('font-size',Math.max(19,Math.floor(22*av/len)));}", 1)

c1 = sub('DB Record', 'PostgreSQL Record')
c2 = sub("Web app; one DB transaction", "Django; one transaction", 1)
sub("impl:'Web application at counter\\nand bench PCs + one\\nshared database'",
    "impl:'Django web app at counter\\nand bench devices; one\\nPostgreSQL database'", 1)
c3 = sub("impl:'Web app", "impl:'Django")
c4 = sub("'Web app", "'Django")  # the PROC table used on the Level 0 diagrams
sub("'Human–machine boundary: QuickPhone web app and database'",
    "'Human–machine boundary: QuickPhone Django app and PostgreSQL database'", 1)

left = re.findall(r"Web app|DB: |DB Record", s)
p.write_text(s, encoding='utf-8')
print(f'store flows {c1}, L1 bands {c3}, L0 bands {c4}; leftover {left}; {n0} -> {len(s)} chars')
