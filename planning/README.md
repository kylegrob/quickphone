# Planning documents

This is the current analysis and design set for the working system in [`../app`](../app). Reconciled November 20, 2026 against local `preview` commit `195c99c` plus the working-tree account-management change in `app/shop/views/records.py`. Earlier sprint versions in `docs/` and `deliverables/` are historical sources, not the current planning baseline. Client confirmations and provisional team decisions remain distinguished.

| Document | File |
|---|---|
| System request | [system-request.docx](system-request.docx) |
| Requirements catalog (15 functional, 6 non-functional) | [requirements-catalog.docx](requirements-catalog.docx) |
| Use cases (UC-01 to UC-13) | [use-cases.docx](use-cases.docx) · [diagram](use-case-diagram.png) |
| Data flow diagrams | [Complete logical set (PDF)](diagrams/dfd/logical-dfd-set.pdf) · [complete physical set (PDF)](diagrams/dfd/physical-dfd-set.pdf) |
| Entity relationship diagrams | [Complete logical ERD (PDF)](diagrams/erd/logical-erd.pdf) · [complete physical ERD (PDF)](diagrams/erd/physical-erd.pdf) |
| DFD to ERD alignment | [dfd-erd-alignment.png](diagrams/dfd-erd-alignment.png) |
| Specification document | [specification.docx](specification.docx) |
| Business rules and implementation decisions | [business-rules.md](business-rules.md) |

## Data flow diagrams

The complete PDFs contain the context diagram, Level 0 and Level 1 diagrams. Level 0 is also shown in four parts for readability; process 9.0 has existing maintenance pages plus a security detail page for event recording and Owner audit review. Security logging is a shared service: the detail page expands the interactions and D7 writes represented by 9.0.

[Logical DFD set (PDF)](diagrams/dfd/logical-dfd-set.pdf) · [Physical DFD set (PDF)](diagrams/dfd/physical-dfd-set.pdf)

## Entity relationship diagrams

The complete logical and physical ERDs are provided as PDFs, including overview, complete model and four detail pages. The model contains 21 business entities in seven DFD stores: AuditEvent belongs to D7; payment void fields belong to D3.

[Logical ERD (PDF)](diagrams/erd/logical-erd.pdf) · [Physical ERD (PDF)](diagrams/erd/physical-erd.pdf)

Rebuild diagrams with the bundled Node runtime: `node planning/sources/render.cjs` (Playwright/Edge and pdf-lib). Editable sources are retained in `planning/sources/` (copied from the revised Sprint 4 model sources). Generated Word text: `python tools/extract_text.py planning docs/_text/planning`.

Current validation (November 20): **182/182 automated tests passed** on isolated SQLite. See [raw results](verification/current-regression.txt) and [run metadata](verification/current-regression.json). Owner-only repair-type maintenance, role overrides and payment/release gates match the working app.
