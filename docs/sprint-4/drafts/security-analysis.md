# Security analysis: Sprint 4 working system (working draft)

Draft input for the security section of the Sprint 4 specification document and the Sprint 5 operations plan. Reviewed: `app/` on branch `preview`, 2026-11-06 (Django 5.2.18, cryptography 46.0.3). Produced with Claude Opus 5.5; logged in the AI Decision Log as PENDING. An AI review is not proof the application is secure ([ai-guidelines.md](../../course/ai-guidelines.md), Security and data safeguards). Method: SAD 8e Ch. 7 (security requirements in the nonfunctional requirements) and Ch. 11 (test planning).

## 1. Assets and sensitive information

| # | Asset | Why it matters | Where it lives |
|---|---|---|---|
| A1 | **Device passcodes** | Unlock the customer's phone: the most sensitive item held. Owner requires secure storage, authorized staff only (client-confirmed, Oct 23 #7) | `RepairJob.device_passcode`, Fernet-encrypted (`shop/crypto.py`) |
| A2 | Customer personal data | Name, phone, email, device, serial/IMEI. Confidential under the MOU | `Customer`, `Device` tables; pickup emails in `app/sent_emails/` |
| A3 | Custody of the physical device | Release to the wrong person is the client's stated fear (project-context problem statement) | Release rule in `services.release_device` |
| A4 | Money owed and paid | Unpaid release loses revenue; the system records payments but takes none and stores no card data | `Payment`, `RepairJob.final_cost` |
| A5 | Inventory and purchase orders | Stock counts, part costs, Owner labor prices, PO approval (client-confirmed: Manager approves POs) | `Part`, `StorePartStock`, `PurchaseOrder`, `InventoryTxn` |
| A6 | Staff accounts and the access matrix | Whoever controls these controls every other asset | `Employee`, `ScreenAccess` |
| A7 | Audit trail | Evidence for NFR02 (who did what, when) and for disputes | `JobStatusHistory`, `InventoryTxn`, PO created/approved by |
| A8 | Secrets | `QP_SECRET_KEY` (sessions, CSRF), `QP_PASSCODE_KEY`, database and SMTP passwords | Environment variables (`quickphone/settings.py`) |
| A9 | The store's email account | Sends pickup notices; misuse damages the shop's reputation | SMTP settings |
| A10 | Database availability and backups | Both stores stop if it is lost (NFR06) | PostgreSQL host, not yet deployed |

## 2. Threats

Scaled to a two-store shop: the realistic attacker is an insider, a customer at the counter, someone on the shop Wi-Fi, or a careless deployment, not a nation-state.

| # | Threat (STRIDE) | Assets | Likelihood |
|---|---|---|---|
| T1 | A counter computer is left signed in; a customer or another employee acts under that login (Spoofing) | A1–A6 | High |
| T2 | Password guessing against staff logins; weak or shared passwords (Spoofing) | A6, all | Medium |
| T3 | Traffic on shop Wi-Fi sniffed for session cookies or passwords if served over plain HTTP (Information disclosure) | A6, A2 | Medium once deployed |
| T4 | Deployment with missing settings: debug pages on, the known fallback secret key, a passcode key derived from it (Information disclosure, Tampering) | A1, A8 | Medium |
| T5 | Insider oversteps role: technician reads passcodes or contact details, Manager approves own PO, inflates stock adjustments, resets a colleague's password (Elevation, Repudiation) | A1, A2, A5, A6 | Medium |
| T6 | Device released to the wrong person or before payment (Spoofing, Tampering) | A3, A4 | Medium |
| T7 | Staff in one store reach the other store's jobs or customers by changing an ID in the URL (Information disclosure) | A2, A1 | Low–Medium |
| T8 | Stolen laptop or database dump exposes customer data and passcodes (Information disclosure) | A1, A2 | Low |
| T9 | Web attacks: CSRF, XSS, SQL injection, open redirect (Tampering) | All | Low (framework defaults) |
| T10 | Training seed run against live data, or loss of the passcode key (Denial of service) | A10, A1 | Low, high impact |
| T11 | Nobody patches Django after the Dec 9 handoff (top organizational risk in the feasibility study) | All | High over time |

## 3. Selected controls and test evidence

The suite was run on 2026-11-06: **79 tests, all pass** (`QP_DB_ENGINE=sqlite`). `manage.py check --deploy` with `QP_DEBUG=0` reports HSTS, SSL redirect and secure-cookie warnings (finding F2). No raw SQL, `.extra()` or `csrf_exempt` appears in `app/shop`, and no template uses `|safe`.

| Control | Threats | Implementation | Test evidence |
|---|---|---|---|
| Server-side role checks on every screen; hidden buttons are not the control | T5 | `screen_required`, `role_required` in `shop/permissions.py` | `test_nfr01_technician_cannot_approve_po`, `test_nfr01_front_desk_cannot_open_inventory`, `test_technician_checks_in_but_cannot_open_the_job_list`, `test_every_screen_renders_for_its_role` |
| Owner-managed access matrix that cannot override business rules or lock out the Owner | T5 | `ScreenAccess`, `access` view | `test_screen_access_does_not_override_business_rules`, `test_only_the_owner_reaches_the_access_screen`, `test_owner_cannot_lock_themself_out_of_access` |
| Store isolation: non-Owners fixed to their home store; jobs and POs filtered by store | T7 | `ActiveStoreMiddleware`, `store_jobs`, `po_detail` store filter | `test_manager_fixed_to_home_store`, `test_fr04_technician_sees_only_own_queue`. No test opens another store's job by ID (gap G1) |
| Passcode encrypted at rest; shown only to assigned technician, Manager, Owner | T5, T8 | Fernet in `crypto.py`, `can_see_passcode` | `test_passcode_is_encrypted_and_hidden_from_front_desk` |
| Only the Owner grants the Owner role; nobody changes their own role or deactivates themself | T5 | `can_assign_role`, `staff_edit` | `test_fr14_manager_cannot_assign_owner_role`, `test_fr14_owner_creates_user_in_each_role`. Self-change block untested (G1) |
| Release needs payment in full and a photo-ID check; no override | T6 | `release_device` | `test_fr08_unpaid_release_blocked_then_paid_release_succeeds`, `test_unrepaired_device_released_without_fee` |
| PO approval before receipt; rejection needs a reason | T5 | `approve_po`, `reject_po`, `receive_po` | `test_fr10_order_cannot_be_received_until_approved`, `test_fr10_reject_returns_to_draft_with_reason` |
| Stock cannot go negative; adjustments need a reason; row locks | T5 | `adjust_stock`, `complete_repair` with `select_for_update` | `test_fr07_stock_cannot_go_below_zero`, `test_fr09_adjustment_needs_reason` |
| CSV import all-or-nothing with row-level errors | T5 | `import_csv` | `test_fr11_import_rejects_file_with_bad_row`, `test_fr11_import_valid_file` |
| Audit trail of job changes, sender of each email | T5, T6 | `JobStatusHistory`, `email_sent_by` | `test_nfr02_every_change_records_who_and_when`, `test_fr12_email_from_store_account_logs_sender` |
| Deactivated staff cannot sign in | T5 | `Employee.is_active` follows `active_flag` | `test_inactive_account_cannot_sign_in` |
| Framework defences: CSRF tokens, auto-escaping, ORM parameters, `X-Frame-Options: DENY`, HttpOnly cookies, safe `next` redirect | T9 | Django middleware, `settings.py`, `switch_store` | Code review only; the redirect guard has no test (G1) |
| Secrets from environment; database, emails and venv git-ignored; no card data stored | T4, T8 | `settings.py`, `.gitignore` | `git check-ignore` confirms `app/dev.sqlite3` and `app/sent_emails/` |

## 4. Findings to fix (prioritized)

| # | Finding | Fix | Effort |
|---|---|---|---|
| F1 | **Settings fail open.** `QP_DEBUG` defaults to on, `SECRET_KEY` falls back to a string published in the repo, and the passcode key is derived from it when `QP_PASSCODE_KEY` is unset. A deployment that forgets one variable exposes debug pages, allows forged sessions, and makes every passcode decryptable by anyone with the repo and a database copy | Default debug off; when debug is off, refuse to start without `QP_SECRET_KEY` and `QP_PASSCODE_KEY` | Small |
| F2 | **No HTTPS settings** (`check --deploy`: W004, W008, W012, W016) | Set `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`, HSTS when debug is off; proxy header if behind one | Small |
| F3 | **Sessions last two weeks** (Django default) on shared counter computers (T1) | Idle timeout around 30 minutes (`SESSION_COOKIE_AGE`, `SESSION_SAVE_EVERY_REQUEST`), expire at browser close | Small |
| F4 | **No login throttling; only a length-8 password rule** (T2) | Add Django's common-password, numeric and similarity validators; lock an account for a few minutes after repeated failures, with no new dependency | Medium |
| F5 | **Staff screen allows escalation.** `can_assign_role` blocks only the Owner role, so a Manager can create more Managers and reset any non-Owner password in the store, then sign in as that person. If the Owner opens Staff to Front Desk or Technician in the matrix, those roles can create a Manager and approve POs | Only the Owner creates Managers or resets a Manager's password; Managers manage Front Desk and Technician accounts only. Needs an owner decision | Small |
| F6 | **Passcodes are kept forever** after the device goes home (A1) | Clear the passcode when a job is released; minimum retention for the most sensitive field | Small |
| F7 | **Payment and release follow the matrix only.** `record_payment` and `release_device` check no role, so opening the Repair jobs screen to Technicians lets them release devices. The README says the matrix "does not change the rules inside a screen", but this rule is not one of those protected | Decide with the owner whether release is a business rule; if so, enforce Front Desk/Manager/Owner in the service | Small |
| F8 | **Audit gaps** (T5): no record of sign-ins and failed sign-ins, account and password changes, store, supplier and labor-price edits, or who viewed a passcode. Payment rows carry no employee (only the history note does) | A small audit-event table written from those views | Medium |
| F9 | **`seed_training --yes` wipes any database**, including a live one (T10) | Refuse when debug is off unless an extra explicit flag is given | Small |
| F10 | **Customers are not store-scoped and can be walked by ID** (`/checkin/?customer=N`, `desk.py:93`), by every check-in role including Technicians | Likely intended (one customer list for both stores); confirm with the owner, or limit to customers with a job or appointment at the active store | Small |
| F11 | CSV upload has no size limit and is read whole into memory | Reject files over about 1 MB | Small |

**Status, 2026-11-06.** F1, F2, F3, F4, F6, F9 and F11 are fixed, and each fix has a test in `SecurityTests` (`app/shop/tests.py`). The suite now runs **94 tests, all pass**. With real keys and debug off, `check --deploy` reports only HSTS subdomains and preload (W005, W021), which are left off on purpose until the shop's domain is known. Without keys, the app refuses to start. F5, F7 and F10 wait for owner decisions. F8 (audit events) is still open. Choices the accountable member should confirm: the 30-minute idle timeout, lockout after 5 failures for 15 minutes counted per account, a 10-character password minimum, a 30-day HSTS start, and deleting the passcode at release rather than keeping it for warranty returns.

**Gaps in test evidence (G1), now covered.** The fix added a test for each gap below. No test covers: opening another store's job, PO or appointment by ID; a technician opening another technician's job; the self-role-change block; the open-redirect guard; CSRF rejection; session expiry. Add these with the fixes so each control has a passing test. The `app/README.md` count of 38 tests is out of date (79 today).

## 5. Residual risks and accepted tradeoffs

These remain after the fixes above and need the accountable member, and where marked the owner, to accept them in writing.

- **Technicians see customer phone and email.** Kyle's decision of 2026-11-02 reverses client confirmation #6; NFR04 is still to be confirmed with the owner. Until then this is an unratified tradeoff, not an accepted one.
- **A Manager may approve their own PO** (`ALLOW_SELF_APPROVAL_OF_PO = True`, team decision 2026-10-28). Segregation of duties is replaced by history showing both names and the Owner's pending-PO count on the dashboard. Owner to confirm.
- **Passcodes appear in plain text on screen** to the assigned technician, Managers and the Owner; shoulder-surfing at the counter is possible. Accepted because technicians must type it into the device.
- **The photo-ID check is a checkbox.** The system records that staff ticked it; it cannot verify the ID.
- **No multi-factor sign-in.** Proportionate for a two-store shop on shop computers; revisit if remote access is ever allowed.
- **The Owner account and the database administrator can read everything,** and the passcode key sits on the same server as the database. A stolen server copy with its environment exposes passcodes; F6 limits that to open jobs.
- **Training password is in the repository** (`seed_training.py`), deliberately and for invented data only. Acceptable only with F9 and real passwords for real accounts.
- **Backups, restore testing and patching are outside the app** (NFR06, T11). They belong in the Sprint 5 operations plan and depend on the open owner decision about support after December 9.
