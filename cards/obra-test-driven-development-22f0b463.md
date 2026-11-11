# Skill Card: test-driven-development obra/superpowers at 22f0b463

## 1. What it does

| Field | Value |
|---|---|
| **Name** | test-driven-development |
| **Description** | Instructions in two Markdown documents for test-driven development by an agent, with no scripts. Write the test first, watch it fail for the expected reason, write minimal code to pass, then refactor while the project's whole suite stays green, and delete any production code written before its test. A reference on writing good tests covers naming the break each test catches, asserting real behavior instead of mock behavior, and a mutation check. Use it when implementing any feature or bugfix, before writing implementation code. |
| **Tasks** | • write one minimal failing test before any production code<br>• verify the test fails because the feature is missing<br>• write the simplest code to pass, then refactor while green<br>• fix a bug by first writing a failing test that reproduces it<br>• write tests that assert real behavior, not mock behavior<br>• run the project's whole test suite before calling a change done<br>• check every box of the verification checklist before marking work complete |
| **Outputs** | • tests, one behavior each with a clear name (information), test files in the project's language, for instance TypeScript, to the project's test files, for instance path/to/test.test.ts<br>• minimal production code that makes the tests pass (information), source code, to the project's source files<br>• test runs, failing first and then passing (information), terminal text from the project's test command, to the terminal the agent runs the tests in<br>• a report naming every test failure the full suite run shows, including ones the agent did not cause (information), a message, to the agent's report to the user |
| **Sample output** | `FAIL: expected 'Email required', got undefined` |
| **Inputs** | • a feature or bug fix to implement, a task in natural language, required for every task, example `Bug: Empty email accepted`<br>• the project's test command, a shell command the repository uses, required for verifying red and green, example `npm test path/to/test.test.ts`<br>• the human partner's permission, a decision by the user, conditional for skipping TDD for throwaway prototypes, generated code or configuration files, example not declared |
| **When an input is missing** | • the agent does not know how to test the feature: write the wished-for API, write the assertion first, ask your human partner<br>• a case looks like an exception to TDD: ask your human partner, no exceptions without their permission |
| **Exclusions** | • throwaway prototypes, after asking your human partner<br>• generated code, after asking your human partner<br>• configuration files, after asking your human partner |
| **Adoption** | • skills.sh: 276.3K installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 315,991 stars, 28,109 forks, counting the obra/superpowers repository, which holds 15 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 23 characters, description 79 characters, body 326 lines and about 2,362 tokens<br>• Codex: does not fit, SKILL.md is 9,578 bytes, 1,578 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 330 lines, listing text 79 characters<br>• ClawHub: fits, folder 17,846 bytes |
| **Software dependencies** | • npm (binary), version not declared, used in an example<br>• jest (package), version not declared, used in an example<br>• pytest (binary), version not declared, used in an example<br>• cargo (binary), version not declared, used in an example |
| **Credentials** | none |
| **Cost, context** | • discovery about 20 tokens<br>• load about 2,395 tokens<br>• on demand about 2,067 tokens, in writing-good-tests.md |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• writes test files and production code, affects workspace, confirmation not declared, reversible not declared<br>• deletes production code written before its test, without keeping it as reference, affects workspace, confirmation not declared, reversible not declared |
| **Network access** | none |
| **Tools and permissions** | allowed-tools: none<br>• the project's test command, such as npm test, pytest or cargo test (shell command), watching a test fail and pass, and running the whole suite, third party<br>• shell and file tools of the agent (agent tool), writing and deleting code and running the test command, built in |
| **Machine access, paths** | • test files of the project, for instance path/to/test.test.ts, write, workspace<br>• production source files of the project, write, workspace<br>• production code written before its test, delete, workspace<br>• writing-good-tests.md in the skill folder, read, skill folder |
| **Machine access, settings** | none |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 19 September 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/obra/superpowers/test-driven-development/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 19 September 2026 | SKILL.md, as quoted in its analysis | pass, risk level SAFE, PROMPT_INJECTION described, high-pressure imperative language and instructions to delete code that could lose work without user confirmation | [report](https://skills.sh/obra/superpowers/test-driven-development/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 19 September 2026 | the skill package, hash 8e8772822d25e4dfc9295cf4526c6251a10458c7417ac50c4b42e5d9fc91e0b0 | pass, checks for malicious behavior, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/obra/superpowers/test-driven-development/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • Code the user wanted to keep is lost when the agent applies the rule to delete code written before its test literally and without asking the user. Source: check C2. Severity: SAFE overall by C2. Mitigation: none stated for the deletion, exceptions to TDD need the human partner's permission. Taxonomy: not examined.<br>• Absolute rules that label alternative reasoning as rationalization override the agent's usual procedure, so the agent may hold to the process where the situation called for another approach. Source: check C2. Severity: SAFE overall by C2. Mitigation: exceptions are to be asked of the human partner, in place in the files. Taxonomy: not examined.<br>• Running the project's whole test suite, required even when the task names one test file, executes every test in the repository with the agent's privileges, including tests with side effects. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | not declared |
| **Known problems** | • the new test passes immediately: it tests existing behavior, fix the test<br>• the new test errors instead of failing: fix the error and re-run until it fails correctly<br>• the test is too complicated: simplify the interface<br>• everything must be mocked: the code is too coupled, use dependency injection<br>• the test setup is huge: extract helpers, and if still complex, simplify the design<br>• mock setup outgrows the test logic: switch to an integration test with real components |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the obra account on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 19 September 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 16 October 2025<br>• content changes 12 since first seen<br>• releases 17<br>• last release 3 November 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:5f2300c235f200c5c728c64744725deacd66c2fc617638f50db147607e74632c`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 22f0b463 |
| **Source** | • repository, GitHub obra/superpowers, path skills/test-driven-development, commit 22f0b463, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/obra/superpowers/test-driven-development<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 9,578 bytes, document<br>• writing-good-tests.md, 8,268 bytes, document |
| **File counts** | 2 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
