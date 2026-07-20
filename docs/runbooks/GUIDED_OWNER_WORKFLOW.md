# Guided Owner Workflow

<!-- guided-catalog-sha256: 2d3b10a3b364b95dba33ecdfb74692fe5722c1654fa9fec398288022cdd30a48 -->

This guide is the human and AI entry point for the external process package. It is read-only: follow the returned command explicitly, retain the named evidence, and stop at every named human decision. The canonical route source is `process/catalogs/guided-owner-workflow.yaml`.

## Start with your situation

| Situation | Provide | Next commands | Human decision |
| --- | --- | --- | --- |
| New business requirement | Proposed classification | `create_change`, then `classify_change` | Tech Lead confirms classification. |
| Existing change | Change ID and known lifecycle state | `prepare_spec_pr`, `evaluate_change_gates`, or `prepare_archive` as applicable | Change Owner records the applicable gate decision. |
| Urgent incident | Retained incident reference | `classify_change`, `create_change`, then `evaluate_change_gates` | Tech Lead confirms hotfix eligibility; urgency does not bypass safety. |
| Blocked or failed operation | Retained failed-run reference | `manual_fallback` | Tech Lead records hold or resume. |

## AI and unavailable surfaces

An AI assistant may explain a catalog route, draft artifacts, and identify missing context. It must not select an undocumented route, confirm classification, approve a gate or waiver, resume work, approve release/archive, merge, deploy, or mutate an external system. If AI, MCP, or an integration is unavailable, pass `--unavailable <surface>` to `scripts/guided_owner_workflow.py`; use the returned `manual_fallback` command and retain the unavailable-surface evidence.

## Verification

Run `python scripts/validate_guided_owner_workflow.py --json` after changing this guide or its catalog. A mismatch is a release blocker because it means people and assistants could receive different operating instructions.
