# FinMarketing

Financial-product marketing for a universal bank, beginning with a retail-first
integrated suite demonstrator and synthetic testing by departmental colleagues.

The demonstrator has one deeply implemented retail workflow and bounded domain
packs for commercial banking, wealth and asset management, and IBD and markets.
CardNPV and SMEWallet are preceding specialist studies used as typed provider
references; they do not define the suite's scope.

Start with [project mission control](docs/plans/project-mission-control.md)
for programme outcomes, dependencies, evidence, risks, resources and recovery.
The [product execution map](docs/plans/product-execution-master-plan.md) shows
dependencies, detailed work steps, parallel work, repair and recovery,
acceptance and current task state. Start there
before selecting implementation work. The
[governing monograph](docs/bank_marketing_quantitative_survey.tex) and
[product records](docs/product/README.md) define required behavior and evidence.

```sh
python3 scripts/mission_control.py --build
python3 scripts/mission_control.py --status
python3 scripts/mission_control.py --brief SCOPE
```

Open `build/mission-control/index.html` for the saved dashboard, or run
`python3 scripts/mission_control.py --serve` and visit `http://127.0.0.1:8765/`
for current validated records. The dashboard loads no external assets and
uses the existing task and incident register.

The current evidence is a manuscript and finite local references. Application
delivery, colleague acceptance and subsequent institutional results have
separate tasks and completion criteria.
Checkpoint and incident events preserve progress across sessions. Bounded
repairs stay with their owning task; reopening accepted work invalidates its
dependent evidence and leaves independent work eligible. The utility checks
and records these transitions; the agent performs the repairs and tests.
