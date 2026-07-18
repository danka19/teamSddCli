# Corporate Adaptation And Governed Pilot

This runbook prepares Phase 3 adaptation and pilot evidence. The shipped files are templates and synthetic examples only. They do not contain real corporate configuration, credentials, project exports, owners, URLs, or pilot results.

Canonical behavior is defined by `openspec/changes/define-transfer-ready-process-package/specs/transfer-readiness/spec.md`, especially the Corporate adaptation boundary, Corporate pilot entry and acceptance, and Release evidence and auditability requirements. This runbook explains operation; it does not redefine those requirements.

## Shipped Contracts

- `process/templates/corporate-adaptation/environment-inventory.yaml` records verified host, runtime, Git/OpenSpec, package distribution, network, integration, MCP, and AI adapter/model facts. Unknown facts remain `unresolved` with a note.
- `configuration-checklist.yaml` verifies installed package identity, project/owner mappings, managed secret references, approved wiring, rollback, and the AI-disabled fallback.
- `pilot-entry-checklist.yaml` requires human acceptance of the exact external candidate plus green environment/configuration, deterministic gates, privacy controls, accountable owners, and rollback or hold.
- `pilot-evidence.yaml` records one future monitored pilot. `process/examples/corporate-adaptation/pilot-evidence-synthetic.yaml` is the only complete shipped example and is not pilot evidence.
- `no-fork-assessment.yaml` classifies corporate findings. Reusable gaps require an external OpenSpec change reference and may not modify the internal process package.

## External Package Check

From the repository or extracted candidate payload, run:

```powershell
python scripts/validate_corporate_adaptation.py --package --process-root process --json
```

The command must return `status: valid`. This mode also rejects inline credentials, email addresses, private/local IP addresses, user-home paths, and non-reserved URLs in shipped templates and examples.

## Phase 3 Adaptation Sequence

1. Copy the templates into approved local evidence storage outside the reusable package. Do not edit the installed package in place.
2. Populate the environment inventory from commands, product administration screens, approved policy sources, and accountable maintainers. Keep unresolved facts explicit.
3. Populate real non-secret project/owner/configuration mappings. Store only managed secret references; keep secret values in approved ignored or managed storage.
4. Validate each document without `--external-package`, because real local non-secret identifiers are expected in Phase 3:

   ```powershell
   python scripts/validate_corporate_adaptation.py path/to/document.yaml --process-root process --json
   ```

5. Run the configuration checklist and every mandatory gate with AI disabled. A `green` checklist fails validation when a mandatory check remains unresolved or failed.
6. Obtain the human pilot-entry decision for the exact accepted release and bounded pilot candidate. AI cannot make or record that decision on a human's behalf.
7. During the pilot, append failed attempts, interventions, deviations, privacy evidence, rollback/hold actions, and follow-up changes. Never erase a failed attempt after a successful retry.
8. Complete the no-fork assessment before treating adaptation findings as resolved.

## Rollback Or Hold

When an integration, adapter, privacy, evidence, or workflow check fails, hold the affected transition or restore the previous pinned package/configuration according to `PROCESS_PACKAGE_SETUP.md`. Accepted specs and archived change history must remain unchanged. Record the failure and accountable disposition in pilot evidence.

## No-Fork Routing

- Real paths, owners, approved secret references, product versions, and supported standard-tool wiring stay in local configuration.
- Thin adapters may translate an available corporate tool surface but may not own process rules.
- Missing reusable schemas, validators, workflow rules, role instructions, or release capabilities become a controlled change in the external canonical OpenSpec repository.
- An internal process-package modification makes the no-fork assessment `blocked`; it is not a valid shortcut for pilot entry or continuation.

No model run is required for this package. Model availability is an inventory fact only, and the AI-disabled path remains mandatory.
