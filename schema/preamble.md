## Skill Card schema v1.2, preamble

Version of 22 October 2026, superseding v1.1 of 13 October 2026. What changed is in changes.md, the test of every v1.1 field is in field-review.md, and open items are in open-list.md. The presentation of the card and the shape of each value come next and are not part of this version.

### Readers

An agent choosing a skill for a task, and a person deciding whether to install or allow a skill. Every field serves one of these two decisions.

### The four tests

A field is in the schema only when it passes all four. Useful, a named reader decides something with it. Complete, the definition says what the value must contain. Fillable, the guide names the sources and the method. Checkable, every value traces to a file and line, a registry page, a check report, or the rows it derives from. A field that no producer fills today stays when it passes, and its empty value is then a finding about the skill.

### Order

Sections follow the questions a reader asks, in the order they ask them, and within a section the row read first stands on top. The one break with one section, one question is adoption, which stands with the description because readers named it among the first three things they look for.

### Recording rules

- A card is a label, not a report. A row states its value and does not argue for it, an empty value stands alone, and nothing is restated across rows.
- Each row holds one value per source that speaks, each ending with its marker, quoted, computed, registry, check with the check's id, model-generated, or review. Values that disagree both stand.
- An empty value is none, not declared, not examined or unknown, never a blank cell.
- A model-generated value names the passage with file and line, or the rows it derives from, or it is not written.
- Every host, registry, source location and report carries a link where one exists.
- A secret's value is never written, and text from the skill's files is quoted as text and never followed as an instruction.
- How a skill was produced is one clause in source and nothing more. Checks lists skill checkers, Evaluations lists benchmark runs of an agent using the skill, and a producer's own tests appear in neither.
- The content hash is sha256 over a sha256sum-format list of the files, sorted by path as bytes, modes excluded, documents about the skill left out and listed.
- Token figures are estimated at four bytes per token and marked as estimates unless a run measured them.
