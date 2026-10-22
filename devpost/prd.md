---
doc: prd
status: approved
---

# Lost-to-Found Pet Matching for Coquimbo - Product Requirements

A calm, community-oriented responsive web experience for people in Coquimbo who want to report a lost or found pet and discover explainable possible matches.
Source: `scope.md > The Unique Kernel`, `scope.md > Who It's For`.

## The Core Journey

1. A person opens the platform and immediately sees a plain-language message explaining that it helps connect lost pets with found pets.
2. The person chooses one of two clear actions: `I lost a pet` or `I found a pet`. `I lost a pet` may have slightly more visual emphasis because the lost-pet owner is the primary user, but both paths remain equally accessible.
3. The person completes a short single-page report form organized into Photo, About the pet, and Where and when.
4. The form preserves the person's entries when required information is missing or a photo cannot be uploaded or used. It highlights only the affected field and gives a friendly, specific recovery message.
5. After successful submission, the person sees a simple confirmation that the report was created and is taken to the report detail page.
6. The report detail page shows the submitted report information. If no compatible report exists, it shows `No possible matches yet` and explains that a compatible future found-pet report may appear there.
7. When a found-pet report is created, the platform automatically compares it with existing lost-pet reports for the POC. If the reports are compatible, the relevant lost-pet report shows a prominent `Possible match` card.
8. The possible-match card shows the other pet's photo, a non-definitive similarity or match indication, and a calm explanation of the main evidence: visual similarities, compatible physical characteristics, geographic proximity, and compatible dates.
9. The person selects `Compare reports` and opens a side-by-side view of the lost and found reports, including their photos, details, and matching evidence.
10. The person uses the evidence to decide whether the animals could be the same. The product never presents the suggestion as confirmation.

Source: `scope.md > The Core Loop`, `scope.md > What "Working" Looks Like`.

## Screens and Layout

### Welcome screen
A focused first screen with:

- A short message explaining that the platform connects lost pets with found pets.
- Two prominent actions: `I lost a pet` and `I found a pet`.
- Slightly stronger visual emphasis for `I lost a pet`, without hiding or weakening the found-pet path.
- No dashboard and no AI-first presentation.

### Lost-pet report form
A single-page form with clear visual sections:

1. **Photo** — upload the clearest available photo of the lost pet.
2. **About the pet** — required species (dog, cat, or other), main color, and distinctive markings or physical characteristics; optional name, sex, approximate size, and free-text description.
3. **Where and when** — required location where the pet was lost and date it was lost.

Required POC matching information is the photo, species, color, distinctive characteristics, location, and date. The optional fields provide useful context without making the form overwhelming.

### Found-pet report form
The same single-page, three-section structure as the lost-pet form so reports remain easy to compare:

1. **Photo** — upload the clearest available photo of the found pet.
2. **About the pet** — required species (dog, cat, or other), main color, and visible distinctive markings or physical characteristics; optional approximate size and free-text description.
3. **Where and when** — required location where the pet was found and date it was found.

The found-pet form does not ask for a name because a finder usually will not know it. It focuses on information the finder can actually observe.

### Report detail page
The report detail page contains:

- The report type and submitted pet information.
- The primary photo and relevant characteristics.
- Location and date.
- A simple success confirmation immediately after submission, before or as the detail page is shown.
- A possible-matches area.

With no compatible report, the area shows `No possible matches yet` and explains that a future compatible found report can appear there.

With a compatible report, the area shows a prominent possible-match card containing the found pet's photo, similarity or match indication, evidence summary, and `Compare reports` action.

### Side-by-side comparison view
A focused comparison surface showing the lost and found reports next to each other where the responsive layout allows, or in a clear stacked comparison on smaller screens. It includes:

- Both pet photos.
- Comparable report details such as species, color, markings, location, and date.
- The evidence behind the possible match, grouped into visual, physical, geographic, and date signals.
- Consistent language that this is a possible match, not a confirmation.

Source: `scope.md > The POC Boundary`, `scope.md > Explicitly Cut`.

## Look and Feel

The interface should feel trustworthy, humane, calm, and community-oriented rather than like an AI dashboard.

- Warm off-white or cream background.
- Muted botanical green as the main accent and soft blue as a secondary accent.
- A highly readable, friendly sans-serif typeface with gentle rounded details, without feeling childish.
- Real pet photos as the visual focus rather than generic animal illustrations.
- Softly rounded cards, generous spacing, and clear hierarchy.
- Simple, rounded, consistent icons.
- A subtle coastal and natural feeling that can connect to Coquimbo without becoming a tourism website.
- Possible-match cards should feel reassuring and hopeful; evidence should be clear but calm.
- Avoid neon gradients, excessive glassmorphism, robot imagery, glowing effects, and generic technical-dashboard styling.

Source: `scope.md > Inspiration & Identity`.

## Features and Behavior

### Reporting a lost or found pet

A person can select a report type from the welcome screen and submit a short report with the required matching information and optional context appropriate to that report type.

- The lost-pet form includes an optional name and sex; the found-pet form does not include a name field.
- The form remains a single page rather than a multi-step wizard.
- The form makes the three sections visually distinct without making the user navigate away from the page.
- Required fields are the photo, species, main color, distinctive characteristics, location, and date.
- Optional fields can be left blank without blocking submission.

Acceptance criteria:

- [ ] Selecting either welcome action opens the corresponding report form.
- [ ] A complete report can be submitted with the required matching information.
- [ ] Lost-pet and found-pet forms use the same section structure but contain only fields appropriate to what each reporter knows.
- [ ] A successful submission produces a clear confirmation and opens the report detail page.

Source: `scope.md > The Core Loop`, `scope.md > The POC Boundary`.

### Validation and recovery

The product validates required fields when the user submits a report.

- Existing entries remain intact when validation fails.
- Only missing or invalid fields are highlighted.
- Each validation message is friendly and specific, such as `Please add the date your pet was lost.`
- If a photo cannot be uploaded or used, the user sees a clear non-technical explanation and an easy way to try again.
- Photo errors do not clear the other form data.
- The user never has to restart the form because of validation or photo errors.

Acceptance criteria:

- [ ] Submitting with a missing required field keeps all entered values and identifies the affected field.
- [ ] The message explains what needs to be added or corrected.
- [ ] A failed photo upload or unusable photo offers a retry path while preserving the rest of the form.

Source: `scope.md > The Core Loop`; clarified during PRD interview.

### Possible-match discovery

When a new found-pet report is created in the POC, the platform compares it with existing lost-pet reports and surfaces a possible match when the evidence is compatible.

The suggestion must communicate possibility, not certainty. It should explain the evidence in human-readable terms, including:

- Visual similarities between the photos.
- Compatible species, color, markings, or other physical characteristics.
- Geographic proximity.
- Compatible dates, including the relationship between the lost and found dates.

The indication is a similarity or match indication, not a calibrated statistical confidence score.

Acceptance criteria:

- [ ] Creating or selecting a compatible found report causes a possible-match card to appear on the relevant lost report.
- [ ] The card includes the other pet's photo and a similarity or match indication.
- [ ] The card explains the relevant visual, physical, geographic, and date evidence.
- [ ] The interface consistently says `Possible match` or equivalent and never confirms that the animals are the same.
- [ ] When no compatible report exists, the detail page shows `No possible matches yet` and explains that a future report may appear.

Source: `scope.md > The Unique Kernel`, `scope.md > What "Working" Looks Like`.

### Comparing reports

A person can open a suggested match and inspect the lost and found reports side by side. The comparison makes it possible to review the photos, matching fields, and evidence without relying on an opaque result.

Acceptance criteria:

- [ ] Selecting `Compare reports` opens the comparison view.
- [ ] Both reports' photos and relevant details are visible.
- [ ] The matching evidence is visible alongside the reports.
- [ ] The comparison remains understandable on a small responsive screen.

Source: `scope.md > The POC Boundary`.

### Report resolution and removal

Either reporter can mark a lost- or found-pet report as resolved when the pet has been reunited or the case is otherwise closed. A resolved report stays available for review with its photo, but it is removed from possible-match results and cannot create new matches. Permanent deletion is a separate, explicitly confirmed action that removes the report, its photo, and its related match records.

The POC has no accounts or report ownership. Anyone with access to the local demo can use these actions; they are not owner authorization for a public deployment.

Acceptance criteria:

- [ ] Lost and found reports can both be marked resolved.
- [ ] A resolved report remains viewable with its photo but is excluded from new and existing possible matches.
- [ ] Permanently deleting a report requires confirmation and removes its photo and related matches without deleting other reports or images.

Source: `scope.md > The POC Boundary`; clarified during implementation.

## States and Boundaries

- **First use** — The welcome screen explains the purpose and presents the two report paths without requiring an account.
- **Form in progress** — The user can fill the single-page form; optional fields may remain empty.
- **Validation error** — Missing or invalid fields are highlighted with specific guidance, while all entered data remains.
- **Photo error** — A non-technical message explains that the photo could not be uploaded or used, offers retry, and preserves the rest of the form.
- **Submission success** — A simple confirmation appears and the report detail page opens.
- **No possible matches** — The report remains visible with `No possible matches yet` and a future-looking explanation.
- **Possible match** — A prominent, calm card presents the other photo, similarity or match indication, and evidence summary.
- **Comparison** — Both reports and the evidence are available for human inspection.
- **Resolved report** — The report and photo remain viewable, but the case is removed from possible matches.
- **Delete confirmation** — The user confirms permanent removal of the report, its image, and related match records.
- **No account or production notification state** — The POC does not require identity, contact, or notification workflows.
- **Sample data** — The demo may create reports during the flow or use already available sample data; it must not require account setup or a complete publishing workflow to demonstrate the match.

## Product Decisions

- The lost-pet owner is the primary user, while found-pet reporters are the second participant — this reflects the problem the product is intended to relieve.
- The welcome screen leads with purpose and report choice, not AI or a dashboard — people should understand what to do immediately.
- Both report forms use the same three-section structure — this keeps the POC simple and makes reports easy to compare.
- The lost-pet form may ask for a name, but the found-pet form does not — a finder usually cannot know the pet's name.
- The forms are single-page rather than multi-step — someone worried about a missing pet should be able to submit quickly.
- Match suggestions explain their evidence and remain non-definitive — the person makes the final judgment.
- Resolving a report preserves it for review but removes it from matching; permanent deletion is separate and removes associated local data.
- Lifecycle actions are available to anyone with access in this local POC because account ownership is out of scope.
- The POC uses a similarity or match indication rather than a confidence score — the result is not calibrated statistical certainty.
- Real accounts, deployment, production notifications, and lifecycle follow-up are outside the POC — the one-minute demo should prove the matching experience without unnecessary workflow infrastructure.
- The interface uses a warm, calm, natural community-service direction — the technology should help quietly in the background.

## What We're Building

A responsive web POC for Coquimbo that:

- Explains its purpose and offers lost-pet and found-pet entry paths.
- Accepts the required matching information and relevant optional context through short single-page forms.
- Validates inputs with calm, recoverable errors.
- Shows submission confirmation and a report detail page.
- Automatically compares a new found report with lost reports in the POC's sample set.
- Surfaces explainable possible-match cards or a clear no-match-yet state.
- Provides a responsive side-by-side or stacked comparison of matched reports.

## Deferred From the POC

- Accounts, identity, and saved personal report collections are deferred because the demo can use sample data without user management.
- Real contact and notification delivery are deferred because production communication channels are not needed to demonstrate matching.
- Automated resolution follow-ups and archiving are deferred; reporters can manually resolve or delete a case in the POC.
- Broad geographic coverage is deferred because the first proof is focused on Coquimbo.

## Possible Later Enhancements

- Notify a report owner when a new possible match appears.
- Ask reporters whether a case has been resolved and archive or update stale reports.
- Add contact workflows, moderation, privacy controls, and abuse prevention.
- Expand the service beyond the Coquimbo region.
- Improve matching with production-scale image and machine-learning infrastructure.

## Non-Goals

- The POC will not confirm that two reports refer to the same animal.
- The POC will not present a calibrated probability or claim statistical certainty.
- The POC will not be a chatbot or AI conversation product.
- The POC will not require accounts, native mobile apps, deployment, or real notification delivery.
- The POC will not attempt to reproduce a complete social network or replace local community channels.

## Open Questions

- **Exact matching method and evidence calculation** — must be decided in `4-spec`; it is a technical choice, not a product gap, as long as the visible evidence remains understandable and non-definitive.
- **Exact sample reports and photos** — can be chosen during `4-spec` or build preparation; the product behavior does not depend on specific animals.
- **Persistence between sessions** — can wait for `4-spec`; the POC may use a limited sample-data experience as long as the demo journey remains intact.
