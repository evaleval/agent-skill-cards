# Skill Card: gh-fix-ci openai/skills at 49f948fa

## 1. What it does

| Field | Value |
|---|---|
| **Name** | gh-fix-ci |
| **Description** | Instructions and one Python script for debugging failing GitHub pull request checks that run in GitHub Actions. With the gh CLI it locates the failing checks, fetches the Actions logs and extracts a failure snippet, then summarizes the failures for the user. It drafts a fix plan and implements it only after explicit approval, while checks from external providers such as Buildkite are reported by their details URL only. Use it when a user asks to debug or fix failing GitHub PR checks. |
| **Tasks** | • verify gh authentication for the repo host<br>• resolve the PR from the current branch or a given number or URL<br>• inspect failing checks and fetch GitHub Actions logs<br>• extract and summarize a failure snippet per failing check<br>• draft a fix plan and implement it after explicit approval<br>• recheck status with gh pr checks after changes |
| **Author's description** | "Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treat external providers (for example Buildkite) as out of scope and report only the details URL." |
| **Outputs** | • failure report per failing check, with check name, details URL, run and job id, status, workflow, branch and SHA, and a failure snippet (information), terminal text, or JSON with --json, to the terminal and the agent's context<br>• summary of failures for the user, with check name, run URL and a concise log snippet, missing logs called out (information), text in the conversation, to the user<br>• fix plan with a request for approval (recommendation), a concise plan, through the create-plan skill or inline, to the user<br>• code changes that apply the approved plan, with a summary of diffs and tests (information), changed files and text in the conversation, to the repository<br>• job log fetched through the GitHub API when the run log is still in progress (information), log file, to a path the agent chooses<br>• exit status, non-zero when failures remain (information), process exit code, to the calling shell or automation |
| **Sample output** | `PR #{pr_value}: no failing checks detected.` |
| **Inputs** | • a path inside the repository, the --repo argument, default ., optional for every task, example `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`<br>• the pull request, PR number or URL in the --pr argument, optional for every task, defaults to the current branch PR, example `--pr "https://github.com/org/repo/pull/123"`<br>• gh authentication for the repo host, a logged-in GitHub CLI, repo and workflow scopes typically required, required for every task, example `gh auth login`<br>• snippet size, the --max-lines and --context arguments, defaults 160 and 30, optional for extracting a failure snippet, example `--max-lines 200 --context 40`<br>• output format, the --json flag, optional for machine-friendly output for summarization, example `--json`<br>• approval of the fix plan, explicit approval from the user, conditional for implementing a fix, example not declared |
| **When an input is missing** | • gh is unauthenticated: the user is asked to run gh auth login with repo and workflow scopes before proceeding, and the script prints gh's message or Error: gh not authenticated. and stops<br>• no PR number or URL is given: the current branch PR is used through gh pr view, and the script prints an error and stops when none is found<br>• the --repo path is not inside a Git repository: the script prints Error: not inside a Git repository. and stops<br>• gh is not installed: the script prints Error: gh is not installed or not on PATH. and stops<br>• gh pr checks rejects a field: the command is rerun with the available fields reported by gh<br>• logs are missing: the summary calls out missing logs explicitly |
| **Exclusions** | • checks from external providers such as Buildkite, only the details URL is reported<br>• checks that are not GitHub Actions runs |
| **Adoption** | • skills.sh: 11.9K installs, counting the skill, first seen 20 January 2026 (read 11 November 2026)<br>• GitHub: 28,680 stars, 2,000 forks, counting the openai/skills repository, which holds 43 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 9 characters, description 313 characters, body 65 lines and about 824 tokens<br>• Codex: fits, SKILL.md is 3,651 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 69 lines, listing text 313 characters<br>• ClawHub: fits, folder 32,642 bytes |
| **Software dependencies** | • gh, the GitHub CLI (binary), version not declared, needed to run<br>• git (binary), version not declared, needed to run<br>• Python 3 (runtime), version not declared, needed to run |
| **Credentials** | • token, gh authentication for the repo host, used for reading PR checks, run metadata and Actions logs through gh and the GitHub API, from unknown, goes to the repo host, github.com in the examples |
| **Cost, context** | • discovery about 78 tokens<br>• load about 913 tokens<br>• on demand none |
| **Cost, per run** | not examined |
| **Cost, services** | • GitHub, through gh and the GitHub API, needs account, price not declared, quota not declared, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install changes state, run changes state<br>• authenticates the GitHub CLI once with gh auth login, affects user home, confirmation not declared, reversible not declared<br>• applies the approved fix plan to the repository files, affects workspace, confirmation yes, reversible not declared<br>• writes a job log to a path with gh api and a shell redirect, affects workspace, confirmation not declared, reversible not declared<br>• opens a pull request after asking the user, affects external service, confirmation yes, reversible not declared |
| **Network access** | • the repo host, github.com in the examples, reached through gh and the GitHub API: data source, every run, to check auth, resolve the PR and fetch checks, run metadata and logs. Sends credential and query text, receives auth status, PR number, check states, run metadata and Actions logs.<br>• the repo host, github.com in the examples: publish, when the user agrees to open a PR after the fix. Sends credential and file content, receives not declared. |
| **Tools and permissions** | allowed-tools: none<br>• python with scripts/inspect_pr_checks.py (program), fetching failing checks, pulling Actions logs and extracting a failure snippet, skill<br>• gh auth status, gh pr view, gh pr checks, gh run view, gh api, gh repo view (shell command), auth check, PR resolution, checks, run metadata, run and job logs, third party<br>• git rev-parse --show-toplevel (shell command), finding the repository root, third party<br>• create-plan skill, if available (agent tool), drafting a concise plan and requesting approval, third party<br>• repo and workflow scopes of the gh login (permission), access to the repository and its workflow runs, third party<br>• shell and file tools of the agent (agent tool), running the commands and editing files to apply the fix, built in |
| **Machine access, paths** | • the repository given by --repo, default ., read, workspace<br>• repository files changed by the approved fix, write, workspace<br>• "&lt;path>" for a job log fetched with gh api, write, unknown<br>• &lt;path-to-skill>/scripts/inspect_pr_checks.py, run from the skill folder, read, skill folder |
| **Machine access, settings** | • PATH, read, finding the gh program |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 15 September 2026 | unknown | warn, risk level MEDIUM, 1 issue, W011 third-party content exposure, indirect prompt injection risk, scored medium risk 0.30 | [report](https://skills.sh/openai/skills/gh-fix-ci/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 15 September 2026 | scripts/inspect_pr_checks.py and the workflow, as cited in its analysis | pass, risk level SAFE, two surfaces described, command execution through subprocess.run with list arguments, and Actions logs ingested without boundary markers or sanitisation | [report](https://skills.sh/openai/skills/gh-fix-ci/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 15 September 2026 | the skill package, hash 25e7c47d9a997aa1cb3dd4e5805b9f4a33c4dc6534ab1a1ceb76bc3887e2453d | pass, checks for malicious behaviour, credential exposure, obfuscated code and suspicious patterns | [report](https://skills.sh/openai/skills/gh-fix-ci/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Third-party content exposure, indirect prompt injection risk, W011 (C1, MEDIUM, scored 0.30, open), location not stated. Fix: not stated |
| **Risks** | • Instructions planted by outsiders in CI logs, PR comments or code changes reach the agent, since log content is handed over without delimiters or sanitisation and the agent can run commands and write files. Source: check C1, check C2. Severity: MEDIUM by C1, SAFE overall by C2. Mitigation: implementation waits for explicit approval of the plan, in place in the workflow, C2 notes that no boundary markers are used. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• A gh login with repo and workflow scopes lets any gh command the agent runs change the repository or its workflows, not only read checks and logs. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• A job log written with a shell redirect to "&lt;path>" replaces any file already at that path. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | • Only GitHub Actions checks are inspected, checks from other providers are labelled external and reported by URL only.<br>• Logs are not available while a run is still in progress, and the check is then reported as log_pending.<br>• Job logs returned as a zip archive cannot be parsed.<br>• The failure snippet is taken around the last line with a failure marker such as error, fail or traceback, otherwise from the end of the log.<br>• No dependency carries a version. |
| **Known problems** | • gh pr checks rejects a field: rerun with the available fields reported by gh, which the bundled script does on its own<br>• the run log says it is still in progress: fetch job logs directly with gh api<br>• gh is unauthenticated: run gh auth login with repo and workflow scopes, then confirm with gh auth status |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the openai organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: LICENSE.txt, Apache License, Version 2.0, January 2004, with the copyright line left as the template placeholder<br>• skills.sh: not declared<br>• GitHub repository: none |
| **Maintenance status** | • last change 2 February 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 19 December 2025<br>• content changes 7 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:9221a5541793085f10f5fd2b3c04e70e7d63067fe86d3dd34d32fc0fc81d09b3`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 49f948fa |
| **Source** | • repository, GitHub openai/skills, path skills/.curated/gh-fix-ci, commit 49f948fa, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/openai/skills/gh-fix-ci<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • LICENSE.txt, 10,776 bytes, document<br>• SKILL.md, 3,651 bytes, document<br>• agents/openai.yaml, 302 bytes, data<br>• assets/github-small.svg, 853 bytes, data<br>• assets/github.png, 1,838 bytes, binary<br>• scripts/inspect_pr_checks.py, 15,222 bytes, script, executable |
| **File counts** | 2 documents, 1 script, 2 data, 1 binary, instructions with scripts |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 42 |
