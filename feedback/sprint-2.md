# Sprint 2 feedback

| Item | Value |
|---|---|
| Deliverables graded | Requirements Catalog and Memo, Use Cases, DFDs, ERD, Change Log, Presentation |
| Grade | _not recorded yet_ |
| Received | _date not recorded_; Professor, written feedback |

## Feedback (verbatim)

Source: Professor, written feedback, pasted into this file 2026-10-22 (receipt date not recorded).

> eam 4 Sprint 2 Feedback
>
> Overall, your team has made solid progress in developing a more complete understanding of the Quick Phone Repair system. The requirements catalog, use cases, DFDs, and ERD demonstrate thoughtful effort and generally show a good understanding of the repair workflow. There are, however, several important areas where greater consistency, refinement, and integration across deliverables are needed before moving forward.
>
> 1. Change Log Revisions
>
> One of the major issues is that I did not see the requested revisions to earlier Sprint 1 deliverables reflected in your submission. The purpose of the change log is to document how feedback from previous sprints affected existing deliverables and how those changes influenced future work.
>
> Your change log currently documents changes to the catalog, use cases, DFDs, and ERD. However, those artifacts were first created in Sprint 2 and therefore cannot represent revisions to Sprint 1 deliverables. Instead, I expected to see updates to the Systems Request and Feasibility Analysis incorporating feedback from the previous sprint.
>
> For the next sprint:
>
> * Update the earlier deliverables when feedback requires revisions.
> * Document those revisions in the change log.
> * Clearly explain how changes affected later deliverables.
>
> 2. Requirements Catalog
>
> The requirements catalog is generally well organized and includes both requirements and acceptance checks, which will be useful later when developing test cases.
>
> However, there are several improvements needed:
>
> AI Requirements Integration
>
> The memo states that the AI-generated catalog contained 31 requirements, of which 10 were identified as salient and added because they revealed gaps.
>
> The problem is that those requirements are not clearly incorporated into the final catalog. The submission references an Appendix A, but that appendix is not included.
>
> For future submissions:
>
> * Combine all approved requirements into a single catalog.
> * Clearly indicate which requirements originated from AI analysis.
> * Include any referenced appendices.
>
> Requirement Sources
>
> I recommend adding an additional "Source" column to the requirements catalog.
>
> Potential sources might include:
>
> * Client interviews
> * Project documents
> * Sprint 1 process models
> * AI-generated suggestions
> * Stakeholder discussions
>
> This will improve traceability and help justify why requirements were included.
>
> Acceptance Checks
>
> I like that every requirement includes an acceptance check.
>
> To improve readability:
>
> * Separate requirements and acceptance checks into separate columns.
> * This structure will also make test planning easier later in the project.
>
> 3. Use Cases
>
> The use cases are generally well structured and include all the major sections expected in a professional use case specification:
>
> * Actors
> * Triggers
> * Stakeholders
> * Descriptions
> * Normal flows
> * Alternative flows
> * Exception handling
>
> Your set of 11 use cases covers the major business processes and workflow steps.
>
> Recommended Improvement: Inputs and Outputs
>
> As you continue refining the design, start documenting:
>
> * Inputs into the system
> * Outputs produced by the system
>
> for each use case.
>
> Doing so will strengthen the connection between:
>
> * Requirements
> * Use Cases
> * DFDs
> * ERD
>
> and help ensure consistency across all modeling artifacts.
>
> Maintain Client Validation
>
> Use cases should not simply be accepted because AI generated them. Continue validating each workflow with the client to ensure the flow accurately reflects real-world operations.
>
> 4. DFD Feedback
>
> Missing Context Diagram
>
> The most significant omission is the lack of a Context Diagram.
>
> You should include a diagram showing:
>
> * The system
> * Customer
> * Front Desk Staff
> * Technician
> * Store Manager
> * Store Owner
>
> and the major information flows between them.
>
> A context diagram is a required part of the DFD hierarchy.
>
> Process Naming Problems
>
> Several processes describe activities performed by people rather than activities performed by the information system.
>
> Examples include:
>
> * Diagnose Device
> * Repair Device
>
> The information system is not actually diagnosing or repairing anything.
>
> Instead, process names should focus on actions the system performs, such as:
>
> * Record Diagnosis
> * Manage Repair Job
> * Capture Repair Information
> * Record Parts Usage
>
> Review all process names and make sure they represent information-processing activities.
>
> Repeated Data Stores and Entities
>
> The Level 0 DFD appears to repeat several:
>
> * Data stores
> * External entities
>
> multiple times.
>
> This is not standard DFD practice and makes the diagram unnecessarily difficult to interpret.
>
> Simplify the diagrams and follow conventional DFD notation.
>
> 5. DFD Level 1 Feedback
>
> Appointment Scheduling
>
> The Check-In DFD begins with booking a drop-off appointment.
>
> However, appointment scheduling appears to be a distinct workflow and may require its own process hierarchy. Requirements FR01 explicitly describe appointment management functionality.
>
> Questions to resolve:
>
> * Is an appointment required?
> * Is an appointment optional?
> * Is appointment scheduling within system scope?
> * Where is that functionality modeled?
>
> The team should answer these questions and reflect the answer consistently throughout the requirements, use cases, DFDs, and ERD.
>
> Process Naming and Logic
>
> Several Level 1 processes seem to describe staff actions rather than system functionality.
>
> For example:
>
> * "Identify Customer"
>
> sounds like a user goal rather than a system process.
>
> You may need more specific process names such as:
>
> * Retrieve Customer Record
> * Create Customer Record
> * Update Customer Information
>
> Focus on what the system is doing rather than what the user is trying to accomplish.
>
> 6. ERD Feedback
>
> The ERD is currently too difficult to read and review.
> At this stage, neither I nor potential stakeholders can reasonably evaluate many of the tables, keys, or relationships.
>
> For the next submission:
>
> * Export at a much larger resolution.
> * Ensure all entities and attributes are readable.
> * Verify that every team member can comfortably explain the model.
>
> If you cannot read the diagram yourself, it will be difficult to validate or defend your design.
>
> 7. DFD and ERD Consistency Problem
>
> This is currently the largest modeling issue in the project.
>
> The ERD appears to contain well over twenty entities.
>
> The DFDs, however, only show a small number of data stores.
>
> These models should broadly align with one another.
>
> Questions to address:
>
> * Where are all ERD entities represented in the DFDs?
> * Are some entities unnecessary?
> * Are some data stores missing from the DFDs?
> * Are some DFD stores improperly combined?
>
> Your team appears to have divided work among members, which is fine, but the final deliverables must be reconciled before submission.
>
> There should be clear consistency among:
>
> * Requirements
> * Use Cases
> * DFDs
> * ERD
>
> Any discrepancies should be resolved before the next sprint.
>
> Overall Assessment
>
> Strengths:
>
> * Well-developed requirements catalog.
> * Strong acceptance criteria.
> * Comprehensive use cases.
> * Evidence of client engagement and workflow understanding.
> * Good effort integrating AI into the analysis process.
>
> Areas Requiring Attention:
>
> * Revise and document Sprint 1 deliverable changes.
> * Integrate AI-generated requirements into a unified catalog.
> * Add requirement source tracking.
> * Include a context diagram.
> * Improve process naming in DFDs.
> * Remove repeated entities and data stores.
> * Clarify appointment scheduling workflows.
> * Improve ERD readability.
> * Reconcile major inconsistencies between the DFDs and ERD.
>
> Overall, I believe the team is moving in the right direction and is developing a solid understanding of the business domain. The primary focus for the next sprint should be improving consistency and integration across all modeling artifacts so that the requirements, use cases, DFDs, and ERD tell the same story and represent the same system.

## Action items

Each was addressed in the Sprint 3 drafts (`docs/sprint-3/drafts/`), which are not yet submitted.

- [x] Change log covered only Sprint 2 artifacts; revise Sprint 1 documents and show how each change carried forward — Sprint 3 Change Log, revised System Requests, Feasibility v2.2
- [x] AI-generated requirements not integrated and Appendix A missing — Catalog: Source column marks AI items; Appendix A maps all 31
- [x] Add a Source column to the catalog — Catalog
- [x] Separate requirement text from its acceptance check — Catalog (separate columns)
- [x] Give each use case its inputs and outputs — Use Cases (Inputs, Outputs, Traces to)
- [x] Keep validating use cases with the client — Use Cases (client validation status per use case). Walkthrough with the owner still to do
- [x] Missing context diagram — DFD and ERD Models (logical and physical)
- [x] Processes were named for people's work, not what the system does — DFD and ERD Models (renamed, section 8)
- [x] Entities and data stores repeated on diagrams — DFD and ERD Models (each drawn once). Oct 23: on seven DFDs two flows shared a stretch of line, so one looked like a branch of the other (e.g. Level 0 part 3, "Job awaiting pickup" appeared to come from D1); re-routed so every flow has its own line, in the models doc, both decks and the physical DFD PDF
- [x] Is an appointment required or optional? — Optional: FR01, UC-12, DFD 1.0
- [x] ERD too hard to read — simplified 22 → 16 entities; overview plus three detail slides; data dictionary
- [x] Diagrams must work in PowerPoint — all redrawn at 16:9 slide size; Level 0 shown whole and in three parts
- [x] DFDs and ERD inconsistent — 16 entities in 7 stores, each exactly once; alignment slide
- [ ] Every member can explain the ERD and its alignment with the DFDs (feedback section 6) — whole team — walk through the Sprint 3 models before presenting
