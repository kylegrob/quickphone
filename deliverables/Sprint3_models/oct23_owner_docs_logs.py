# Oct 23: log rows for carrying the owner's clarifications and the Screen/Input Form names into the models docx,
# the DFD and ERD slides deck and the Sprint 3 presentation.
import os
from oct23_erd_twoway_logs import LOGS
from oct23_screen_logs import append

AI_ROWS = [
 ['2026-10-23', 3, 'DFD and ERD Models (sections 3, 5, 6, 7; Appendices A and B), DFD and ERD Slides, Sprint 3 Presentation',
  'Claude Opus 5.5',
  'Carried the owner\'s October 23 clarifications and the Screen/Input Form names into the three documents: swapped every '
  'diagram image; rewrote Table 3.1 rows 2.0 to 7.0, the section 5 naming rule and implementation paragraph, the section 6 '
  'physical design note, Tables 7.1 and 7.2 and the appointment decision; edited eight Appendix A columns and added '
  'repair_job.device_passcode; rebuilt Appendix B (now 80 Level 0 and 91 Level 1-only flows, checked one-for-one against '
  'the diagrams); rewrote speaker notes in both decks and the presentation slides on equipment, the prototypes, risks, '
  'decisions needed and next steps. Fixed two existing slips: a broken sentence in the presentation\'s ERD detail 2 notes '
  'and "three Level 0 parts" (four) in the slides deck.',
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: the owner\'s October 23 clarifications 1 to 8 and docs/project-context.md; page 2 of '
  'docs/sprint-3/drafts/Sprint 3 - Physical DFDs (full set).pdf; Appendix B against the logical Level 1 diagrams; slides '
  '9 to 13 of docs/sprint-3/Sprint 3 - Presentation.pptx, whose prototype screenshots still show the old rules. The '
  'presenter should rewrite the changed speaker notes in their own words.',
  'Kyle Robertson (CONFIRM)'],
]
CHANGE_ROWS = [
 [3, 'DFD and ERD Models; DFD and ERD Slides; Sprint 3 Presentation',
  'All diagram images replaced with the owner-clarification renders. Models: Table 3.1 (2.0 passcode and optional technician, '
  '3.0 claims and D2, 4.0 part requests, 5.0 sent on a click by staff or the Technician, 6.0 no diagnostic fee, 7.0 low-stock '
  'alert and Manager approval), section 5 (Input Form and Screen, ThinkPads, the owner\'s changes), section 6 note, Tables 7.1 '
  'and 7.2 (3.0 reads and updates D2), Appendix A (optional technician keys, device type and brand; new device_passcode; '
  'approved_by_id a Manager; reorder_point set by the Manager), Appendix B (171 flows). Slides deck: speaker notes for 1.0 to '
  '7.0, the bench and release parts, ERD details 1 and 2, and the physical naming. Presentation: ThinkPad hardware line, '
  '171 flows, ERD and prototype notes, prototype bullets, limitations, risks, decisions needed and next steps.',
  'Owner\'s October 23 clarifications; Kyle Robertson, Oct 23: carry them and the Screen/Input Form names into every Sprint 3 '
  'model document.',
  'The prototype screenshots (presentation slides 9 to 11 and Quick Phone Sprint 3 Prototypes.pptx) still show Owner approval, '
  'automatic assignment and no claim queue, and need regenerating. The catalog, use cases, Owner Design Review Packet and the '
  'hardware/software specification still state the September 21 rules.'],
]

if __name__ == '__main__':
    append(os.path.join(LOGS, 'AI Decision Log.xlsx'), AI_ROWS)
    append(os.path.join(LOGS, 'Change Log.xlsx'), CHANGE_ROWS)
