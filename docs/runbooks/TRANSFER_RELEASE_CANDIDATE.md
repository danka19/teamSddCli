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
