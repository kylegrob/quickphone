# Oct 23: AI Decision Log and Change Log rows for applying the owner's eight clarifications to the physical DFDs and ERD.
import os

from oct23_erd_twoway_logs import LOGS

AI_ROWS = [
 ['2026-10-23', 3, 'Physical DFDs and physical ERD (owner clarifications of October 23)', 'Claude Opus 5.5',
  'Turned the owner\'s eight answers into model changes. DFDs: Technician may send the pickup notification (Send Notification '
  'Input Form into 5.4, on the context, complete Level 0 and Level 0 part 3); 7.3 PO approval moved from the Owner to the '
  'Manager; 7.1 renamed List Parts to Order with a Low-Stock Alert Output Form and open part requests; 4.4 renamed Record Part '
  'Request with a Part Request Input Form; 3.1 renamed Select Repair Job with a Job Claim Input Form and D2 reads and updates '
  '(technicians claim unassigned jobs and appointments); optional Passcode Input Form into 2.4; 6.3 passes an unrepaired job '
  'on as a Settled Job with no payment; ThinkPads in the process bands. Re-laid out the context, Level 0 parts 2 to 4 and the '
  'complete Level 0 (5.0 moved last in its column). ERD: assigned_tech_id and appointment.technician_id made optional '
  '(zero-or-one on EMPLOYEE), device_type and brand optional, new repair_job.device_passcode (encrypted). Added a page to the '
  'DFD PDF mapping each answer to the diagrams. Proposed, not from the owner: Managers use the assignment screens as Front '
  'Desk does; passcodes visible to the assigned technician, Manager and Owner; part requests stay job_part rows (Needed).',
  'PENDING: accountable member to decide',
  'PENDING. Evidence to cite: the owner\'s October 23 clarifications (items 1 to 8); the September 21 confirmations #4 and #6, '
  'which items 2 and 1 reverse; SAD 8e Ch. 4 balancing and Ch. 9 Steps 1 and 2; SAD 8e Ch. 10 on optional foreign keys; '
  'page 2 and the balancing table of docs/sprint-3/drafts/Sprint 3 - Physical DFDs (full set).pdf; the notes page of '
  'docs/sprint-3/drafts/Sprint 3 - Physical ERD (full).pdf. Decide whether to draw Technician sending before the owner '
  'confirms it overrides #6, whether part requests need their own table if they are not tied to a job, and who may see a '
  'passcode.',
  'Kyle Robertson (CONFIRM)'],
]
CHANGE_ROWS = [
 [3, 'Physical DFDs (full set) PDF; Physical ERD (full) PDF',
  'Owner clarifications applied. DFDs: 5.0 also takes a Send Notification Input Form from the Repair Technician; 7.3 approval '
  'flows run to the Store Manager, and the Owner keeps only 8.0; 7.1 List Parts to Order sends a Low-Stock Alert Output Form '
  'with open part requests; 4.4 Record Part Request takes a Part Request Input Form; 3.1 Select Repair Job lets a technician '
  'claim unassigned jobs and appointments (3.0 now reads and updates D2); 2.4 takes an optional Passcode Input Form; 6.3 settles '
  'an unrepaired job with no payment; bands name the ThinkPads. Fixed: the 4.0 Stock Shortage line ended on 4.3, not 4.4, and '
  'the balancing table still said "DB Record". ERD: assigned_tech_id and appointment.technician_id optional, device_type and '
  'brand optional, new repair_job.device_passcode (encrypted); the full sheet was re-spaced.',
  'Owner\'s October 23 clarifications: staff or the Technician click to send the pickup email (never automatic), a Manager '
  'approves every purchase order, automatic low-stock alerts, technician part requests, manual or self assignment, no diagnostic '
  'fee for unrepairable devices, Manager-set reorder points, optional passcode at intake, ThinkPad computers.',
  'Not yet carried through: the logical DFD and ERD images and Appendices A and B in the DFD and ERD Models document, the '
  'DFD and ERD Slides deck, the Sprint 3 Presentation, the catalog (FR04, FR10, FR12, NFR05 and the open questions), the use '
  'cases (UC-01, UC-02, UC-05, UC-06, UC-09), the prototypes, the hardware/software specification and project-context.md. '
  'NFR05 and client confirmation #6 must be resolved with the owner first.'],
]

if __name__ == '__main__':
    import oct23_erd_twoway_logs as base
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
