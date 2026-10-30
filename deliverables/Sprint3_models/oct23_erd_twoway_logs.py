# Oct 23: AI Decision Log and Change Log rows for the ERD pass against the lecture's physical ERD (SAD 8e Fig. 10-8).
import os

LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'logs')

AI_ROWS = [
 ['2026-10-23', 3, 'Physical and logical ERD (relationship names in both directions)', 'Claude Opus 5.5',
  'Compared the physical ERD with the lecture example (SAD 8e Fig. 10-8) and proposed a reverse name for every relationship '
  '(29 pairs, e.g. employs / is employed by, undergoes / is performed on, tracks / belongs to, sends notification for / '
  'has notification sent by), made the overview and the full sheet use the same pair for each line (part-job_part is now '
  '"is included in / includes", purchase_order-job_part "supplies / is supplied by", employee-repair_job "works on / is '
  'assigned to"), and re-laid out the overview, detail 3 and the full sheet (now 3040 px wide) so both names fit.',
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: SAD 8e Fig. 10-8 on p. 348 and the lecture slide of it ("Places / Is Placed By"); SAD 8e '
  'Ch. 5 Step 3 on naming relationships; the crow\'s-foot ends against the NN flags in Appendix A of the models document; '
  'the renders in deliverables/Sprint3_models/slides/physical and slides/logical. Check that each reverse name reads '
  'correctly from the "many" side, especially "is stock of", "belongs to" and "has notification sent by".',
  'Kyle Robertson (CONFIRM)'],
 ['2026-10-23', 3, 'Physical data dictionary (defaults and valid values) and ERD notes (Step 5 trace)', 'Claude Opus 5.5',
  'Added Default and Valid values columns to all 16 tables of Appendix A (SAD 8e Fig. 10-9): identity keys, '
  'CURRENT_TIMESTAMP time stamps, TRUE/FALSE flags, starting statuses (Checked In, Booked, Pending, Pending Approval, Paid), '
  'zero quantities, the value lists for every CK column and range rules for amounts and quantities. Proposed two values the '
  'documents do not yet state: inventory_txn.txn_type "Import" for the 9.5 starting-stock batch and purchase_order.po_status '
  'starting at Pending Approval. Rewrote ERD notes Step 5 to name the physical DFD process and flow that writes each '
  'system-added field.',
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: SAD 8e Fig. 10-9 and Step 2 on p. 349 (default value, valid value) and Step 5 on p. 350; '
  'FR06 (eight statuses, client-confirmed #2), FR07 (stock never below zero), FR08 and FR14 (four roles, client-confirmed #1) '
  'in the Sprint 3 catalog; the "Status =", "TxnType =" and "POStatus =" values in Appendix B; the physical Level 1 DFDs '
  '2.0, 5.0, 6.0 and 9.0 in docs/sprint-3/drafts/Sprint 3 - Physical DFDs (full set).pdf. Decide whether "Import" should '
  'be its own transaction type or recorded as an Adjustment.',
  'Kyle Robertson (CONFIRM)'],
]
CHANGE_ROWS = [
 [3, 'Physical and logical ERD; DFD and ERD Models (section 6, Appendix A); DFD and ERD Slides; Sprint 3 Presentation; Physical ERD (full) PDF',
  'Every ERD relationship line is now named in both directions (first name from the "one" side, second read back), and the '
  'overview and full sheet use the same pair for each line. The overview, detail 3 and the full sheet were re-spaced so both '
  'names fit; store labels on the overview no longer sit under lines. The full sheet is 3040 x 1860. The footnotes and the '
  'EMPLOYEE line say "pickup notification" instead of "completion email/notice". Appendix A gains Default and Valid values '
  'columns. The ERD notes page cites Fig. 10-8 for the names and ties each system-added field to its physical DFD flow. '
  'Models section 6, presentation slide 3 and the ERD speaker notes describe the two-way names.',
  'Kyle Robertson: the lecture\'s physical ERD example (SAD 8e Fig. 10-8) names each relationship both ways and Fig. 10-9 '
  'adds default and valid values; the Oct 23 rename of 5.0 to Send Pickup Notification had not reached the ERD.',
  'The Sprint 4 database specification can take its CHECK, DEFAULT and range constraints straight from Appendix A. The '
  'proposed "Import" transaction type and the Pending Approval starting status need the team\'s decision; if Import is '
  'dropped, Appendix A and the 9.5 flow description change.'],
]

if __name__ == '__main__':
    import copy, openpyxl

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
