# Skill Card: find-skills vercel-labs/skills at e781cb4d

## 1. What it does

| Field | Value |
|---|---|
| **Name** | find-skills |
| **Description** | Instructions only, one SKILL.md, for discovering and installing skills from the open agent skills ecosystem with the Skills CLI, npx skills. The agent checks the skills.sh leaderboard, searches with npx skills find, verifies install count, source reputation and GitHub stars, and presents matching skills with their install count, install command and a skills.sh link. If the user wants to proceed, it installs the skill with npx skills add, and when nothing is found it offers to help directly or to create a new skill. Use it when the user asks how to do a task, asks for a skill for something, or wants to extend the agent's capabilities. |
| **Tasks** | • check the skills.sh leaderboard for a well-known skill<br>• search for skills with npx skills find<br>• verify install count, source reputation and GitHub stars<br>• present options with install count, install command and skills.sh link<br>• install a chosen skill with npx skills add<br>• update installed skills with npx skills update<br>• suggest creating a skill with npx skills init when none is found |
| **Author's description** | "Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill." |
| **Outputs** | • skill options with name, purpose, install count, source, install command and a link to learn more (recommendation), chat message, to the user<br>• a skill installed globally at user level (action), installed skill, to the user-level skill location of the agent<br>• a notice that no matching skill was found, with an offer to help directly (information), chat message, to the user |
| **Sample output** | `I found a skill that might help! The "react-best-practices" skill provides React and Next.js performance optimization guidelines from Vercel Engineering. (185K installs)` |
| **Inputs** | • the user's need, the domain and the specific task, a question in natural language, required for every task, example `how do I make my React app faster?`<br>• search keywords, a query argument to the find command, optional for searching with the CLI, example `npx skills find react performance`<br>• a GitHub owner to scope the search, a flagged argument, optional for searching with the CLI, example `npx skills find [query] [--owner <owner>]`<br>• the skill to install, a package identifier in the form owner/repo@skill, conditional for installing a skill, example `npx skills add vercel-labs/agent-skills@react-best-practices` |
| **When an input is missing** | • the leaderboard does not cover the user's need: the agent runs npx skills find<br>• a search term returns nothing: the agent tries alternative terms, for instance deployment or ci-cd for deploy<br>• no relevant skill exists: the agent says so, offers to help with the task directly, and suggests creating a skill with npx skills init |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 4.3M installs, counting the skill, first seen 26 January 2026 (read 11 November 2026)<br>• GitHub: 38,928 stars, 3,400 forks, counting the vercel-labs/skills repository, which holds 3 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 11 characters, description 303 characters, body 137 lines and about 1,282 tokens<br>• Codex: fits, SKILL.md is 5,472 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 141 lines, listing text 303 characters<br>• ClawHub: fits, folder 5,472 bytes |
| **Software dependencies** | • skills, the Skills CLI (package), version not declared, needed to run<br>• npx (binary), version not declared, needed to run |
| **Credentials** | none |
| **Cost, context** | • discovery about 76 tokens<br>• load about 1,368 tokens<br>• on demand none |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• installs a skill globally at user level with npx skills add -g -y, skipping the CLI's confirmation prompts, affects user home, confirmation yes, reversible not declared<br>• updates all installed skills with npx skills update, affects user home, confirmation not declared, reversible not declared<br>• fetches and runs the skills package through npx, affects software environment, confirmation not declared, reversible not declared |
| **Network access** | • skills.sh: data source, when the leaderboard is checked before a search, and for links to learn more. Sends none, receives the leaderboard of skills ranked by installs.<br>• the search backend of the Skills CLI, not named in the files: data source, when npx skills find runs. Sends query text, receives matching skills.<br>• GitHub or other sources, github.com not named as a host: install, when a skill is installed or updated, and when repository stars are checked. Sends none, receives the skill files and repository star counts.<br>• the npm registry, not named in the files: install, when npx fetches the skills package. Sends none, receives the skills package. |
| **Tools and permissions** | allowed-tools: none<br>• npx skills find, npx skills add, npx skills update (shell command), searching, installing and updating skills, third party<br>• npx skills init (shell command), creating a new skill, suggested to the user when nothing is found, third party<br>• shell tool of the agent (agent tool), running the npx skills commands, built in<br>• web access of the agent (agent tool), checking the skills.sh leaderboard and GitHub stars, built in |
| **Machine access, paths** | • the user-level location where skills are installed globally, not named in the files, write, user home |
| **Machine access, settings** | none |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 15 September 2026 | unknown | warn, risk level MEDIUM, 1 issue, W011 third-party content exposure, indirect prompt injection risk, scored low risk 0.10 | [report](https://skills.sh/vercel-labs/skills/find-skills/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 15 September 2026 | the skill's instructions, as cited in its analysis | pass, risk level SAFE, three surfaces described, command execution with npx skills and the -y flag, external downloads, and indirect prompt injection from ecosystem metadata | [report](https://skills.sh/vercel-labs/skills/find-skills/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 15 September 2026 | the skill package, hash b146008599c31057cef1c145774cea5d5afb30e8f43fa802e47a4b461419aaaf | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/vercel-labs/skills/find-skills/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Third-party content exposure, indirect prompt injection risk, W011 (C1, MEDIUM, open), location not stated. Fix: not stated |
| **Risks** | • Instructions embedded in skill descriptions or registry metadata from the public ecosystem reach the agent when it reads search results. Source: check C1, check C2. Severity: MEDIUM by C1, SAFE overall by C2. Mitigation: partly in place, the files have the agent verify installs, source and stars before recommending, which C2 credits. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• A harmful or low-quality skill from the open ecosystem is installed at user level, since -y skips the CLI's confirmation prompts. Source: check C2. Severity: SAFE overall by C2. Mitigation: in place in the files, quality checks before recommending and installing only if the user wants to proceed. Taxonomy: not examined.<br>• A changed upstream skill replaces the version already installed when npx skills update updates all installed skills at once. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | not declared |
| **Known problems** | • a search term finds nothing: try alternative terms, for instance deployment or ci-cd instead of deploy<br>• no relevant skill exists: help with the task directly, or create a skill with npx skills init |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the vercel-labs organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 10 July 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 26 January 2026<br>• content changes 3 since first seen<br>• releases 55<br>• last release 10 November 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:4f4ed5e34b9a9bb47098110ea2c7f0cb66334b2017bad9cbfdcb073a807b30c9`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit e781cb4d |
| **Source** | • repository, GitHub vercel-labs/skills, path skills/find-skills, commit e781cb4d, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/vercel-labs/skills/find-skills<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 5,472 bytes, document |
| **File counts** | 1 document, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 39 |
