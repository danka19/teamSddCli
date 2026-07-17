# Transfer Release Candidate

This runbook defines the deterministic pre-rehearsal candidate boundary. The
candidate contains an immutable `payload/` directory and a sibling
`release-manifest.yaml`. Host rehearsal and acceptance evidence stays outside
the candidate and binds to `payload_sha256`.

## Build

Create an input YAML containing only `release_id`, `known_limitations`, and the
local `raw_artifact_root`. Raw evidence bytes are inspected for checksums but
are never copied into the candidate.

```powershell
python scripts/manage_release_candidate.py build --root . --destination C:\release\candidate --inputs C:\release\inputs.yaml
```

The destination must not exist and must not overlap the source repository.
Construction uses a sibling staging directory and publishes the destination
only after schema and semantic validation pass.

## Validate

```powershell
python scripts/manage_release_candidate.py validate --candidate C:\release\candidate --manifest C:\release\candidate\release-manifest.yaml
```

Exit `0` means the manifest and exact payload inventory agree. Exit `1` is a
deterministic acceptance rejection. Exit `3` means required local input is
missing or malformed. Validation rejects links, reparse points, unsafe or
colliding portable paths, undeclared entry points, payload mutation, and
mutable release/development evidence.

Windows requires `full-clean-rehearsal`; Linux on WSL2 requires
`portability-smoke`; macOS is explicitly `not-certified`. No AI or human
acceptance decision is recorded by this command.

Standalone smoke and rehearsal commands must set `PYTHONDONTWRITEBYTECODE=1`
so Python does not write cache files into the frozen payload.

## Rehearse The Immutable Candidate

Use a new workspace and an output path outside the candidate, workspace, and
accepted/archive history. The command inventories the host with fixed argv and
`shell=False`, then calls the packaged bootstrap, configuration, class-flow,
migration, update, failed-update/hold, and rollback operations. It never edits
the candidate.

Windows PowerShell:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python C:\release\candidate\payload\scripts\manage_release_candidate.py rehearse --candidate C:\release\candidate --workspace C:\release\windows-rehearsal --platform-id windows --evidence-level full-clean-rehearsal --mcp-status explicitly-unavailable --output C:\release\host-evidence\windows.yaml
```

Linux/WSL2 Bash:

```bash
export PYTHONDONTWRITEBYTECODE=1
python3 /mnt/c/release/candidate/payload/scripts/manage_release_candidate.py rehearse --candidate /mnt/c/release/candidate --workspace /tmp/sdd-linux-rehearsal --platform-id linux-wsl2 --evidence-level portability-smoke --mcp-status explicitly-unavailable --output /mnt/c/release/host-evidence/linux-wsl2.yaml
```

When MCP is provisioned, replace the last status with `provisioned` and add
`--mcp-evidence-ref <approved-non-secret-reference>`. Never put a token,
credential, endpoint with userinfo, or private output in that reference.

## Evaluate Evidence

The host root must contain exactly `windows.yaml` and `linux-wsl2.yaml`. The raw
artifact root is separate and must contain the exact logical roots selected by
`process/release-certification-selection.yaml`.

```powershell
python C:\release\candidate\payload\scripts\manage_release_candidate.py accept --candidate C:\release\candidate --manifest C:\release\candidate\release-manifest.yaml --host-evidence-root C:\release\host-evidence --raw-artifact-root C:\release\raw-artifacts
```

```bash
python3 /mnt/c/release/candidate/payload/scripts/manage_release_candidate.py accept --candidate /mnt/c/release/candidate --manifest /mnt/c/release/candidate/release-manifest.yaml --host-evidence-root /mnt/c/release/host-evidence --raw-artifact-root /mnt/c/release/raw-artifacts
```

The validator owns the 30-day freshness window and ignores evidence-provided
expiry claims. A complete packet returns `evidence-complete` and
`human_acceptance_required: true`; only the human owner may accept or reject
transfer readiness.
