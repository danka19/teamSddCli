# NIS and teamSDD Presentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a verified 15-slide editable PowerPoint presentation showing NIS as the corporate-process foundation and teamSDD as its engineering development, with concise Russian speaker notes and a separate critical report outside the deck.

**Architecture:** Use `outputs/team-sdd-project-overview.pptx` as the only source-slide template. Inspect and duplicate inherited slides into a starter deck, edit mapped inherited elements with `@oai/artifact-tool`, add speaker notes through the presentation API, and export the result to `outputs/nis-vs-team-sdd-engineering-evolution.pptx`.

**Tech Stack:** PowerPoint PPTX, JavaScript ES modules, `@oai/artifact-tool`, bundled presentation template-following scripts, bundled Python rendering/QA utilities, Git.

## Global Constraints

- Visible slide content and speaker notes are written in Russian.
- The deck contains 15 slides following the approved narrative in `docs/superpowers/specs/2026-07-14-nis-team-sdd-presentation-design.md`.
- NIS is framed as the foundation; teamSDD is framed as engineering formalization and development.
- Weaknesses, rejected NIS elements, and direct criticism stay outside the deck and are reported only to the user.
- Every slide contains 2–4 short speaker-note sentences that expand the thought without repeating visible copy.
- Accepted direction must be distinguished from implemented behavior.
- Human authority, deterministic verification, the permanent AI-disabled fallback, and safe-parallel execution boundaries must remain explicit.
- Preserve the source template’s typography, palette, spacing, page markers, and visual chrome.
- Final QA must inspect every rendered slide at full size and must not accept unintended overlap, clipping, wrapping, or empty inherited placeholders.

---

### Task 1: Build the source-slide and content map

**Files:**
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/template-audit.txt`
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/template-frame-map.json`
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/deviation-log.txt`
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/source-notes.txt`

**Interfaces:**
- Consumes: the approved presentation design, the 17-slide source deck inventory, `docs/audits/NIS_V1_6_PRESENTATION_COMPARISON_REPORT_2026-07-13.md`, and active NIS OpenSpec artifacts.
- Produces: a validated `template-frame-map.json` containing exactly 15 `outputSlides`, each mapped to one inherited source slide with explicit inherited `editTargets`.

- [ ] **Step 1: Inspect the complete canonical source deck**

Run:

```powershell
$env:HOME='C:\Users\danoc'
$env:PATH='C:\Program Files\Git\usr\bin;'+$env:PATH
node "$env:USERPROFILE\.codex\plugins\cache\openai-primary-runtime\presentations\26.709.11516\skills\presentations\template_following_scripts\inspect_template_deck.mjs" --workspace "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp" --pptx "C:\Users\danoc\Documents\projects\teamSsdCli\outputs\team-sdd-project-overview.pptx"
```

Expected: exit code `0`, manifest reports `slideCount: 17`, and 17 source-slide PNGs plus 17 layout JSON files exist.

- [ ] **Step 2: Write the exact narrative-to-frame mapping**

Create the four task files. The frame map must use source slides `1, 3, 4, 10, 8, 7, 6, 7, 6, 13, 15, 14, 15, 16, 17` in output order and must name each rewritten, replaced, or deleted inherited element by stable source element ID.

- [ ] **Step 3: Validate the frame map**

Run:

```powershell
node "$env:USERPROFILE\.codex\plugins\cache\openai-primary-runtime\presentations\26.709.11516\skills\presentations\template_following_scripts\validate_template_plan.mjs" --workspace "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp" --map "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-frame-map.json"
```

Expected: exit code `0`; all 15 output slides and all inherited edit targets resolve.

### Task 2: Create and author the inherited presentation

**Files:**
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/template-starter.pptx`
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/build-deck.mjs`
- Create: `outputs/nis-vs-team-sdd-engineering-evolution.pptx`

**Interfaces:**
- Consumes: the validated frame map and inherited `template-starter.pptx`.
- Produces: an editable 15-slide PPTX whose visible text, notes, and implementation-status statements match the approved design.

- [ ] **Step 1: Prepare the inherited starter deck**

Run:

```powershell
node "$env:USERPROFILE\.codex\plugins\cache\openai-primary-runtime\presentations\26.709.11516\skills\presentations\template_following_scripts\prepare_template_starter_deck.mjs" --workspace "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp" --pptx "C:\Users\danoc\Documents\projects\teamSsdCli\outputs\team-sdd-project-overview.pptx" --map "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-frame-map.json" --out "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-starter.pptx" --preview-dir "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-starter-preview" --layout-dir "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-starter-layout" --contact-sheet "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-starter-contact-sheet.png"
```

Expected: exit code `0`; starter deck contains exactly 15 inherited slides.

- [ ] **Step 2: Initialize the artifact-tool workspace**

Run:

```powershell
node "$env:USERPROFILE\.codex\plugins\cache\openai-primary-runtime\presentations\26.709.11516\skills\presentations\container_tools\setup_artifact_tool_workspace.mjs" --workspace "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp"
```

Expected: `node_modules/@oai/artifact-tool` resolves inside the scratch workspace.

- [ ] **Step 3: Implement inherited-element edits and notes**

Create `build-deck.mjs` with four focused operations:

```javascript
import fs from "node:fs/promises";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const presentation = await PresentationFile.importPptx(
  await FileBlob.load("C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/template-starter.pptx"),
);

// Resolve only inherited targets declared in template-frame-map.json.
// Rewrite the 15 approved slide narratives without changing source typography.
// Assign 2–4 concise Russian speaker-note sentences to every slide.
// Export slide renders/layouts and the final editable PPTX.

const pptx = await PresentationFile.exportPptx(presentation);
await fs.mkdir("C:/Users/danoc/Documents/projects/teamSsdCli/outputs", { recursive: true });
await pptx.save("C:/Users/danoc/Documents/projects/teamSsdCli/outputs/nis-vs-team-sdd-engineering-evolution.pptx");
```

The completed module must contain the exact approved Russian visible copy and notes for all 15 slides; it must not create parallel replacement layouts over inherited slides.

- [ ] **Step 4: Run the deck build**

Run:

```powershell
node "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\build-deck.mjs"
```

Expected: exit code `0`; final PPTX exists and contains 15 slides.

### Task 3: Verify content, notes, and visual fidelity

**Files:**
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/qa/content-check.txt`
- Create: `C:/Users/danoc/AppData/Local/Temp/codex-presentations/019f5ef7-618d-7d72-bf1f-b9649a27d5d3/nis-team-sdd/tmp/qa/slide-review.txt`

**Interfaces:**
- Consumes: final PPTX, final renders/layouts, approved design, and current NIS comparison report.
- Produces: evidence that slide count, notes, copy, status boundaries, template fidelity, and canvas/layout constraints were checked.

- [ ] **Step 1: Run structural and canvas checks**

Run:

```powershell
python "$env:USERPROFILE\.codex\plugins\cache\openai-primary-runtime\presentations\26.709.11516\skills\presentations\container_tools\slides_test.py" "C:\Users\danoc\Documents\projects\teamSsdCli\outputs\nis-vs-team-sdd-engineering-evolution.pptx"
```

Expected: exit code `0`; no slide content exceeds the canvas.

- [ ] **Step 2: Run template-fidelity validation**

Run:

```powershell
node "$env:USERPROFILE\.codex\plugins\cache\openai-primary-runtime\presentations\26.709.11516\skills\presentations\template_following_scripts\check_template_fidelity.mjs" --workspace "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp" --starter-pptx "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-starter.pptx" --final-pptx "C:\Users\danoc\Documents\projects\teamSsdCli\outputs\nis-vs-team-sdd-engineering-evolution.pptx" --map "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-frame-map.json" --starter-layout-dir "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\template-starter-layout" --final-layout-dir "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp\layout\final" --edit-dir "C:\Users\danoc\AppData\Local\Temp\codex-presentations\019f5ef7-618d-7d72-bf1f-b9649a27d5d3\nis-team-sdd\tmp"
```

Expected: exit code `0`; no unauthorized template divergence or unresolved inherited placeholder remains.

- [ ] **Step 3: Inspect every final slide at full size**

Record one pass/fail line for slides 1–15 covering hierarchy, wrapping, clipping, unintended overlap, icon alignment, footer/page marker, and claim accuracy. Fix and rebuild any failed slide, then repeat the full 15-slide review.

- [ ] **Step 4: Verify notes and implementation status**

Inspect notes from the exported PPTX and verify exactly 15 slides have notes, each with 2–4 concise Russian sentences. Confirm slide 14 explicitly separates accepted direction from current implementation.

### Task 4: Final repository state and delivery report

**Files:**
- Modify only if needed: `docs/superpowers/plans/2026-07-14-nis-team-sdd-presentation.md`
- Deliver: `outputs/nis-vs-team-sdd-engineering-evolution.pptx`

**Interfaces:**
- Consumes: successful QA evidence and final PPTX.
- Produces: an intentional Git commit plus a Russian report containing the excluded NIS critique and the next recommended human action.

- [ ] **Step 1: Review repository state**

Run:

```powershell
git status --short --branch
git diff --check
```

Expected: no unintended tracked changes; pre-existing untracked `.claude/` and `.vite/` remain untouched.

- [ ] **Step 2: Commit intentional tracked changes**

Run:

```powershell
git add docs/superpowers/plans/2026-07-14-nis-team-sdd-presentation.md outputs/nis-vs-team-sdd-engineering-evolution.pptx
git commit -m "docs: add NIS engineering evolution deck"
```

If `outputs/` is ignored, add the final PPTX explicitly with `git add -f` so the requested deliverable is preserved in the session commit.

- [ ] **Step 3: Deliver the final report**

Report the final deck path, slide and notes counts, verification commands and results, deliberate deck exclusions, NIS weaknesses and non-applicable elements, commit hash, and the single most useful next step: review the deck in PowerPoint and rehearse the speaker notes against the intended meeting duration.
