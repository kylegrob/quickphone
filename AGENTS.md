# Instructions for AI assistants

This repository holds the course deliverables for the Quick Phone Repair Management System (MIS 4173, Fall 2026). There is no application code yet; the work is systems analysis and design documents. Read [README.md](README.md) for the layout and sprint calendar.

## Read first, in this order

1. [docs/project-context.md](docs/project-context.md): scope, client-confirmed requirements, decisions, open questions and conventions.
2. [docs/course/](docs/course/): the course rules. [project-spec.md](docs/course/project-spec.md) defines each deliverable, [ai-guidelines.md](docs/course/ai-guidelines.md) governs AI use, and `sprint-N-presentation.md` lists what each sprint must show.
3. [feedback/](feedback/): professor feedback for every sprint so far. Do not repeat a mistake already called out there.
4. [docs/README.md](docs/README.md): which file is current for each deliverable. Several deliverables exist in more than one version.
5. The deliverable you are working on, through its Markdown copy in `docs/_text/` (same path as the original, plus `.md`).
6. [docs/plan-sprints-4-6.md](docs/plan-sprints-4-6.md) and [docs/review-sprints-1-3.md](docs/review-sprints-1-3.md) for remaining work and known defects.

**Method reference.** Every deliverable, through Sprint 6, follows Dennis, Wixom, Roth & Haley, *Systems Analysis and Design*, 8th ed. (Wiley, 2021): Ch. 1 system request and feasibility, Ch. 3 requirements, Ch. 4 use cases and DFDs, Ch. 5 ERD and normalization, Ch. 6 alternative matrix, Ch. 7 architecture and hardware/software specification, Ch. 8 interface design, Ch. 9 program design, Ch. 10 data storage, Ch. 11 testing and documentation, Ch. 12 transition, training and project assessment, Ch. 13 Scrum. Cite chapter and figure when a decision rests on it. The PDF stays outside this repository; ask the user for its path.

## Working with the files

- **Read** the `docs/_text/*.md` copies; they are generated from the Office files and are much faster than parsing .docx/.pptx/.xlsx. Diagrams are images: open the PNG/PDF files directly, or unzip a .docx/.pptx and look in `word/media/` or `ppt/media/`.
- **Never edit `docs/_text/` by hand.** Change the original, then run `python tools/extract_text.py`.
- **Edit the original Office files**, keeping their names. When you produce a new version of a submitted deliverable, put it in `docs/sprint-N/drafts/` until the team submits it.

## Keeping the logs (in the same change, not afterwards)

Both logs live in `docs/logs/` and are submitted every sprint. Add their rows as part of the edit that causes them, then run the extractor.

- **Change Log.xlsx:** whenever a change alters a deliverable that was already submitted, append a complete row: Sprint, Deliverable, What changed, Why (whose feedback or which downstream change), and Effect on later deliverables. These rows are factual, so the assistant writes them in full. Edits to unsubmitted drafts need no row until the draft is submitted.
- **AI Decision Log.xlsx:** for every substantive AI contribution (requirements, use cases, models, prototypes, code, tests, security advice, user documentation), append a row with Date, Sprint, Artifact, Tool (name the model) and What the AI produced. Leave Decision as `PENDING: accountable member to decide`. Write Rationale as `PENDING. Evidence to cite: ...`, pointing to the sources the member should check. Name the accountable member, or mark them `CONFIRM`. **Never fill in the decision or rationale yourself.** The course grades the team's judgement, and any member may be asked to defend any row. Grammar, spelling and formatting fixes need no row.
- The course treats an unlogged substantive AI contribution as an academic integrity matter, and a rationale must cite evidence, not restate the decision ([docs/course/project-spec.md](docs/course/project-spec.md), Appendix A). Tell the user which rows are pending so they can complete them.

## Rules that come from feedback and the client

- Cite requirements by the numbering in the **current** catalog (see docs/README.md), and tag client-confirmed items as such.
- DFDs follow Dennis, Wixom & Roth, *Systems Analysis and Design* 8e, Ch. 4: Gane and Sarson symbols; process names are verb + noun with no "and"; no two-headed arrows; 3–7 processes per diagram (Fig. 4-24; the Ch. 4 text allows up to nine, which is why Level 0 keeps nine); every data store has an input and an output; external entities also appear on Level 1; include "maintain" processes; context diagram required.
- No entity or data store may be drawn twice on one diagram. Every ERD entity belongs to exactly one DFD data store, and the DFDs and ERD must stay aligned.
- Diagrams must be readable on a 16:9 PowerPoint slide (labels at least 19 px at 1920 px wide). Split large diagrams into an overview plus detail slides.
- Mark every dollar or hour figure as an estimate and keep stated assumptions visible. Do not invent cost lines; label a placeholder as a placeholder and say where the number came from.
- Keep requirements-stage documents (system request, requirements) technology-neutral: state the business need, not vendors, hosting, protocols or product names.
- The team prefers short, dense prose: flowing paragraphs of roughly 150–200 words per section, not long bulleted lists.

## Confidentiality

The MOU commits the team to keep client information confidential. Do not paste client details into public tools or public repositories, and never add credentials, API keys or real customer data to this repository.
