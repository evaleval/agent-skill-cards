# Contributing to Agent Skill Cards

Thanks for contributing! This repository holds the Skill Card schema (`schema/`), the cards (`cards/`) and the start of the pipeline that generates them (`src/skillcard/`). For what a Skill Card is and how the pipeline works, start with the [README](README.md).

> **Using an AI coding agent?** See [AGENTS.md](AGENTS.md). The rules below apply to agent-authored PRs too.

## Development setup

```bash
git clone https://github.com/<org>/agent-skill-cards.git
cd agent-skill-cards
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

pytest            # tests
ruff check .      # lint
black --check .   # formatting (line length 100)
```

Or with [uv](https://docs.astral.sh/uv/), which creates the virtual environment for you:

```bash
uv venv --python 3.11            # creates .venv (any Python 3.11 or later)
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

pytest
ruff check .
black --check .
```

Without activating the environment, prefix the commands with `uv run`, for example `uv run pytest`. Note that `uv run` only sees the dev tools if they are installed in the environment, so run the `uv pip install` step first.

Python 3.11 or later is required.

### Pre-commit hooks

[`.pre-commit-config.yaml`](.pre-commit-config.yaml) runs the same checks as CI before each commit: ruff (with `--fix`), black, and basic file hygiene (trailing whitespace, end-of-file, valid YAML and JSON, no large files). Files under `cards/` are exempt from the whitespace fixers so generated cards are not rewritten.

```bash
pre-commit install            # once, after cloning
pre-commit run --all-files    # run on everything, e.g. before opening a PR
```

If a hook changes a file, review the change, stage it and commit again. CI fails the PR if lint is not clean, whether or not you installed the hooks.

The hook versions are pinned. To update them, run `pre-commit autoupdate` and commit the result in a `[Pipeline]` or `[Docs]` PR of its own.

### Dependency updates

[Dependabot](.github/dependabot.yml) checks weekly for new versions of the GitHub Actions in `.github/workflows/` and of the Python dependencies in `pyproject.toml`, and opens one grouped PR per ecosystem. Review these like any other PR: CI must pass, and for a major version bump read the release notes first. Dependabot does not update the hook versions in `.pre-commit-config.yaml`, see above.

## What you can contribute

| Kind | Where | Typical PR title |
|---|---|---|
| A new or corrected card | `cards/` | `[Card] ...` |
| A change to the schema or a filling guide | `schema/` | `[Schema] ...` |
| A change to the pipeline | `src/skillcard/`, `tests/` | `[Pipeline] ...` |
| Documentation | `README.md`, `docs/` | `[Docs] ...` |
| A fix for a specific issue | anywhere | `[Issue #N] ...` |

## How your PR gets reviewed

**Fast lane.** No conflicts with `main`; scoped to one card, one pipeline phase, the tests or the docs; understood and verified by you; under ~500 hand-written lines.

**Needs a human maintainer** if any of the above does not hold, or for: any change to the schema or a filling guide, a change to the files the phases exchange (`snapshot.json`, `card.json`, `evidence.json`, `validation.json`), a change to how the hash is computed, a change spanning several phases, or a change that makes the same input produce a different card.

**Agree the approach first** for anything structural, especially schema changes. They affect every card, so open an issue before the PR. A large structural PR that arrives cold will sit.

Generated cards in `cards/` and fixtures under `tests/fixtures/` do not count toward the line limit.

## Pipeline rules

These come from the README and every phase must keep them.

1. A phase only adds its own files. It does not change the files of another phase.
2. Validation checks the card but does not change it.
3. We only read the files of a skill. We never run them, and we never follow links out of the skill folder.
4. A card must not carry paths from your machine.

## Contributing cards

- Cards under `cards/` are named `<owner>-<skill>-<short commit>.json` with a matching `.md`, and both files must be committed together.
- Check committed cards with `python -m skillcard.validate cards/*.json`. It checks that the card names the schema it follows, has the seven sections, has a content hash that matches its own file list, and has no blank values. CI runs it on every card. It cannot compare the file list with the skill's files, because those are not stored with the card. That check runs only during the pipeline.
- Generate them with the pipeline (`skillcard <skill folder>`) rather than by hand, and commit the output of a run that passed validation.
- Every value on a card must be supported by the skill's files or by a collected source. Follow the guides in [schema/guides/](schema/guides/). Do not fill in a value you cannot support; say that it is not known.
- Cards are model-generated and have **not** been reviewed by the authors of the skills unless a card says so. If you are the author of a skill, or you have reviewed a card, say so in your PR.
- A card is about one version of a skill (the commit in its name). When a skill changes, add a new card rather than editing the old one.

### Requesting a correction or removal

If you wrote a skill and a card about it is wrong, or you want it removed, open an issue using the *Card correction* template. A maintainer will respond within a reasonable time.

## Changing the schema

1. Open an issue describing the problem and the proposed change.
2. Wait for a maintainer to agree to the approach.
3. In the PR, update the schema, the affected filling guides, the pipeline and the tests together, and say whether existing cards need to be regenerated.
4. Bump the schema version following [CHANGELOG.md](CHANGELOG.md).

## Pull request checklist

- `pytest` is green and `ruff check .` is clean (the pre-commit hooks check this for you).
- Tests are added for new behaviour. Tests must run offline.
- Documentation is updated if behaviour changed.
- All commits are signed (see [Signing your commits](#signing-your-commits)).
- The PR template is filled in.

## Signing your commits

Commits to this repository must be signed, so that each commit can be tied to its author. GitHub shows a "Verified" badge on signed commits, and a maintainer may enable branch protection that rejects unsigned ones. Set up signing before you open a PR.

The simplest way is with an SSH key. If you already authenticate to GitHub with SSH, you can reuse that key or create a separate signing key:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true    # sign every commit by default
```

Then add the same public key to GitHub under *Settings → SSH and GPG keys* as a **Signing Key** (a key added only for authentication does not verify commits). If you prefer GPG, see GitHub's guide to [signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).

Check that it worked:

```bash
git log --show-signature -1
```

The commit's email must be one of the verified emails on your GitHub account, otherwise GitHub will not mark it as verified.

If you already pushed unsigned commits to your PR branch, re-sign them with `git rebase --exec 'git commit --amend --no-edit -S' origin/main` and force-push the branch (`--force-with-lease`). Never rewrite history on `main`.

## Commit and PR conventions

- Use a short imperative summary line, for example `Add hash check for left-out files`.
- Keep PRs focused. Do not split one coherent change into several to duck under a threshold.

## Code of conduct

By participating you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing you agree that your contributions are licensed under the MIT license, see [LICENSE](LICENSE).
