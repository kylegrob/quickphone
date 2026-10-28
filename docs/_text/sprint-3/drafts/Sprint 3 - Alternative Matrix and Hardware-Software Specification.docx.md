<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - Alternative Matrix and Hardware-Software Specification.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - Alternative Matrix and Hardware-Software Specification

SYSTEMS ANALYSIS & DESIGN PROJECT

## Quick Phone Repair Management System

Acquisition Alternative Matrix and Hardware and Software Specification

Project sponsor: Dr. Ashiqullah Pardisi, owner, Quick Phone Repair & Designs, Raleigh, NC

Prepared by: Project team – Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann

Sprint 3 draft – October 23, 2026. Method: Dennis, Wixom, Roth & Haley, Systems Analysis and Design, 8th ed., Ch. 6 (acquisition strategy, Figs. 6-3, 6-5, 6-6) and Ch. 7 (architecture design and hardware and software specification, Figs. 7-2, 7-9, 7-10, 7-11).

Status: provisional. The weights and scores below were drafted with AI assistance and are for the team to accept, modify or reject (AI Decision Log, October 23); the owner has not yet confirmed the route. Every dollar figure is an estimate.

### 1. Purpose and Status

The Sprint 3 brief asks the team to defend an acquisition route and a technical approach. Until now every design document assumed the Sprint 1 planning idea, a custom web application with one shared database, while Feasibility section 2.4 said that no route had been analysed. This document closes that gap. Section 2 describes three routes and section 3 compares them in a weighted alternative matrix built as SAD 8e Ch. 6 describes: 100 points of weight spread across technical, economic and organizational criteria, each route scored from 1 (poor fit) to 5 (perfect fit), and the weighted scores totalled (Fig. 6-6). Section 4 tests how far the result can move. Sections 5 and 6 state the architecture and the hardware and software specification in the form of Ch. 7, and section 7 lists what the choice changes in the physical models. The decision is provisional because the owner has not yet answered the two questions that move it most: who looks after the system after December 9, and what equipment and internet connection each store has. Both are on the agenda for the late-October walkthrough.

### 2. Alternatives Considered

The three routes follow the acquisition strategies of SAD 8e Ch. 6 (Fig. 6-3). In route A, custom development, the team builds a web application in Python using the Django framework, with a PostgreSQL database, hosted offsite and used through a browser at the counter and the bench in both stores. Route B is packaged software bought as a subscription: a product made for repair shops. The two products checked on October 23 list multi-location tiers at about $140–$150 per store per month (RepairDesk Growth, $149; RepairShopr Big Chain, $139.99–$149.99, less on annual billing), or roughly $3,400–$3,600 a year for two stores. These are published list prices, not quotes, and review sites disagree with the vendor pages. Route C extends tools the business may already have: a shared spreadsheet and online forms in the office suite that comes with many business email accounts, if the store’s account includes one. Outsourcing, the third Ch. 6 strategy, is not scored. Fig. 6-5 suits it to needs that are not core to the business, and paid development is priced at $15,000–$26,000 in Feasibility 3.9, several times the business’s likely annual cost.

The listed subscription prices are above the $1,200–$2,400 a year band in Feasibility 3.10; that table should be updated to these figures and their sources.

### 3. Weighted Alternative Matrix

Weights follow what the client has told us matters. Fit to the seven confirmed rules carries the most weight because they are the only requirements the owner has validated (September 21), and the owner set every one of them. Cost to the business comes next, because the sponsor carries it every year, and support after handoff is weighted as the top organizational risk in Feasibility 4.5. The MOU deliverables count because the engagement is a contract for a prototype, interface designs, a specification and training, not only for a working shop system. Each score cites its evidence in the second table, and an unverified vendor claim is scored at the middle of the scale, not the top.

| Criterion | Weight | A: Custom (Django, PostgreSQL) | Wtd | B: Repair-shop subscription | Wtd | C: Shared spreadsheet and forms | Wtd |
|---|---|---|---|---|---|---|---|
| Technical: fit to the confirmed workflow and rules | 25 | 5 | 125 | 3 | 75 | 2 | 50 |
| Technical: access control and record integrity (NFR01, NFR02, NFR04, NFR05) | 15 | 4 | 60 | 5 | 75 | 1 | 15 |
| Technical: one current view of both stores (FR13) | 10 | 5 | 50 | 5 | 50 | 3 | 30 |
| Economic: annual cost to QuickPhone (sponsor view) | 20 | 4 | 80 | 2 | 40 | 5 | 100 |
| Organizational: support after the December 9 handoff | 15 | 2 | 30 | 5 | 75 | 3 | 45 |
| Organizational: delivers the MOU deliverables | 10 | 5 | 50 | 2 | 20 | 3 | 30 |
| Organizational: adoption by staff used to paper | 5 | 4 | 20 | 3 | 15 | 3 | 15 |
| Total | 100 |  | 415 |  | 350 |  | 285 |

Scores: 1 = poor fit, 5 = perfect fit (SAD 8e Fig. 6-6). Weighted score = weight × score.

| Criterion | A: Custom | B: Subscription | C: Spreadsheet |
|---|---|---|---|
| Fit to the confirmed rules (client confirmations #3–#7; FR08, FR10, FR12) | 5. Built to the rules: automatic deduction with no reservation, Owner approval of every purchase order, email only from the store’s account, no release before payment. | 3. Tickets, stock, purchase orders and customer email are standard features. Whether one product enforces Owner approval of every order and hides contact details from technicians is unverified; to check in a vendor demo. | 2. A sheet cannot stop stock going below zero, block a release before payment or limit who may send the email. |
| Access control and record integrity | 4. Role checks on the server and database constraints (CHECK, unique keys, transactions). Built and tested by students, so one point below a mature product. | 5. Role-based permissions and audit history are long-established in these products (vendor claim). | 1. Sharing works per file, not per field; anyone who can edit can rewrite history. |
| One view of both stores | 5. One shared database for both stores. | 5. Multi-location tiers are built for this. | 3. One shared file, but per-store stock and the dashboard need hand-built formulas. |
| Annual cost (estimates) | 4. About $1,460 a year, likely case, including a $600 support placeholder (Feasibility 3.3). | 2. About $3,400–$3,600 a year at list price for two stores (section 2). | 5. About $0 if the store’s email account already includes the suite; to confirm. |
| Support after handoff | 2. Nobody is named yet. Django 5.2 is a long-term-support release with security fixes to April 2028, which limits forced upgrades. | 5. The vendor maintains, updates and supports the product. | 3. Simple enough for the owner to keep, but formulas break silently. |
| MOU deliverables | 5. Prototype, interface designs, technical specification and training all follow directly. | 2. Configuration and training only; no prototype or specification of our own unless the MOU is amended. | 3. A working tool and training, but a thin technical specification. |
| Staff adoption | 4. Screens limited to each role’s tasks. | 3. Carries features the shop does not need (Feasibility 3.10). | 3. Familiar grids, but easy to type in the wrong row. |

### 4. How Far the Result Can Move

Route A leads by 65 points, but the lead rests on two scores. The first is support: custom scores 2 because nobody has agreed to maintain the system after December 9. The second is fit: the subscription scores 3 only because no vendor has shown that its product enforces the owner’s rules. The table recalculates the matrix under each change. A vendor demo that proved full fit would narrow the gap to 15 points without reversing it. If the owner can name nobody to support a custom system, so that support carries 30 points and rule fit 10, the subscription wins. Cheaper subscription pricing alone does not change the order. The team’s recommendation is therefore conditional, and the condition is something the owner can answer in one meeting: if someone will own the system after handoff, build route A; if not, tell the owner the subscription is the better buy, even though it ends the build.

| Scenario | A: Custom | B: Subscription | C: Spreadsheet | Leader |
|---|---|---|---|---|
| As scored | 415 | 350 | 285 | Custom |
| Vendor demo proves full rule fit (B fit = 5) | 415 | 400 | 285 | Custom |
| Subscription priced at $1,200–$2,400 a year (B cost = 4) | 415 | 390 | 285 | Custom |
| No one will support a custom system (support 30, fit 10) | 370 | 380 | 300 | Subscription |
| Both: no support and full vendor fit | 370 | 400 | 300 | Subscription |

### 5. Architecture

The system uses a thin client–server architecture in three tiers (SAD 8e Fig. 7-2). A browser on each counter and bench device handles presentation, the Django application on a hosted server handles the business rules, and a managed PostgreSQL server holds the data. Both tiers run on a public cloud platform (Ch. 7, Cloud Computing), so nothing is installed or maintained in the stores. Fig. 7-9 points this way for three of our requirements. Portability: staff may use the existing laptop, a second-hand PC or a tablet, and a browser runs on all of them. Maintainability: there is no client software to reinstall, which matters when nobody is yet named to support the system. Access control: every role check (NFR01, NFR04, NFR05) runs on the server, where a user cannot bypass it by hiding a button. Performance needs are modest: about ten staff accounts across two stores and a few users at once. Availability is the weak point. An internet outage stops both stores, so the agreed fallback is the fourth option in Feasibility 2.3: record on paper and key it in afterwards. The owner’s experience of outages on the card machine line should confirm that this is acceptable.

### 6. Hardware and Software Specification

The table follows SAD 8e Fig. 7-10: software, hardware and network for each component, with quantities and the minimum standard. Cost bands are the Feasibility estimates, not quotes. Device numbers assume a counter and a bench position in each store, four in all. The confirmed laptop covers one of them, and the equipment inventory may reduce the rest.

|  | Counter and bench devices | Label printer | Application server (hosted) | Database server (hosted) | Email |
|---|---|---|---|---|---|
| Operating system | Any current OS with a supported browser: the existing laptop’s Windows; Windows 11, ChromeOS or iPadOS for added devices | Driver on the counter device | Linux container provided by the host | Managed by the host | The store’s existing mailbox (client confirmation #7) |
| Special software | Current Chrome, Edge or Safari; nothing to install | Prints device tag and claim ticket from the browser (FR03) | Python 3.12 or later; Django 5.2 LTS; Gunicorn; HTTPS certificate from the host | PostgreSQL 16 or later; daily automated backup and point-in-time restore (NFR06) | Authenticated SMTP over TLS; password kept as a host secret, never in the repository |
| Hardware (minimum) | 4 GB RAM; 13-inch or larger screen at the counter, 10-inch tablet or laptop at the bench | Direct thermal, USB, about 2-inch labels | Smallest paid instance (about 0.5 GB RAM, shared CPU) | Smallest managed plan, 1 GB storage (ample for years at two stores) | None |
| Network | Always-on broadband and Wi-Fi at each store (to confirm, Feasibility 2.2) | USB to the counter device | Internet, HTTPS only | Private connection to the application server | Outbound from the application server |
| Quantity | 4 positions: 1 existing laptop, up to 3 added | 1 per store (2) | 1, shared by both stores | 1, shared | 1 mailbox per store or one shared |
| Estimated cost (low / likely / high) | $0 / $800 / $2,400 one-time (Feasibility 3.2) | $0 / $300 / $400 one-time (3.2); only if printed tags are adopted | $0 / $250 / $450 a year, both servers together (3.3) | Included in the hosting line | $0; existing account |

Why Django and PostgreSQL within route A. The factors of SAD 8e Fig. 7-11 decide it. On functions and features, Django ships the pieces our models need: user accounts and groups for the four roles (NFR01, NFR05), an admin site that covers most of 9.0 Maintain Shop Records (FR14), forms with built-in cross-site request protection, database migrations generated from the physical ERD, transactions that keep the three stored totals in step with their rows, and an SMTP email backend for the pickup notification (FR12). Flask, the lighter Python option, would need each of these assembled from separate extensions, which means more code for the team to review. On cost of ownership, both are free and open source, and the 5.2 long-term-support release limits upgrade work. On skills, team members have used Python (team statement, October 23; each member to confirm), and no one has PHP or Java experience to set against it. PostgreSQL enforces the CHECK constraints, unique keys and the composite store_part_stock key in the physical data dictionary, and most hosts offer it as a managed service with the daily backup NFR06 requires. MySQL would also work, but it gains us nothing.

Development tools, at no cost to QuickPhone: Git with a private GitHub repository, Visual Studio Code, pytest for tests, and the course’s AI coding workflow (plan, implement, test, review, commit). Seed data uses made-up customers only. The hosting provider is chosen in the October 26 – November 1 gap week by comparing current prices for both servers.

### 7. Effect on the Physical Models and Next Steps

The physical DFDs now name the implementation as SAD 8e Ch. 9 Step 1 asks (Figs. 9-2, 9-4). Each data store is labelled “PostgreSQL: …” with its tables listed, each store flow is a “PostgreSQL Record: …” or “PostgreSQL Record Update: …”, each process band names Django, and the human–machine boundary encloses the Django application and the PostgreSQL database. The two manual steps in 6.0, the photo-ID check and payment on the unlinked card machine, stay outside it. The physical ERD’s generic SQL types are all valid PostgreSQL types, so the tables do not change; the Sprint 4 specification will fix the exact types and the Django model for each table. Four inputs could still change this document. The first is the owner’s answer on support, which decides the route (section 4). The second is the equipment and connection inventory, which sets the device count. The third is a vendor demo on the three rules a subscription might not enforce. The fourth is the owner’s outage experience, which tests the paper fallback. Each answer goes into project-context.md and the Change Log, and this matrix is re-scored when it arrives.
