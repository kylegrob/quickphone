# Oct 23: AI Decision Log and Change Log rows for the technology choice and the physical DFD relabel.
import copy, os
import openpyxl

LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'logs')

AI_ROWS = [
 ['2026-10-23', 3, 'Acquisition alternative matrix and hardware/software specification', 'Claude Opus 5.5',
  'Drafted a weighted alternative matrix (SAD 8e Fig. 6-6) comparing a custom Django and PostgreSQL web app, a repair-shop '
  'subscription and a shared spreadsheet: proposed the seven criteria, their weights and every 1-5 score (custom 415, '
  'subscription 350, spreadsheet 285), a sensitivity table showing the subscription wins if nobody will support the system '
  'after December 9, and a hardware and software specification in the form of Fig. 7-10. Looked up published list prices '
  'for RepairDesk and RepairShopr (about $140-$150 per store per month on October 23), which are above the Feasibility 3.10 band.',
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: SAD 8e Ch. 6 (Figs. 6-3, 6-5, 6-6) and Ch. 7 (Figs. 7-2, 7-9, 7-10, 7-11); client '
  'confirmations #3-#7 behind the fit weight; Feasibility v2.2 sections 3.2, 3.3, 3.9 and 4.5 for the cost and support '
  'scores; the RepairDesk and RepairShopr pricing pages (check current prices before citing); team members\' Python '
  'experience (each member to confirm). Review whether the weights reflect the client\'s priorities, not the team\'s.',
  'Kyle Robertson (CONFIRM)'],
 ['2026-10-23', 3, 'Physical DFDs (implementation references and human-machine boundary)', 'Claude Opus 5.5',
  'Relabelled every physical DFD for the chosen technology: stores "PostgreSQL: ...", store flows "PostgreSQL Record: ..." '
  'and "PostgreSQL Record Update: ...", Django in each process band. Replaced the single line around the automated part '
  'with a dashed boundary around each person who uses the system\'s screens (Front Desk with the manual steps 6.5 and 6.6, '
  'Technician, Manager, Owner) and none around the Customer, and updated the models document, both decks and the physical DFD PDF to match.',
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: SAD 8e Ch. 9 Step 1 and Step 2 (p. 302): "a line drawn on the model to separate human action '
  'from automated processes"; Fig. 9-2 (lines around the Shop Manager and the Customer, none around the Customer Service '
  'Department, which only receives an email) and Fig. 9-4 (MySQL and Python references); the lecture slides of both figures; '
  'docs/sprint-3/drafts/Sprint 3 - Physical DFDs (full set).pdf.',
  'Kyle Robertson (CONFIRM)'],
]
CHANGE_ROWS = [
 [3, 'Physical DFDs; DFD and ERD Models; DFD and ERD Slides; Sprint 3 Presentation; Physical ERD notes',
  'Physical DFDs now name the implementation: data stores "PostgreSQL: <store>", store flows "PostgreSQL Record: ..." / '
  '"PostgreSQL Record Update: ...", Django in every process band. The human-machine boundary is drawn as in SAD 8e Figs. 9-2 '
  'and 9-4, around each person who uses the system\'s screens; the Customer, who only receives a printout and an email, has '
  'none, and the manual steps 6.5 and 6.6 sit inside the Front Desk\'s line. Models section 5, the slide notes, the PDF '
  'reading guide and the ERD notes now cite the provisional Django and PostgreSQL choice instead of the unconfirmed Sprint 1 '
  'assumption; the presentation\'s limitation, uncertainty and next-step text says the choice is provisional.',
  'Kyle Robertson: the lecture\'s physical DFD examples name the technology (HTML/PHP, MySQL) and leave entities that only '
  'receive email outside any boundary; the new Sprint 3 alternative matrix chose the route (review finding A1).',
  'The Sprint 4 specification builds on Django 5.2 and PostgreSQL; the matrix is re-scored after the owner answers who '
  'supports the system after December 9, and a different route would mean relabelling the physical DFDs again. Feasibility '
  '3.10\'s subscription price band should be updated to the October 23 list prices.'],
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


append(os.path.join(LOGS, 'AI Decision Log.xlsx'), AI_ROWS)
append(os.path.join(LOGS, 'Change Log.xlsx'), CHANGE_ROWS)
