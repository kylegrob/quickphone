<!-- Auto-generated from docs/sprint-3/drafts/Sprint 3 - Feasibility Analysis v2.2.docx by tools/extract_text.py. Do not edit by hand; edit the original and re-run. -->

# Sprint 3 - Feasibility Analysis v2.2

SYSTEMS ANALYSIS & DESIGN PROJECT

## QuickPhone Repair Tracking System

Preliminary Feasibility Analysis

Project sponsor: Dr. Ashiqullah Pardisi, owner, Quick Phone Repair & Designs, Raleigh, NC

Prepared by: Project team – Bara Abusamhan, Ehsanullah Pardisi, Kyle Robertson, Leonard Mann

Submitted: Sprint 1 – September 14–20, 2026

Version: 2.2 – preliminary assessment, updated October 19, 2026 for the client’s September 21 confirmations and the Sprint 2 requirements (cost figures unchanged)

How to read this document. This is a preliminary feasibility assessment prepared during initial planning, before the solution options have been analysed and before any technology has been chosen. Its purpose is to establish whether the project is worth continuing into requirements analysis, not to commit QuickPhone to a design, a product or a budget. Every dollar figure in this document is an estimate, shown as a range wherever the underlying facts are not yet known. The estimates are order-of-magnitude and should be treated as accurate to within roughly plus or minus fifty per cent until the open items in section 6 are closed. Sprint 2 settled the requirements (14 functional and 6 nonfunctional, with seven items confirmed by the client on September 21) but not the equipment inventory or the comparison of delivery options, so the cost estimates are unchanged and those items carry into Sprint 3.

QuickPhone Repair Tracking System	1

1. Executive Summary	2

2. Technical Feasibility	2

2.1 What the Business Needs the System to Do	3

2.2 What QuickPhone Has Today	3

2.3 Keeping Working When the Internet Is Down	3

2.4 Delivery Options Not Yet Analysed	4

2.5 Technical Risk Assessment	4

2.6 Conclusion	5

3. Economic Feasibility	5

3.1 How These Estimates Should Be Read	5

3.2 Estimated One-Time Costs	6

3.3 Estimated Annual Operating Costs	6

3.4 Estimated Tangible Benefits	7

3.5 Intangible Benefits and Costs	8

3.6 Cost-Benefit Analysis (Likely Case, 3 Years)	9

3.7 Estimated Economic Value: ROI, Break-Even and NPV	9

3.8 Sensitivity of the Result	10

3.9 The View If Development Had To Be Paid For	10

3.10 Indicative Comparison of Routes	10

3.11 Conclusion	11

4. Organizational Feasibility	11

4.1 Strategic Alignment	11

4.2 Stakeholders, Champion and Management Support	12

4.3 System Users and Adoption	12

4.4 Training and Go-Live	12

4.5 Organizational Risks	13

4.6 Conclusion	13

5. Overall Recommendation	13

6. What Must Be Settled Before These Estimates Firm Up	14

### 1. Executive Summary

Nothing found so far suggests the project should stop. The business problem is clear, the owner has defined what a solution has to do, and on current estimates the value of the staff time returned is several times any plausible cost. What is not yet established is how the system should be delivered or what QuickPhone would need to buy to run it, because the equipment currently in use across the two stores amounts to a laptop and a credit card machine. That gap is the main reason the technical conclusion is provisional rather than firm.

| Dimension | Preliminary result | Basis |
|---|---|---|
| Technical | Provisionally feasible – medium risk | Nothing the business needs is technically unusual, and comparable systems are in everyday use in this industry. Confirmation depends on an inventory of what QuickPhone actually has: devices, connectivity, printing and existing records. Handling internet outages is an open design question, not a solved one. |
| Economic | Feasible on current estimates | Estimated $1,550 one-time and $1,460 a year against an estimated $8,952 a year in staff time returned and losses avoided. Estimated three-year NPV about $17,100, ROI about 353%, payback about 2.5 months. The conclusion holds across the full cost range and fails only if costs land at the top of every range at the same time as benefits come in at half. |
| Organizational | Feasible – low risk | The owner requested the system, defined its goals and sponsors it. The user group is small, sits inside two shops and is already comfortable with technology, so training effort is light. The real adoption question is whether new counter and bench steps survive a busy day. |
| Recommendation | Continue into design in Sprint 3. Requirements analysis is complete; the equipment, connectivity and records inventory and the evaluation of delivery options are still to be done and should come first, so that this assessment can be firmed up before any spending is committed. |  |

### 2. Technical Feasibility

Overall technical risk is medium, and the conclusion is provisional. The reason is not that anything QuickPhone wants is hard to do — it is not — but that the starting position is largely undocumented. Until the team knows what equipment is in the stores, how reliable the connection is and what records exist in what form, any statement that the system will fit is an assumption rather than a finding.

#### 2.1 What the Business Needs the System to Do

Stated as business needs rather than as technology, the system has to give staff at both stores one shared, current record of every repair job; track each job from check-in through to customer pickup with a history of who did what and when; show parts stock at each store, what a job is waiting on and what needs reordering; make each physical device identifiable so it cannot be mixed up or released to the wrong person; email the customer from the store’s account when the device is ready; limit what each person can see and change according to their role; and keep customer information private both where it is stored and while it is being sent. It also has to record whether a job has been paid, alongside the job — the business needs the fact recorded, not the money taken, so nothing has to pass between the system and the card machine. The client confirmed on September 21 that parts are deducted automatically when they are used and that the owner approves every purchase order; neither changes the technical picture. How these needs are met is a design question for Sprint 3.

#### 2.2 What QuickPhone Has Today

Only two items are confirmed: the stores use a laptop and a credit card machine. Everything else in the table below has to be established before the technical position can be settled, and the most consequential unknown is device coverage. One laptop cannot serve two stores, a front counter and a repair bench at the same time, so some additional equipment is the most likely hardware cost in this project. The card machine, by contrast, raises no compatibility question at all: it carries on exactly as it does today and the system simply records whether a job was paid.

| What QuickPhone has | Status | Why it matters | Action |
|---|---|---|---|
| One laptop | Confirmed | A single shared device cannot cover two stores, a counter and a bench at once | Inventory what is actually available at each location; size any additional devices needed |
| Credit card machine | Confirmed | No connection to the system is needed; the system records a paid indicator only | None — the existing payment process is unaffected |
| Internet connection at each store | To confirm | Determines which delivery options are viable and what happens during an outage | Confirm what each store has and how often it drops (see 2.3) |
| Any other staff devices (phones, tablets, a second computer) | To confirm | May remove or substantially reduce the equipment cost | Include in the inventory |
| Printing capability | To confirm | Needed only if the business wants printed device tags and claim tickets | Confirm what exists; confirm with the owner whether printed tagging is wanted |
| Business email mailbox | Confirmed | Customer alerts depend on being able to send from the shop's own address | None — the owner approved sending from the store’s account on September 21 |
| Existing job, parts and customer records | To confirm | Determines whether there is anything to carry across, and how much work that is | Establish what form the records are in and how far back they go |

The equipment position is the single largest source of uncertainty in the cost estimates in section 3, which is why the one-time cost is shown as a range rather than a figure.

#### 2.3 Keeping Working When the Internet Is Down

This is a real question rather than a hypothetical one, and it has to be answered before a delivery option is chosen, because the answer pulls against the owner's goal of one view across two stores. A system reached over the internet gives both stores the same record at all times but stops when the line does; a system running inside each store keeps working through an outage but lets the two stores drift apart until they are brought back into line. There is a useful starting data point already: the card machine depends on the same connection, so the stores have direct experience of what an outage costs them and roughly how often one happens. The owner should be asked for that experience, and for how long a store could reasonably work from paper, before the options below are narrowed.

| Approach | During an outage | Effect on one shared view | Relative cost |
|---|---|---|---|
| System runs offsite, reached over the internet | Unavailable at both stores until the connection returns | Best — both stores always see the same record | Lowest; covered by the hosting estimate in 3.3 |
| System runs on equipment inside each store | Keeps working locally | Weakest — the two stores diverge until they are reconciled | Moderate; two installations to keep in step |
| Offsite, with a local standby copy at each store | Limited use continues; work catches up afterwards | Good, with a short catch-up delay | Highest; additional build and ongoing effort |
| Offsite, with an agreed paper fallback | Staff record on paper and key it in afterwards | Unaffected once the backlog is entered | None to build; adds staff time after every outage |

A paper fallback procedure should be agreed regardless of which approach is chosen, since no option removes the possibility of the system being unavailable.

#### 2.4 Delivery Options Not Yet Analysed

Three broad routes are open and none has been evaluated yet. QuickPhone could have a system built to its own workflow; it could subscribe to a product already made for repair shops; or it could extend something already in use in the business, if the inventory turns up anything suitable. Each carries a different cost shape, a different answer to the outage question and a different position on who maintains it afterwards. Comparing them properly is Sprint 2 work, and the cost ranges in section 3 are drawn wide enough to cover any of them. The estimates should not be read as a decision in favour of one route.

#### 2.5 Technical Risk Assessment

| Risk factor | Assessment | Risk | Mitigation |
|---|---|---|---|
| Current equipment and connectivity are undocumented | Only a laptop and a card machine are confirmed. Device coverage, connection reliability, printing and mailbox all remain open, and they drive both cost and design. | Medium–High | Inventory at both stores as the first task in Sprint 2, before any option is chosen |
| Behaviour during an internet outage is undecided | The choice trades the owner's shared-view goal against continuity of service, and cannot be settled without the owner's experience of outages. | Medium | Put the question to the owner in Sprint 2; agree a paper fallback in every case |
| Familiarity with the business area | The team is new to repair-shop operations, though the owner has already defined the roles, the job workflow and the intake, pickup and inventory rules. | Medium | Owner interview in Sprint 1; requirements walkthroughs in Sprint 2; staff review of designs in Sprint 3 |
| Familiarity with the technology | Cannot be rated until a delivery route is chosen. Nothing the business needs is unusual, and systems of this kind are common in the industry. | Medium | Weight the Sprint 2 option evaluation towards what the team can deliver in the time available; trial the harder parts early |
| Scale of what has to be built | Four part-time students, roughly thirteen weeks, and a Sprint 2 catalog of fourteen functional requirements, twelve of them Must, across twelve use cases. | Medium | Essential and desirable items separated in the backlog; scope frozen after Sprint 2; a working version demonstrated in Sprint 4 |
| Existing records may be harder to carry across than expected | Their form and volume are unknown, so the conversion effort cannot yet be sized. | Low–Medium | Establish scope in Sprint 2; starting with an empty system and building records up from new intakes remains a valid fallback |

#### 2.6 Conclusion

Provisionally feasible at medium risk. Nothing QuickPhone needs is technically unusual and there is no obvious obstacle, but a firm conclusion depends on work not yet done: an inventory of equipment, connectivity and existing records, a decision on how the system should behave when the internet is down, and an evaluation of the delivery options. All three are still open, carry into Sprint 3, and none of them is expensive to carry out.

### 3. Economic Feasibility

#### 3.1 How These Estimates Should Be Read

Costs and benefits are identified below, given estimated values, and then assessed over three years using return on investment, break-even and net present value at a ten per cent discount rate. Because the delivery route has not been chosen and QuickPhone's equipment position is not yet known, costs are shown as a low, likely and high range rather than as single figures, and the range is drawn wide enough to cover any of the delivery routes in section 2.4. The financial measures are then calculated on the likely column, with the other columns tested in the sensitivity analysis at 3.8. Year 0 is the build period; benefits begin when the system is in use, so Year 1 is the first full year of operation.

| Assumption used in the estimates | Value | Basis and confidence |
|---|---|---|
| Front desk hourly wage | $21.53 | National average, May 2025. Estimate — replace with QuickPhone's payroll rate. |
| Repair technician hourly wage | $35.81 | National average for an electronics repairer occupation, May 2025. Estimate, and probably above what QuickPhone pays; the benefit line it supports is the one most likely to fall. |
| Store manager hourly wage | $23.33 | National average, May 2025. Estimate — replace with QuickPhone's payroll rate. |
| Blended staff rate | $27.60 | Weighted average of the three rates above; used for mixed-role time |
| Discount rate | 10% | Standard small-business assumption; not derived from QuickPhone's finances |
| Analysis horizon | 3 years | Five years also shown where the longer view changes the answer |

All operating volumes are analyst assumptions, not measurements. Twenty-five status calls per store per week, four jobs per store awaiting parts, three hours per store per week of inventory administration, three lost-device incidents a year and a $120 average repair were assumed in order to produce a figure at all. They will be replaced with QuickPhone's own baseline after the owner interview, and the benefit estimate will move when they are.

#### 3.2 Estimated One-Time Costs

The one-time cost turns almost entirely on what the equipment inventory finds. If the stores already have enough devices between them, QuickPhone's outlay is close to nothing; if two or three additional devices are needed, it is a few thousand dollars. Development labour is supplied by the project team as coursework and costs QuickPhone nothing, though it is priced separately at 3.9 because it is not free in an economic sense. No consultant fees, office equipment or facilities costs are anticipated on any route.

| Cost category (all figures estimated) | Low | Likely | High | Basis and confidence |
|---|---|---|---|---|
| Development team salaries | $0 | $0 | $0 | Supplied by the student team as coursework; priced at 3.9 for the economic view |
| Consultant fees | $0 | $0 | $0 | None anticipated; the course instructor and the owner advise at no charge |
| Development training | $0 | $0 | $0 | Team self-study; no paid courses or materials assumed |
| Staff computing devices | $0 | $800 | $2,400 | Largest unknown. $0 if existing equipment covers both stores; up to roughly three additional devices if it does not. Depends entirely on the inventory. |
| Device tagging and ticket printing hardware | $0 | $300 | $400 | Only if printed tags and claim tickets are adopted; roughly one unit per store. Owner decision outstanding. |
| Software licences and tools | $0 | $0 | $600 | $0 on routes built from freely available components; a packaged product may carry a setup or licence charge |
| Vendor installation and configuration | $0 | $0 | $500 | $0 where the project team installs; applies only if a packaged product is chosen |
| Office equipment and facilities | $0 | $0 | $0 | No new counters, furniture or cabling anticipated |
| Network improvements | $0 | $0 | $400 | Only if the connectivity review at 2.3 finds the current arrangement inadequate |
| Data conversion | $0 | $250 | $700 | Scope not yet decided. $0 if the system starts empty and records build up from new intakes; up to roughly twenty-five staff-hours if stock and open jobs are loaded first. |
| Initial user training | $100 | $200 | $350 | Staff are comfortable with technology, so this is familiarisation rather than instruction: roughly four to twelve staff-hours plus printed reference cards |
| Estimated total one-time cost to QuickPhone | $100 | $1,550 | $5,350 |  |

#### 3.3 Estimated Annual Operating Costs

Operating cost is small in absolute terms on every route, but its shape changes completely depending on which route is chosen: a system QuickPhone runs itself carries running and storage costs, while a subscription replaces most of this table with a single monthly fee. The table below estimates the first case. No additional staff are needed in either case — account administration is a few minutes of the manager's existing time — and refresher training is light because the staff are already comfortable with technology.

| Cost category (all figures estimated) | Low | Likely | High | Basis and confidence |
|---|---|---|---|---|
| Running the system (hosting or equivalent) | $0 | $250 | $450 | $0 if it runs on equipment already in the store; a few hundred a year if run offsite. Depends on the delivery route. |
| Data storage and backup | $0 | $150 | $250 | May be included in the line above; shown separately because backup must be provided either way |
| Address and naming | $0 | $10 | $15 | Applies only if the system is reached over the internet |
| Software licensing | $0 | $0 | $300 | $0 on routes built from freely available components. A subscription product is treated separately at 3.10, not added here. |
| Consumables — labels and ticket stock | $0 | $120 | $200 | Only if printed tagging is adopted |
| Hardware repair and replacement reserve | $50 | $250 | $600 | Devices and any printing hardware written down over roughly three years; scales with whatever 3.2 turns out to require |
| Software upgrades and application support | $0 | $600 | $1,800 | Placeholder, not a quote. See the note below. |
| Operational team salaries | $0 | $0 | $0 | No new staff; account administration absorbed into the manager's existing duties |
| Refresher and new-hire training | $30 | $80 | $150 | Roughly one to five staff-hours a year; low because staff are comfortable with technology |
| Estimated total annual operating cost | $80 | $1,460 | $3,765 |  |

Note on the support line. No quote has been obtained for this and no support arrangement exists yet, so the figure is a placeholder rather than a finding. It is carried because a system that nobody is responsible for maintaining is not free — it simply fails later — and leaving the line at zero would make the estimate look better than it is. The likely figure is roughly the cost of one hour of paid help a month, and the range spans the realistic outcomes: $0 if the owner or a member of staff takes the system on, or if a subscription product is chosen where support is included in the fee; $1,800 if outside help has to be paid for at commercial rates. This is the single largest swing item in the operating estimate, and it rests on an owner decision recorded in section 6 as the most important one outstanding.

#### 3.4 Estimated Tangible Benefits

The tangible benefits are staff hours returned to productive work, plus the avoided cost of lost devices. On the volumes assumed at 3.1, the system would return roughly six hours a week across both stores, or about 315 hours a year, worth an estimated $8,952. Every figure in this table is an estimate built on assumed volumes, and the estimate will move — probably downwards — once real baselines and payroll rates replace the assumptions.

| Estimated benefit | Hrs/wk | Hrs/yr | Rate | Est. value/yr | Calculation |
|---|---|---|---|---|---|
| Fewer status-enquiry calls | 1.67 | 86.7 | $21.53 | $1,866 | 2 stores x 25 calls x 50% reduction x 4 min |
| Less time chasing jobs waiting on parts | 2.00 | 104.0 | $35.81 | $3,724 | 2 stores x 4 jobs x 0.5 hr x 50% reduction |
| Less inventory administration | 2.40 | 124.8 | $23.33 | $2,912 | 2 stores x 3 hrs x 40% reduction |
| Fewer lost or wrongly released devices | – | – | – | $450 | 3 incidents/yr x $300 x 50% reduction |
| Estimated total tangible benefit per year | 6.07 | 315.5 |  | $8,952 |  |

Stated a second way: the 104 technician hours returned are roughly 100 additional repairs a year at about an hour of bench time each, worth an estimated $12,000 in added revenue at an assumed $120 average repair. This is the same recovered capacity valued as revenue instead of as saved labour. It is not added to the $8,952; the more conservative labour valuation is used throughout.

#### 3.5 Intangible Benefits and Costs

None of the items below is carried into the financial model, and no dollar value is claimed for any of them. Two are nevertheless more important to a two-store independent repair business than anything in the tables above. Customers notice being told their device is ready rather than having to chase it, and they notice a shop that never loses a device. In a trade where reviews and word of mouth decide where people take a cracked screen, that is the most plausible route to a real gain in local market share.

| Intangible benefit | Effect on the business |
|---|---|
| Improved customer service | Customers are told when the device is ready and get an accurate answer immediately if they call; waiting becomes shorter and more predictable |
| Brand recognition and reputation | A visible, consistent intake and pickup process; fewer disputes and lost devices feed better reviews and word of mouth |
| Local market share | Faster turnaround and a reputation for not losing devices are what win repeat and referred business from competing shops |
| Better supplier relations | Visible stock levels and parts needed by waiting jobs produce accurate, better-timed orders and fewer rush requests |
| Accountability and control | Every check-in, approval, part used and release recorded against a person and a time, making disputes resolvable |
| Consistency across two stores | One process and one record make it easier to train new staff and to move staff between stores |
| Foundation for later reporting | Clean operational data enables future reporting on turnaround time, parts usage and technician workload |

| Intangible cost | Effect on the business |
|---|---|
| Short adjustment period | Intake and pickup will be a little slower for the first week while staff settle into the screens; the effect is expected to be small given how comfortable staff are with technology |
| New steps can be skipped | Identifying the device at check-in, recording parts at the bench and checking before release are new habits that can be dropped when a queue forms |
| Owner and manager attention | Reviews, decisions and training take owner and manager time away from running the stores |
| Dependence and availability risk | If the system is unavailable and staff fall back to paper, customer confidence suffers more than it would have before the system existed |
| Privacy exposure | Holding customer contact details raises the cost of a mistake; role-based access and encryption reduce but do not remove it |
| Uncertainty about ongoing support | Until responsibility for the system is settled, staff may hesitate to rely on it for anything they cannot redo by hand |

#### 3.6 Cost-Benefit Analysis (Likely Case, 3 Years)

The table brings the estimated costs and benefits together over three years, discounted at ten per cent, using the likely column from 3.2 and 3.3. One-time costs fall in Year 0; benefits and operating costs run from Year 1, when the system is in use. All figures are estimates and are rounded in the conclusions that follow.

| Estimated cash flow | Year 0 | Year 1 | Year 2 | Year 3 | Total |
|---|---|---|---|---|---|
| Tangible benefits | $0 | $8,952 | $8,952 | $8,952 | $26,856 |
| One-time costs | ($1,550) | $0 | $0 | $0 | ($1,550) |
| Annual operating costs | $0 | ($1,460) | ($1,460) | ($1,460) | ($4,380) |
| Net cash flow | ($1,550) | $7,492 | $7,492 | $7,492 | $20,926 |
| Cumulative net cash flow | ($1,550) | $5,942 | $13,434 | $20,926 |  |
| Discount factor at 10% | 1.0000 | 0.9091 | 0.8264 | 0.7513 |  |
| Present value of net cash flow | ($1,550) | $6,811 | $6,192 | $5,629 | $17,082 |
| Cumulative present value | ($1,550) | $5,261 | $11,453 | $17,082 |  |

#### 3.7 Estimated Economic Value: ROI, Break-Even and NPV

| Measure (estimated) | Result | How it is calculated |
|---|---|---|
| Total benefits, 3 years | about $26,900 | $8,952 x 3 years |
| Total costs, 3 years | about $5,900 | $1,550 one-time + $4,380 operating |
| Net benefit, 3 years | about $20,900 | Total benefits less total costs |
| Return on investment | about 353% | Net benefit / total costs |
| Net present value at 10% | about $17,100 | Sum of discounted net cash flows, Years 0–3 |
| Simple payback period | about 2.5 months | $1,550 / ($7,492 / 12 months) |
| Discounted break-even point | about 0.23 years, or 2.7 months into Year 1 | $1,550 / $6,811 of Year 1 present value |
| Benefit-cost ratio | about 4.5 : 1 | Total benefits / total costs |

#### 3.8 Sensitivity of the Result

Because every input is an estimate, what matters is not the central figure but how much has to go wrong before the answer changes. The table below recalculates the result at the edges of the cost ranges and with the benefit estimate halved. The project remains worth doing in every combination except one: costs landing at the top of every range at the same time as benefits come in at half. That combination is possible but not likely, and it would be visible well before the money was spent, because the equipment inventory and the support decision both happen early.

| Scenario | One-time | Annual cost | Annual benefit | 3-yr NPV | Payback |
|---|---|---|---|---|---|
| Low cost, benefit as estimated | $100 | $80 | $8,952 | about $22,000 | immediate |
| Likely case (section 3.6) | $1,550 | $1,460 | $8,952 | about $17,100 | 2.5 months |
| High cost, benefit as estimated | $5,350 | $3,765 | $8,952 | about $7,500 | 12.4 months |
| Likely cost, benefit halved | $1,550 | $1,460 | $4,476 | about $5,950 | 6.2 months |
| High cost, benefit halved | $5,350 | $3,765 | $4,476 | about ($3,600) | not recovered in 3 years |

#### 3.9 The View If Development Had To Be Paid For

The project team's labour costs QuickPhone nothing, but it is not free in an economic sense, and pricing it is the only honest way to compare building a system against subscribing to one. At roughly 520 hours of team effort valued at junior contract rates, development would cost somewhere between $15,000 and $26,000, with about $18,200 as a working estimate. On that basis the system roughly breaks even over three years and is clearly worthwhile over five. The practical reading is that the donated development effort is what makes building attractive; without it the comparison against a subscription would be much closer.

| Measure (estimated) | 3-year horizon | 5-year horizon | Note |
|---|---|---|---|
| Total costs | about $24,100 | about $27,000 | $18,200 development estimate plus one-time and operating costs |
| Total benefits | about $26,900 | about $44,800 | $8,952 a year from Year 1 |
| Net present value at 10% | about ($1,100) | about $8,650 | Turns positive during Year 4 |
| Simple payback period | about 2.6 years | about 2.6 years | $19,750 / $7,492 a year |

#### 3.10 Indicative Comparison of Routes

No option has been evaluated yet, so the table below gives only the shape of each route and an indicative cost band. Products made for repair shops are commonly listed in the region of one to two hundred dollars a month for a multi-store business, which puts a subscription in the same general territory as running a system QuickPhone owns, once realistic support costs are included on the owned side. That is a useful thing to know early: the decision is unlikely to be settled on price alone, and will probably turn on fit, on who carries the support burden, and on who holds the data. Named products and quoted prices are still to be compared, in Sprint 3.

| Route | Indicative annual cost | What decides it |
|---|---|---|
| Do nothing | $0 | Forgoes an estimated $8,952 a year. The owner's three stated problems remain unaddressed. Included as a baseline, not as a serious option. |
| Have a system built for QuickPhone | About $1,500 a year on current estimates, including an allowance for support | Fits the owner's workflow exactly and QuickPhone holds its own data. Depends on someone being responsible for it after the project ends. |
| Subscribe to an existing repair-shop product | Commonly listed around $1,200–$2,400 a year for a multi-store business | Support and updates are included and the arrangement is straightforward, but the business fits itself to the product and carries features it does not need. Prices to be confirmed with vendors. |
| Extend something already in use | Cannot be estimated yet | Depends entirely on what the equipment and records inventory finds. May not be a real option. |

#### 3.11 Conclusion

Economically feasible on current estimates. The likely case gives an estimated three-year net present value of about $17,100, a return of about 353% and payback in roughly the first quarter of operation, and the conclusion survives both a doubling of costs and a halving of benefits. The figures are preliminary and will move once the equipment inventory, the support decision and QuickPhone's own operating baselines are available. The important finding for initial planning is not the precise return but its margin: the value of the staff time at stake is several times any plausible cost of addressing it.

### 4. Organizational Feasibility

Organizational risk is low, and this is the strongest of the three dimensions. The system addresses problems the owner raised, in a business the owner controls, for a user group of fewer than a dozen people who all work in two shops and are already comfortable with technology. There is no competing agenda and no group whose interests are threatened by the change.

#### 4.1 Strategic Alignment

QuickPhone makes money by finishing repairs quickly and by being trusted with customers' devices, and every goal the owner set for this system serves one of those two levers — which is what strategic alignment amounts to in a business this size. Nothing in the scope pulls away from that: taking payment, online booking and reporting were all set aside so the system stays aimed at the owner's three stated problems.

| Business goal (from the owner) | How the system supports it |
|---|---|
| Fewer "where's my phone?" calls | Any staff member can look a job up and answer immediately; an automatic message when the device is ready stops many calls before they are made |
| Fewer jobs stuck waiting on parts | Parts recorded against jobs, jobs flagged as waiting, low stock visible, and supplier orders tracked against the jobs that need them |
| No lost devices | Each device identifiable from check-in; release only after the agreed checks; a full history of every job |
| One view across two stores | One shared record, viewable by store, technician and status |
| Keep it simple | The system records whether a job was paid rather than taking payment, and does only what the owner asked for |

#### 4.2 Stakeholders, Champion and Management Support

The project champion is the store owner, and the championship is real rather than nominal: the owner initiated the request, defined the goals and the workflow, sponsors the project and signs off at each review. Below the owner, the store manager is the key management stakeholder and the person whose routine changes most, since purchasing and stock administration move into the system. Securing the manager's active use early matters more than any other adoption step, because front desk staff and technicians will take their cue from whether the manager actually works from the system.

| Stakeholder | Role in the project | What they need from it | Support level and action |
|---|---|---|---|
| Store owner | Sponsor and project champion | Visibility across both stores; the three stated problems solved | Committed — requested the system, attends reviews and signs off scope. Confirmed seven requirements on September 21, including approving every purchase order. |
| Store manager | Organizational management; daily power user | Reliable stock levels, supplier order tracking, staff accounts | Assumed supportive — confirm at the owner interview; involve in Sprint 2 requirements and Sprint 3 design review |
| Front desk staff | Day-to-day users; intake and pickup | Fast intake, fewer interruptions, a clear answer for every caller | Adoption turns on speed at the counter; name a lead user at each store and review designs with them in Sprint 3 |
| Repair technicians | Day-to-day users; bench work | A clear job queue and parts availability without leaving the bench | Adoption turns on updates being quick; keep routine actions to one or two steps |
| Customers | Affected, not users | To be told when the device is ready and to get it back | No training needed; the pickup notification email from the store’s account was approved on September 21 |
| Suppliers | Affected, not users | Accurate, timely orders | No change to how orders are placed; the manager records them in the system |
| Project team | Builds and hands over | Stable scope and timely owner decisions | Fixed review dates; Member B acts as Product Owner proxy if the owner is unavailable |

#### 4.3 System Users and Adoption

Every role in the business maps onto a role in the system, and no one is being asked to do a fundamentally different job. The system follows the job statuses the stores already use, so the workflow itself barely changes; what changes is the record-keeping around it. Three new habits are required — identifying the device at check-in, recording parts against the job at the bench, and running the agreed checks before release — and each takes under a minute. The risk is not that staff cannot do them but that they are exactly the steps that get skipped when a queue forms at the counter. The response is to build them into the flow of work as required steps rather than optional extras, and to have the manager review exceptions weekly.

#### 4.4 Training and Go-Live

Training effort is expected to be light. The staff are comfortable with technology and are already following the workflow the system records, so the sessions are familiarisation rather than instruction: a short hands-on session at each store on the staff's own equipment, with real devices rather than a classroom exercise, supported by a one-page reference at the counter and the bench. The estimate at 3.2 allows roughly four to twelve staff-hours in total. What deserves more attention than the training itself is the first week of live use, when the team should stay reachable, record what staff actually find awkward and fix it before handing the system over. A paper fallback procedure should be agreed before go-live, and whether existing open repairs are entered at cutover is an open decision recorded in section 6.

#### 4.5 Organizational Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| No one is responsible for the system after the project ends | Medium | High | Settle in Sprint 3, before any build decision; budget for it as estimated at 3.3; hand over setup and administration notes; keep a subscription route open as a fallback |
| New check-in, parts and release steps get skipped when the shop is busy | Medium | High | Build them into the workflow as required steps; weekly manager review of exceptions; cover them explicitly in the training session |
| Manager does not move purchasing and stock administration into the system | Low | High | Involve the manager in Sprint 2 requirements and Sprint 3 design review; make sure stock is accurate from the first day of use |
| One store adopts and the other does not | Low | Medium | Bring both stores in during the same week; name a lead user at each; owner reviews both stores |
| Owner unavailable for timely decisions | Low | Medium | Review dates agreed in advance; Member B acts as Product Owner proxy; open decisions listed with deadlines |
| Purchase orders wait on the owner, who must approve every one (confirmed September 21) | Medium | Medium | Approval queue shown to the owner; a spending threshold or urgent path is an open question (FR10) |
| Equipment turns out to be insufficient to use the system at the counter and the bench | Medium | Medium | Inventory first in Sprint 2; the cost of closing the gap is estimated at 3.2 and is modest relative to the benefit |

#### 4.6 Conclusion

Organizationally feasible at low risk. The project has a committed champion in the owner, clear alignment with how the business makes money, a small and identifiable user group, and staff who will not struggle with the tool itself. The one decision still outstanding — who is responsible for the system once the project ends — remains the highest-rated organizational risk and is still open and should be settled early in Sprint 3.

### 5. Overall Recommendation

| Dimension | Preliminary conclusion | Basis |
|---|---|---|
| Technical feasibility | Provisionally feasible – medium risk | Nothing the business needs is unusual, but equipment, connectivity, records and outage behaviour are all unresolved and must be established before this can be confirmed |
| Economic feasibility | Feasible on current estimates | Estimated NPV about $17,100, ROI about 353%, payback about 2.5 months in the likely case; holds across the cost range and a halved benefit |
| Organizational feasibility | Feasible – low risk | Owner is champion and sponsor; all roles map to system roles; staff are comfortable with technology; adoption risk limited to three new steps at the counter and bench |
| Overall | Continue into design in Sprint 3. Requirements analysis is complete; begin Sprint 3 with the equipment, connectivity and records inventory and the evaluation of delivery options. Commit no spending until those are done and this assessment is firmed up. |  |

### 6. What Must Be Settled Before These Estimates Firm Up

Three things carry most of the uncertainty. The equipment inventory sets the one-time cost and could move it by several thousand dollars in either direction. The decision on who is responsible for the system after the project ends is the largest swing item in the annual cost and the highest-rated organizational risk. And QuickPhone's own operating baselines — how many status calls, how many jobs actually sit waiting, how much time goes on stock administration, and what the staff are actually paid — determine the whole benefit side, which is currently built on assumptions rather than measurements.

| Open item | Owner | Why it matters and when it is needed |
|---|---|---|
| Inventory of equipment, connectivity, printing and existing records at both stores | Store manager | Sets the one-time cost and constrains the delivery options. Still open; first task in Sprint 3. |
| Who is responsible for the system after the project ends | Store owner | Largest swing item in the annual estimate and the top organizational risk. Still open; Sprint 3, before any build decision. |
| QuickPhone's own baselines: status calls, jobs awaiting parts, inventory admin time, lost-device incidents | Store owner | The entire benefit estimate rests on assumed figures until these are supplied. Owner interview. |
| Actual payroll rates for front desk, technicians and manager | Store owner | Replaces national averages; the technician rate in particular is probably too high, which would reduce the estimated benefit. Sprint 3. |
| How the system should behave when the internet is down, and how often that happens | Store owner | Shapes the delivery route and trades against the shared-view goal. Sprint 3, before options are narrowed. |
| Whether printed device tags and claim tickets are wanted | Store owner | Determines whether the printing hardware and consumables lines apply at all. Sprint 3. Sprint 2 lists printed tickets and tags as a Must (FR03), not yet confirmed by the owner. |
| Whether existing records are carried across, and how far back | Store owner | Data conversion is currently a placeholder; starting the system empty remains a valid choice. Sprint 3. Sprint 2 proposes a spreadsheet import of parts (FR11). |
| Approval to send customer alerts from the shop’s existing mailbox — resolved September 21: approved, from the store’s account | Store owner | Closed. |
| Whether the pickup notification is sent by staff or automatically | Store owner | Decides who can trigger it (technicians may not) and the pickup screen design. Sprint 3. |
| Purchase-order spending threshold, or an urgent path when the owner is unavailable | Store owner | Every order now waits on owner approval. Sprint 3. |

Sources and status of figures. Wage rates are national averages for the relevant occupations, May 2025, used as estimates in place of QuickPhone's payroll. Equipment, running and consumable costs are indicative bands drawn from published prices for this category of product as of September 2026; no quotes have been obtained and no supplier or product has been selected. Subscription costs are indicative list ranges for repair-shop products generally, to be confirmed with vendors in Sprint 2. Operating volumes, reduction percentages, incident counts and the $120 average repair are analyst assumptions pending the owner interview. Version 2.1 superseded v1.1 and restated the assessment as a preliminary one appropriate to initial planning. Version 2.2 (October 19, 2026) brings it into line with the client’s September 21 confirmations and the Sprint 2 requirements; no cost or benefit figure has changed.
