# Skill Card: audit-website squirrelscan/skills at 29f17762

## 1. What it does

| Field | Value |
|---|---|
| **Name** | audit-website |
| **Description** | Instructions for auditing a website with the squirrel CLI and fixing the findings in the site's code. The agent runs squirrel audit against a URL with the LLM report format, presents the score, grade and top issues, maps each issue to the template, component or content file behind it, applies the fixes the user approves in batches and re-audits until a score target is met. A reference file describes the LLM report and diff format. Use it to discover and assess website or webapp issues and drive them to fixed. |
| **Tasks** | • audit a website against 300+ rules with the squirrel CLI<br>• map audit issues to the templates, components or content files behind them<br>• fix approved issues in batches and re-audit until the score target is met<br>• compare audits against a baseline to catch regressions<br>• tailor audits by disabling rules that do not apply to the site<br>• start the fix loop from a squirrelscan channel event |
| **Outputs** | • audit report with health score, grade, issues by category, broken links and recommendations (information), compact XML and text hybrid in the llm format, to the terminal and the agent's context, cached locally for later reports<br>• the report presented to the user with proposed fixes and judgment calls flagged for review (recommendation), message to the user, to the conversation<br>• fixes to the templates, components and content files behind each finding (action), edited source files, to the user's project<br>• diff and regression reports against a baseline audit (information), compact XML diff in the llm format, to the terminal and the agent's context<br>• before and after score comparison with a summary of every change made (information), message to the user, to the conversation<br>• rules disabled for findings that do not apply (action), a [rules] disable entry in squirrel.toml or the website's disable_rules, to squirrel.toml in the project, or the squirrelscan cloud<br>• a published report, a capped summary that samples affected pages (action), published report, to squirrelscan |
| **Sample output** | `<score overall="78" grade="C">` |
| **Inputs** | • the URL of the site to audit, a URL as a command argument, required for every audit, example `squirrel audit https://example.com --format llm`<br>• the site's source code and content files, a local project, conditional for the fix loop, example not declared<br>• an audit id, an id as a command argument, conditional for re-rendering a cached audit or diffing against a baseline, example `squirrel report --diff <baseline-audit-id> --format llm`<br>• the run_id of a cloud audit, an id from a squirrelscan channel event, conditional for a fix loop started from a channel event, example not declared<br>• Web Bot Auth headers, repeated -H flags, optional for a site that blocks unknown crawlers, example `-H "Name: Value"` |
| **When an input is missing** | • the user does not provide a URL: the agent asks which site to audit<br>• the audit exits with code 3, 4 or 5: nothing was audited and there is no score, so no fix loop starts<br>• the start URL redirects to another site: the destination is relayed and the audit re-run with --follow-redirect only after the user confirms the site<br>• a finding needs a judgment call, such as a broken link: it is flagged for user review instead of guessing |
| **Exclusions** | • not for CLI setup, login, publishing, MCP or general CLI usage, which the companion squirrelscan skill covers |
| **Adoption** | • skills.sh: 75.0K installs, counting the skill, first seen 22 January 2026 (read 11 November 2026)<br>• GitHub: 108 stars, 10 forks, counting the squirrelscan/skills repository, which holds 2 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 13 characters, description 419 characters, body 88 lines and about 1,538 tokens<br>• Codex: fits, SKILL.md is 6,829 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 98 lines, listing text 419 characters<br>• ClawHub: fits, folder 21,820 bytes |
| **Software dependencies** | • squirrel CLI (binary), version 0.0.108 or later for --level, needed to run |
| **Credentials** | • other, Web Bot Auth header values, used for auditing a site that blocks unknown crawlers, from command argument, goes to the audited website |
| **Cost, context** | • discovery about 105 tokens<br>• load about 1,707 tokens<br>• on demand about 2,282 tokens, in references/OUTPUT-FORMAT.md |
| **Cost, per run** | not examined |
| **Cost, services** | • squirrelscan, needs account, price signed in, every pass is billed in credits, 50 plus 2 per audited page, signed out or with --offline it costs nothing, quota not declared, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install changes state, run changes state<br>• installs the squirrel CLI from squirrelscan.com/download, affects software environment, confirmation not declared, reversible not declared<br>• edits templates, components and content files to fix findings, affects workspace, confirmation yes, reversible not declared<br>• caches audits locally, affects other, confirmation not declared, reversible not declared<br>• signed in, adds an audited site to the user's dashboard and schedules it unless --ephemeral is passed, affects external service, confirmation not declared, reversible not declared<br>• signed in, spends squirrelscan credits on every audit pass, affects external service, confirmation not declared, reversible not declared<br>• disables rules in squirrel.toml or in the website's cloud disable_rules, affects workspace, confirmation yes, reversible not declared<br>• publishes a report to share results, affects external service, confirmation yes, reversible not declared |
| **Network access** | • the website the user names, formed at run time: data source, every audit, with Web Bot Auth headers only when passed. Sends credential, receives the site's pages, crawled up to 25, 100 or 500 by level.<br>• squirrelscan.com: install, once, when the squirrel CLI is installed from squirrelscan.com/download. Sends none, receives the squirrel CLI.<br>• the squirrelscan cloud, host not named in the files: data source, when signed in, for cloud runs, channel events and reports fetched by run_id. Sends query text, receives cloud audit reports and channel events.<br>• the squirrelscan cloud, host not named in the files: publish, when the user wants to share results. Sends user content, receives a published report.<br>• docs.squirrelscan.com: data source, when looking up a rule. Sends query text, receives the rule's documentation. |
| **Tools and permissions** | allowed-tools: Bash(squirrel:*) Read Edit Grep Glob<br>• squirrel audit and squirrel report (shell command), running audits, re-rendering cached audits and diffing against a baseline, third party<br>• Bash, limited to squirrel (agent tool), running the squirrel CLI, built in<br>• Read, Edit, Grep and Glob (agent tool), mapping issues to source files and applying fixes, built in<br>• the project's build and existing checks (shell command), verifying the project still builds after each batch, third party<br>• claude (shell command), piping the LLM report to an agent, in one example, third party |
| **Machine access, paths** | • the site's templates, components and content files, read, workspace<br>• the site's templates, components and content files, write, workspace<br>• squirrel.toml, write, workspace<br>• the local audit cache, location not named, write, unknown<br>• references/OUTPUT-FORMAT.md, read, skill folder |
| **Machine access, settings** | • PATH, read, the squirrel CLI must be accessible in PATH<br>• [rules] disable in squirrel.toml, set, to stop reporting a finding class that does not apply to the site<br>• disable_rules of the website in the squirrelscan cloud, set, to stop reporting a finding class in cloud runs |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 5 November 2026 | unknown | warn, risk level MEDIUM, 1 issue, W011 third-party content exposure, indirect prompt injection risk, scored low risk 0.10 | [report](https://skills.sh/squirrelscan/skills/audit-website/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 5 November 2026 | SKILL.md instructions and allowed tools, as cited in its analysis | pass, risk level SAFE, two surfaces described, indirect prompt injection from crawled sites and channel events, and command execution limited to the squirrel binary | [report](https://skills.sh/squirrelscan/skills/audit-website/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 6 November 2026 | the skill package, hash 8d312b4b5bdb098e4c584b30a13992d0eeebd572c9adea44a93c8cf6375bc755 | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/squirrelscan/skills/audit-website/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Third-party content exposure, indirect prompt injection risk, W011 (C1, MEDIUM, scored low risk 0.10, open), location not stated. Fix: not stated |
| **Risks** | • Instructions hidden in a crawled page or a channel event reach the agent through the audit report, while the agent can edit the project's source code. Source: check C1, check C2. Severity: MEDIUM by C1, SAFE overall by C2. Mitigation: in the instructions, event text is treated as data and the user confirms before any change, no technical boundary. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• Repeated re-audits in the fix loop spend squirrelscan credits when signed in, 50 plus 2 per audited page on every pass. Source: model. Severity: none. Mitigation: signed out or with --offline it costs nothing, and a quick first pass caps pages at 25. Taxonomy: not examined.<br>• Web Bot Auth header values passed with -H on the command line can stay in shell history or logs. Source: model. Severity: none. Mitigation: header values are redacted in squirrel output, shell history not addressed. Taxonomy: not examined. |
| **Limitations** | • A skipped check is not clean and is not reported as fixed.<br>• Exit codes 3, 4 and 5 mean nothing was audited and there is no score.<br>• Requests listed under refused-fetches are unknown, not missing.<br>• A local dev server does not show true rendering, performance and redirect behaviour.<br>• The quick pass samples only part of the site, so sign-off needs a --level full crawl.<br>• --level needs squirrel 0.0.108 or later.<br>• A published report is a capped summary that samples affected pages, so fixes come from the local report.<br>• Broken links and other judgment calls need a human decision. |
| **Known problems** | • the site blocks unknown crawlers, such as Shopify or Cloudflare: pass Web Bot Auth headers with repeated -H flags<br>• the start URL redirected to another site: relay the destination and re-run with --follow-redirect after the user confirms<br>• an interrupted crawl: continue it with --resume<br>• cached results after deploys or content changes: re-audit with --refresh<br>• a finding class does not apply to the site: disable it in squirrel.toml or the website's disable_rules and re-audit |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author squirrelscan, from the metadata of SKILL.md<br>• publisher the squirrelscan organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: See LICENSE file in repository root<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 4 November 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 8 July 2026<br>• content changes 10 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:d611567e7fd2a37d078501bf75fa9aeb1c4fbbe51f67d68f40d97a2249514fc3`, files left out none<br>• author version 2.9<br>• registry version not declared<br>• commit 29f17762 |
| **Source** | • repository, GitHub squirrelscan/skills, path skills/audit-website, commit 29f17762, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/squirrelscan/skills/audit-website<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • README.md, 1,152 bytes, document<br>• SKILL.md, 6,829 bytes, document<br>• agents/openai.yaml, 229 bytes, data<br>• assets/icon-large.png, 2,763 bytes, binary<br>• assets/icon-small.svg, 1,721 bytes, data<br>• references/OUTPUT-FORMAT.md, 9,126 bytes, document |
| **File counts** | 3 documents, 0 scripts, 2 data, 1 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
