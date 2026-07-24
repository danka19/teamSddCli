# Central team-specs and AI role workflow reality audit

Date: 2026-07-24

Status: completed for implementation-plan input; no product implementation was
performed by this audit.

## Scope

The audit checks whether the approved FAQ design
`docs/superpowers/specs/2026-07-24-central-team-specs-and-ai-role-workflow-faq-design.md`
matches the repository as it exists now.

The audit evaluates:

1. one-adapter/one-technical-project default;
2. sibling, relative-path and registry reference support;
3. separation of central specification truth and project implementation truth;
4. availability of AI discovery and bounded read-pack mechanisms;
5. public versus specialist command boundaries;
6. FP/project many-to-many implementation status;
7. multi-repository orchestration status;
8. current FAQ/role coverage and focused regression evidence.

Classifications:

- **pass** — directly supported by code, schema, accepted spec or passing test;
- **verified limitation** — current implementation does not provide the
  capability and documentation must say so;
- **documentation gap** — behavior exists or is planned, but current FAQ does
  not explain the practical route;
- **unverified** — evidence is insufficient for a factual claim.

## Reproducible evidence

Commands run from repository root:

```text
python scripts/sdd.py --help
python scripts/sdd.py op list --json
python -m pytest tests/test_validate_process_config.py tests/test_weak_model_kit.py tests/test_product_faq_docs.py -q
openspec list
node %USERPROFILE%/.codex/skills/roadmap-openspec-validator/scripts/validate-roadmap-openspec.mjs --root <repository-root>
```

Inspected artifacts:

- `process/schemas/project-adapter.schema.json`;
- `process/schemas/projects.schema.json`;
- `process/schemas/reference.schema.json`;
- `process/validators/config_discovery.py`;
- `process/validators/config_validation.py`;
- `process/catalogs/operations.yaml`;
- `process/operation_dispatcher.py`;
- `scripts/build_read_pack.py`;
- `templates/project-adapter/.sdd-project.yaml`;
- `templates/team-specs/`;
- accepted `openspec/specs/repo-topology-config/spec.md`;
- active `openspec/changes/define-fp-analytics-publication-model/`;
- active `openspec/changes/add-ai-analyst-discovery/`;
- current installation/setup/Analyst/Developer/QA FAQ pages.

Observed results:

| Check | Result |
| --- | --- |
| Public `sdd --help` | package `0.3.7`; commands `guide`, `start`, `setup`, `next`, `op`, `check`, `prepare`, `request`, `run` |
| Public `sdd op list --json` | no public `build-read-pack`, `validate-process-config`, clone, pull or context operation |
| Focused config/read-pack/FAQ tests | `118 passed` |
| Roadmap/OpenSpec validator | `0 errors`, 3 unrelated lifecycle warnings |
| FP implementation tasks | `define-fp-analytics-publication-model` remains `0/70` |
| Analyst discovery tasks | `add-ai-analyst-discovery` is `12/13`; only first-time human walkthrough remains |

The complete repository test suite was not rerun for this planning audit.
Existing evidence in `add-ai-analyst-discovery/tasks.md` records a recent full
run of `801 passed, 11 skipped, 20 failed`; therefore this audit does not claim
that the full suite is green.

## Findings

### TS-AI-REAL-001 — one adapter selects one technical project

Classification: pass with a documented-default caveat.

Evidence:

- `project-adapter.schema.json` requires exactly one scalar `project_id`;
- adapter validation requires that ID to exist in central `projects.yaml`;
- the adapter records one central reference and one pair of local code/test
  paths.

Practical conclusion: the first supported and simplest documented route may
say “one code repository normally registers as one technical project ID”.

Caveat: the current project registry does not deterministically reject two
different project entries that point to the same repository reference.
Therefore FAQ wording must describe a supported default, not claim a hard
global invariant. Monorepository or multiple-project-per-repository use still
requires an explicit topology decision.

### TS-AI-REAL-002 — sibling/path/registry discovery works

Classification: pass.

Evidence: `config_discovery.py`, adapter schemas and focused tests cover:

- `sibling:<id>`;
- `path:<relative>`;
- `registry:<id>` with explicit `--registry ID=PATH`;
- bounded path resolution;
- rejection of absolute, traversal, ambiguous and unsafe references;
- adapter-to-central project and version compatibility.

Practical conclusion: sibling checkout can be the recommended local route,
with registry mapping as the corporate fallback.

### TS-AI-REAL-003 — central/project source ownership is accepted

Classification: pass.

Evidence: accepted `repo-topology-config` requires `team-specs` to own shared
requirements, changes and traceability while project repositories own code,
tests and implementation-local technical truth.

Practical conclusion: the FAQ can state this as current architecture, not
future intent.

### TS-AI-REAL-004 — configuration validation is specialist-only

Classification: verified limitation.

Evidence:

- `validate-process-config` exists in the canonical operation catalogue and
  `scripts/validate_process_config.py`;
- it is not exposed by the current public `sdd op list`;
- current setup FAQ already notes that full team-config validation has no
  separate self-service public command.

Required documentation rule: show the exact specialist command and do not
invent a public `sdd config` or equivalent command.

### TS-AI-REAL-005 — bounded read packs exist but are not a polished public route

Classification: pass for the lower-level mechanism; verified limitation for
self-service use.

Evidence:

- `scripts/build_read_pack.py` and `process/weak_model_kit.py` build
  authority-labelled, hashed, task-specific packs;
- focused read-pack tests pass;
- `build-read-pack` is in the canonical operation catalogue;
- it is absent from the public `sdd op list`;
- no public `sdd context` command exists.

Required documentation rule: direct sibling/multi-root access is the primary
practical route; bounded read pack is a specialist fallback.

### TS-AI-REAL-006 — Analyst discovery is implemented, not merely designed

Classification: pass with pending human acceptance.

Evidence:

- active `add-ai-analyst-discovery` has 12/13 tasks complete;
- packaged companion contains `analyst-discovery` and `guided-change`;
- FAQ and focused tests cover one-question-at-a-time discovery, truth statuses,
  separate draft/action permissions and stage boundaries;
- only real first-time human walkthrough task 5.3 remains open.

Required documentation rule: describe this feature as implemented with pending
first-time human acceptance, not as a design without an OpenSpec change.

### TS-AI-REAL-007 — FP/project many-to-many remains planned

Classification: verified limitation.

Evidence:

- the active publication change defines FP catalogue/namespaces and
  project ↔ FP many-to-many requirements;
- it has `0/70` implementation tasks complete;
- current `process/schemas/` has no FP catalogue schema;
- current `templates/team-specs/` has no `fp-catalog.yaml` or `fps/` root.

Required documentation rule: explain the target model and its usefulness, but
label FP registry, FP navigation and release publication as planned.

### TS-AI-REAL-008 — automatic multi-repository orchestration does not exist

Classification: verified limitation.

Evidence:

- public `sdd` has no clone, pull, workspace, context or multi-repository
  orchestration command;
- the operation catalogue contains no clone/pull implementation;
- current tools validate explicit local references and prepare bounded work;
  they do not manage checkouts or coordinate writes across repositories.

Required documentation rule: humans update/open both checkouts; AI receives
explicit workspace roots and write scope. Cross-project work is decomposed
into separate tasks/PRs and combined later.

### TS-AI-REAL-009 — current role pages do not provide the complete practical start

Classification: documentation gap.

Evidence: current role pages contain role boundaries, `sdd next`, evidence and
handoff, but do not fully explain:

- cloning/opening sibling repositories;
- adapter validation from the project root;
- granting AI access to two roots;
- central read-only versus project write permissions;
- requirement-to-code/test impact mapping;
- separate central evidence-update permission;
- cross-project task/PR decomposition.

Remediation is authorized by the owner and belongs in the detailed FAQ plan.

## Plan constraints produced by the audit

The implementation plan must:

1. use “normally/default” for one repository ↔ one technical project ID;
2. distinguish current accepted topology from planned FP many-to-many storage;
3. treat Analyst discovery as implemented but pending human walkthrough;
4. expose specialist config/read-pack commands honestly;
5. avoid nonexistent `sdd context`, clone, pull or orchestration examples;
6. teach sibling/multi-root access and explicit AI workspace permissions;
7. keep `team-specs` read-only for Developer/QA implementation sessions;
8. require separate permission for traceability/evidence updates;
9. preserve both outstanding human walkthrough gates;
10. avoid claiming the complete repository test suite is green.

## Residual risks

- A real corporate AI tool may restrict multi-root filesystem access; exact
  product configuration must be documented during corporate capability probe.
- The one-repository/one-project default is not a repository-reference
  uniqueness invariant in current validation.
- FP registry and release publication examples cannot be executable until the
  planned publication model is implemented.
- Automated documentation checks cannot prove first-time usability; human
  walkthrough evidence remains mandatory.

## Remediation decision

The human owner explicitly authorized FAQ/OpenSpec planning for all confirmed
documentation gaps. No separate remediation question remains. Implementation
must still follow the detailed plan and preserve human acceptance gates.
