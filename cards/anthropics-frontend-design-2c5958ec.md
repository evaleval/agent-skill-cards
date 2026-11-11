# Skill Card: frontend-design anthropics/skills at 2c5958ec

## 1. What it does

| Field | Value |
|---|---|
| **Name** | frontend-design |
| **Description** | Instructions only, for the visual design of a new UI or the reshaping of an existing one, working from the client's design brief. The agent grounds the design in the subject, drafts a compact plan of color, type, layout and principles, reviews it against the brief and against common AI-generated defaults, then writes the code and critiques it. Guidance covers the hero, typography, visual structure, motion, a quality floor for accessibility and interface copy. Use it when building or reshaping a UI where a distinctive, non-templated look is wanted. |
| **Tasks** | • identify the subject, audience and primary job of the design<br>• plan a token system with 4 to 6 named hex colors, typefaces, layout and principles<br>• review the plan against the brief and common generated-design defaults<br>• write the front-end code following the revised plan<br>• critique the build, with screenshots where the environment supports it<br>• write interface copy, calls to action, errors and empty states |
| **Outputs** | • a proposed subject, audience and primary job when the brief names none (recommendation), text, to the client, to confirm<br>• a short design plan with palette, typefaces and roles, layout concept with ASCII wireframes, and principles (information), text, to the conversation<br>• a note of what was changed in the plan after review and why (information), text, to the conversation<br>• the front-end code with its copy and placeholder content (information), code with CSS, destination not declared<br>• notes on what was tried, where a space for notes exists (information), notes, to a space for notes, if the environment has one |
| **Sample output** | `Save changes` |
| **Inputs** | • a design brief, a request in natural language, required for every task, example `a dashboard for financial analysts`<br>• an existing UI to reshape, existing front-end code, conditional for reshaping an existing UI, example not declared<br>• the brief's real content, text for the design, optional for every task, example not declared<br>• the client's preferences or context from memory, information in the agent's memory, optional for grounding the design, example not declared |
| **When an input is missing** | • the brief does not identify the product or subject matter: the agent proposes one concrete subject, audience and primary job and confirms with the client<br>• the brief contains no real content: the agent comes up with copy and placeholder content<br>• the brief leaves a visual axis free: the agent avoids the listed generated-design defaults on that axis |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 1.1M installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 192,784 stars, 22,682 forks, counting the anthropics/skills repository, which holds 20 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 15 characters, description 204 characters, body 66 lines and about 2,276 tokens<br>• Codex: does not fit, SKILL.md is 9,390 bytes, 1,390 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 71 lines, listing text 204 characters<br>• ClawHub: fits, folder 19,564 bytes |
| **Software dependencies** | none |
| **Credentials** | none |
| **Cost, context** | • discovery about 51 tokens<br>• load about 2,348 tokens<br>• on demand none |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• writes front-end code for a new UI, affects workspace, confirmation not declared, reversible not declared<br>• changes the code of an existing UI when reshaping it, affects workspace, confirmation not declared, reversible not declared |
| **Network access** | none |
| **Tools and permissions** | allowed-tools: none<br>• file tools of the agent (agent tool), writing the front-end code, built in<br>• screenshots of the build (agent tool), reviewing the work while building, if the environment supports it, built in<br>• memory or a space for notes (agent tool), client preferences as a hint, and notes on what was tried, built in |
| **Machine access, paths** | • front-end code files at paths the agent chooses, write, unknown<br>• the code of an existing UI being reshaped, read, unknown |
| **Machine access, settings** | none |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 15 September 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/anthropics/skills/frontend-design/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 15 September 2026 | the skill's instructional content, no files named | pass, risk level SAFE, purely instructional content without executable code, network operations or sensitive file access, user design briefs noted as an entry point | [report](https://skills.sh/anthropics/skills/frontend-design/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 15 September 2026 | the skill package, hash 7e9c2af00fd5b3144f49ce6fb1b16037b392ab9c2f049423b0b6114d99381ba2 | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/anthropics/skills/frontend-design/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • Instructions placed in a design brief from an outside source reach the agent, since the skill processes user-provided briefs as its entry point for external data. Source: check C2. Severity: SAFE overall by C2. Mitigation: none in the files, C2 rates the risk effectively null as the skill names no shell, file system or network operations. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• Existing UI code can be lost when the agent reshapes it, since the files ask for no confirmation and name no way to undo a change. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• Details about a client held in the agent's memory can appear in a design or its copy shown to others, since memory is used as a hint. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | • Visual self-critique with screenshots works only where the environment supports taking them.<br>• Notes on what was tried carry over to later passes only where the environment offers a space to jot them down. |
| **Known problems** | • CSS classes cancel each other out, often with padding and margin between sections: structure CSS selector specificities with care<br>• part of the design plan reads like the generic default for any similar page: revise that part before building and say what changed and why |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the anthropics organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: Complete terms in LICENSE.txt<br>• license file: LICENSE.txt, Apache License Version 2.0, January 2004, terms for use, reproduction and distribution, with no copyright notice naming a licensor<br>• skills.sh: not declared<br>• GitHub repository: none |
| **Maintenance status** | • last change 3 September 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 1 December 2025<br>• content changes 3 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:bfaf399ef64709e44984c746e0ba0d6d8f24b2de4d5579dd9daae98c84965293`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 2c5958ec |
| **Source** | • repository, GitHub anthropics/skills, path skills/frontend-design, commit 2c5958ec, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/anthropics/skills/frontend-design<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • LICENSE.txt, 10,174 bytes, document<br>• SKILL.md, 9,390 bytes, document |
| **File counts** | 2 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
