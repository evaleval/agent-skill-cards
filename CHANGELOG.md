# Changelog

All notable changes to the schema and the pipeline. The schema version (currently v1.2) changes when what a card can say changes; the package version is in `src/skillcard/__init__.py`.

## Unreleased
- Added CONTRIBUTING, AGENTS, PR and issue templates, and CI.
- Renamed the card sections to Overview, Requirements, Permissions, Checks and Evaluations, Ownership and Version. The keys in the card JSON and the existing cards keep the old names for now.
- Added a first version of every phase of the pipeline.
  - Identification reads a skill from a repository with a path and a commit, as the commit stores the files. `snapshot.json` gained `skill_id`, `original_skill_name`, `hash_scheme` and `known`, and the kind of every file. The hash rule is unchanged and is now named `skill-tree-v1`.
  - Collection stores what GitHub and skills.sh say about the skill and reports that are handed over, and logs every item in `sources/log.json`.
  - Composition writes the card in one call to a model and writes `evidence.json`. Without a model key the pipeline still runs.
  - Validation checks the card against the card template and checks the files that `evidence.json` names.
- Added `schema/card-template.json`, which writes down the shape of `card.json` as the cards in `cards/` have it. Its word lists are provisional until issue #10 is decided.
- A card written by the pipeline has the shape of the cards in `cards/`. The stamp of the card holds the schema, the date and one sentence on how the card was made.
