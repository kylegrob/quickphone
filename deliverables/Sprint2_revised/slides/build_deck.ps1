# Builds the QuickPhone Sprint 2 presentation through PowerPoint COM and exports PNG previews.
$ErrorActionPreference = 'Stop'
$dir = $PSScriptRoot
$out = Join-Path $dir 'QuickPhone_Sprint2_Presentation.pptx'

function Rgb([string]$h) { [Convert]::ToInt32($h.Substring(0,2),16) + 256 * [Convert]::ToInt32($h.Substring(2,2),16) + 65536 * [Convert]::ToInt32($h.Substring(4,2),16) }
$NAVY = Rgb '1F4E79'; $NAVY_T = Rgb 'EAF1F8'; $NAVY_L = Rgb 'BFD3E6'; $INK = Rgb '1A2430'; $MUTED = Rgb '55606B'; $FAINT = Rgb '9AA6B2'
$GREEN = Rgb '4D7A2E'; $GREEN_T = Rgb 'EEF5E9'; $GOLD = Rgb '9A6F06'; $GOLD_T = Rgb 'FDF5DD'; $RED = Rgb 'A8432F'; $RED_T = Rgb 'FBEDEA'
$GREY_T = Rgb 'F1F3F5'; $WHITE = Rgb 'FFFFFF'
$HEAD = 'Cambria'; $BODY = 'Calibri'
$SECTIONS = @('Problem', 'Requirements', 'Models', 'Value', 'Reflection')

$pp = New-Object -ComObject PowerPoint.Application
$pres = $pp.Presentations.Add(0)
$pres.PageSetup.SlideWidth = 960; $pres.PageSetup.SlideHeight = 540
$layouts = @{}; foreach ($cl in $pres.SlideMaster.CustomLayouts) { $layouts[$cl.Name] = $cl }
$titleOnly = $layouts['Title Only']; $blank = $layouts['Blank']
$script:n = 0

function TB($s, $x, $y, $w, $h, [string]$text, $size, $color, [switch]$Bold, [switch]$Italic, [string]$font = $BODY, [int]$align = 1, [string]$name) {
  $b = $s.Shapes.AddTextbox(1, $x, $y, $w, $h); if ($name) { $b.Name = $name }
  $tf = $b.TextFrame; $tf.WordWrap = -1; $tf.AutoSize = 0; $tf.MarginLeft = 0; $tf.MarginRight = 0; $tf.MarginTop = 0; $tf.MarginBottom = 0
  $r = $tf.TextRange; $r.Text = $text; $r.Font.Name = $font; $r.Font.Size = $size; $r.Font.Color.RGB = $color
  if ($Bold) { $r.Font.Bold = -1 }; if ($Italic) { $r.Font.Italic = -1 }
  $r.ParagraphFormat.Alignment = $align
  return $b
}
function Box($s, $type, $x, $y, $w, $h, $fill, [string]$name, $radius = 0.06) {
  $b = $s.Shapes.AddShape($type, $x, $y, $w, $h); if ($name) { $b.Name = $name }
  $b.Fill.ForeColor.RGB = $fill; $b.Line.Visible = 0; $b.Shadow.Visible = 0
  if ($type -eq 5) { $b.Adjustments.Item(1) = $radius }
  $b.TextFrame.TextRange.Text = ''
  return $b
}
function Marker($s, $x, $y, [string]$glyph, $fill, $size = 26, [string]$name) {
  $o = Box $s 9 $x $y $size $size $fill $name
  $t = $o.TextFrame; $t.MarginLeft = 0; $t.MarginRight = 0; $t.MarginTop = 0; $t.MarginBottom = 0; $t.WordWrap = 0
  $r = $t.TextRange; $r.Text = $glyph; $r.Font.Name = 'Segoe UI Symbol'; $r.Font.Size = [single][Math]::Round([double]$size / 2); $r.Font.Bold = -1; $r.Font.Color.RGB = $WHITE; $r.ParagraphFormat.Alignment = 2
  return $o
}
# Two-paragraph item: bold heading line, then a muted detail line.
function Item($s, $x, $y, $w, $h, [string]$head, [string]$detail, $headSize = 17, $headColor = $INK, $detailColor = $MUTED, [string]$name) {
  $b = TB $s $x $y $w $h ("{0}`r{1}" -f $head, $detail) 14 $detailColor -name $name
  $p1 = $b.TextFrame.TextRange.Paragraphs(1); $p1.Font.Bold = -1; $p1.Font.Size = $headSize; $p1.Font.Color.RGB = $headColor
  $b.TextFrame.TextRange.Paragraphs(2).ParagraphFormat.SpaceBefore = 2
  return $b
}
function Notes($s, [string]$t) { $s.NotesPage.Shapes.Placeholders.Item(2).TextFrame.TextRange.Text = $t }
function Content([int]$sec, [string]$title, [string]$takeaway) {
  $script:n++
  $s = $pres.Slides.AddSlide($script:n, $titleOnly)
  # section tracker: the current section in navy, the rest muted
  $txt = ($SECTIONS | ForEach-Object -Begin { $i = 0 } -Process { $i++; "$i  $_" }) -join '      '
  $t = TB $s 36 14 700 14 $txt 11 $FAINT -name 'Section tracker'
  $start = 1; for ($k = 0; $k -lt $SECTIONS.Count; $k++) { $seg = "$($k+1)  $($SECTIONS[$k])"; if ($k -eq $sec - 1) { $c = $t.TextFrame.TextRange.Characters($start, $seg.Length); $c.Font.Color.RGB = $NAVY; $c.Font.Bold = -1 }; $start += $seg.Length + 6 }
  $sh = $s.Shapes.Title; $sh.Left = 36; $sh.Top = 30; $sh.Width = 888; $sh.Height = 46
  $tf = $sh.TextFrame; $tf.MarginLeft = 0; $tf.MarginRight = 0; $tf.MarginTop = 0; $tf.MarginBottom = 0; $tf.VerticalAnchor = 3; $tf.WordWrap = -1
  $r = $tf.TextRange; $r.Text = $title; $r.Font.Name = $HEAD; $r.Font.Size = 34; $r.Font.Bold = -1; $r.Font.Color.RGB = $NAVY; $r.ParagraphFormat.Alignment = 1
  if ($takeaway) { [void](TB $s 36 82 888 22 $takeaway 16 $MUTED -name 'Takeaway') }
  [void](TB $s 36 516 400 12 'QuickPhone Repair Tracking System  ·  Sprint 2' 10 $FAINT -name 'Footer')
  [void](TB $s 884 516 40 12 "$($script:n)" 10 $FAINT -align 3 -name 'Slide number')
  return $s
}

# =============================== 1. Title ===============================
$script:n++
$s = $pres.Slides.AddSlide(1, $blank)
$s.FollowMasterBackground = 0; $s.Background.Fill.Solid(); $s.Background.Fill.ForeColor.RGB = $NAVY
[void](TB $s 60 92 840 20 'MIS 4173 SYSTEMS ANALYSIS AND DESIGN  ·  SPRINT 2 REVIEW' 13 $NAVY_L -Bold -name 'Kicker')
[void](TB $s 60 122 840 120 "QuickPhone Repair`rTracking System" 48 $WHITE -Bold -font $HEAD -name 'Deck title')
[void](TB $s 60 262 840 26 'Requirements and analysis: what the system must do, and how the models fit together' 20 $NAVY_L -name 'Subtitle')
[void](TB $s 60 304 840 20 'Kyle Robertson  ·  Ehsanullah Pardisi  ·  Bara Abusamhan  ·  Leonard Mann' 15 $WHITE -name 'Team')
# motif: the job status chain, the thread through the whole deck
$chips = @('Checked In', 'Diagnosing', 'Awaiting Approval', 'In Repair', 'Ready for Pickup', 'Closed')
$cx = 60; $cw = 124; $gap = 19
for ($i = 0; $i -lt $chips.Count; $i++) {
  $c = Box $s 5 $cx 420 $cw 34 (Rgb '2C6496') "Status $($i+1)" 0.5
  $ct = $c.TextFrame; $ct.MarginLeft = 2; $ct.MarginRight = 2; $ct.WordWrap = 0
  $cr = $ct.TextRange; $cr.Text = $chips[$i]; $cr.Font.Name = $BODY; $cr.Font.Size = 13; $cr.Font.Bold = -1; $cr.Font.Color.RGB = $WHITE; $cr.ParagraphFormat.Alignment = 2
  if ($i -lt $chips.Count - 1) { $a = $s.Shapes.AddLine($cx + $cw + 3, 437, $cx + $cw + $gap - 3, 437); $a.Line.ForeColor.RGB = $NAVY_L; $a.Line.Weight = 1.5; $a.Line.EndArrowheadStyle = 2 }
  $cx += $cw + $gap
}
[void](TB $s 60 466 840 16 'Every repair, from check-in to pickup, at both stores' 12 $NAVY_L -Italic -name 'Motif caption')
Notes $s @'
Introduce the team and the client: Quick Phone Repair & Designs, two stores in Raleigh, owner Ashiqullah Pardisi.
Sprint 2 was requirements and analysis. We'll cover the problem, the requirements we're defending, how the models connect, the value, and what we need from you for Sprint 3.
The chain along the bottom is the job status list. It runs through the use cases, the DFDs and the ERD, and you'll see it again.
'@

# =============================== 2. Problem ===============================
$s = Content 1 'Two stores, no shared view of repairs' 'Sprint 1 problem statement, unchanged after the client interview'
[void](TB $s 36 124 420 60 'Staff cannot see, in one place, where each repair stands and which parts it needs.' 20 $INK -Bold -name 'Problem statement')
$cons = @(@('Customers call to ask where their device is', 'Front Desk stops work to find the answer'),
          @('Jobs stall waiting on parts', 'Low stock is noticed too late to reorder'),
          @('Devices can be lost or released to the wrong person', 'No consistent tag or release check'))
for ($i = 0; $i -lt 3; $i++) { $y = 214 + $i * 78; [void](Marker $s 36 ($y + 2) ([string]($i + 1)) $NAVY 24 "Consequence marker $($i+1)"); [void](Item $s 72 $y 380 66 $cons[$i][0] $cons[$i][1] 16 -name "Consequence $($i+1)") }
$stats = @(@('50%', 'fewer "where''s my phone?" calls per store, within 60 days'), @('50%', 'fewer jobs stuck on parts for more than 5 days'), @('0', 'devices lost or released to the wrong person, per quarter'))
for ($i = 0; $i -lt 3; $i++) {
  $y = 124 + $i * 120
  [void](Box $s 5 500 $y 424 104 $NAVY_T "Target card $($i+1)" 0.08)
  [void](TB $s 520 ($y + 22) 130 60 $stats[$i][0] 46 $NAVY -Bold -font $HEAD -name "Target value $($i+1)")
  [void](TB $s 660 ($y + 30) 246 50 $stats[$i][1] 15 $INK -name "Target label $($i+1)")
}
[void](TB $s 500 488 424 16 'Targets from Sprint 1; baseline figures still to confirm with the owner.' 12 $MUTED -Italic -name 'Target caption')
Notes $s @'
The problem hasn't changed since Sprint 1: there's no single, shared view of repair jobs and parts across both stores.
That causes three things: status calls, jobs stalled on parts, and the risk of a lost or wrongly released device.
Those three map to the success measures on the right. They're still targets: we don't yet have the owner's baseline figures, which we'll come back to under limitations.
'@

# =============================== 3. What changed ===============================
$s = Content 1 'What changed since Sprint 1' 'The 21 September client interview confirmed seven requirements; four of them changed the design'
[void](TB $s 216 122 290 16 'SPRINT 1 ASSUMPTION' 12 $MUTED -Bold -name 'Before header')
[void](TB $s 572 122 352 16 'SPRINT 2, CLIENT-CONFIRMED' 12 $GREEN -Bold -name 'After header')
$rows = @(@('Purchasing', 'The Manager orders parts on their own authority', 'The Owner approves every purchase order (new use case UC-09)'),
          @('Parts', 'Parts are reserved for a job, then consumed', 'Parts are deducted automatically when a technician logs them'),
          @('Customer email', 'Alerts on several status changes', 'One completion email, sent from the store''s account'),
          @('Who can email', 'Any staff member', 'Owner, Manager and Front Desk only, never Technicians'))
for ($i = 0; $i -lt 4; $i++) {
  $y = 146 + $i * 86
  [void](TB $s 36 ($y + 22) 160 30 $rows[$i][0] 17 $INK -Bold -name "Row label $($i+1)")
  $b1 = Box $s 5 216 $y 300 70 $GREY_T "Before $($i+1)" 0.1
  [void](TB $s 232 ($y + 14) 270 44 $rows[$i][1] 15 $MUTED -name "Before text $($i+1)")
  $ar = $s.Shapes.AddShape(33, 528, $y + 24, 32, 22); $ar.Name = "Arrow $($i+1)"; $ar.Fill.ForeColor.RGB = $GREEN; $ar.Line.Visible = 0; $ar.Shadow.Visible = 0
  [void](Box $s 5 572 $y 352 70 $GREEN_T "After $($i+1)" 0.1)
  [void](TB $s 588 ($y + 14) 322 44 $rows[$i][2] 15 $INK -Bold -name "After text $($i+1)")
}
[void](TB $s 36 494 888 16 'Also confirmed: four roles, the intake-to-closure workflow, and email as the only customer channel.' 12 $MUTED -Italic -name 'Also confirmed')
Notes $s @'
The client interview on 21 September confirmed seven requirements. Four of them changed what we're building.
Purchasing gains a control step: every PO now waits for the Owner, which adds a use case and new PO statuses.
Reservation is gone: a part leaves stock when the technician logs it.
Email is narrower than Sprint 1 assumed: one completion email, from the store's account, and Technicians can't send it.
'@

# =============================== 4. Consequential requirements ===============================
$s = Content 2 'The requirements that shape the design' 'Each one is client-confirmed and changes what a user does, not just what the screen shows'
$req = @(@('Owner approves every purchase order', 'Gives the Owner control of spending. Adds an approval queue and a "Pending Approval" status.'),
         @('Parts deduct automatically on use', 'Keeps stock accurate without a reservation step. Stock cannot go below zero.'),
         @('Completion email only, never from Technicians', 'One trusted channel from the store''s account. Sending is limited to Owner, Manager and Front Desk.'),
         @('Release only after tag match and photo ID', 'Delivers the "no lost devices" goal. Who released the device is recorded on the job.'))
for ($i = 0; $i -lt 4; $i++) {
  $x = 36 + ($i % 2) * 456; $y = 120 + [Math]::Floor($i / 2) * 186
  [void](Box $s 5 $x $y 432 170 $NAVY_T "Requirement card $($i+1)" 0.06)
  $pill = Box $s 5 ($x + 24) ($y + 22) 118 22 $GREEN "Confirmed tag $($i+1)" 0.5
  $pt = $pill.TextFrame; $pt.MarginLeft = 0; $pt.MarginRight = 0; $pt.MarginTop = 0; $pt.MarginBottom = 0; $pt.WordWrap = 0
  $pr = $pt.TextRange; $pr.Text = 'CLIENT-CONFIRMED'; $pr.Font.Name = $BODY; $pr.Font.Size = 10; $pr.Font.Bold = -1; $pr.Font.Color.RGB = $WHITE; $pr.ParagraphFormat.Alignment = 2
  [void](Item $s ($x + 24) ($y + 58) 384 100 $req[$i][0] $req[$i][1] 19 -name "Requirement $($i+1)")
}
Notes $s @'
Of our 24 requirements, these four do the most to shape the design. All four came out of the client interview.
PO approval adds a whole use case and a control the Owner asked for.
Automatic deduction replaced the reservation design we had in Sprint 1.
The email rule decides who sees the notification screen.
Release checks are how we meet the "no lost devices" target.
'@

# =============================== 5. Team vs AI catalog ===============================
$s = Content 2 'Our catalog versus the AI catalog' 'Our catalog: 18 functional and 6 nonfunctional requirements, 11 confirmed by the client'
[void](TB $s 36 122 888 20 'Claude Opus 5.5 produced 31 requirements from the same interview notes. We sorted every one.' 16 $INK -Bold -name 'Bar heading')
$segs = @(@(11, 'restate ours', $FAINT), @(10, 'salient', $GREEN), @(7, 'spurious', $RED), @(3, 'conflict', $GOLD))
$bx = 36
foreach ($g in $segs) {
  $w = 888 * $g[0] / 31
  $b = Box $s 1 $bx 152 $w 46 $g[2] "Bar $($g[1])"
  $bt = $b.TextFrame; $bt.MarginLeft = 0; $bt.MarginRight = 0; $bt.WordWrap = 0
  $br = $bt.TextRange; $br.Text = "$($g[0]) $($g[1])"; $br.Font.Name = $BODY; $br.Font.Size = 15; $br.Font.Bold = -1; $br.Font.Color.RGB = $WHITE; $br.ParagraphFormat.Alignment = 2
  $bx += $w
}
[void](Box $s 5 36 222 432 252 $GREEN_T 'Kept card' 0.06)
[void](TB $s 60 240 384 24 'Kept: 3 gaps we added' 19 $GREEN -Bold -name 'Kept heading')
$kept = @(@('Awaiting Parts status', 'Shows which jobs are held up by stock'), @('Receiving against an approved PO', 'Closes the purchasing loop'), @('Daily backup', 'Protects the shop''s only record of open repairs'))
for ($i = 0; $i -lt 3; $i++) { $y = 280 + $i * 62; [void](Marker $s 60 ($y + 1) ([string][char]0x2713) $GREEN 22 "Kept marker $($i+1)"); [void](Item $s 92 $y 352 56 $kept[$i][0] $kept[$i][1] 16 -name "Kept $($i+1)") }
[void](Box $s 5 492 222 432 252 $RED_T 'Rejected card' 0.06)
[void](TB $s 516 240 384 24 'Rejected: 7 with no client source' 19 $RED -Bold -name 'Rejected heading')
$rej = @(@('Revenue and productivity reports', 'The Owner asked only for open repairs and parts'), @('Editable email templates, warranty tracking', 'Never raised; warranty is still an open question'), @('2-second pages, 99.5% uptime, 5-minute email', 'Invented targets with no client basis'))
for ($i = 0; $i -lt 3; $i++) { $y = 280 + $i * 62; [void](Marker $s 516 ($y + 1) ([string][char]0x2715) $RED 22 "Rejected marker $($i+1)"); [void](Item $s 548 $y 352 56 $rej[$i][0] $rej[$i][1] 16 -name "Rejected $($i+1)") }
[void](TB $s 36 488 888 16 'Limitation: the AI session had already seen our draft, so the comparison was not fully independent.' 12 $MUTED -Italic -name 'Method caption')
Notes $s @'
We gave Claude Opus 5.5 the same 21 September interview notes and asked for a complete catalog. It returned 31 requirements.
11 restated what we already had. 10 were salient, and three of those exposed real gaps that we added: the Awaiting Parts status, receiving against an approved PO, and daily backup.
7 were spurious, with no source in the interview, so we rejected them. The performance targets are the clearest example: they sound professional, but nobody at Quick Phone asked for them.
The 3 conflicts are on the next slide.
'@

# =============================== 6. Conflicts and stopping ===============================
$s = Content 2 'Conflicts we resolved, and why we can stop' 'Where stakeholders pull in different directions, and how the catalog settles it'
$conf = @(@('Owner  vs  Manager', 'The Owner wants to approve every PO; the Manager needs parts fast.', 'Manager creates, Owner approves; a spending limit is still open.'),
          @('Client rule  vs  AI catalog', 'The AI emailed customers automatically when a technician marked a job done.', 'Drafted as staff-sent, so a Technician can never trigger the email.'),
          @('Front Desk  vs  Owner', 'A busy counter wants fast pickups; the Owner wants zero wrong releases.', 'Tag match and photo ID come before payment, every time.'))
for ($i = 0; $i -lt 3; $i++) {
  $y = 122 + $i * 124
  $pill = Box $s 5 36 $y 196 24 $GOLD_T "Conflict pill $($i+1)" 0.5
  $pt = $pill.TextFrame; $pt.MarginLeft = 0; $pt.MarginRight = 0; $pt.MarginTop = 0; $pt.MarginBottom = 0; $pt.WordWrap = 0
  $pr = $pt.TextRange; $pr.Text = $conf[$i][0]; $pr.Font.Name = $BODY; $pr.Font.Size = 12; $pr.Font.Bold = -1; $pr.Font.Color.RGB = $GOLD; $pr.ParagraphFormat.Alignment = 2
  [void](TB $s 36 ($y + 32) 520 22 $conf[$i][1] 15 $MUTED -name "Conflict tension $($i+1)")
  $res = TB $s 36 ($y + 56) 520 44 ([string][char]0x2192 + '  ' + $conf[$i][2]) 16 $INK -Bold -name "Conflict resolution $($i+1)"
}
[void](Box $s 5 588 122 336 372 $NAVY 'Stopping card' 0.05)
[void](TB $s 612 144 288 26 'Why elicitation can stop' 20 $WHITE -Bold -font $HEAD -name 'Stopping heading')
$stop = @('The interview brought confirmations, not new processes', 'Every Must traces to the client or the Sprint 1 process model', 'The AI''s 31 items added refinements, but no new user or process', 'We reopen only if the two blocking answers add scope')
for ($i = 0; $i -lt 4; $i++) { $y = 190 + $i * 72; [void](Marker $s 612 ($y + 1) ([string][char]0x2713) (Rgb '2C6496') 22 "Stop marker $($i+1)"); [void](TB $s 644 $y 256 64 $stop[$i] 15 $WHITE -name "Stop reason $($i+1)") }
Notes $s @'
Three tensions mattered most.
Owner versus Manager: control of spending against speed. We kept creation with the Manager and approval with the Owner, so the control means something. Whether small or urgent orders skip approval is still a question for the owner.
The AI's automatic email would have let a Technician trigger a customer email, which the client ruled out, so we drafted it as staff-sent.
Front Desk speed versus release safety: the ID check comes first.
Why we can stop eliciting: the last interview confirmed what we had instead of revealing new processes, every Must is traceable, and the AI found refinements but nothing new. Two blocking questions remain, and if either adds scope we reopen elicitation for that item only.
'@

# =============================== 7. One repair, three models ===============================
$s = Content 3 'One repair, three models' 'Every user step in the use cases maps to a DFD process and the ERD entities it writes'
$img = $s.Shapes.AddPicture((Join-Path $dir 'overview_crop.png'), 0, -1, 80, 112, 800, 395)
$img.Name = 'Model overview diagram'
$img.AlternativeText = 'Repair job lifecycle from Checked In to Closed. Each status shows the acting role, its DFD process and ERD entity, with Returned Unrepaired and Awaiting Parts side paths and a parts and purchasing loop where the Owner approves every purchase order.'
Notes $s @'
Walk one job through all three models: UC-06 Release Device. Front Desk is the actor; DFD 5.0 verifies ID, records payment and takes the signature; the data lands in PAYMENT and REPAIR_JOB.
Then the owner control: UC-09 Approve Purchase Order runs through DFD 6.3 and is stored as ApprovedByEmployeeID on PURCHASE_ORDER.
The seven DFD data stores hold the 23 ERD entities, and one status list runs through all three models.
'@

# =============================== 8. Where the models disagreed ===============================
$s = Content 3 'Where the models disagreed' "Four people built the models in parallel; we checked each one against the client's 21 September confirmations"
function Card($s, $x, [string]$head, $tint, $accent, [string]$mark, $items, [string]$name) {
  $y = 116; $w = 432; $h = 380
  [void](Box $s 5 $x $y $w $h $tint "$name card" 0.05)
  [void](TB $s ($x + 22) ($y + 18) ($w - 44) 28 $head 22 $accent -Bold -name "$name heading")
  for ($i = 0; $i -lt $items.Count; $i++) {
    $ry = $y + 66 + $i * 76
    [void](Marker $s ($x + 22) ($ry + 1) $mark $accent 26 "$name marker $($i+1)")
    [void](Item $s ($x + 60) $ry ($w - 82) 64 $items[$i][0] $items[$i][1] 17 -name "$name item $($i+1)")
  }
}
Card $s 36 'Fixed, and why' $GREEN_T $GREEN ([string][char]0x2713) @(
  @('Dropped part reservation', 'The client confirmed parts deduct automatically on use'),
  @('Added Returned Unrepaired', 'Declined jobs no longer get a "repair complete" email'),
  @('ID check before payment', 'The wrong person is never charged or handed a device'),
  @('DFDs renumbered', 'Every diagram now matches the final 11 use cases')) 'Fixed'
Card $s 492 'Still open for the owner' $GOLD_T $GOLD '?' @(
  @('Unpaid release approver', 'Drafted as the Manager, with the reason saved on the job'),
  @('Completion email', 'Sent by staff, or automatically when the repair is done?'),
  @('PO spending limit', 'And an urgent path when the Owner is unavailable'),
  @('Appointments and dashboard', 'Both are in the catalog, but neither has a use case yet')) 'Open'
Notes $s @'
The models were built in parallel, so they drifted. We cross-checked the catalog, use cases, DFDs and ERD against the client's confirmations.
Fixed: reservation was never confirmed, so it's gone. Declined jobs were landing in Ready for Pickup and would have triggered a "repair complete" email, so we added Returned Unrepaired. The DFD took payment before checking ID, so we swapped them. The DFDs cited an older use case numbering.
Still open: these go to the owner before Sprint 3 design.
'@

# =============================== 9. Sprint 2 PSPI ===============================
$s = Content 4 'The Sprint 2 increment' 'An analysis package the owner can sign to freeze the MVP scope before design starts'
$pspi = @(@('24', 'requirements', '11 client-confirmed'), @('11', 'use cases', '4 roles'), @('9', 'data flow diagrams', 'context, Level 0, 7 Level 1'), @('23', 'ERD entities', 'in 7 data stores'))
for ($i = 0; $i -lt 4; $i++) {
  $x = 36 + $i * 228
  [void](TB $s $x 116 204 56 $pspi[$i][0] 50 $NAVY -Bold -font $HEAD -name "PSPI value $($i+1)")
  [void](TB $s $x 176 204 20 $pspi[$i][1] 16 $INK -Bold -name "PSPI label $($i+1)")
  [void](TB $s $x 198 204 18 $pspi[$i][2] 13 $MUTED -name "PSPI detail $($i+1)")
}
$thumbs = @(@('uc_diagram.png', 'Use case diagram'), @('..\DFDs\QuickPhone_DFD_1_Level0.png', 'Level 0 DFD'), @('..\QuickPhone_ERD.png', 'Logical ERD'))
$pics = @(); foreach ($t in $thumbs) { $p = $s.Shapes.AddPicture((Resolve-Path (Join-Path $dir $t[0])).Path, 0, -1, 0, 0, -1, -1); $p.LockAspectRatio = -1; $p.Height = 210; $p.Line.Visible = -1; $p.Line.ForeColor.RGB = (Rgb 'D5DCE3'); $p.Line.Weight = 0.75; $p.Name = $t[1]; $p.AlternativeText = "$($t[1]) from the Sprint 2 analysis package"; $pics += $p }
$total = ($pics | Measure-Object -Property Width -Sum).Sum + 2 * 24
if ($total -gt 888) { $k = (888 - 48) / ($total - 48); foreach ($p in $pics) { $p.Height = $p.Height * $k } }
$x = 36 + (888 - (($pics | Measure-Object -Property Width -Sum).Sum + 48)) / 2
for ($i = 0; $i -lt 3; $i++) { $p = $pics[$i]; $p.Left = $x; $p.Top = 240; [void](TB $s $x (240 + $p.Height + 8) $p.Width 16 $thumbs[$i][1] 13 $MUTED -align 2 -name "$($thumbs[$i][1]) caption"); $x += $p.Width + 24 }
[void](TB $s 36 490 888 16 'Done means: every requirement has an acceptance check and a source, the DFDs balance, and all four models agree.' 12 $MUTED -Italic -name 'Definition of done')
Notes $s @'
This is the Sprint 2 PSPI: the requirements catalog and memo, 11 use cases, nine DFDs and the logical ERD.
It's potentially shippable because the owner can act on it: signing the catalog freezes the MVP scope, so Sprint 3 design starts from a fixed target.
Our definition of done: every requirement has an acceptance check and a source, the DFDs balance with the context diagram, and the four models were cross-checked against each other.
'@

# =============================== 10. Outcomes ===============================
$s = Content 4 'From models to outcomes' 'Each Sprint 1 goal now has a defined process, the data behind it and a clear beneficiary'
[void](TB $s 36 118 230 16 'GOAL' 12 $MUTED -Bold -name 'Goal header')
[void](TB $s 290 118 380 16 'WHAT SPRINT 2 DEFINED' 12 $MUTED -Bold -name 'Defined header')
[void](TB $s 694 118 230 16 'WHO BENEFITS' 12 $MUTED -Bold -name 'Benefit header')
$out3 = @(@('50%', 'fewer status calls', 'A completion email from the store account (UC-05) and instant status lookup (DFD 7.0)', 'Front Desk gets fewer interruptions; customers know without calling'),
          @('50%', 'fewer jobs stuck on parts', 'Awaiting Parts status, a low-stock list, and POs linked to the jobs waiting on them', 'Technicians resume sooner; the Manager reorders before stock runs out'),
          @('0', 'lost devices', 'A device tag at check-in, then tag match and photo ID before payment and release', 'The Owner and customers: every release has a named staff member'))
for ($i = 0; $i -lt 3; $i++) {
  $y = 142 + $i * 112
  [void](Box $s 5 36 $y 888 100 ($(if ($i % 2 -eq 0) { $NAVY_T } else { $GREY_T })) "Outcome row $($i+1)" 0.08)
  [void](TB $s 56 ($y + 18) 90 56 $out3[$i][0] 40 $NAVY -Bold -font $HEAD -name "Outcome value $($i+1)")
  [void](TB $s 150 ($y + 32) 130 40 $out3[$i][1] 15 $INK -Bold -name "Outcome goal $($i+1)")
  [void](TB $s 290 ($y + 22) 380 60 $out3[$i][2] 15 $INK -name "Outcome defined $($i+1)")
  [void](TB $s 694 ($y + 22) 214 60 $out3[$i][3] 14 $MUTED -name "Outcome benefit $($i+1)")
}
[void](TB $s 36 486 888 18 'Estimated value: about $8,952 a year in staff time and fewer lost devices (Sprint 1 estimate, based on analyst assumptions).' 13 $INK -Italic -name 'Value estimate')
Notes $s @'
Rather than list features, here is how the work connects to the three goals.
Status calls: the completion email and instant lookup take the question away from the counter.
Parts: the Awaiting Parts status and PO links make delays visible before they become complaints, and jobs move back to the technician when parts arrive.
Lost devices: the tag and release checks put a named person on every release.
The Sprint 1 estimate puts this at about $8,952 a year in staff time, but those volumes are our assumptions until we have the owner's baseline.
'@

# =============================== 11. AI decisions ===============================
$s = Content 5 'Three AI decisions that shaped Sprint 2' 'We used AI to check our work, and kept the decisions with the team'
$ai = @(@('AI catalog as a check, not a source', 'Claude generated 31 requirements from the same interview notes.', 'We kept 3 gaps it found and rejected 7 with no client source.'),
        @('Rejected the automatic email', 'The AI sent the email when a technician marked a job done.', 'That would let a Technician email customers, so we drafted it as staff-sent.'),
        @('AI cross-check of all four models', 'An AI review compared the catalog, use cases, DFDs and ERD.', 'It caught reservation, status and numbering drift; we chose each fix.'))
for ($i = 0; $i -lt 3; $i++) {
  $x = 36 + $i * 300
  [void](Box $s 5 $x 118 276 336 $NAVY_T "AI decision card $($i+1)" 0.05)
  [void](Marker $s ($x + 22) 140 ([string]($i + 1)) $NAVY 34 "AI decision number $($i+1)")
  [void](TB $s ($x + 22) 190 232 52 $ai[$i][0] 19 $INK -Bold -name "AI decision title $($i+1)")
  [void](TB $s ($x + 22) 254 232 14 'WHAT THE AI DID' 11 $MUTED -Bold -name "AI did label $($i+1)")
  [void](TB $s ($x + 22) 272 232 66 $ai[$i][1] 14 $MUTED -name "AI did $($i+1)")
  [void](TB $s ($x + 22) 352 232 14 'WHAT WE DECIDED' 11 $GREEN -Bold -name "Decided label $($i+1)")
  [void](TB $s ($x + 22) 370 232 90 $ai[$i][2] 15 $INK -Bold -name "Decided $($i+1)")
}
Notes $s @'
Three AI decisions mattered most.
One: we treated the AI catalog as a check on our own, not as the source. That's where the Awaiting Parts gap came from, and it's also why we rejected seven items the client never raised.
Two: the AI's automatic email looked efficient but broke a client rule, because a technician marking a job done would have emailed the customer.
Three: an AI-assisted review compared all four models and found where they disagreed. The team decided each fix, such as dropping reservation and adding Returned Unrepaired.
'@

# =============================== 12. Limitations and feedback ===============================
$s = Content 5 'Limitations, and what we need from you' 'Your answers decide what we design in Sprint 3'
[void](Box $s 5 36 116 400 380 $GREY_T 'Limitations card' 0.05)
[void](TB $s 58 134 356 26 'Limitations' 21 $INK -Bold -name 'Limitations heading')
$lim = @(@('Only the owner was interviewed', 'No front desk or technician input yet'), @('Value figures are estimates', 'No baseline counts of calls, delays or lost devices'), @('The AI comparison was not independent', 'The AI session had already seen our draft'), @('Two catalog versions exist', 'They must be merged before sign-off'))
for ($i = 0; $i -lt 4; $i++) { $y = 178 + $i * 76; [void](Marker $s 58 ($y + 1) '!' $FAINT 24 "Limit marker $($i+1)"); [void](Item $s 92 $y 324 64 $lim[$i][0] $lim[$i][1] 16 -name "Limitation $($i+1)") }
[void](Box $s 5 460 116 464 380 $NAVY_T 'Feedback card' 0.05)
[void](TB $s 482 134 420 26 'Feedback for Sprint 3 design' 21 $NAVY -Bold -name 'Feedback heading')
$fb = @(@('Staff-sent or automatic completion email?', 'Decides whether the pickup screen has a Send button'), @('A PO spending limit, or an urgent path?', 'Decides the Owner''s approval queue'), @('Who may release an unpaid device?', 'Drafted as the Manager'), @('Signature at pickup: keep it or drop it?', 'Sprint 1 removed it; our use case still captures it'), @('Do our intake fields match the counter today?', 'Sets the check-in form'))
for ($i = 0; $i -lt 5; $i++) { $y = 174 + $i * 62; [void](Marker $s 482 ($y + 1) '?' $NAVY 24 "Feedback marker $($i+1)"); [void](Item $s 516 $y 388 56 $fb[$i][0] $fb[$i][1] 16 -name "Feedback $($i+1)") }
Notes $s @'
Limitations: we've only interviewed the owner; our value figures are estimates without a baseline; the AI comparison wasn't fully independent; and the catalog exists in two versions that we'll merge before sign-off.
Then ask for feedback. Each of these questions changes a Sprint 3 screen: the email decision changes the pickup screen, the PO threshold changes the approval queue, and the signature question decides whether we design a signature capture at all.
Ask the audience which one matters most for Sprint 3.
'@

$pres.SaveAs($out, 24)
foreach ($k in 1..$pres.Slides.Count) { $pres.Slides.Item($k).Export((Join-Path $dir "deck_preview_$k.png"), 'PNG', 1600, 900) }
$c = $pres.Slides.Count; $pres.Close(); $pp.Quit()
"saved $out ($c slides)"
