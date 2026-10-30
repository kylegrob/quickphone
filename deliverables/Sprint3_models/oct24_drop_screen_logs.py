# Oct 24: log rows for dropping "Screen" from the physical DFD flow names.
import os
from oct23_screen_logs import append
from oct23_erd_twoway_logs import LOGS

AI_ROWS = [
 ['2026-10-24', 3, 'Physical DFDs (flow names for what the system shows a person)', 'Claude Sonnet 5.5',
  'Applied Kyle\'s naming change: dropped "Screen" from 28 physical flow names and kept only the data name, e.g. Part '
  'Request Confirmation Screen -> Part Request Confirmation. Lists end in "List" (Pending Quotes List, Ready Jobs List, '
  'Pickup Jobs List, Job Status List, Low Stock Alert List, Pending Purchase Orders List, Purchase Order Status List, '
  'Released Jobs List); Status Dashboard Screen -> Status List; Appointment Schedule Screen -> Appointment Schedule (the '
  'Level 0 group of Available Times, Booking Confirmation and Change Confirmation). Names Kyle did not list were '
  'shortened the same way. Re-rendered the physical DFDs and rebuilt the PDF and its reading guide.',
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: SAD 8e Ch. 9 Figs. 9-2 and 9-4 (flow names); the full old-to-new list in '
  'deliverables/Sprint3_models/oct24_drop_screen.py; whether "Appointment Schedule" is the right name for the group, and '
  'whether "Status List" is distinct enough from "Job Status List".',
  'Kyle Robertson (CONFIRM)'],
]
CHANGE_ROWS = [
 [3, 'Physical DFDs (full set) PDF',
  'The 28 flows the system shows a person no longer end in "Screen"; they carry the data name, with "List" for lists '
  '(e.g. Ready Jobs List, Low Stock Alert List, Repair Job Details, Shop Record Confirmation). The reading guide and '
  'balancing table use the new names.',
  'Kyle Robertson, Oct 24: "Screen" names the medium, not the data.',
  'The DFD and ERD Models document, the DFD and ERD Slides deck and the Sprint 3 Presentation still carry the older '
  'physical names and need the same renames; Sprint 4 interface designs can take screen titles from these names.'],
]
if __name__ == '__main__':
    append(os.path.join(LOGS, 'AI Decision Log.xlsx'), AI_ROWS)
    append(os.path.join(LOGS, 'Change Log.xlsx'), CHANGE_ROWS)
