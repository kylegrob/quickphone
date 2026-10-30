# Applies logical_renames.RENAMES to dfd_slides.html. In the source a label may break a line with the two
# characters backslash + n where the name has a space; both forms are matched. Each old name must be found.
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from logical_renames import RENAMES

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dfd_slides.html')
s = open(p, encoding='utf-8').read()
for old, new in sorted(RENAMES, key=lambda r: -len(r[0])):
    pat = re.compile("(['\"])" + r'(?:\s|\\n|\s\\n|\\n\s)'.join(re.escape(w) for w in old.split(' ')) + r"\1")
    n = len(pat.findall(s))
    if n == 0:
        sys.exit('not found: ' + old)
    s = pat.sub(lambda m: m.group(1) + new + m.group(1), s)
    print('%2d  %s -> %s' % (n, old, new))
open(p, 'w', encoding='utf-8').write(s)
