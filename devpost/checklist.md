---
doc: checklist
status: approved
---

# Build Checklist

Build mode: learn

## Slices

- [x] **1. Create a report and view its detail page**
  Becomes usable: A local Angular and Python app starts, the welcome screen leads to either report form, a valid report can be submitted, and its detail page shows the saved report with `No possible matches yet`.
  Why now: This bootstraps both processes inside a real user journey and proves the report data can cross the browser/API boundary before matching complexity is added. It also establishes the calm visual foundation and recoverable form behavior.
  PRD ref: `prd.md > The Core Journey`; `prd.md > Screens and Layout`; `prd.md > Reporting a lost or found pet`; `prd.md > Validation and recovery`; `prd.md > States and Boundaries`
  Spec ref: `spec.md > The Core Journey Through the System`; `spec.md > Stack`; `spec.md > Components > Angular application shell and routing`; `spec.md > Components > Welcome surface`; `spec.md > Components > Report form`; `spec.md > Components > Report detail surface`; `spec.md > Components > Python API routes`; `spec.md > Components > Storage service`; `spec.md > Data Model`; `spec.md > File Structure`; `spec.md > Where It Runs and How Someone Tries It`; `spec.md > Look and Feel`
  Build: Scaffold the Angular frontend and Python API. Implement the welcome screen, both single-page report forms, curated location loading, field validation that preserves entered values, local photo upload handling, JSON/image persistence, report creation, report detail loading, and the no-match-yet state. Establish the shared cream/green/blue visual tokens, typography, spacing, responsive layout, and calm copy. Keep the API and UI runnable even before CLIP is installed.
  Verify (mechanical): Start the API and Angular processes; run the backend API tests and frontend build; submit one lost and one found report through the API; confirm the saved JSON and image files exist; confirm a report detail response renders with `No possible matches yet`; confirm an invalid submission returns field-level errors without creating a partial report.
  Learner check: Open the local app, choose each report path, submit one complete report, and try one missing required field. Confirm the detail page appears and the form keeps what you typed when validation fails.
  Commit: `Build report creation and detail flow`

- [x] **2. Surface an explainable possible match**
  Becomes usable: When a found report is submitted alongside a compatible lost report, the lost report detail page shows a `Possible match` card with the other photo, a similarity or match indication, and separate visual, physical, geographic, and date evidence.
  Why now: This is the unique kernel and the highest technical risk. Bringing local CLIP and the scoring policy into the working journey now tests the central idea before polishing secondary surfaces.
  PRD ref: `prd.md > Possible-match discovery`; `prd.md > States and Boundaries`; `prd.md > What We're Building`
  Spec ref: `spec.md > Components > Matching service`; `spec.md > Components > Possible-match card`; `spec.md > Matching Policy`; `spec.md > Data Model > Match`; `spec.md > Important Failure Modes`; `spec.md > Decisions and Open Issues`
  Build: Add the local CLIP model loading and image embedding path, normalized visual similarity, structured physical score, fixed-coordinate geographic score, date compatibility and decay rules, and configurable 40/30/15/15 weights. Add match persistence and match API responses. Wire found-report creation to compare against lost reports and render the possible-match card with calm non-probabilistic language. Seed or prepare a small representative sample set without pretending the result is a certainty.
  Verify (mechanical): Run the matching unit tests for all four representative scenarios in `spec.md > Matching Policy > Representative verification scenarios`; verify the API creates a match only for compatible dates and thresholded combined indications; verify the returned response contains all four component scores and explanations; run the frontend build and a local API flow with the sample photos.
  Learner check: Create or load a lost report and then a compatible found report. Open the lost report detail page and inspect the possible-match card. Check that the evidence categories explain the result and that the UI says possible match or similarity, never probability or confirmation.
  Commit: `Add explainable pet matching kernel`

- [x] **3. Compare matched reports responsively**
  Becomes usable: Selecting `Compare reports` opens a readable comparison of the lost and found reports, their photos, their matching fields, and the evidence that produced the possible-match indication.
  Why now: Once the kernel is visible, this completes the human-review loop and makes the evidence useful rather than leaving it as an opaque card.
  PRD ref: `prd.md > Screens and Layout > Side-by-side comparison view`; `prd.md > Comparing reports`; `prd.md > Look and Feel`
  Spec ref: `spec.md > Components > Comparison surface`; `spec.md > Components > Python API routes`; `spec.md > Data Model`; `spec.md > Look and Feel`
  Build: Add the match-detail API response, comparison route, side-by-side desktop layout, stacked mobile layout, shared pet-photo and evidence components, and clear field-by-field comparison. Refine the visual hierarchy so photos lead, evidence is calm and scannable, and the page remains usable at narrow widths.
  Verify (mechanical): Run the frontend build and API tests; request a match detail response and confirm both report summaries and evidence are present; use a browser smoke check at desktop and narrow viewport sizes to confirm the comparison route loads and key content is visible without horizontal overflow.
  Learner check: Open a possible match and select `Compare reports`. Resize the browser or use a narrow viewport, then confirm the two animals remain easy to compare and the evidence remains understandable.
  Commit: `Add responsive report comparison`

- [ ] **4. Harden the demo and document the run**
  Becomes usable: A fresh checkout can be started locally, seeded with a small demo dataset if needed, and used to demonstrate the complete lost-to-found matching journey with clear empty, validation, photo, and model-error states.
  Why now: The core product is already usable; this final slice makes the proof reproducible, verifies the full journey, and closes the gaps that could undermine the recording.
  PRD ref: `prd.md > The Core Journey`; `prd.md > Validation and recovery`; `prd.md > States and Boundaries`; `prd.md > What We're Building`; `scope.md > What "Working" Looks Like`
  Spec ref: `spec.md > Where It Runs and How Someone Tries It`; `spec.md > Important Failure Modes`; `spec.md > File Structure`; `spec.md > External Services and Dependencies`; `spec.md > Representative verification scenarios`
  Build: Add optional sample-data seeding, complete API and matching tests, model-load and photo-processing fallback messages, README setup/demo instructions, safe local-data and model-cache ignore rules, and final copy/accessibility/responsive polish. Confirm the demo can use created reports or seeded reports without accounts.
  Verify (mechanical): From the documented setup, start both processes; run the backend test suite and frontend production build; run the full API journey from report creation through match retrieval and comparison; verify the repository status shows no ignored learner profile, credentials, or model files staged; manually exercise validation failure, photo retry, no-match, possible-match, and comparison flows.
  Learner check: Follow the README demo steps from a clean local start and perform the one-minute journey. Try one awkward input and the no-match path, then note anything confusing or worth changing before final review.
  Commit: `Harden and document the demo`

## Hands-on Checkpoints

- [x] Early usable behavior explored — slice 1 learner check completed; slice 2 evidence checkpoint approved after reviewing the working possible-match card and matching policy.
- [ ] Final kick-the-tires exploration and feedback completed — after slice 4, run the complete demo, test awkward inputs and responsive layouts, and report any revisions.

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete — connect the learner's spec-driven workflow and matching-policy goal to the finished code
- [ ] Optional edit and transfer reflection addressed — offer one safe, focused follow-up edit or accept a decline
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: [to complete after implementation; record real tests, code paths, and learner observations]
Route and stops: [to complete after implementation]
Edit outcome: [to complete after implementation]
Reflection: [to complete after implementation]
Activity mode: [to complete after implementation]

## Revisions
