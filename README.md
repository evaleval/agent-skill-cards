# Agent Skill Cards

A skill is a package of instructions that an agent can load to do a specific task. What a skill needs, what it can reach and whether it does what it says is mostly not written down anywhere a reader could check, and a person installing a skill or an agent choosing one needs documentation that answers these questions before the skill runs.

Agent Skill Cards is a working group that develops documentation cards for agent skills, so that people and agents can see what is known about a skill before they use it. The group runs openly in [EvalEval](https://github.com/evaleval), an open research community on the evaluation of AI systems.

This repository holds the schema of the card, a set of cards and the code that generates them.

## What is in this repository

| Folder | What it holds |
|---|---|
| `schema/` | The Skill Card schema in version 1.2, with 24 fields in seven sections. `skill-card-v1.2.md` gives the description, the structure and an example for every field. `preamble.md` gives the rules that all fields share. `guides/` says how each section is filled. |
| `cards/` | Skill Cards for real skills. The last section of every card says how it was made. |
| `src/skillcard/` | The pipeline that generates a card from the files of a skill. |
| `tests/` | The tests of the pipeline and a small example skill. |

## Workstreams

| Workstream | What it works on | Where in this repository |
|---|---|---|
| Schema | Which fields a card has, what each field means and how it is filled. | `schema/` |
| Generation | The pipeline that generates the cards automatically. | `src/skillcard/` |
| Presentation | How a card is shown, since an agent, a technical user and a person interested in policy each look for different things in a card. | `src/skillcard/render.py` |

The generation work is split along the four phases of the pipeline.

## The pipeline

The pipeline takes the folder of one skill and writes a card for it. It runs in four phases. Each phase has one file in `src/skillcard/`, reads the run folder and adds its own output to it.

| Phase | File | What it is for | What it does today |
|---|---|---|---|
| Skill identification | `identify.py` | Pins down the exact files of one skill version and computes their hash. | Works for a local folder. |
| Source collection | `collect.py` | Gathers what is known about the skill outside its files, such as registry entries and the reports of skill checkers. | Collects nothing yet. |
| Composition | `compose.py` | Fills the fields of the card. | Fills the fields that can be computed or quoted from the files. Every other field reads "not examined". |
| Validation | `validate.py` | Checks the card against the files and the collected sources. | Recomputes the hash, compares the file list with the files and looks for blank values. |

The code is a skeleton. It runs from end to end on a local skill folder, so that every phase has something to run and to extend, and most of the card is still empty.

The pipeline reads the files of a skill and never runs them. Text in a skill is treated as data and never as an instruction.

## Running it

The pipeline needs Python 3.11 or newer. These commands install it, generate the card for the example skill and run the tests.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

skillcard tests/fixtures/hello-skill
pytest
```

A run writes one folder under `runs/`, named after the skill and the first characters of its hash.

```
runs/hello-skill-d2b31cc7/
  snapshot.json     the hash, the source and the file list
  files/            a frozen copy of the files of the skill
  sources/          what was collected about the skill
  card.json         the card as data
  validation.json   the result of the checks
  card.md           the card as text
```

## Status

This is early work. The schema is in version 1.2 and still changes as the cards get used. The cards in this repository are examples and were not reviewed by the authors of the skills they describe.

## Taking part

The working group meets in the #agent-skill-cards channel of the EvalEval Slack.

## License

MIT, see `LICENSE`.
