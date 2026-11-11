# Skill Card: security-review getsentry/skills at e94f2221

## 1. What it does

| Field | Value |
|---|---|
| **Name** | security-review |
| **Description** | Instructions and reference guides for a security code review of a file, diff or component the user names. The agent researches the whole codebase to trace data flow, upstream validation and framework protections, then reports only high-confidence exploitable vulnerabilities with location, impact, evidence and fix, and notes medium-confidence ones as needing verification. Seventeen OWASP-derived vulnerability references, Python and JavaScript framework guides and a Dockerfile guide are loaded by code type. Use it when asked for a security review, to find vulnerabilities or for an OWASP review. |
| **Tasks** | • review a file, diff or component for exploitable vulnerabilities<br>• trace data flow to confirm attacker-controlled input before flagging<br>• classify findings by severity and confidence<br>• check Django, Flask, FastAPI, Express, React, Vue and Next.js patterns<br>• review Dockerfiles for container security<br>• report findings in a fixed format with a fix for each |
| **Outputs** | • security review report with summary, findings and items that need verification (information), Markdown text in the fixed Security Review format, with VULN and VERIFY entries, to a reply to the user<br>• a fix for each high-confidence finding (recommendation), a Fix line in each finding, to the report<br>• a statement that nothing was found (information), one sentence, to a reply to the user |
| **Sample output** | `No high-confidence vulnerabilities identified.` |
| **Inputs** | • the code to report on, a file, diff, pull request or component the user names, required for every task, example `security review this`<br>• the surrounding codebase, with settings, config files and middleware, files the agent can read, required for researching each candidate finding, example not declared |
| **When an input is missing** | • the code is in a language other than Python or JavaScript: no dedicated guide is loaded, the references/ files are used and framework protections are verified in the codebase<br>• the django-access-review skill is not available for Django access control: authorization.md is used instead<br>• the gha-security-review skill is not available for GitHub Actions workflows: references/supply-chain.md is used instead |
| **Exclusions** | • not for GitHub Actions workflow exploitation, which belongs to the gha-security-review skill<br>• not for in-depth Django access-control review of permission classes and endpoint scopes<br>• not for Kubernetes, Terraform or cloud IAM configuration review<br>• not for running scanners, fuzzers or dynamic testing tools<br>• not for general code review or performance review<br>• not for writing exploits against systems the user does not own |
| **Adoption** | • skills.sh: 23.2K installs, counting the skill, first seen 29 January 2026 (read 11 November 2026)<br>• GitHub: 1,141 stars, 68 forks, counting the getsentry/skills repository, which holds 31 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 15 characters, description 312 characters, body 298 lines and about 2,849 tokens<br>• Codex: does not fit, SKILL.md is 11,808 bytes, 3,808 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 304 lines, listing text 312 characters<br>• ClawHub: fits, folder 227,367 bytes |
| **Software dependencies** | • grep (binary), version not declared, used in an example<br>• npm audit, pip-audit, cargo audit, bundle audit and safety check (binary), version not declared, used in an example |
| **Credentials** | none |
| **Cost, context** | • discovery about 78 tokens<br>• load about 2,952 tokens<br>• on demand about 51,426 tokens, in references/api-security.md, references/authentication.md, references/authorization.md, references/business-logic.md, references/cryptography.md, references/csrf.md, references/data-protection.md, references/deserialization.md, references/error-handling.md, references/file-security.md, references/injection.md, references/logging.md, references/misconfiguration.md, references/modern-threats.md, references/ssrf.md, references/supply-chain.md, references/xss.md, languages/python.md, languages/javascript.md and infrastructure/docker.md |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run read only |
| **Network access** | • vulnerability databases of the package registries, not named in the files: data source, only when the npm audit or pip-audit example commands in references/supply-chain.md are run. Sends file content, receives known vulnerabilities in the dependencies. |
| **Tools and permissions** | allowed-tools: Read Grep Glob Bash Task<br>• Read, Grep, Glob, Bash and Task (agent tool), reading and searching the codebase, running commands and delegating research, built in<br>• grep and ls detection commands (shell command), searching the reviewed code for vulnerable patterns, third party<br>• npm audit, pip-audit, cargo audit, bundle audit, safety check (shell command), checking dependencies for known vulnerabilities, in an example, third party<br>• django-access-review and gha-security-review skills (agent tool), Django access control and GitHub Actions workflow review, if available, third party |
| **Machine access, paths** | • the file, diff or code the user names, read, workspace<br>• the entire codebase, including settings, config files and middleware, read, workspace<br>• the references/, languages/ and infrastructure/ guides, read, skill folder |
| **Machine access, settings** | none |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 24 October 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/getsentry/skills/security-review/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 24 October 2026 | SKILL.md, languages/python.md, references/supply-chain.md and references/deserialization.md, as cited in its analysis | pass, risk level SAFE, eval, exec, a reverse shell pattern, encoding and placeholder keys found and read as detection examples, no network-active components | [report](https://skills.sh/getsentry/skills/security-review/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 24 October 2026 | the skill package, hash c16bdb280ed58b089f0c871a771178fb659cf863418c954a424cc5267a674f0c | fail, 1 alert, Malware rated HIGH in references/supply-chain.md, confidence 90 percent, severity 95 percent | [report](https://skills.sh/getsentry/skills/security-review/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Malware, install-time execution, base64 payloads, secret harvesting, exfiltration and a reverse shell to attacker.com:4444 (C3, HIGH, severity 95 percent, confidence 90 percent, open), location references/supply-chain.md. Fix: treat the package as compromised and avoid installation, rotate exposed secrets and revoke tokens possibly present in CI/CD environments |
| **Risks** | • Installing the skill brings in references/supply-chain.md, which C3 rates as malware for its install-hook, exfiltration and reverse shell code, while C2 reads the same code as red flags for the auditor. Source: check C3, check C2. Severity: HIGH by C3, SAFE overall by C2. Mitigation: none stated, C2 notes the code sits under Malicious Package Indicators as detection examples. Taxonomy: not examined.<br>• Secrets, customer data or PII found in the reviewed code can end up in the report or be stored, since each finding quotes the vulnerable code as evidence. Source: author. Severity: none. Mitigation: a rule that secrets, customer data and PII are not stored, an instruction only. Taxonomy: not examined.<br>• Instructions planted in comments or files of the reviewed codebase reach an agent that holds Bash, since the whole codebase is read without boundary markers. Source: model. Severity: none. Mitigation: none stated. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas. |
| **Limitations** | • Language coverage beyond Python and JavaScript relies on language-agnostic references, so framework-specific mitigations in Go, Rust, Java, PHP and Ruby may be missed or over-flagged.<br>• Infrastructure coverage is limited to Dockerfiles, and Kubernetes, Terraform and cloud IAM review produce generic results.<br>• On very large codebases the research step can be incomplete and findings may land in Needs Verification more often.<br>• The reference material is a derivative of the OWASP cheat sheets at a point in time and does not track upstream revisions automatically. |
| **Known problems** | not declared |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the getsentry organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: LICENSE<br>• license file: LICENSE, reference material derived from the OWASP Cheat Sheet Series under Creative Commons Attribution-ShareAlike 4.0 International, with attribution and share-alike terms<br>• skills.sh: not declared<br>• GitHub repository: Apache-2.0, as GitHub detects it |
| **Maintenance status** | • last change 19 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 19 April 2026<br>• content changes 4 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:1f19166a309cb1f75fca68d19f7d228499130b85664d9492d7de298a77ee2373`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit e94f2221 |
| **Source** | • repository, GitHub getsentry/skills, path skills/security-review, commit e94f2221, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/getsentry/skills/security-review<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • LICENSE, 884 bytes, document<br>• SKILL.md, 11,808 bytes, document<br>• SPEC.md, 8,974 bytes, document<br>• infrastructure/docker.md, 9,400 bytes, document<br>• languages/javascript.md, 10,028 bytes, document<br>• languages/python.md, 9,492 bytes, document<br>• references/api-security.md, 12,741 bytes, document<br>• references/authentication.md, 9,071 bytes, document<br>• references/authorization.md, 10,007 bytes, document<br>• references/business-logic.md, 12,660 bytes, document<br>• references/cryptography.md, 8,703 bytes, document<br>• references/csrf.md, 9,943 bytes, document<br>• references/data-protection.md, 9,565 bytes, document<br>• references/deserialization.md, 10,234 bytes, document<br>• references/error-handling.md, 11,632 bytes, document<br>• references/file-security.md, 12,344 bytes, document<br>• references/injection.md, 6,813 bytes, document<br>• references/logging.md, 12,012 bytes, document<br>• references/misconfiguration.md, 10,305 bytes, document<br>• references/modern-threats.md, 13,269 bytes, document<br>• references/ssrf.md, 10,734 bytes, document<br>• references/supply-chain.md, 9,149 bytes, document<br>• references/xss.md, 7,599 bytes, document |
| **File counts** | 23 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
