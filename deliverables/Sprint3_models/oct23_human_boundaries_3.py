# Oct 23 (3): the boundary key goes on whichever header row has room (subtitle row, then title row), and falls back to
# a short wording, so it never runs into a long subtitle.
import pathlib

p = pathlib.Path(__file__).with_name('dfd_slides.html')
s = p.read_text(encoding='utf-8')

def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)

a = s.index('function boundaryKey(W){')
b = s.index('}\n', s.index("'stroke-dasharray':'12 7'});}", a)) + 2
s = s[:a] + r'''function boundaryKey(W,hdr){const x=W-30;
  const ends=hdr.map(t=>t?t.getBBox().x+t.getBBox().width:0); // [title row, subtitle row]
  for(const words of ['Human–machine boundary (around each person who uses the system’s screens)','Human–machine boundary'])
    for(const [row,y] of [[1,80],[0,42]]){
      const t=txt(x,y,words,{fs:17,fw:700,anchor:'end',fill:C.hmb}),w=t.getComputedTextLength();
      if(x-w-74>ends[row]+30){mk('line',{x1:x-w-74,y1:y,x2:x-w-14,y2:y,stroke:C.hmb,'stroke-width':3,'stroke-dasharray':'12 7'});return;}
      t.remove();}
}
''' + s[b:]
rep("  txt(40,42,d.title+(key==='align'?'':PHYS?' (physical)':' (logical)'),{fs:32,fw:700,anchor:'start',fill:'#1f4e79'});\n"
    "  if(d.sub)txt(40,80,pick(d.sub),{fs:20,anchor:'start',fill:'#555'});",
    "  const hdr=[txt(40,42,d.title+(key==='align'?'':PHYS?' (physical)':' (logical)'),{fs:32,fw:700,anchor:'start',fill:'#1f4e79'}),\n"
    "    d.sub?txt(40,80,pick(d.sub),{fs:20,anchor:'start',fill:'#555'}):null];")
rep("root=svg;boundaryKey(d.W);root=gb;}", "root=svg;boundaryKey(d.W,hdr);root=gb;}")
p.write_text(s, encoding='utf-8')
print('ok')
