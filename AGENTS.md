# Instructions for AI assistants

This repository holds the Quick Phone Repair Management System (MIS 4173, Fall 2026): the working app in `app/` and its current analysis models. Read [README.md](README.md) for the layout and [app/README.md](app/README.md) for the build and its business rules.

**Method reference.** The models follow Dennis, Wixom, Roth & Haley, *Systems Analysis and Design*, 8th ed. (Wiley, 2021): Ch. 3 requirements, Ch. 4 use cases and DFDs, Ch. 5 ERD and normalization, Ch. 9 program design, Ch. 10 data storage, Ch. 11 testing. Cite chapter and figure when a decision rests on it. The PDF is not in this repository; ask the user for its path.

## Working with the files

- Edit the Office files in place, keeping their names. Diagrams are rendered from `models/source/*.html`; change the source and re-render rather than editing an image.
- Cite requirements by the numbering in `requirements/`, and tag client-confirmed items as such.
- The DFDs, the ERD and the app's models must stay aligned. Every ERD entity belongs to exactly one DFD data store (`models/19_DFD_ERD_Alignment`).

## Logs kept outside this repository

The team's AI Decision Log and Change Log are submitted every sprint but are not stored here. For every substantive AI contribution (requirements, use cases, models, code, tests, security advice, user documentation), tell the user which row to add: date, sprint, artifact, tool (name the model) and what the AI produced. Never write the decision or rationale for the team; the course grades their judgement. A change to an already-submitted deliverable also needs a Change Log row.

## Rules from feedback and the client

- DFDs use Gane and Sarson symbols; process names are verb + noun with no "and"; no two-headed arrows; 3–7 processes per diagram (Level 0 keeps nine, as the Ch. 4 text allows); every data store has an input and an output; external entities also appear on Level 1; include "maintain" processes; a context diagram is required. No entity or data store is drawn twice on one diagram.
- Diagrams must be readable on a 16:9 slide (labels at least 19 px at 1920 px wide). Split large diagrams into an overview plus detail slides.
- Mark every dollar or hour figure as an estimate and keep assumptions visible.
- Keep requirements-stage documents technology-neutral.
- No explanatory notes, hints or disclaimers in the app UI: labels, validation errors, empty states and short status messages only.
- The team prefers short, dense prose: paragraphs of roughly 150–200 words, not long bulleted lists.

## Confidentiality

The MOU commits the team to keep client information confidential. Do not paste client details into public tools or public repositories, and never add credentials, API keys or real customer data to this repository.
