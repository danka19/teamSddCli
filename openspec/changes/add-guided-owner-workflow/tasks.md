## 1. Specify the guided-operation contract

- [x] 1.1 Add the `guided-owner-workflow` Delta Spec with route, authority, evidence, blocker, and fallback requirements.
- [x] 1.2 Define versioned catalog schema and synthetic route fixtures for new requirement, existing change, hotfix, blocked work, and unavailable surfaces.
- [x] 1.3 Add RED tests for unknown routes, missing context, undocumented commands, route/policy drift, and AI-owned decision claims.

## 2. Deliver the self-service entry point

- [x] 2.1 Implement a discoverable read-only guided CLI entry point with human-readable and JSON output.
- [x] 2.2 Make the entry point select only catalog-declared next commands and return structured blocks/fallbacks when prerequisites are absent.
- [x] 2.3 Preserve explicit invocation and authority for every mutating command and every human gate.

## 3. Deliver shared human and AI onboarding

- [x] 3.1 Create one situation-based onboarding guide that starts with a business requirement and links each route to commands, evidence, and human decisions.
- [x] 3.2 Generate or validate the guide from the catalog so instructions cannot drift.
- [x] 3.3 Add bounded AI route instructions/read-pack integration without granting AI routing or approval authority.

## 4. Verify pre-corporate usability

- [ ] 4.1 Run synthetic human walkthroughs for minor, major, and hotfix routes, including Delta Spec, implementation, QA, and archive preparation.
- [ ] 4.2 Run AI-disabled and available-model route exercises; record unavailable runtime as an explicit fallback, not a fabricated pass.
- [ ] 4.3 Verify failed-run retention, stop/hold/resume, privacy, update/rollback, and forbidden authority cases through the guided route.
- [ ] 4.4 Update package version, release evidence, transfer documentation, and roadmap status only after all focused and complete checks pass.
