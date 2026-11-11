# Skill Card: improve-codebase-architecture mattpocock/skills at 4ae2317d

## 1. What it does

| Field | Value |
|---|---|
| **Name** | improve-codebase-architecture |
| **Description** | Instructions for an architecture review of a codebase in a fixed vocabulary of module, interface, depth, seam, adapter, leverage and locality. It scopes the scan to a direction the user names or to hot spots in the commit history, has a sub-agent walk the code, and writes deepening candidates with before and after diagrams to a self-contained HTML report in the OS temp directory. Once the user picks a candidate, it grills the decision tree with them and keeps GLOSSARY.md and ADRs current. The user invokes it, the model does not. |
| **Tasks** | • find hot spots in the commit history<br>• find shallow modules and seams that leak<br>• render deepening candidates as an HTML report with before and after diagrams<br>• name a top recommendation<br>• grill the decision tree of the candidate the user picks<br>• add terms to GLOSSARY.md and offer ADRs for rejected candidates |
| **Outputs** | • architecture review with one card per deepening candidate, a recommendation strength badge and a top recommendation (recommendation), self-contained HTML file, to &lt;tmpdir>/architecture-review-&lt;timestamp>.html, opened in the user's browser<br>• the absolute path of the report and the question which candidate to explore (information), message to the user, to the conversation<br>• new or sharpened domain terms (information), entries in a Markdown file, to GLOSSARY.md in the project<br>• a record of a rejected candidate with its reason (information), ADR document, to docs/adr/ in the project |
| **Sample output** | `Which of these would you like to explore?` |
| **Inputs** | • the codebase and its commit history, a git repository, required for every task, example `git log --oneline`<br>• a direction to look in, a module, a subsystem or a pain point, a request in natural language, optional for scoping the scan, example not declared<br>• the project's domain glossary, a Markdown file, optional for naming domain concepts in the report, example `GLOSSARY.md`<br>• architecture decision records, files in a folder, optional for decisions the review should not re-litigate, example `docs/adr/`<br>• the candidate the user picks, a reply in natural language, conditional for the grilling loop, example not declared |
| **When an input is missing** | • the user names no direction: the commit history is walked back to find hot spots, which get attention first<br>• the changes are scattered with no clear hot spot: the net is widened<br>• GLOSSARY.md does not exist when a new term is named: the file is created lazily |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 1.3M installs, counting the skill, first seen 13 March 2026 (read 11 November 2026)<br>• GitHub: 321,456 stars, 26,945 forks, counting the mattpocock/skills repository, which holds 39 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | • harnesses: not declared<br>• models: not declared<br>• capabilities: tool calling |
| **Harness limits** | • Agent Skills specification: fits, name 29 characters, description 125 characters, body 66 lines and about 1,453 tokens, frontmatter fields the specification does not define, disable-model-invocation<br>• Codex: fits, SKILL.md is 6,028 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 71 lines, listing text 125 characters<br>• ClawHub: fits, folder 12,835 bytes |
| **Software dependencies** | • git (binary), version not declared, needed to run<br>• xdg-open, open or start (binary), version not declared, needed to run<br>• Tailwind CSS from cdn.tailwindcss.com (package), version not declared, needed to run<br>• mermaid from cdn.jsdelivr.net (package), version 11, needed to run |
| **Credentials** | none |
| **Cost, context** | • discovery about 31 tokens<br>• load about 1,507 tokens<br>• on demand about 1,660 tokens, in HTML-REPORT.md |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• writes an HTML report to the OS temp directory, a fresh file per run, affects system, confirmation not declared, reversible not declared<br>• opens the report in the user's default browser, affects system, confirmation not declared, reversible not declared<br>• adds or updates terms in GLOSSARY.md, creating the file if it does not exist, affects workspace, confirmation not declared, reversible not declared<br>• records an ADR for a rejected candidate, affects workspace, confirmation yes, reversible not declared |
| **Network access** | • cdn.tailwindcss.com: other, each time the report is opened in a browser. Sends none, receives the Tailwind CSS script.<br>• cdn.jsdelivr.net: other, each time the report is opened in a browser. Sends none, receives the Mermaid ESM module, mermaid@11. |
| **Tools and permissions** | allowed-tools: none<br>• Skill tool with "codebase-design", "grilling" and "domain-modeling" (agent tool), the architecture vocabulary, the grilling loop, keeping the domain model current, built in<br>• a sub-agent with a fresh context window (agent tool), walking the codebase, built in<br>• git log --oneline (shell command), finding hot spots in the commit history, third party<br>• xdg-open, open, start (shell command), opening the report on Linux, macOS or Windows, third party<br>• shell and file tools of the agent (agent tool), running the commands, writing the report, GLOSSARY.md and ADRs, built in |
| **Machine access, paths** | • the source files and git history of the project, read, workspace<br>• GLOSSARY.md, read, workspace<br>• GLOSSARY.md, created or updated, write, workspace<br>• docs/adr/, read, workspace<br>• docs/adr/, a new ADR, write, workspace<br>• &lt;tmpdir>/architecture-review-&lt;timestamp>.html, write, system<br>• HTML-REPORT.md, read, skill folder |
| **Machine access, settings** | • TMPDIR, read, to resolve the temp directory, falling back to /tmp<br>• TEMP, read, to resolve the temp directory on Windows |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 29 October 2026 | unknown | warn, risk level MEDIUM, 1 issue, W012 unverifiable external dependency, Tailwind CSS and Mermaid JS loaded from external CDNs at runtime, scored 0.30 | [report](https://skills.sh/mattpocock/skills/improve-codebase-architecture/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 29 October 2026 | SKILL.md and HTML-REPORT.md, as cited in its analysis | pass, risk level SAFE, four surfaces described, indirect prompt injection, command execution, external downloads, and dynamic execution through Mermaid securityLevel loose | [report](https://skills.sh/mattpocock/skills/improve-codebase-architecture/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 29 October 2026 | the skill package, hash bb2b46f09aa3640009ec4a4a6fd9a03c8a03b752d30f924b5bb5bbeb8a732d2e | pass, checks for malicious behaviour, credential exposure, obfuscated code and suspicious patterns | [report](https://skills.sh/mattpocock/skills/improve-codebase-architecture/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Unverifiable external dependency detected, runtime URL that controls agent, W012 (C1, MEDIUM, scored 0.30, open), location not stated. Fix: not stated |
| **Risks** | • Instructions planted in source files, commit messages, GLOSSARY.md or ADRs reach the agent, since the codebase is read without delimiters or sanitisation. Source: check C2. Severity: SAFE overall by C2. Mitigation: none in the files, C2 notes that boundary markers and sanitisation are absent. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• Script from cdn.tailwindcss.com and cdn.jsdelivr.net runs in the browser when the report opens, so a changed or compromised CDN file controls the page. Source: check C1, check C2. Severity: MEDIUM by C1. Mitigation: none stated. Taxonomy: not examined.<br>• With Mermaid securityLevel loose, file names or comments from the codebase copied into a diagram can run as script in the report. Source: check C2. Severity: SAFE overall by C2. Mitigation: none stated. Taxonomy: not examined.<br>• On a shared machine, the report on the codebase's architecture lands in /tmp, where other users may be able to read it. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• GLOSSARY.md in the project is changed inline as decisions crystallize, with no confirmation step stated. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | not declared |
| **Known problems** | • Mermaid's layout fights the diagram, or cannot give a deep module the right weight: draw modules as divs with inline SVG arrows positioned over a relative container |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the mattpocock account on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 29 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 28 April 2026<br>• content changes 16 since first seen<br>• releases 10<br>• last release 29 October 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:c16bd7629780da17d40d0bfb1844c259c828aef8cbc1c3366664857b3225471c`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 4ae2317d |
| **Source** | • repository, GitHub mattpocock/skills, path skills/engineering/improve-codebase-architecture, commit 4ae2317d, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/mattpocock/skills/improve-codebase-architecture<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • HTML-REPORT.md, 6,641 bytes, document<br>• SKILL.md, 6,028 bytes, document<br>• agents/openai.yaml, 166 bytes, data |
| **File counts** | 2 documents, 0 scripts, 1 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
