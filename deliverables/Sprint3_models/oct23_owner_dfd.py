# Oct 23: apply the owner's eight clarifications to the DFDs (dfd_slides.html, both views).
#  #1 pickup notification sent by a click from a Technician or authorized staff  -> Technician -> 5.0 / 5.4
#  #2 a Manager approves every purchase order (not the Owner)                     -> 7.3 moves to the Manager
#  #3 low-stock alerts, technician part requests, no automatic ordering           -> 7.1 alert, 4.4 part request
#  #4 manual assignment; technicians may claim jobs and appointments              -> 3.1 Select Repair Job, D2 on 3.0
#  #5 no diagnostic fee when a device cannot be repaired                          -> 6.2 -> 6.4 no-charge path
#  #6 Managers set reorder points (already 9.3)                                   -> wording only
#  #7 optional device passcode at intake                                          -> Passcode Input Form into 2.4
#  #8 stores use ThinkPad computers                                               -> process bands
# Also fixes 4.0: the Stock Shortage line from 4.2 ended on 4.3 instead of 4.4.
import pathlib, sys

p = pathlib.Path(__file__).with_name('dfd_slides.html')
s = p.read_text(encoding='utf-8')


def sub(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit(f'expected {n}, found {c}: {old[:90]!r}')
    s = s.replace(old, new)


# ---------- Level 0 flow table ----------
sub(" e5e:['p5','fd',['Notification preview','Email Preview Output Form']],",
    " e5e:['p5','fd',['Notification preview','Email Preview Output Form']],\n"
    " e5f:['tech','p5',['Technician send request','Send Notification Input Form']],")
sub(" e7b:['p7','mgr',['Low-stock report','Low-Stock Output Form']],",
    " e7b:['p7','mgr',['Low-stock alert','Low-Stock Alert Output Form']],")
sub(" e7c:['own','p7',['Purchase order approval','PO Approval Input Form']], e7d:['p7','own',['Purchase orders awaiting approval','Pending POs Output Form']],",
    " e7c:['mgr','p7',['Purchase order approval','PO Approval Input Form']], e7d:['p7','mgr',['Purchase orders awaiting approval','Pending POs Output Form']],")
sub(" s3a:['d3','p3',['Diagnosis queue','PostgreSQL Record: Diagnosis Queue']],",
    " s3d:['d2','p3',['Unassigned appointments','PostgreSQL Record: Unassigned Appointments']], s3e:['p3','d2',['Appointment claim','PostgreSQL Record Update: Appointment Claimed']],\n"
    " s3a:['d3','p3',['Diagnosis queue','PostgreSQL Record: Diagnosis Queue']],")

# ---------- process bands (ThinkPads, #8) ----------
sub("p3:['3.0','Record\\nDiagnosis','Django · bench PC'],p4:['4.0','Record Repair\\nWork','Django · bench PC'],",
    "p3:['3.0','Record\\nDiagnosis','Django · bench ThinkPad'],p4:['4.0','Record Repair\\nWork','Django · bench ThinkPad'],")
sub("impl:'Django web app at counter\\nand bench devices; one\\nPostgreSQL database'",
    "impl:'Django web app on the\\nstores\\' ThinkPads; one\\nPostgreSQL database'")

# ---------- context ----------
sub("E('tech',165,887,'Repair\\nTechnician',{h:175}),", "E('tech',165,887,'Repair\\nTechnician',{h:175}),")
sub("E('cust',1700,75,'Customer',{w:300,h:130}),E('own',1700,315,'Store\\nOwner',{w:300,h:250}),E('mgr',1700,725,'Store\\nManager',{w:300,h:480})],",
    "E('cust',1700,75,'Customer',{w:300,h:130}),E('own',1700,235,'Store\\nOwner',{w:300,h:110}),E('mgr',1700,652,'Store\\nManager',{w:300,h:625})],")
sub("   ...ctx('tech',['e3c','e3d','e4a','e4b'],820,42),",
    "   ...ctx('tech',['e3c','e3d','e4a','e4b','e5f'],815,36),")
sub("   ...ctx('own',['e7c','e7d','e8d','e8c'],215,60),\n"
    "   ...ctx('mgr',['e7a','e7e','e7f','e7b','e7g','e7h','e9a','e9c','e9b','e9d'],PHYS?505:510,PHYS?45:55)];})()};",
    "   ...ctx('own',['e8d','e8c'],215,45),\n"
    "   ...ctx('mgr',['e7b','e7a','e7d','e7c','e7e','e7g','e7f','e7h','e9a','e9c','e9b','e9d'],PHYS?370:375,PHYS?50:55)];})()};")

# ---------- Level 0 parts ----------
sub("  PR('p4',PXP,200,{h:280}),PR('p3',PXP,640,{h:420}),S('d4',SXP,200,160),S('d3',SXP,640,420)],",
    "  PR('p4',PXP,200,{h:280}),PR('p3',PXP,640,{h:420}),S('d4',SXP,170,160),S('d2',SXP,370,100),S('d3',SXP,690,380)],")
sub(" nodes:[E('fd',EXP,380,'Front Desk\\nStaff',{h:600}),E('cust',PXP,895,'Customer',{w:300,h:90}),\n"
    "  PR('p6',PXP,200,{h:280}),PR('p5',PXP,590,{h:300}),S('d1',SXP,150,160),S('d3',SXP,470,360),S('d7',SXP,760,100)],\n"
    " flows:[L('e6a',{y:110}),L('e6b',{y:170}),L('e6d',{y:230}),L('e6e',{y:290}),L('e5a',{y:520}),L('e5b',{y:580}),L('e5e',{y:640}),L('e5c',{x:PXP})]});",
    " nodes:[E('fd',EXP,370,'Front Desk\\nStaff',{h:580}),E('tech',EXP,790,'Repair\\nTechnician',{h:140}),E('cust',PXP,895,'Customer',{w:300,h:90}),\n"
    "  PR('p6',PXP,200,{h:280}),PR('p5',PXP,600,{h:330}),S('d1',SXP,150,160),S('d3',SXP,470,360),S('d7',SXP,760,100)],\n"
    " flows:[L('e6a',{y:110}),L('e6b',{y:170}),L('e6d',{y:230}),L('e6e',{y:290}),L('e5a',{y:520}),L('e5b',{y:580}),L('e5e',{y:640}),L('e5f',{y:755}),L('e5c',{x:PXP})]});")
sub(" nodes:[E('mgr',EXP,285,'Store\\nManager',{h:550}),E('own',EXP,690,'Store\\nOwner',{h:200}),E('fd',EXP,895,'Front Desk\\nStaff',{h:130}),\n"
    "  PR('p9',PXP,130,{h:240}),PR('p7',PXP,470,{h:400}),PR('p8',PXP,835,{h:270}),",
    " nodes:[E('mgr',EXP,315,'Store\\nManager',{h:610}),E('own',EXP,733,'Store\\nOwner',{h:86}),E('fd',EXP,895,'Front Desk\\nStaff',{h:130}),\n"
    "  PR('p9',PXP,130,{h:240}),PR('p7',PXP,465,{h:390}),PR('p8',PXP,835,{h:270}),")
sub("  L('e7a',{y:300}),L('e7e',{y:345}),L('e7f',{y:390}),L('e7b',{y:435}),L('e7g',{y:480}),L('e7h',{y:525}),\n"
    "  L('e7c',{y:610}),L('e7d',{y:650}),L('e8d',{y:740}),L('e8c',{y:780}),L('e8a',{y:860}),L('e8b',{y:920})]});",
    "  L('e7b',{y:300}),L('e7a',{y:340}),L('e7d',{y:380}),L('e7c',{y:420}),L('e7e',{y:460}),L('e7g',{y:500}),L('e7f',{y:540}),L('e7h',{y:580}),\n"
    "  L('e8d',{y:715}),L('e8c',{y:752}),L('e8a',{y:860}),L('e8b',{y:920})]});")

# ---------- complete Level 0 ----------
sub("  // 2.0 sits last so its claim ticket drops straight down to the Customer; 5.0's notification takes the gap on the left\n"
    "  const LEFT=['p1','p8','p6','p5','p2'],",
    "  // 5.0 sits last so its email drops straight down to the Customer and the Technician's send request can enter it\n"
    "  // from below; 2.0's claim ticket takes the gap on the left\n"
    "  const LEFT=['p1','p8','p6','p2','p5'],")
sub("  outer.p5.push({k:'e5c',p:'p5',cust:1});                                    // lowest port on 5.0's left edge",
    "  outer.p2.push({k:'e2d',p:'p2',cust:1});                                    // lowest port on 2.0's left edge")
sub("  const ERx=RPR+EZ+EW/2,W=ERx+EW/2+M;",
    "  const ERx=RPR+EZ+EW/2,XT=ERx+EW/2+40,W=XT+M+20;                            // XT: Technician -> 5.0 riser")
sub("  fl.push(L('e2d',{x:LPx}));\n"
    "  const p7b=nodes.p7.y+nodes.p7.h;\n"
    "  fl.push(L('e7c',{pts:[[RPx-70,(p7b+Yb)/2]],lp:[RPx-82,Yb-84],la:'end'}));\n"
    "  fl.push(L('e7d',{pts:[[RPx+70,(p7b+Yb)/2]],lp:[RPx+82,Yb-84],la:'start'}));",
    "  fl.push(L('e5c',{pts:[[LPx-60,bottom+20]],lp:[LPx-72,(bottom+Yb-45)/2],la:'end'}));\n"
    "  // the Technician's send request runs down the right edge, along the bottom and up into 5.0\n"
    "  const tY=(nodes.p3.y+nodes.p4.y+nodes.p4.h)/2;\n"
    "  fl.push(L('e5f',{pts:[[XT,tY],[XT,Yb-100],[LPx+100,Yb-100]],lp:[LPx+120,Yb-114],la:'start'}));")

# ---------- Level 1 2.0: passcode (#7), optional assignment (#4) ----------
sub(" sub:'From UC-01 and FR02–FR04. 2.1 finds a returning customer by phone; 2.2 creates the record when none matches or updates the one found.',",
    " sub:['From UC-01 and FR02–FR04. 2.1 finds a returning customer; 2.4 takes an optional device passcode and an optional technician.',\n"
    "  'From UC-01 and FR02–FR04. The passcode is optional (needed for camera repairs) and stored encrypted; the technician is optional.'],")
sub("  F('fd','p24',['Technician assignment','Technician Assignment Input Form'],{y:645}),",
    "  F('fd','p24',['Device passcode','Passcode Input Form'],{y:605}),\n"
    "  F('fd','p24',['Technician assignment','Technician Assignment Input Form'],{y:675}),")

# ---------- Level 1 3.0: technicians claim jobs and appointments (#4) ----------
sub(" sub:'From UC-02 and UC-03 (FR05–FR07). The system records the diagnosis and quote; the technician does the diagnosing.',boundary:BND,ortho:1,\n"
    " nodes:[E('tech',EX,385,'Repair\\nTechnician',{h:750}),E('fd',EX,880,'Front Desk\\nStaff',{h:160}),\n"
    "  P('p31',PX,R5[0],'3.1','Retrieve\\nAssigned Jobs',{impl:'Django job queue'}),P('p32',PX,R5[1],'3.2','Record Diagnosis\\nFindings',{impl:'Django diagnosis form',fs:24}),\n"
    "  P('p33',PX,R5[2],'3.3','Check Part\\nStock',{impl:'Django stock lookup'}),P('p34',PX,R5[3],'3.4','Record Repair\\nQuote',{impl:'Django quote form'}),\n"
    "  P('p35',PX,R5[4],'3.5','Record Quote\\nDecision',{impl:'Django approval queue'}),\n"
    "  S('d4',SX,70,110),S('d3',SX,580,720)],\n"
    " flows:[F('tech','p31',['Job to diagnose','Diagnosis Job Selection Input Form'],{y:65}),F('p31','tech',['Assigned job queue','Assigned Jobs Output Form'],{y:125}),\n"
    "  F('d3','p31',['Assigned jobs','PostgreSQL Record: Assigned Jobs'],{ao:[0,-330],bo:[0,30]}),F('p31','p32',['Job under diagnosis','Job Under Diagnosis'],{x:PX}),\n"
    "  F('tech','p32',['Diagnosis','Diagnosis Findings Input Form'],{y:290}),",
    " sub:['From UC-02 and UC-03 (FR04–FR07). A technician works their own jobs and may claim an unassigned job or appointment (3.1).',\n"
    "  'From UC-02 and UC-03 (FR04–FR07). 3.1 lists the technician\\'s jobs and the unassigned jobs and appointments they may claim.'],boundary:BND,ortho:1,\n"
    " nodes:[E('tech',EX,385,'Repair\\nTechnician',{h:750}),E('fd',EX,880,'Front Desk\\nStaff',{h:160}),\n"
    "  P('p31',PX,110,'3.1','Select Repair\\nJob',{impl:'Django job queue; claim button',h:210}),P('p32',PX,320,'3.2','Record Diagnosis\\nFindings',{impl:'Django diagnosis form',fs:24}),\n"
    "  P('p33',PX,505,'3.3','Check Part\\nStock',{impl:'Django stock lookup'}),P('p34',PX,690,'3.4','Record Repair\\nQuote',{impl:'Django quote form'}),\n"
    "  P('p35',PX,880,'3.5','Record Quote\\nDecision',{impl:'Django approval queue'}),\n"
    "  S('d2',SX,60,96),S('d4',SX,215,110),S('d3',SX,630,620)],\n"
    " flows:[F('tech','p31',['Job to diagnose','Diagnosis Job Selection Input Form'],{y:60}),F('p31','tech',['Job queue','Job Queue Output Form'],{y:115}),\n"
    "  F('tech','p31',['Job claim','Job Claim Input Form'],{y:170}),\n"
    "  F('d3','p31',['Own and unassigned jobs','PostgreSQL Record: Open Jobs'],{ao:[0,-330],bo:[0,30]}),F('p31','d3',['Job claim record','PostgreSQL Record Update: Job Claimed']),\n"
    "  F('d2','p31',['Unassigned appointments','PostgreSQL Record: Unassigned Appointments']),F('p31','d2',['Appointment claim','PostgreSQL Record Update: Appointment Claimed']),\n"
    "  F('p31','p32',['Job under diagnosis','Job Under Diagnosis'],{x:PX}),\n"
    "  F('tech','p32',['Diagnosis','Diagnosis Findings Input Form'],{y:320}),")
sub("F('p33','tech',['Part availability','Part Availability Output Form'],{y:485}),",
    "F('p33','tech',['Part availability','Part Availability Output Form'],{y:505}),")
sub("  F('tech','p34',['Labor amount','Labor Amount Input Form'],{y:680}),",
    "  F('tech','p34',['Labor amount','Labor Amount Input Form'],{y:690}),")

# ---------- Level 1 4.0: part requests (#3) and the misrouted Stock Shortage line ----------
sub(" sub:'From UC-04 (FR06, FR07). Recording a part as used deducts it from the store\\'s stock automatically; there is no reservation.',",
    " sub:'From UC-04 (FR06, FR07). A part used is deducted from stock automatically; a part request goes to the Manager, who orders it.',")
sub("P('p44',PX,R5[3],'4.4','Record Parts\\nShortage',{impl:'Django; listed for Manager'}),",
    "P('p44',PX,R5[3],'4.4','Record Part\\nRequest',{impl:'Django; listed for Manager'}),")
sub("  F('p42','p44',['Stock shortage','Stock Shortage'],{pts:[[PX-180,330],[PX-180,560]],lp:[PX-192,445],la:'end'}),",
    "  F('p42','p44',['Stock shortage','Stock Shortage'],{pts:[[PX-180,330],[PX-180,615]],lp:[PX-192,470],la:'end'}),")
sub("  F('p44','d3',['Parts shortage record','PostgreSQL Record:\\nParts Shortage'],{ao:[0,0],bo:[0,-10]}),F('p44','tech',['Parts shortage notice','Parts Shortage Output Form'],{y:680}),",
    "  F('tech','p44',['Part request','Part Request Input Form'],{y:665}),\n"
    "  F('p44','d3',['Part request record','PostgreSQL Record:\\nPart Request'],{ao:[0,0],bo:[0,-10]}),F('p44','tech',['Part request confirmation','Part Request Output Form'],{y:725}),")

# ---------- Level 1 5.0: a Technician may send (#1) ----------
sub(" sub:['From UC-05 (FR12, NFR05). One pickup notification email from the store\\'s account, sent by Owner, Manager or Front Desk; never by a Technician.',\n"
    "  'UC-05 (FR12, NFR05). Open question: staff-sent or automatic email. Drawn staff-sent; if automatic, the Send Approval Input Form is removed.'],boundary:BND,ortho:1,\n"
    " nodes:[E('fd',EX,385,'Front Desk\\nStaff',{h:750}),E('cust',450,895,'Customer',{w:220,h:100}),\n"
    "  P('p51',PX,R5[0],'5.1','List Jobs Ready\\nfor Pickup',{impl:'Django list; no Technicians',fs:24}),",
    " sub:['From UC-05 (FR12). Never automatic: staff, or the Technician who finished the repair, click Send. The system fills in the address.',\n"
    "  'From UC-05 (FR12). Sent only on a click: Send Approval (staff) or Send Notification (Technician); the Technician never sees the address.'],boundary:BND,ortho:1,\n"
    " nodes:[E('fd',EX,335,'Front Desk\\nStaff',{h:650}),E('tech',EX,790,'Repair\\nTechnician',{h:180}),E('cust',1700,880,'Customer',{w:260,h:90}),\n"
    "  P('p51',PX,R5[0],'5.1','List Jobs Ready\\nfor Pickup',{impl:'Django ready-jobs list',fs:24}),")
sub("  F('fd','p54',['Send instruction','Send Approval Input Form'],{y:680}),F('p54','cust',['Pickup notification','Pickup Notification Email'],{pts:[[450,745]],lp:[536,731]}),",
    "  F('fd','p54',['Send instruction','Send Approval Input Form'],{y:640}),F('tech','p54',['Technician send request','Send Notification Input Form'],{y:735}),\n"
    "  F('p54','cust',['Pickup notification','Pickup Notification Email'],{pts:[[1700,745]],lp:[954,731],la:'start'}),")

# ---------- Level 1 6.0: no diagnostic fee for an unrepairable device (#5) ----------
sub(" sub:['From UC-06 (FR08). A device is released only after payment is recorded; only the fact of the ID check is stored.',\n"
    "  'From UC-06 (FR08). The photo-ID check (6.5) and taking payment (6.6) are manual; the card machine is not linked to the system.'],",
    " sub:['From UC-06 (FR08). Released only after payment is recorded. A device that could not be repaired owes nothing (no diagnostic fee).',\n"
    "  'From UC-06 (FR08). 6.5 and 6.6 are manual. An unrepairable device owes nothing (no diagnostic fee), so 6.3 settles it with no payment.'],")
sub("F('p63','p64',['Paid job','Paid Job'],{x:PX6}),", "F('p63','p64',['Settled job','Settled Job'],{x:PX6}),")

# ---------- Level 1 7.0: Manager approves (#2), low-stock alert and part requests (#3) ----------
sub(" sub:'From UC-08 to UC-10 (FR09, FR10). The Owner approves every purchase order; orders are placed with the supplier outside the system.',boundary:[650,-5,1258,975],ortho:1,\n"
    " nodes:[E('mgr',115,485,'Store\\nManager',{w:170,h:940}),E('own',360,463,'Store\\nOwner',{w:190,h:130}),\n"
    "  P('p71',PX7,80,'7.1','List Low-Stock\\nParts',{impl:'Django report',h:160}),",
    " sub:'From UC-08 to UC-10 (FR09, FR10). A Manager approves every order and places it with the supplier outside the system; nothing is ordered automatically.',boundary:[650,-5,1258,975],ortho:1,\n"
    " nodes:[E('mgr',115,485,'Store\\nManager',{w:170,h:940}),\n"
    "  P('p71',PX7,80,'7.1','List Parts\\nto Order',{impl:'Django; alert at reorder point',h:160}),")
sub("F('d3','p71',['Jobs awaiting parts','PostgreSQL Record: Jobs Awaiting Parts'],{ao:[0,-50],bo:[0,50]}),\n"
    "  F('p71','mgr',['Low-stock report','Low-Stock Output Form'],{y:80}),",
    "F('d3','p71',['Open part requests','PostgreSQL Record: Open Part Requests'],{ao:[0,-50],bo:[0,50]}),\n"
    "  F('p71','mgr',['Low-stock alert','Low-Stock Alert Output Form'],{y:80}),")
sub("P('p73',PX7,460,'7.3','Record Purchase\\nOrder Approval',{impl:'Django queue (Owner only)',h:160}),",
    "P('p73',PX7,460,'7.3','Record Purchase\\nOrder Approval',{impl:'Django queue (Manager only)',h:160}),")
sub("  F('p73','own',['Purchase orders\\nawaiting approval','Pending POs Output Form'],{y:435}),F('own','p73',['Purchase order approval','PO Approval Input Form'],{y:492}),",
    "  F('p73','mgr',['Purchase orders\\nawaiting approval','Pending POs Output Form'],{y:435}),F('mgr','p73',['Purchase order approval','PO Approval Input Form'],{y:492}),")

# ---------- alignment slide: 3.0 now reads and updates D2 ----------
sub("const rows=[['D1','Customers & Devices','CUSTOMER, DEVICE','1.0, 2.0','1.0, 2.0, 5.0, 6.0, 8.0'],\n"
    "   ['D2','Appointments','APPOINTMENT','1.0, 2.0','1.0, 2.0'],",
    "const rows=[['D1','Customers & Devices','CUSTOMER, DEVICE','1.0, 2.0','1.0, 2.0, 5.0, 6.0, 8.0'],\n"
    "   ['D2','Appointments','APPOINTMENT','1.0, 2.0, 3.0','1.0, 2.0, 3.0'],")
sub("'3.0':{D3:'CRU',D4:'R'}", "'3.0':{D2:'RU',D3:'CRU',D4:'R'}")

p.write_text(s, encoding='utf-8')
print('ok')
