# Delivery plan: Sprints 4–6

Drafted 2026-10-22 (Claude Code, Claude Opus 5.5) from the [Sprint 4–6 briefs](course/sprint-4-6-deliverables.md), [project-spec.md](course/project-spec.md), [ai-guidelines.md](course/ai-guidelines.md), the Sprint 2 feedback and the [Sprint 1–3 review](review-sprints-1-3.md). Method reference: Dennis, Wixom, Roth & Haley, *Systems Analysis and Design* 8e (SAD 8e), Part 3 (design, Ch. 6–10), Part 4 (implementation, Ch. 11–12) and Ch. 13 (Scrum). This is a proposal for the team to adopt, change or reject; dates come from the README calendar.

## What the rubric rewards, and what that means for us

Judgment is 40 of 100 points in every remaining sprint, Execution 30, Alignment 20, Revision 10. Judgment is scored on evidence, stated assumptions, alternatives and tradeoffs, and on independent accept/modify/reject decisions about AI output; "Developing" is defined as rationales that restate the decision or treat client statements, assumptions or AI output as sufficient. Our weakest evidence today is the owner: seven confirmations from September 21, no walkthrough of any use case, no baseline figures, no equipment inventory, and no answer on who supports the system after December 9. So the plan front-loads one owner session per sprint, and every major decision (technology, MVP scope, conversion approach, support model) gets a short decision record citing that evidence. The second theme is consistency: the professor's Sprint 2 verdict was that requirements, use cases, DFDs and ERD must "tell the same story", and Sprint 6 adds that earlier documents must not look frozen in time. Each sprint therefore ends with a consistency pass across every current deliverable, not just the new ones, and the Change Log rows are written in the same edit as the change.

## Critical path

The physical design, specification, code and manual all depend on three decisions that are still open: the acquisition route and technology (review finding A1–A2), the interface design the owner selects (A3), and the two blocking business rules (staff-sent vs automatic completion email, FR12; PO threshold or urgent path, FR10). None of these can slip past **November 1** without squeezing the build into five days. The gap week after Sprint 3 (Oct 26–Nov 1) is for closing them, freezing MVP scope and setting up the build environment.

## Bridge: finish Sprint 3 and prepare the build (Oct 22–Nov 1)

Before the Oct 25 submission, close review section A (alternative matrix, hardware/software specification, two more interface alternatives, owner packet sent, presentation) and as much of B as fits; anything deferred goes in the Change Log with its reason. In the gap week, hold the owner walkthrough: rate the three designs, walk through UC-01 to UC-12 step by step (this finally satisfies the "maintain client validation" feedback), answer the blocking and deferred questions, and take the equipment and support inventory. Record each answer in project-context.md and flow it into the catalog, use cases and models. Then fix MVP scope: the Must requirements that a training session needs, which in practice is UC-01 to UC-11 and FR13, with FR01 appointments and FR11 import built only if capacity allows. Write the choice down with its tradeoff. Set up the repository, a recovery branch and seed data with made-up customers only.

## Sprint 4 (Nov 2–8, accountable: Kyle): usable, testable, explainable

**Deliverables:** working system able to run a training session; Specification document with test cases and results; AI Decision Log; Change Log.

**Specification document.** The course wants it detailed enough for an AI coding tool to generate the application, plus test criteria, security and deployment. Build it from the textbook design chapters rather than from scratch: architecture design and the nonfunctional requirements that drive it (SAD 8e Ch. 7, operational, performance, security, cultural/political), the hardware/software specification from Sprint 3, and a security plan centred on role-based access control (the four roles, technicians blocked from customer contact and email, server-side checks, not hidden buttons). Data design follows Ch. 10: the physical ERD and data dictionary we already have, the documented denormalizations from review finding B5, the entity-level CRUD matrix (B7) and a rough storage estimate. Program design follows Ch. 9 in the lightest form that helps an AI tool: the physical DFDs plus one short program specification per feature (inputs, outputs, rules, the use case it implements). Close with the interface standards and the selected design.

**Test plan and results.** Ch. 11 Test Planning gives the structure: unit, integration, system and acceptance tests, each test case with its expected and actual result, and at least valid, invalid and boundary cases for each input rule. Our catalog already has an acceptance check per requirement, which the professor praised for exactly this reason; turn each into one or more numbered test cases and add the failure and security cases the AI guidelines require (a technician trying to send email or approve a PO, an unpaid release, stock below zero, a Manager assigning Owner). Keep a traceability table: requirement → use case → test case → result. Report failures honestly; a failed test with a fix plan scores better under Judgment than a suspiciously clean sheet.

**Build process.** Follow the AI guidelines' coding cycle one feature at a time: plan, implement, test, inspect the diff, run the real scenario, review, decide, commit, then log. Each feature gets a Code Acceptance Checklist entry and an AI Decision Log row. Sequence features in workflow order so a training scenario works end to end early: accounts and roles, check-in, diagnosis and quote, approval, repair with parts deduction, completion email, release after payment, inventory and purchase orders with owner approval, dashboard.

**Revision.** Carry the Sprint 3 feedback into every affected document and the Change Log. Update models wherever the build reveals a design change (it will), so that the ERD and DFDs match the database and screens.

## Sprint 5 (Nov 16–22, accountable: Bara; due Nov 22): ready for real use

**Deliverables:** training and user manual; AI Decision Log; Change Log. The purpose line adds deployment, security and operation beyond the classroom, so the manual should come with a short operations plan.

**Training and user manual.** Ch. 11, Developing Documentation, separates reference documents, procedures manuals and tutorials, and asks for a deliberate structure, task-based topics and navigation terms. Organize the manual by role and task (Front Desk: check in, release; Technician: diagnose, record parts; Manager: stock and orders; Owner: approvals and dashboard), with a one-page quick reference for the counter and bench, which Feasibility 4.4 already promised. The course grades the team's review of an AI-generated draft, so keep the raw draft, mark every correction and gap, and write the short note on what the AI got wrong or missed. Screenshots must come from the working system with sample data, never real customers.

**Deployment, security and operation.** Ch. 12 supplies the outline. The migration plan chooses a conversion style (direct or parallel) and location (pilot store first, phased or both stores at once) and defends it, a natural place for a short alternatives table. The business contingency plan is the paper fallback Feasibility 2.3 called for. Preparing the technology covers installation, backups (NFR06) and account setup; preparing people covers resistance to change, the policy changes (release only after payment, every PO approved by the owner) and how adoption will be motivated and measured. The post-implementation section names who provides support and maintenance after December 9. That is the top organizational risk in the feasibility study, so it needs an owner decision, not an assumption. Scale everything to a two-store shop; the brief rewards realistic, consistent plans over exhaustive detail.

**Training session.** Run it with the owner or staff, using the manual. Record attendance, what confused people and what was changed afterwards; that is direct evidence for Sprint 6 and for the usability requirement (NFR03).

## Sprint 6 (Nov 30–Dec 9, accountable: Kyle): complete and coherent

**Deliverables:** final working system; the final version of every deliverable; post-project review; client adoption pitch (project-spec Sprint 6).

**Final versions.** Plan a full pass in Sprint 6 week one, one owner per document, against the system as built: System Request and Feasibility restated with actual costs, the chosen route and what the owner's baselines showed; catalog statuses updated (built, deferred, rejected, each with its reason); use cases, DFDs and ERD matched to the delivered behaviour and schema; interface design matched to the final screens; specification and test results rerun on the final build; manual matched to the final screens. Each change gets a Change Log row. The project name is settled once, in every document.

**Post-project review.** SAD 8e Ch. 12, Project Assessment, separates the project team review (what we learned about estimating, teamwork, AI use) from the system review (did the system deliver the benefits the feasibility study promised). Compare our Sprint 1 estimates with what we actually found, especially the 6 hours a week and the cost ranges, and be candid about the assumptions that did not hold. Each member completes the course form; the AI Decision Log supplies the evidence for reflections on AI use.

**Handoff and pitch.** Deliver the system, documentation, admin notes and support arrangement to the owner by December 9 under the MOU, and send the thank-you letter the project spec asks for. The pitch should run problem → requirements → design → system → measured or expected value, using the same figures as the final documents.

## Every sprint

- One owner contact of 30–60 minutes, with minutes; each answer recorded in project-context.md with its date.
- AI Decision Log rows written as the work happens; the accountable member fills in Decision and Rationale with evidence before submission.
- Change Log rows for every change to a submitted deliverable, including "no change needed" with a reason where feedback was weighed and declined.
- A consistency pass across requirements, use cases, models, interface, specification, tests and manual before submitting.
- The submission checklist at the end of the AI guidelines, and a team walkthrough so any member can defend any artifact.

## Main risks

| Risk | Effect | Response |
|---|---|---|
| Owner unavailable for the late-October walkthrough | Technology, interface and blocking rules stay unresolved; the build starts on assumptions | Book the session now; send the packet in advance; if it slips, choose provisionally, label the assumption and log it |
| No one takes over support after December 9 | The system is unusable after handoff; Sprint 5 plan is not credible | Raise it at every owner meeting from now; offer the options (owner, staff member, paid help, subscription) with costs from Feasibility 3.3 |
| Build overruns the Sprint 4 week | Not enough working to train on | Freeze MVP in the gap week; build in workflow order so a partial system still trains end to end |
| Documents drift from the code | Execution and Revision scores fall | Model and manual updates are part of each feature's definition of done |
| Unreviewed AI output in code, tests or manual | Integrity risk and weak Judgment | One feature per AI cycle; checklist and log row before merge |
