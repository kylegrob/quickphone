# Oct 23: draw the human-machine boundary the way SAD 8e Figs. 9-2 and 9-4 do. A dashed line goes around each person
# who works the system's own screens (Front Desk, Technician, Manager, Owner); the two manual steps in 6.0 sit inside
# the Front Desk's line because they are human action. The Customer gets no line: like the Customer Service Department
# in Fig. 9-2, the customer only receives a printout and an email and never uses the system's interface.
import pathlib, sys

p = pathlib.Path(__file__).with_name('dfd_slides.html')
s = p.read_text(encoding='utf-8')

old_fn = s[s.index('function boundary(b){'):s.index('function legend(x,y){')]
new_fn = r'''// Human-machine boundary (SAD 8e Ch. 9, Step 2; Figs. 9-2, 9-4): a dashed line around each person who uses the
// system's screens, so it separates human action from the automated processes. Manual processes are human action and
// sit inside the Front Desk's line. No line around the Customer: the customer only receives a printout and an email.
const NOUI=['cust'];
function humanBoundaries(nodes,H){
  const people=nodes.filter(n=>n.type==='entity'&&!NOUI.includes(n.id)),manual=nodes.filter(n=>n.manual);
  const labels=[];
  people.forEach(n=>{const grp=[n].concat(n.id==='fd'?manual:[]);
    let l=Math.min(...grp.map(g=>g.x-g.w/2-(g.type==='entity'?8:0)))-14,r=Math.max(...grp.map(g=>g.x+g.w/2))+14;
    let t=Math.min(...grp.map(g=>g.y-g.h/2-(g.type==='entity'?8:0)))-14,b=Math.max(...grp.map(g=>g.y+g.h/2))+34;
    l=Math.max(l,4);t=Math.max(t,-14);b=Math.min(b,H-4);
    mk('rect',{x:l,y:t,width:r-l,height:b-t,rx:14,fill:'none',stroke:C.hmb,'stroke-width':3,'stroke-dasharray':'16 9'});
    labels.push(txt((l+r)/2,b-12,r-l>230?'Human–machine boundary':'Human–machine\nboundary',{fs:15,fw:700,fill:C.hmb,halo:1}));});
  return labels;
}

'''
s = s.replace(old_fn, new_fn)

old_call = "  if(d.boundary&&PHYS){root=gb;boundary(d.boundary);top.appendChild(gb.querySelector('text'));}"
assert s.count(old_call) == 1
s = s.replace(old_call, "  if(d.boundary&&PHYS){root=gb;humanBoundaries(nodes,d.H).forEach(t=>top.appendChild(t));}")
assert 'Django app and PostgreSQL database' not in s
p.write_text(s, encoding='utf-8')
print('ok')
