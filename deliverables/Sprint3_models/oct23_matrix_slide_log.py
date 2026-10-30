# Oct 23: AI Decision Log row for the presentation's alternative matrix slide.
import copy, os
import openpyxl

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'logs', 'AI Decision Log.xlsx')
ROW = ['2026-10-23', 3, 'Sprint 3 presentation: alternative matrix slide', 'Claude Opus 5.5',
       'Added slide 4, "Acquisition and technical approach": the weighted alternative matrix as a table (custom 415, '
       'subscription 350, spreadsheet 285, with each 1-5 score), the hardware and software summary, and the condition that '
       'reverses the result (nobody to support the system after December 9). Wrote its speaker script.',
       'PENDING: accountable member to decide',
       'PENDING. Evidence to cite: docs/sprint-3/drafts/Sprint 3 - Alternative Matrix and Hardware-Software Specification.docx '
       '(the source of every number on the slide); docs/course/sprint-3-presentation.md ("defend the acquisition and technical '
       'approach"); SAD 8e Fig. 6-6. The presenter should rewrite the script in their own words and be ready to defend each weight.',
       'Kyle Robertson (CONFIRM)']

wb = openpyxl.load_workbook(PATH); ws = wb.worksheets[0]
last = ws.max_row
while last > 1 and all(c.value in (None, '') for c in ws[last]):
    last -= 1
assert ws.cell(row=last, column=3).value != ROW[2], 'row already added'
for j, v in enumerate(ROW, start=1):
    c = ws.cell(row=last + 1, column=j, value=v); src = ws.cell(row=last, column=j)
    if src.has_style:
        c._style = copy.copy(src._style)
tmp = PATH + '.tmp.xlsx'; wb.save(tmp); os.replace(tmp, PATH)
print('row', last + 1)
