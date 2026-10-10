# Counterparty Pre-check: neatHack Plan

Oct 10, 2026

## Summary

We are building an agent that pre-checks a prospective business counterparty in India (company, LLP or proprietor) from public sources and returns a cited, confidence-rated report. Working name is still open.

- **User:** a small business deciding whether to give credit to, or work with, a vendor, customer or partner of a similar size.
- **Input:** a name, plus any identifiers on hand (CIN, GSTIN, PAN, city).
- **Output:** a schema-validated report where every claim links to its evidence, plus a list of what could not be verified.
- **Built in 48 hours:** the pre-check only.
- **Not built:** the post-check (needs the counterparty's consent and guarded sources), default prediction, personal dossiers on individuals, LinkedIn scraping.
- **Moat direction, not yet real:** affordable, explainable reports for tiny businesses, and later a feedback loop from actual payment outcomes.
- **Why it fits the rubric:** a multi-step agent (resolve the entity, gather signals, reconcile conflicts, verify claims, report) with failure recovery and verification built in.

## Rules and rubric

The agent is 30% of the score, and all three sponsor tools must be used and shown in the demo. Source: [neatHack page](https://neatlogs.com/hackathon), read on Oct 10, 2026. Re-check it before submitting.

- **Dates (IST):** build Oct 10 (starts 12:30 PM) to Oct 12; submissions Oct 12, 7:00 to 11:55 PM; winners Oct 16.
- **One track:** build an agent that completes a substantial task start to finish. Judged areas include planning, tool use, state, context, execution, recovery, verification and iteration.
- **Required tools:** neatlogs and Entire to build and improve the agent; cfo.ai to plan its business (pricing, costs, revenue, runway), with the plan included in the submission.
- **Demo video, 3 minutes max:** must explicitly cover architecture, implementation, runtime, reasoning and result for each of the three tools.
- **Submit:** public repo with commits dated during the event, plus a quote post of the official neatlogs post on X.

| Category | Weight | What judges look at |
| --- | --- | --- |
| The agent | 30% | How well it handles a substantial task end to end |
| Use of neatlogs, Entire, cfo.ai | 25% | How well each was used to build, improve and plan the business |
| Demo video | 20% | Clarity of the agent and of the use of all three tools |
| Building in public | 15% | What we shared while building, tagged #neatHack |
| Usefulness and originality | 10% | A real problem, solved in a new way |

Evidence the submission must carry:

- [ ] Two neatlogs traces, before and after a change, with the numbers compared
- [ ] A neatlogs run where an action failed and the agent recovered
- [ ] Entire checkpoints or entire-graph output from our repo
- [ ] A cfo.ai business plan: pricing, costs, revenue, runway
- [ ] Links to build-in-public posts tagged #neatHack
- [ ] Public repo with commits dated Oct 10 to 12

Credits and setup: AWS credits go to the first 200 teams to complete web check-in; Crustdata gives 5,000 credits to everyone. For cfo.ai, sign up at cfo.ai/neathacks; the page says a card is required and the subscription must be cancelled right away in Settings, then Billing, and the organizers supply the credits.

## Sources to build connectors for

Six sources cover companies and LLPs; proprietors get a thinner report. Everything below was checked through search results only, not by opening each source, so open each one in the first hours of the build.

| Source | What it gives | Lookup key | Access | Status |
| --- | --- | --- | --- | --- |
| Identifier checks (offline) | Format and checksum validity of PAN, GSTIN, CIN; entity type decoded from the PAN | PAN, GSTIN, CIN | None needed | From our own knowledge of the formats; confirm while building |
| [MCA company master on data.gov.in](https://data.gov.in/catalog/company-master-data) | Status, registration date, capital, class, registered office, industry code for about 3.67M companies | CIN or name | Personal data.gov.in API key | No directors, DIN, charges or AGM dates. License not considered open by one open-data index, so read the terms. LLP coverage unconfirmed |
| [IBBI public announcements](https://www.ibbi.gov.in/public-announcement) | Insolvency and liquidation process announcements, listed with the company CIN | CIN | Public website; check its terms, cache snapshots | Pages keyed by CIN seen in search results |
| GST taxpayer status | Status, constitution, registration date, business activity | GSTIN | Portal search is captcha-gated with no public third-party API; use a licensed provider (one advertises 10 free lookups, untested) or fixtures | We will not use captcha-solving tools |
| Adverse media | News and public reports that mention the entity | Name plus city | Web search tool | Lowest confidence; every claim needs a cited link |
| Crustdata (optional) | Company and people data APIs | Name or domain | 5,000 credits for all participants | Coverage of small Indian businesses unknown; test on 5 entities in hour 1, drop if thin |

**Dropped or deferred:** LinkedIn (personal data and terms-of-use problems), eCourts (captcha-gated, no open API verified, shown as roadmap), director-level data, Udyam.

**Proprietors:** they have no MCA record, so the report rests on GST, identifier checks and media only. The report must say so, with lower confidence. That graceful degradation is a feature to demo.

## Architecture

A plain state machine: each step is a function with its own neatlogs span, so failures and retries show per step, and the verifier is what makes the report trustworthy.

```
Name + identifiers          (CIN, GSTIN, PAN, city)
  -> Validate identifiers   (checksum, entity type)
  -> Resolve entity         (prune MCA candidates)
  -> Connectors, run in parallel (a failed one is marked unverified)
       MCA master | IBBI | GST status | Adverse media
  -> Reconcile              (rank source trust)
  -> Synthesize             (risk bands)
  -> Verify                 (every claim cited)
       uncited claim: fix or drop -> back to Synthesize
  -> Report                 (with confidence)
```

Identifiers are validated first, the entity is resolved against MCA candidates, connectors run in parallel, conflicts are reconciled, and the verifier drops or fixes any claim that lacks a cited signal.

**Signal record, returned by every connector:** source, signal type, value, observed date, evidence URL, source confidence, match confidence.

**Where pruning is used:** entity resolution narrows MCA candidates by name, state, address and age before any model judgment, so the model sees a handful of candidates, not millions.

**Stack:** Python 3.12 with uv, Pydantic, httpx, a SQLite cache of raw responses, Streamlit, the Anthropic SDK (a small model for resolution, a stronger one for the explanation), and the neatlogs workflow `counterparty-precheck`.

## Eval plan

The eval measures whether the agent finds the right entity, extracts the right signals and backs every claim with a source. It does not measure whether a counterparty will default, and we must not claim it does. Ground truth comes from the same public sources the agent reads, so a good score proves resolution, extraction and citation quality, not risk judgment.

| Test group | Count | Ground truth from | What it tests |
| --- | --- | --- | --- |
| Healthy active companies | 15 | MCA status | False-alarm rate |
| Under insolvency or liquidation | 10 | IBBI announcement, matched by CIN | Signal recall |
| Struck-off companies | 5 | MCA status field | Status recall |
| Name collisions (similar names, different CINs) | 5 to 8 | MCA records | Entity-resolution accuracy |
| Planted identifier inconsistencies (synthetic) | 5 | We create them, e.g. GSTIN whose PAN type contradicts the claimed entity type | Deterministic checks |

**Metrics:** entity-resolution accuracy, signal precision and recall, citation correctness (share of claims whose link supports them), unsupported-claim rate, cost per check, latency per check.

**Baseline vs pipeline:** the baseline is one LLM with web search and no resolver or verifier. Version 1 of our agent is the pipeline without the verifier; version 2 adds it. The v1 and v2 neatlogs traces are our before-and-after evidence.

**Recovery test:** force a connector to time out or return a captcha page. The run must continue, mark that source as unverified, and lower the report's confidence. That run is our failure-and-recovery evidence.

## Timeline

Settle data access in the first three hours, because everything after builds on it. Times are IST and planned, assuming a night of sleep each night; adjust once the kickoff details are clear.

| Item | Start | End |
| --- | --- | --- |
| Setup and access | Oct 10, 12:30 | Oct 10, 14:30 |
| Hour-3 data gate | Oct 10, 15:30 | (milestone) |
| Resolver, identifiers, eval v0 | Oct 10, 15:30 | Oct 10, 23:00 |
| Connectors, verifier, recovery | Oct 11, 08:00 | Oct 11, 23:00 |
| cfo.ai plan, video, README | Oct 12, 08:00 | Oct 12, 17:00 |
| Submission window on X | Oct 12, 19:00 | Oct 12, 23:55 |

Gates and what to cut if one fails:

| Gate | When | Pass | If it fails |
| --- | --- | --- | --- |
| Data access | Oct 10, hour 3 (about 3:30 PM) | MCA lookup by name works, one IBBI record is fetched by CIN, one GST result comes live or from a fixture | Use fixtures for the failing source and move on |
| Core pipeline | End of Oct 10 | Identifiers, MCA connector, resolver and eval v0 run end to end with traces in neatlogs | Cut Crustdata; keep adverse media as a thin connector |
| Verifier and recovery | End of Oct 11 | v1 and v2 traces compared; a forced connector failure recovered | Keep the failure run; drop UI polish |
| Evidence | Oct 12, 5 PM | cfo.ai plan done, demo video recorded, README links all evidence | Submit what is verified; cut features, not evidence |

Build-in-public posts, tagged #neatHack, go out at each gate.

## Sponsor usage

Each tool has one clear job, and the demo must show all three. neatlogs and Entire help us build and improve the agent; cfo.ai plans its business.

| Tool | Role in the project | How we use it | Evidence we keep |
| --- | --- | --- | --- |
| neatlogs | Observe and improve the agent | Instrument from the first commit under the workflow name `counterparty-precheck`, with one span per connector, the resolver, the reconciler, the verifier and the synthesis step. Debug resolution failures from traces. Read cost and latency per check from it | v1 vs v2 traces with the numbers compared; a trace of a forced connector failure and recovery |
| Entire | Record how it was built | Enable it in the repo in the first hour; commit in small steps so checkpoints capture decisions, such as why we added the verifier. Use entire-graph for the codebase map | Checkpoint links and entire-graph output from our repo |
| cfo.ai | Plan the business around the agent | Model price per check; data cost per check (GST lookups, model tokens, taken from neatlogs); volume scenarios; the bad debt a small trader avoids by checking first; runway | The business plan, included in the submission |

Two cautions from the event pages:

- Checkpoints stored in a public repo are public, and our repo must be public. Keep secrets and private data out of agent sessions.
- Entire needs a GitHub repo we can import as admin, and the page says changes can take up to an hour to sync, so set it up first.

## Demo plan

The hero scenario: a small business is about to give a new vendor 60 days of credit, and the agent finds what a quick search would miss. The video is 3 minutes at most.

| Time | Scene | What is on screen | Tool covered |
| --- | --- | --- | --- |
| 0:00 to 0:20 | The problem | A small trader, a new vendor, no cheap way to check them | None |
| 0:20 to 0:50 | The run | Enter the vendor's name and GSTIN; the agent's steps appear live | neatlogs spans shown building up |
| 0:50 to 1:30 | The twist | The identifier check flags a PAN type that contradicts the claimed company type. The resolver finds two similar names; the insolvency announcement belongs to the other CIN, and the agent rejects it with reasons | Agent reasoning |
| 1:30 to 2:00 | Failure and recovery | The GST lookup times out. The agent continues, marks it unverified, lowers confidence | neatlogs trace of the failed and recovered run |
| 2:00 to 2:30 | Proof | v1 vs v2 numbers from neatlogs; the Entire checkpoint that records why the verifier was added, and the graph output | neatlogs, Entire |
| 2:30 to 2:50 | The business | The cfo.ai plan: price per check, cost per check from traces, one growth scenario | cfo.ai |
| 2:50 to 3:00 | Close | The cited report and the one-line pitch | None |

For each of the three tools the video must state the architecture, implementation, runtime, reasoning and result, so script those lines before recording. Say plainly where data comes from cached snapshots or fixtures. Demo on companies, LLPs and a synthetic proprietor, never a real individual.

## Risks, guardrails and decisions

The two biggest risks are matching the wrong entity and harming a real business with a careless claim, so the report shows evidence and confidence, never a verdict. This is not legal advice; read each source's terms before using it.

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Wrong entity match | A false claim lands on the wrong business | Resolver with a match-confidence score, an explicit "cannot verify" state, and a name-collision test set |
| A source breaks or blocks us | The demo fails | Adapters with live and cached modes, fixtures for demo entities, no captcha-solving, cached snapshots |
| Privacy of individuals | Proprietors are individuals, and compiling profiles of private people needs care | Company and LLP data first; synthetic or consenting proprietors only; no personal dossiers; no LinkedIn |
| API rate limits | Hitting API quota during demo or eval | Check directory.apisetu.gov.in for rate limits per API; test at demo scale; document limits in README |
| Personal data caching | API Setu requires informed consent and 24-hour breach notification for personal data; uncontrolled cache grows liability | Use fixtures and synthetic data only; set `CACHE_TTL_HOURS` for auto-deletion; document cache retention policy; never cache real personal data beyond test runs |
| Overclaiming | Loses trust with judges and users | No default prediction; every report lists what was and was not checked |
| Too much for one person in 48 hours | Missing the deadline | Hour gates and cut lines in the timeline |
| Existing verification vendors | Weak originality story | Position as affordable, explainable, cited reports for tiny businesses; the moat is a direction, not yet built |
| Prior employer's work | IP questions | Build from scratch on public data and keep it out of the demo and README |

**Decisions made so far:**

- Pre-check only for the hackathon.
- Companies and LLPs first; proprietors get a thinner, lower-confidence report.
- Plain Python state machine, Streamlit UI and SQLite cache, with no agent framework, so each step gets its own neatlogs span.
- Eval claims are limited to resolution, extraction and citation quality.

## Task split

Two tracks can run in parallel from the start: Track A gets the repo and tooling ready, Track B settles data access and the product shape. Both feed the hour-3 gate in the timeline.

### Track A: repo and setup

- [ ] Complete web check-in (AWS credits go to the first 200 teams)
- [ ] Create the public GitHub repo; keep it empty until kickoff so commit dates are clean
- [ ] Sign in to Entire with GitHub, import the repo, install the CLI, enable it for our coding agent, confirm a first checkpoint appears
- [ ] Create the neatlogs account and project, copy the API key, send a test trace from a stub
- [ ] Python 3.12 project with uv, Pydantic, httpx, SQLite cache and a Streamlit shell
- [ ] Add a Makefile with `make eval`, and keep `.env` in `.gitignore`; keep keys out of agent sessions
- [ ] Write the connector adapter interface (live and cached modes) and the Signal schema skeleton
- [ ] Deploy a Streamlit hello-world so hosting is never a last-hour surprise
- [ ] Start `hackathon.md` as the build log

### Track B: research and product

- [ ] Sign up at cfo.ai/neathacks and follow its card-and-cancel instructions
- [ ] Get the data.gov.in API key; confirm which fields the company master returns and whether LLPs are covered
- [ ] Confirm an IBBI lookup by CIN works, read its terms, decide how to cache snapshots
- [ ] Pick a GST route (licensed provider with free lookups, or fixtures) and test 3 GSTINs
- [ ] Test Crustdata on 5 entities; keep it only if the data is useful
- [ ] Build the 40-entity test list with ground truth, including the name-collision and planted-inconsistency cases
- [ ] Choose the adverse-media approach and write the query templates
- [ ] Draft the report schema and the wording of risk bands (evidence and confidence, no verdicts)
- [ ] Pick the name, one-liner and handles; draft the first build-in-public post
- [ ] List the cfo.ai plan inputs: price per check, cost per check, volume scenarios, bad-debt-avoided case
- [ ] **[API Setu Compliance]** Check directory.apisetu.gov.in for rate limits on: MCA, IBBI, GST, Crustdata
- [ ] **[API Setu Compliance]** Read data.gov.in Terms of Use for MCA — confirm automated use is allowed
- [ ] **[API Setu Compliance]** Read IBBI site terms — confirm caching snapshots is allowed
- [ ] **[API Setu Compliance]** Document in repo: which APIs are tested live vs. fixtures; use synthetic/fixture data only for proprietor demos
- [ ] **[API Setu Compliance]** Add to `.env.example`: `CACHE_TTL_HOURS=24` with cache deletion policy

## Open questions to verify first

These decide whether the connector plan holds, so settle them before the hour-3 gate.

- Does the data.gov.in company master include LLPs, or is there a separate LLP dataset?
- **[API Setu Terms]** Do the data.gov.in terms and the IBBI site's terms allow our automated use, and for how much volume? (Check their ToU and API Setu prohibitions.)
- **[API Setu Terms]** What are the rate limits per API on directory.apisetu.gov.in for MCA, IBBI, GST, Crustdata?
- Which GST route do we use, and what does a lookup cost beyond the free ones?
- Does Crustdata return useful data for small Indian businesses, or do we drop it?
- Does cfo.ai accept the inputs we need for the plan (per-check cost, volume scenarios), and when do the organizer credits arrive?
- Did the kickoff call on Oct 10 (9:00 AM IST) change any rule or the rubric?
- Name and one-liner: which do we commit to, and are the handles free?
