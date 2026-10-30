# Oct 23 (2): one boundary key per diagram, at the right end of the subtitle row, instead of a label in every box.
import pathlib

p = pathlib.Path(__file__).with_name('dfd_slides.html')
s = p.read_text(encoding='utf-8')

def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)

rep("  const labels=[];\n", "")
rep("b=Math.max(...grp.map(g=>g.y+g.h/2))+34;", "b=Math.max(...grp.map(g=>g.y+g.h/2))+14;")
rep("    mk('rect',{x:l,y:t,width:r-l,height:b-t,rx:14,fill:'none',stroke:C.hmb,'stroke-width':3,'stroke-dasharray':'16 9'});\n"
    "    labels.push(txt((l+r)/2,b-12,r-l>230?'Human–machine boundary':'Human–machine\\nboundary',{fs:15,fw:700,fill:C.hmb,halo:1}));});\n"
    "  return labels;\n}",
    "    mk('rect',{x:l,y:t,width:r-l,height:b-t,rx:14,fill:'none',stroke:C.hmb,'stroke-width':3,'stroke-dasharray':'16 9'});});\n}\n"
    "// key at the right end of the subtitle row (drawn in page coordinates, above the diagram)\n"
    "function boundaryKey(W){const x=W-30,y=80;\n"
    "  const t=txt(x,y,'Human–machine boundary (around each person who uses the system’s screens)',{fs:17,fw:700,anchor:'end',fill:C.hmb});\n"
    "  const w=t.getComputedTextLength();mk('line',{x1:x-w-74,y1:y,x2:x-w-14,y2:y,stroke:C.hmb,'stroke-width':3,'stroke-dasharray':'12 7'});}")
rep("  if(d.boundary&&PHYS){root=gb;humanBoundaries(nodes,d.H).forEach(t=>top.appendChild(t));}",
    "  if(d.boundary&&PHYS){root=gb;humanBoundaries(nodes,d.H);root=svg;boundaryKey(d.W);root=top;}")
p.write_text(s, encoding='utf-8')
print('ok')
