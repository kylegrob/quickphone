# Oct 23: AI Decision Log and Change Log rows for renaming the physical DFD flows ("Output Form" -> "Screen").
import copy, os

import openpyxl

from oct23_erd_twoway_logs import LOGS
N_RENAMED = 35  # entries in oct23_screen_names.RENAME (importing it would re-run the renames)

AI_ROWS = [
 ['2026-10-23', 3, 'Physical DFDs (flow names for screens and forms)', 'Claude Opus 5.5',
  'Proposed and applied a naming rule after Kyle found "Low-Stock Alert Output Form" and "Part Request Output Form" '
  'confusing: a form a person fills in is "... Input Form", and anything the system shows a person is "... Screen". '
  'Renamed %d physical flows, e.g. Part Request Output Form -> Part Request Confirmation Screen, Low-Stock Alert Output '
  'Form -> Low-Stock Alert Screen, Pickup Notification Input Form -> Notification Approval Input Form, Release Input Form '
  '-> Release Authorization Input Form, PO Request/PO Approval -> Purchase Order Request/Approval Input Form. Updated '
  'the PDF reading guide and balancing table.' % N_RENAMED,
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: SAD 8e Ch. 9 Step 1 and Figs. 9-2 and 9-4 (physical flows name their medium) and the '
  'lecture slides of both figures, to check that "Screen" is an acceptable medium name next to the textbook\'s forms; '
  'the reading guide on page 1 and every diagram in docs/sprint-3/drafts/Sprint 3 - Physical DFDs (full set).pdf; the '
  'full old-to-new list in deliverables/Sprint3_models/oct23_screen_names.py.',
  'Kyle Robertson (CONFIRM)'],
]
CHANGE_ROWS = [
 [3, 'Physical DFDs (full set) PDF',
  'Every flow the system shows a person is now named "... Screen" instead of "... Output Form" (28 names), and seven '
  'input names now say what the data is: Requested Date, Diagnosis Details, Notification Approval, Release Authorization, '
  'Received Quantities, Purchase Order Request and Purchase Order Approval Input Form. The reading guide and balancing '
  'table use the new names.',
  'Kyle Robertson, Oct 23: "Output Form" made an alert and a confirmation read like forms, and "Part Request Output Form" '
  'named the request rather than its confirmation.',
  'The DFD and ERD Models document (section 5, Appendix B), the DFD and ERD Slides deck and the Sprint 3 Presentation still '
  'use the old physical names and need the same renames; the Sprint 4 interface designs can take their screen names from '
  'these flows.'],
]


def append(path, rows):
    wb = openpyxl.load_workbook(path); ws = wb.worksheets[0]
    last = ws.max_row
    while last > 1 and all(c.value in (None, '') for c in ws[last]):
        last -= 1
    for r in rows:
        last += 1
        for j, v in enumerate(r, start=1):
            c = ws.cell(row=last, column=j, value=v); src = ws.cell(row=last - 1, column=j)
            if src.has_style:
                c._style = copy.copy(src._style)
        if ws.row_dimensions[last - 1].height:
            ws.row_dimensions[last].height = ws.row_dimensions[last - 1].height
    tmp = path + '.tmp.xlsx'; wb.save(tmp); os.replace(tmp, path)
    print(os.path.basename(path), 'rows now', last)


if __name__ == '__main__':
    append(os.path.join(LOGS, 'AI Decision Log.xlsx'), AI_ROWS)
    append(os.path.join(LOGS, 'Change Log.xlsx'), CHANGE_ROWS)
