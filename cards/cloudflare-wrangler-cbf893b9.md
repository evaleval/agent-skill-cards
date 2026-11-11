# Skill Card: wrangler cloudflare/skills at cbf893b9

## 1. What it does

| Field | Value |
|---|---|
| **Name** | wrangler |
| **Description** | Instructions for running and troubleshooting Wrangler CLI commands in Cloudflare Workers projects that already have a wrangler.jsonc, wrangler.json or wrangler.toml file. The agent inspects the project, retrieves the current Cloudflare documentation for the task, edits config and bindings, and runs local development, Preview deployments, deployments, secrets and resource commands through the project's own Wrangler version. It validates with wrangler types, typechecks and wrangler deploy --dry-run, then reports what changed, the target environment, the checks performed and any validation gaps. A second file drafts and, after approval, posts feedback about the skill as a public GitHub issue. |
| **Tasks** | • local development with local or remote bindings<br>• deploy Workers and framework applications<br>• edit Wrangler config, bindings and environments<br>• create and manage Workers Previews for branches and pull requests<br>• set secrets and choose API token scopes<br>• generate binding and runtime types<br>• submit skill feedback as a GitHub issue on cloudflare/skills |
| **Author's description** | "Run or troubleshoot Wrangler CLI commands in projects that have a wrangler.jsonc, wrangler.json, or wrangler.toml file, including local development, Previews, deployment, and resource management. For new projects and projects without a Wrangler configuration file, use the cf CLI instead." |
| **Outputs** | • changed Wrangler config, bindings and compatibility date (information), wrangler.jsonc, wrangler.json or wrangler.toml, to the config source used by the project's build or deploy command<br>• deployed Workers, Preview deployments and Worker versions (action), a deployment with a returned URL, to the target Cloudflare account, Worker and environment<br>• secrets set or deleted, and changes to remote resources and data (action), a new Worker version or a resource change, to the target Cloudflare account<br>• generated binding and runtime types (information), type declaration files, to the project<br>• a report of what changed, the target environment, checks performed and unresolved validation gaps, with links to the documentation used (information), message to the user, to the conversation<br>• a skill feedback issue (action), GitHub issue, to the cloudflare/skills repository |
| **Sample output** | `skill-feedback: wrangler: <summary of the problem>` |
| **Inputs** | • a project with a Wrangler configuration file, a project folder, required for every task, example `wrangler.jsonc`<br>• the target account, Worker, environment and resource, names and an --env value, conditional for commands that change a target, example not declared<br>• an authenticated login or an account-owned API token, a Wrangler login or token, conditional for remote commands, example `wrangler login`<br>• secret values, interactive input or a protected file or stdin, conditional for setting secrets locally, in CI or on a deployed Worker, example not declared<br>• the user's report of incorrect, outdated or missing guidance, text in the conversation, conditional for skill feedback, example `Unknown option: --preview` |
| **When an input is missing** | • the project has no Wrangler configuration file, is new, or has cloudflare.config.ts: the cf CLI is used instead and Wrangler is not added<br>• the project has a Wrangler configuration file but Wrangler is not a dependency: Wrangler is added locally following the installation guide<br>• documentation retrieval is unavailable: the gap is stated and local evidence is used rather than invented syntax<br>• the target Worker or Wrangler environment is unclear: the target is established and confirmed with the user before running commands<br>• the user declines to send feedback or to approve the issue text: no issue is posted |
| **Exclusions** | • not for new projects, use the cf CLI<br>• not for projects with cloudflare.config.ts<br>• not for projects with no Cloudflare configuration<br>• do not add Wrangler to projects that use the cf CLI |
| **Adoption** | • skills.sh: 144.6K installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 3,338 stars, 348 forks, counting the cloudflare/skills repository, which holds 22 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 8 characters, description 288 characters, body 71 lines and about 2,872 tokens<br>• Codex: does not fit, SKILL.md is 11,813 bytes, 3,813 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 75 lines, listing text 288 characters<br>• ClawHub: fits, folder 14,594 bytes |
| **Software dependencies** | • Wrangler, project-local (package), version 4.135.0 or later for Workers Previews, needed to run<br>• the project's package manager (binary), version not declared, needed to install<br>• Cloudflare Vite plugin (package), version not declared, needed to run<br>• gh (binary), version not declared, used in an example |
| **Credentials** | • token, account-owned API token, used for remote Wrangler commands with granular access, from unknown, goes to Cloudflare, host not named in the files<br>• token, wrangler login OAuth flow, used for authenticating Wrangler to a Cloudflare account, from unknown, goes to Cloudflare, host not named in the files<br>• other, Worker secrets and local secret files, used for secrets set locally, in CI or on a deployed Worker, from unknown, goes to Cloudflare, host not named in the files |
| **Cost, context** | • discovery about 72 tokens<br>• load about 2,953 tokens<br>• on demand about 695 tokens, in references/skill-feedback.md |
| **Cost, per run** | not examined |
| **Cost, services** | • Cloudflare Workers, needs account, price not declared, quota not declared, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• edits Wrangler config, bindings and compatibility date, affects workspace, confirmation not declared, reversible not declared<br>• installs dependencies and adds or upgrades Wrangler locally, affects software environment, confirmation not declared, reversible not declared<br>• regenerates type declarations with wrangler types, affects workspace, confirmation not declared, reversible not declared<br>• deploys Workers and Preview deployments, affects external service, confirmation not declared, reversible not declared<br>• wrangler secret put and secret delete create a version and deploy it immediately, affects external service, confirmation not declared, reversible not declared<br>• can overwrite dashboard variables and routes, and omitted identifiers can trigger automatic provisioning, affects external service, confirmation not declared, reversible not declared<br>• writes to production resources, destructive testing and deletion of named Previews, affects external service, confirmation yes, reversible not declared<br>• rolls back a Worker to an earlier version, without its connected resources and data, affects external service, confirmation not declared, reversible not declared<br>• posts a public GitHub issue on cloudflare/skills, affects external service, confirmation yes, reversible not declared |
| **Network access** | • developers.cloudflare.com: data source, when retrieving documentation for a task. Sends none, receives documentation pages.<br>• Cloudflare MCP server, not named in the files: data source, when the Cloudflare MCP docs tool is available. Sends query text, receives documentation.<br>• Cloudflare API, not named in the files: publish, remote commands, deployments, Previews, secrets and resource management. Sends credential and file content, receives deployment results, Preview URLs and resource state.<br>• package registry, not named in the files: install, when dependencies or Wrangler are installed. Sends none, receives the packages.<br>• github.com: publish, when the user approves a skill feedback issue. Sends credential and user content, receives the issue URL. |
| **Tools and permissions** | allowed-tools: none<br>• wrangler, run through the project's scripts or package manager (program), local development, deploy, Previews, secrets, types, rollback and resource management, third party<br>• the project's package manager (shell command), installing dependencies from the existing lockfile, third party<br>• Cloudflare MCP docs tool (external server), retrieving Cloudflare documentation, third party<br>• gh issue create --repo cloudflare/skills (shell command), posting approved skill feedback, third party<br>• Cloudflare roles and API token permissions (permission), the narrowest scope that satisfies the remote operation, third party<br>• shell, file and web fetch tools of the agent (agent tool), running commands, editing config and fetching documentation pages, built in |
| **Machine access, paths** | • wrangler.jsonc, wrangler.json or wrangler.toml, write, workspace<br>• cloudflare.config.ts, read, workspace<br>• package scripts and the lockfile, read, workspace<br>• wrangler/config-schema.json, usually under node_modules, read, workspace<br>• generated type declarations, write, workspace<br>• local secret files, read, workspace<br>• references/skill-feedback.md, read, skill folder |
| **Machine access, settings** | • CLOUDFLARE_ENV, set, selects the environment for the Cloudflare Vite plugin at dev or build time<br>• compatibility date, set, set to today for a new project<br>• secrets.required, read, checked when local secrets are missing |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 28 October 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/cloudflare/skills/wrangler/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 28 October 2026 | unknown | pass, risk level SAFE, describes secure secret management, links only to official Cloudflare domains, and project-local Wrangler | [report](https://skills.sh/cloudflare/skills/wrangler/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 28 October 2026 | the skill package, hash 398aebc6edb1d2e690b00bf25b9cae335a7c7354573917545a1bd2c954c93399 | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/cloudflare/skills/wrangler/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • Preview URLs are reachable by anyone when no access controls are configured. Source: author. Severity: none. Mitigation: the user is told and decides whether to protect the URLs. Taxonomy: not examined.<br>• A deploy can overwrite dashboard variables and routes when dashboard changes are not reconciled with the config. Source: author. Severity: none. Mitigation: reconcile dashboard changes with the config before deploying. Taxonomy: not examined.<br>• A locally running Worker can still write to real resources when remote bindings are selected. Source: author. Severity: none. Mitigation: check the selected bindings before testing writes. Taxonomy: not examined.<br>• A rollback leaves connected resources and their data as they are, so data changed by a bad deploy stays changed. Source: author. Severity: none. Mitigation: check rollback limitations before a rollback. Taxonomy: not examined.<br>• Sensitive information from the conversation becomes public when it is left in a feedback issue posted on GitHub. Source: author. Severity: none. Mitigation: credentials, identifiers and private data are removed and the user approves the exact text, in place. Taxonomy: not examined.<br>• Instructions planted in a fetched documentation page or MCP result reach the agent, since pages are fetched and followed without delimiters. Source: model. Severity: none. Mitigation: none stated. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas. |
| **Limitations** | • A successful dry run checks the build and packaging, it does not prove remote resources or runtime behavior work.<br>• The wrangler login OAuth flow does not support granular authorization.<br>• Workers Previews requires project-local Wrangler 4.135.0 or later, and project commands do not use a newer global installation.<br>• Connected resources and their data are not rolled back with Worker code.<br>• A returned Preview URL does not validate behavior that depends on bindings Wrangler reports as missing.<br>• Local secret files are not automatically uploaded as deployed secrets.<br>• With the Cloudflare Vite plugin, setting an environment at deploy time does not retarget its flattened config. |
| **Known problems** | • a documentation page moves: rediscover it through the Wrangler command index or Cloudflare docs search<br>• documentation retrieval is unavailable: state the gap and use available local evidence<br>• a required feature needs a newer Wrangler: make the dependency upgrade explicit<br>• local secrets are missing: check file precedence and any secrets.required declaration in the secrets docs<br>• submitting the feedback issue fails: give the user the approved title and body and the link to create the issue manually |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the cloudflare organisation on GitHub<br>• signer none<br>• contact issues on the cloudflare/skills repository, https://github.com/cloudflare/skills/issues/new |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: Apache-2.0, as GitHub detects it |
| **Maintenance status** | • last change 27 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 28 January 2026<br>• content changes 17 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:97052c293ef66b948982fdc06f7b93c659be17a3ae673f50bb19e3bc3327db92`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit cbf893b9 |
| **Source** | • repository, GitHub cloudflare/skills, path skills/wrangler, commit cbf893b9, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/cloudflare/skills/wrangler<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 11,813 bytes, document<br>• references/skill-feedback.md, 2,781 bytes, document |
| **File counts** | 2 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 62 |
