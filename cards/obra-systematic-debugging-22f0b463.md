# Skill Card: systematic-debugging obra/superpowers at 22f0b463

## 1. What it does

| Field | Value |
|---|---|
| **Name** | systematic-debugging |
| **Description** | Instructions for a four-phase debugging process, root cause investigation, pattern analysis, hypothesis and testing, and implementation, with no fix proposed before the root cause is found. Three reference documents cover backward tracing through the call stack, validation at every layer and condition-based waiting in flaky tests, with a TypeScript example and a bash script that finds which test creates unwanted files. The result is a confirmed root cause, a failing test and a single fix, or a discussion of the architecture after three failed fixes. Use it for any bug, test failure or unexpected behaviour, before proposing fixes. |
| **Tasks** | • investigate the root cause of a bug before any fix<br>• add diagnostic instrumentation at component boundaries<br>• trace bad values backward through the call stack<br>• test one hypothesis at a time with the smallest change<br>• write a failing test, then a single fix at the source<br>• replace arbitrary timeouts in flaky tests with condition polling<br>• find the test that creates unwanted files or state |
| **Author's description** | "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes" |
| **Outputs** | • a stated hypothesis and the identified root cause (information), text, I think X is the root cause because Y, to the conversation<br>• a failing test case and a single fix at the source, with validation added at each layer (information), code and test files, to the user's codebase<br>• diagnostic log lines and stack traces from added instrumentation (information), terminal text, to the terminal or test output<br>• the result of the polluter search, the test file that created the file or directory (information), terminal text, to the terminal the agent runs find-polluter.sh in<br>• after three or more failed fixes, the question whether the architecture is sound (recommendation), a discussion with the human partner, to the conversation |
| **Sample output** | `FOUND POLLUTER!` |
| **Inputs** | • the bug, test failure or unexpected behaviour with its error messages and stack traces, error output and a description of the issue, required for every task, example `Error: git init failed in ~/project/packages/core`<br>• the file or directory whose creation marks pollution, a positional script argument, conditional for finding the polluting test with find-polluter.sh, example `'.git'`<br>• a pattern for the test files to run, a positional script argument, conditional for finding the polluting test with find-polluter.sh, example `./find-polluter.sh <file_or_dir_to_check> <test_pattern>` |
| **When an input is missing** | • find-polluter.sh is called without exactly two arguments: it prints its usage line and an example, and exits<br>• the issue cannot be reproduced reliably: gather more data, don't guess<br>• the cause is not understood: say I don't understand X, ask for help and research more |
| **Exclusions** | • condition-based waiting is not for testing actual timing behavior, such as debounce or throttle intervals |
| **Adoption** | • skills.sh: 328.4K installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 315,991 stars, 28,109 forks, counting the obra/superpowers repository, which holds 15 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 20 characters, description 91 characters, body 279 lines and about 2,347 tokens<br>• Codex: does not fit, SKILL.md is 9,530 bytes, 1,530 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 283 lines, listing text 91 characters<br>• ClawHub: fits, folder 29,057 bytes |
| **Software dependencies** | • bash (runtime), version not declared, needed to run<br>• npm (binary), version not declared, needed to run<br>• TypeScript (runtime), version not declared, used in an example<br>• git (binary), version not declared, used in an example<br>• security and codesign (binary), version not declared, used in an example |
| **Credentials** | • other, IDENTITY, used for the signing identity checked and passed to codesign in the multi-layer diagnostic example, from environment variable, stays on the machine |
| **Cost, context** | • discovery about 23 tokens<br>• load about 2,383 tokens<br>• on demand about 4,386 tokens, in root-cause-tracing.md, defense-in-depth.md, condition-based-waiting.md and condition-based-waiting-example.ts |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• adds diagnostic logging, failing tests, fixes and validation to the user's code, affects workspace, confirmation not declared, reversible not declared<br>• runs npm test on each matching test file, which can create files or state, affects workspace, confirmation not declared, reversible not declared |
| **Network access** | none |
| **Tools and permissions** | allowed-tools: none<br>• find-polluter.sh (program), running tests one by one to find which test creates unwanted files or state, skill<br>• npm test (shell command), running tests and capturing debug output, third party<br>• git diff (shell command), checking recent changes, third party<br>• security list-keychains, security find-identity, codesign (shell command), checking keychain and signing state in the multi-layer example, third party<br>• superpowers:test-driven-development and superpowers:verification-before-completion (other), writing the failing test and verifying the fix before claiming success, third party<br>• shell and file tools of the agent (agent tool), running commands, reading code and editing files, built in |
| **Machine access, paths** | • the project's source and test files, read, workspace<br>• source and test files changed by instrumentation, tests and fixes, write, workspace<br>• test files matching the pattern under the current directory, and the pollution file or directory checked, read, workspace<br>• the skill folder, find-polluter.sh and the reference documents, read, skill folder |
| **Machine access, settings** | • NODE_ENV, read, logged in debug instrumentation and used to refuse git init outside the temp directory during tests |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 4 November 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/obra/superpowers/systematic-debugging/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 4 November 2026 | find-polluter.sh, as cited in its analysis | warn, risk level MEDIUM, COMMAND_EXECUTION and INDIRECT_PROMPT_INJECTION, find-polluter.sh runs npm test on discovered files and uses TEST_PATTERN in find without sanitization | [report](https://skills.sh/obra/superpowers/systematic-debugging/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 5 November 2026 | the skill package, hash 60e7465ae62f622e075f5b204d5f4acb20e8ff7d51e9cb59d3edf3e7e16de221 | pass, checks for malicious behaviour, credential exposure, obfuscated code and suspicious patterns | [report](https://skills.sh/obra/superpowers/systematic-debugging/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • COMMAND_EXECUTION, find-polluter.sh executes npm test on files discovered on the local file system (C2, MEDIUM, open), location find-polluter.sh. Fix: not stated<br>• INDIRECT_PROMPT_INJECTION, TEST_PATTERN is interpolated into the find command without sanitization (C2, MEDIUM, open), location find-polluter.sh, the TEST_PATTERN argument. Fix: not stated |
| **Risks** | • Running find-polluter.sh executes every matching test file through npm test, so code in those tests runs with the user's privileges. Source: check C2. Severity: MEDIUM by C2. Mitigation: none stated. Taxonomy: not examined.<br>• A test pattern taken from untrusted input and passed to find-polluter.sh could change which files find selects and runs, since TEST_PATTERN is not validated. Source: check C2. Severity: MEDIUM by C2. Mitigation: none stated, C2 notes that sanitization and boundary markers are absent. Taxonomy: not examined.<br>• Diagnostic output can expose signing identities and environment details in shared CI logs, since the multi-layer example runs security find-identity -v and logs environment state. Source: model. Severity: none. Mitigation: partly in place, the example prints SET or UNSET for IDENTITY instead of its value. Taxonomy: not examined. |
| **Limitations** | • Some issues are truly environmental, timing-dependent or external, and then the process ends in handling, monitoring and logging instead of a root-cause fix.<br>• When tracing backward reaches a dead end, the fix is made at the symptom point.<br>• find-polluter.sh skips a test file when the pollution already exists before that test runs.<br>• find-polluter.sh runs each test with npm test and discards the test output. |
| **Known problems** | • three or more fixes have failed: stop, question the architecture and discuss with the human partner before more fixes<br>• the issue is not reproducible: gather more data, don't guess<br>• logger output does not show in tests: use console.error() for debug output in tests<br>• flaky tests with arbitrary delays: wait for the actual condition with a polling function and a timeout<br>• unwanted files appear during tests and the test is unknown: run find-polluter.sh to bisect the test files |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the obra account on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 3 November 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 16 October 2025<br>• content changes 14 since first seen<br>• releases 17<br>• last release 3 November 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:f376836c637d9bc2aab31f4536a3fb0c628c3ab96494cb9d28c89a45057ca489`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 22f0b463 |
| **Source** | • repository, GitHub obra/superpowers, path skills/systematic-debugging, commit 22f0b463, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/obra/superpowers/systematic-debugging<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 9,530 bytes, document<br>• condition-based-waiting-example.ts, 5,054 bytes, script<br>• condition-based-waiting.md, 3,516 bytes, document<br>• defense-in-depth.md, 3,650 bytes, document<br>• find-polluter.sh, 1,986 bytes, script, executable<br>• root-cause-tracing.md, 5,321 bytes, document |
| **File counts** | 4 documents, 2 scripts, 0 data, 0 binary, instructions with scripts |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 35 |
