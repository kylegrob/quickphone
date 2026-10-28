# Project specifications

*MIS 4173 outside project. Transcribed from the Canvas project details on 2026-10-22; the Canvas copy is authoritative. Wording is unchanged apart from formatting.*

The purpose of the outside project is for students to experience inception through the implementation phases of the systems development process. The project is to be a team effort with each team composed of 4-5 students. Professionalism, critical thinking, and communication are critical skills in this project.

This project mirrors how entry-level systems analysts, business analysts, and technical consultants work in practice — balancing incomplete information, stakeholder feedback, technical constraints, and time pressure to design and develop a working information system. In today's practice, AI tools generate much of the raw material: requirements catalogs, models, prototypes, and code. What the analyst is paid for is judgment — validating what the machine produced, deciding what to accept, modify, or reject, and standing accountable for the result. This project is built around that reality.

## Definition of project success

A successful project demonstrates (1) clear alignment between business problem, requirements, design, and implementation; (2) continuous improvement across sprints using feedback; (3) the team's ability to explain, defend, and justify its decisions as systems analysts; and (4) documented, defensible judgments about every substantive AI contribution to the project.

## How AI fits in this project

AI use is required, documented, and audited. Three principles govern it:

- **Construct before you generate.** For each major artifact type, you will first build a bounded version manually (a slice of the requirements catalog, the logical models, a wireframe). Only then do you use AI to generate the full artifact. The manual work helps you develop the skills for judging the generated work.
- **Every AI contribution gets a decision.** Each substantive AI output must appear in your team's AI Decision Log with an explicit accept / modify / reject decision and a rationale (see template, Appendix A).
- **Judgment is graded, not artifacts.** Polished artifacts are cheap to produce with AI; grades attach to the quality of your validation, critique, and decision rationale, and to your ability to defend those decisions orally. See the sprint grading rubric.

**Academic integrity with AI:** Using AI is not a violation. Misrepresenting the truth is a violation. Document every use of AI in this class in the AI decision log. An undocumented substantive AI contribution, or a decision-log rationale you cannot support when asked, will be treated as an academic integrity matter.

See also [ai-guidelines.md](ai-guidelines.md).

## Finding and engaging a client

Each team finds its own client: a real person or organization with a real problem a small system could improve. Start week one; your client must be confirmed before the Sprint 1 Systems Request. Two teams may not use the same client without approval.

**Where to look.** Start with who you know. Small businesses you know, campus organizations and clubs, university offices and labs, nonprofits and churches, or family businesses. If you can't find an organization from who you know, reach out to employers of friends or family. Prior-semester clients often return — ask the professor.

**What makes a good client.** The client should have a bounded problem (scheduling, tracking, sign-ups, reporting) that your team can handle in a semester. The client should have a decision maker who can approve what you build. The client should be willing to dedicate 30-60 minutes of their time each sprint and provide honest feedback. Avoid clients with protected data (student, medical, payment), inaccessible system integrations, and sponsors who cannot commit time.

**How to approach them.** Contact the decision maker directly and keep it short — who you are, what you'll do, what it costs ($0), what they get, and an easy next step. Focus on what they get out of it, not what you get out of it. Types of problems that might be a good fit: (1) processes with an excessive paper trail, (2) SaaS that could be rewritten and hosted in-house, saving them money, (3) processes or current apps with frequent errors, that are very time consuming, or inefficient. You can provide them with outside eyes on a process nobody questions, documentation of how the work really gets done, a prototype they keep, and trained users. Don't oversell — you are not promising a production system or support after the semester.

**Common objections.** They are too busy? Kindly remind them that you do the work; they only have to give about 30 minutes every two weeks. Sensitive data? Remind them you can use anonymized samples and sign whatever terms they require. Already have software? Ask them what it doesn't do, or whether you could rebuild it to host in-house and save them money. After the semester? They keep the documentation, prototype, and manual, at no cost. Expect most approaches to fail. Contact several prospects at once and follow up once after a week.

**Confirming.** When a client agrees, send the completed Memorandum of Understanding (MOU) and the Sprint 6 pitch date. Keep it in your Teams folder. If a client withdraws, notify the professor immediately.

**Professionalism.** You represent the university: use your ECU email, send replies within one business day, be on time with an agenda, share minutes after each meeting, wear appropriate dress, and write a thank-you at the end of the semester.

## Requirements for this project

**Deliverables.**

- The primary emphasis will be on the ability to explain your deliverables. The list of deliverables, along with their descriptions, can be found below.
- One individual is accountable for the final quality and submission of each deliverable; however, collaboration, peer review, and feedback from all team members are expected and required.
- **Revision policy (revise on feedback):** After the first submission of a deliverable, revise it in future sprints only where feedback (from the professor, classmates, or the client) or downstream changes require it. Blanket resubmission of unchanged deliverables is not required. Each sprint, submit a Change Log listing what changed, why, and in response to whose feedback. "No changes required" is an acceptable entry when it is true and defensible.

**Teamwork.**

- Roles, duties, and responsibilities should be identified and assigned by the team. Roles within the team should include a meeting facilitator, scribe, scheduler, and any additional roles as your team deems necessary. Each member of your group should perform each of the 3 roles at least once throughout the semester. After everyone has had a turn in each role, the group may assign one individual to each role or continue to rotate between individuals, at the team's discretion.
- Teams should meet at least once a week (preferably daily for a short standup meeting, see chapter 13) to discuss progress, assess quality of work, and assign action items. A regular meeting time at the same place, time, day is strongly recommended.
- It is important that teams review individual work before turning in deliverables to be graded. The mechanisms for review and dealing with poor quality work should be defined in the team contract.

**AI usage.** AI tools are encouraged to support ideation, drafting, refinement, and error correction. However, assessment will emphasize your ability to explain what the system does and why it was designed that way.

## Software

- Required: email.
- Suggested diagramming tools: Lucidchart, Figma.
- Suggested file sharing and collaboration: Microsoft Teams.
- Suggested development tools: VS Code, GitHub, ChatGPT, Copilot, Claude AI.

## Deliverables

### Management-oriented deliverables

| Deliverable | Description |
|---|---|
| AI Decision Log | Running team record of every substantive AI contribution and the accept/modify/reject decision made about it, with rationale and an accountable owner (template in Appendix A). Updated continuously; submitted every sprint. |
| Change Log | Running record of every substantive change you made to previously submitted deliverables, with notes on what changes and why. Submitted every sprint. |
| Sprint retrospective | After a sprint presentation, each team should meet and reflect on the sprint and identify areas for improvement. |
| Team Contract | Written and signed by all team members indicating agreed upon conduct and responsibilities. The contract may be changed but will continue to require the signature of all members. All versions of the contract should be preserved with project documentation. |
| Memorandum of Understanding | A signed document between yourself, the client, and the course instructor. |

### Sprint deliverables

| Deliverable | Description |
|---|---|
| Working system | Fully functional system exceeding all client requirements: robust and seamless user experience. AI-assisted construction is expected, however the team is accountable for everything it ships (see Code Acceptance Memo). |
| Systems Request | Narrative description of the organization and application which your team's system will support, including a description of the core business, a description of the existing systems, a description of the problem, a product vision statement, a description of the core functionality to be added, a description of the expected value to be gained, and any issues or constraints. Due at Sprint 1. |
| Feasibility Analysis | Should document the technical, organizational, and economic feasibility of conducting this project. Full documentation should back up claims. Due at Sprint 1. |
| Requirements catalog | Each team derives its own requirements catalog from its client interview notes for a bounded slice of the project. The team then generates a full catalog with AI from its transcripts/notes and writes a short memo comparing the two: which machine-identified requirements are spurious, which are salient to the client's actual priorities, which conflicts the AI surfaced, and why the team considers elicitation complete (the stopping decision). Due at Sprint 2. |
| Interface Design | Generate at least three distinct interface design prototypes for the same core requirements. Share the prototypes with your sponsor for feedback. After feedback, modify the interface and submit the selected design plus a short curation memo defending the selection on the sponsor's feedback, focusing on user-fit, accessibility, and personal taste. The design should include versions for each major use case and consistently match the inputs and outputs identified in the models. Due at Sprint 3. |
| Use cases | Must include actors, preconditions, triggers, normal course, alternate paths, and postconditions and follow the examples in the textbook. Due by Sprint 2. |
| Process models | Logical and physical DFDs, representing system processes and the flow of data. Use the textbook's notation. Logical DFDs due at Sprint 2, and physical DFDs due at Sprint 3. |
| Data models | Your data model should accurately capture the data that the system objects need to store, as defined in the use cases and process models. The data model should be in 3rd normal form. Logical ERD due at Sprint 2 and Physical ERD (which may be AI-generated based on logical ERD) due at Sprint 3. |
| Training and user manual | May be AI-generated from your system and models. Graded on the team's review: corrections, gaps found, and a short note on what the AI got wrong or missed. An uncorrected AI draft is not a deliverable. Due by Sprint 5. |
| Specification document | Details the technical details of the application such that an AI coding tool can generate the application appropriately. Besides the business requirements, the specification document should include testing criteria, security protocols, deployment details, and any additional information to help build the application. Due by Sprint 4 and any subsequent sprint if changes are required. |
| Post Project Review | After the final presentation, each team member must fill out the post project review form detailing their lessons learned. Due at Sprint 6. |

### When each deliverable is first due

| Sprint | Phase | Deliverables |
|---|---|---|
| 1 | Planning | Systems Request, Feasibility Analysis |
| 2 | Analysis | Requirements catalog, Use Cases, Process Models (logical DFDs), Data Model (logical ERD) |
| 3 | Design | Interface Design, physical DFDs, physical ERD |
| 4 | Implementation | Specification document, Working System |
| 5 | Training session | Training & User Manual |
| 6 | Client pitch | Post project review |

## Team roles

**Facilitator.** In charge of distributing the agenda to all members and the professor. Keeps all members focused on the agenda during the meeting and resolves any conflict that may arise. Responsible for issuing Reprimand and Termination Forms and personally delivering a copy of all forms to the professor.

**Scribe.** Responsible for minutes of each meeting. These may be captured by hand or through AI summaries of meeting transcripts, verified by the scribe. The minutes must include: week number, members present, members absent, a copy of the agenda, detailed notes on discussions/decisions for each agenda item, and a list of action items and who they are assigned to. The agenda for the next meeting must be distributed to each team member within one day of the meeting. Minutes must be uploaded to the shared Microsoft Teams folder before being distributed to team members and the instructor for approval via email no more than two days after each meeting.

**Scheduler.** Must contact each team member at least two days before each meeting to confirm attendance, reschedule meetings when attendance is problematic, and maintain the project timetable. Reports the status of the project against the timetable at each meeting.

Other team roles may be identified and assigned as needed.

## Appendix A: AI Decision Log template

Maintain as a shared spreadsheet or table. One row per substantive AI contribution. Trivial uses (grammar fixes, formatting) do not require entries.

| Date | Sprint | Artifact / task | Tool used | What the AI produced (1–2 sentences) | Decision (Accept / Modify / Reject) | Rationale (why — be specific) | Accountable member |
|---|---|---|---|---|---|---|---|

A strong rationale points to evidence: "Rejected — the generated ERD merged Customer and Account, but the client bills accounts with multiple customers." A weak rationale restates the decision: "Modified because it needed changes."

## Appendix B: Sprint Change Log template

| Deliverable | What changed | Why (feedback source or downstream cause) |
|---|---|---|

Unchanged deliverables need only one line: "No changes — no feedback received and no downstream impact."
