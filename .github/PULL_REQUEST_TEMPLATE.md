<!-- Thanks for contributing! Delete sections that don't apply. -->

## What / why
<!-- What does this change do? For a card: which skill and which commit? -->

## Kind of change
- [ ] Card
- [ ] Schema / filling guide
- [ ] Pipeline
- [ ] Docs

## Review lane
<!-- See CONTRIBUTING.md, "How your PR gets reviewed". A maintainer may disagree. -->
- [ ] **Fast** — no conflicts, scoped to one card / one phase / tests / docs, verified by me, under ~500 hand-written lines
- [ ] **Needs a human** — schema or guide change, changed file formats or hash rule, cross-phase, or changes the output for the same input

Design agreed in: <!-- link the issue, required for schema and structural changes -->

## Checklist
- [ ] `pytest` is green and `ruff check .` is clean
- [ ] Tests added for new behaviour, and they run offline
- [ ] Pipeline rules kept: a phase only adds its own files, validation does not change the card, skill files are never run
- [ ] No paths from my machine in any file
- [ ] My commits are signed (Verified on GitHub)

### Cards only
- [ ] Generated with the pipeline, validation passed (`validation.json`)
- [ ] `.json` and `.md` committed together
- [ ] Values spot-checked against the skill's files
- [ ] I am / am not the author of the skill, and a human has / has not reviewed this card

## Decisions
<!-- Non-obvious choices you made, and what you chose instead. "None" is fine. -->
