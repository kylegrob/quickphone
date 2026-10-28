# Quick Phone Repair Management System

MIS 4173 (Systems Analysis, Design and Development), Fall 2026, Professor John Drake. A student consulting project for **Quick Phone Repair & Designs** (Raleigh, NC; two stores), owned by Ashiqullah Pardisi. The system tracks every repair from check-in to pickup and manages parts inventory and purchase orders across both stores.

**Team:** Kyle Robertson, Ehsanullah Pardisi, Bara Abusamhan, Leonard Mann.

> Client information in this repository is confidential under the Student Consulting MOU. Keep the repository private and share it only with the team and course staff.

## Repository layout

```
README.md               You are here
AGENTS.md               Instructions for AI assistants (Claude, ChatGPT, Copilot ...)
CLAUDE.md               Points Claude Code at AGENTS.md
docs/
  README.md             Index of every document, with its sprint and status
  project-context.md    One-page brief: scope, decisions, confirmed requirements, open items
  admin/                Team contract and Student Consulting MOU
  course/               Course rules: project spec, AI guidelines, sprint presentation briefs
  sprint-1/, sprint-2/… Deliverables as submitted, one folder per sprint
  sprint-3/drafts/      Revised work not yet final (replaces older versions when submitted)
  logs/                 AI Decision Log, Change Log, Time Log
  _text/                Auto-generated Markdown copies of every .docx/.pptx/.xlsx
feedback/               Professor and client feedback, one file per sprint
tools/extract_text.py   Regenerates docs/_text/
```

## Sprint calendar

| Sprint | Dates | Focus | Accountable |
|---|---|---|---|
| 1 | Sep 14–20 | Systems request, feasibility | Kyle |
| 2 | Oct 5–11 | Requirements, use cases, logical DFDs and ERD | Bara |
| 3 | Oct 19–25 | Analysis refinement, physical models, interface design | Ehsanullah |
| 4 | Nov 2–8 | Technical specification, working system | Kyle |
| 5 | Nov 16–22 | Deployment, training session, user manual | Bara |
| 6 | Nov 30–Dec 9 | Final presentation and handoff | Kyle |

## How we work in this repo

1. **Adding or updating a deliverable.** Put the file in the right `docs/sprint-N/` folder using the same name as on OneDrive/Teams (`Sprint N - Title.docx`). Revise rather than duplicate: when a draft is submitted, move it out of `drafts/` and over the old file (git keeps the history). Then run `python tools/extract_text.py` so `docs/_text/` stays in step, and update the status in [docs/README.md](docs/README.md).
2. **Recording feedback.** When grades or comments come back, paste them verbatim into `feedback/sprint-N.md` using the [template](feedback/_template.md), then list the action items. See [feedback/README.md](feedback/README.md).
3. **Recording decisions.** Anything the client confirms, or the team decides, goes into [docs/project-context.md](docs/project-context.md) (and the Change Log when it alters a submitted deliverable). AI use goes in the AI Decision Log, as the team contract requires.
4. **Commit messages** say what changed and why, e.g. `Sprint 3: catalog FR10 adds PO threshold (client email Oct 24)`.

Python 3.9+ is the only requirement for the extractor; it uses the standard library.
