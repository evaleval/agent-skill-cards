# Skill Card: deploy-to-vercel vercel-labs/agent-skills at 1a2c79d4

## 1. What it does

| Field | Value |
|---|---|
| **Name** | deploy-to-vercel |
| **Description** | Instructions for deploying a project to Vercel from an agent, with the Vercel CLI and git. The agent checks for a git remote, a .vercel link and a logged-in CLI, then deploys by git push, by vercel deploy, or without an account through a temporary deployment with a claim URL. Deployments are previews unless the user explicitly asks for production, and the deployment URL is always shown to the user. Use it when the user asks to deploy an app, push it live or create a preview deployment. |
| **Tasks** | • deploy a project to Vercel as a preview, or to production on request<br>• detect the git remote, the .vercel link and the CLI login<br>• select a team and link the project to Vercel<br>• deploy by git push after the user approves<br>• deploy without an account through vercel deploy --temporary<br>• report the deployment URL and build status<br>• works in Claude Code, claude.ai and Codex sandboxes |
| **Author's description** | "Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment"." |
| **Outputs** | • a deployment on Vercel, preview by default, production when the user asks (action), a Vercel deployment, to Vercel<br>• a temporary deployment that needs no account (action), a temporary production URL with a claim URL and an expiry, to Vercel, until it expires unless claimed<br>• a linked Vercel project with automatic deployments on future git pushes (action), a Vercel project and .vercel/project.json or .vercel/repo.json, to Vercel and the project directory<br>• a commit of the project pushed to the git remote (action), a git commit with the message deploy: &lt;description of changes>, to the git remote<br>• the deployment URL, build status, claim URL and expiry (information), a message to the user, to the conversation |
| **Sample output** | `Your deployment is ready at [url]. It expires in [time] unless you claim it at [claimUrl]. Don't share the claim link.` |
| **Inputs** | • the project to deploy, a directory path, optional for every deploy, example `vercel deploy [path] -y --no-wait`<br>• the team to deploy to, a team slug chosen from a list, conditional for accounts with several teams and an unlinked project, example `vercel deploy [path] -y --no-wait --scope <team-slug>`<br>• approval to commit and push, an answer from the user, conditional for a linked project with a git remote, example `This project is connected to Vercel via git. I can commit and push to trigger a deployment. Want me to proceed?`<br>• an explicit request for production, the user's request, conditional for production deploys, example `vercel deploy [path] --prod -y --no-wait`<br>• a Vercel login, authentication in the user's browser, conditional for a CLI that is not authenticated, outside the no-auth fallback, example `vercel login` |
| **When an input is missing** | • the user does not ask for production: the project is deployed as a preview<br>• the user has only one team or a personal account: the team prompt is skipped and that account is used<br>• the project is already linked: the orgId in the .vercel files determines the team, with no question<br>• the CLI has no credentials and vercel login is not possible: the no-auth fallback deploys with npx vercel@latest deploy [path] --temporary -y<br>• the CLI is not authenticated after a git push: the user is told to check the Vercel dashboard or the commit status checks for the preview URL |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 189.0K installs, counting the skill, first seen 6 March 2026 (read 11 November 2026)<br>• GitHub: 33,874 stars, 2,960 forks, counting the vercel-labs/agent-skills repository, which holds 9 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | • harnesses: Claude Code, claude.ai and Codex, named in the agent-specific notes<br>• models: not declared<br>• capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 16 characters, description 194 characters, body 223 lines and about 2,359 tokens<br>• Codex: does not fit, SKILL.md is 9,721 bytes, 1,721 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 230 lines, listing text 194 characters<br>• ClawHub: fits, folder 9,721 bytes |
| **Software dependencies** | • vercel, the Vercel CLI (package), version not declared, latest when run with npx vercel@latest, needed to run<br>• git (binary), version not declared, needed to run<br>• npm and npx (binary), version not declared, needed to install |
| **Credentials** | • other, the Vercel CLI login from vercel login, used for linking, deploying and listing teams and deployments, from prompt to the user, goes to Vercel |
| **Cost, context** | • discovery about 49 tokens<br>• load about 2,430 tokens<br>• on demand none |
| **Cost, per run** | not examined |
| **Cost, services** | • Vercel, needs account, price not declared, quota not declared, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install changes state, run changes state<br>• installs the Vercel CLI globally with npm install -g vercel, affects software environment, confirmation not declared, reversible not declared<br>• links the project, creating a Vercel project and .vercel/project.json or .vercel/repo.json, affects external service, confirmation no, reversible not declared<br>• stages all changes with git add . and commits them, affects workspace, confirmation yes, reversible not declared<br>• pushes to the git remote, which triggers a Vercel deployment, affects external service, confirmation yes, reversible not declared<br>• deploys the project with vercel deploy, as a preview or with --prod, affects external service, confirmation not declared, reversible not declared<br>• deploys to a temporary production URL with vercel deploy --temporary, affects external service, confirmation not declared, reversible not declared |
| **Network access** | • vercel.com, named as *.vercel.com in the files: publish, every login, link, deploy and status check. Sends file content and credential, receives deployment URL, build status, team list, claim URL and expiry.<br>• registry.npmjs.org: install, when the CLI is installed with npm or run with npx vercel@latest. Sends none, receives the vercel package.<br>• the git remote, not named in the files: publish, when a linked project with a git remote is deployed by git push. Sends file content, receives not declared. |
| **Tools and permissions** | allowed-tools: none<br>• vercel whoami, teams list, link, deploy, inspect, ls and login (shell command), checking login, choosing a team, linking, deploying and reading status, third party<br>• git remote get-url, git add, git commit, git push (shell command), detecting the remote and deploying by git push, third party<br>• npm install -g vercel and npx vercel@latest (shell command), installing or running the Vercel CLI, third party<br>• cat and sleep (shell command), reading the .vercel files and waiting before listing deployments, third party<br>• sandbox_permissions=require_escalated (permission), escalated network access for the deploy command in Codex when the sandbox blocks it, built in<br>• shell tool of the agent (agent tool), running the CLI and git commands, full shell access in Claude Code, built in |
| **Machine access, paths** | • .vercel/project.json and .vercel/repo.json, read, workspace<br>• .vercel/project.json or .vercel/repo.json, created by vercel link, write, workspace<br>• the project directory, [path], uploaded or committed, read, workspace<br>• the git repository of the project, through git add . and git commit, write, workspace<br>• the global npm install location, through npm install -g vercel, write, unknown |
| **Machine access, settings** | • orgId in .vercel/project.json or .vercel/repo.json, read, determines the team of a linked project<br>• sandbox_permissions=require_escalated, set, only when sandboxing blocks the deploy network call in Codex<br>• allowed domains at https://claude.ai/settings/capabilities, set, the user adds *.vercel.com and registry.npmjs.org after a network egress error on claude.ai |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 28 October 2026 | deploy.sh and deploy-codex.sh, as named in its analysis, scripts that are not among the files of this version | warn, risk level MEDIUM, 1 issue, W012 unverifiable external dependency, runtime URL that controls agent, scored medium risk 0.30 | [report](https://skills.sh/vercel-labs/agent-skills/deploy-to-vercel/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 28 October 2026 | the instructions and the deployment scripts, as described in its analysis, scripts that are not among the files of this version | pass, risk level SAFE, flags EXTERNAL_DOWNLOADS and COMMAND_EXECUTION, describes official Vercel domains, exclusion of .env and .git from the upload, npm install of the CLI and approval before git push | [report](https://skills.sh/vercel-labs/agent-skills/deploy-to-vercel/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 28 October 2026 | the skill package, hash 9b883827e904cd6c93a98457f1ea5aaae1dfdb30ae704bddf5e9e70c9d10de36 | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/vercel-labs/agent-skills/deploy-to-vercel/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Unverifiable external dependency detected, runtime URL that controls agent, W012 (C1, MEDIUM, scored 0.30, open), location deploy.sh and deploy-codex.sh, which are not among the files at 1a2c79d4. Fix: not stated |
| **Risks** | • In the package C1 examined, which held deploy.sh and deploy-codex.sh, those scripts post project code to claude-skills-deploy.vercel.com and codex-deploy-skills.vercel.sh and take instructions or URLs back at run time, an external dependency the agent cannot verify. Source: check C1. Severity: MEDIUM by C1. Mitigation: none stated, the scripts C1 names are not among the files at 1a2c79d4. Taxonomy: not examined.<br>• Anyone who gets the claim link of a temporary deployment can claim that deployment. Source: author. Severity: none. Mitigation: the user is told not to share the claim link, in place in the message. Taxonomy: not examined.<br>• git add . stages every change in the project, so files with secrets that are not ignored can be committed and pushed to the remote and deployed. Source: model. Severity: none. Mitigation: the user is asked before pushing, in place, no files are excluded. Taxonomy: not examined.<br>• The no-auth fallback deploys the project to a temporary production URL without a confirmation step, so project files become reachable on the web. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | • Temporary deployments don't work in CI or in a directory already linked to a Vercel project.<br>• A temporary deployment expires unless it is claimed.<br>• vercel login is not possible in non-interactive environments.<br>• Without an authenticated CLI, the preview URL of a git push deploy has to be found in the Vercel dashboard or the commit status checks.<br>• vercel link without --repo matches by directory name and often fails when the local folder and the Vercel project are named differently. |
| **Known problems** | • deployment fails due to network restrictions on claude.ai: add *.vercel.com and registry.npmjs.org to the allowed domains at https://claude.ai/settings/capabilities and deploy again<br>• deployment fails due to network issues in Codex or a sandboxed environment: rerun the deploy command with sandbox_permissions=require_escalated<br>• vercel login or vercel deploy fails with authentication errors: use the no-auth fallback, vercel deploy --temporary -y<br>• state detection in an unlinked directory prompts or links as a side effect: use only vercel whoami there, not vercel project inspect, vercel ls or vercel link |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author vercel, from the frontmatter metadata<br>• publisher the vercel-labs organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: none |
| **Maintenance status** | • last change 27 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 6 March 2026<br>• content changes 3 since first seen<br>• releases 5<br>• last release 27 October 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:cbf9be989f413417d26315a017b88a20e32dd9abe3d9f0038ae17498ef222828`, files left out none<br>• author version 4.0.0<br>• registry version not declared<br>• commit 1a2c79d4 |
| **Source** | • repository, GitHub vercel-labs/agent-skills, path skills/deploy-to-vercel, commit 1a2c79d4, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/vercel-labs/agent-skills/deploy-to-vercel<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 9,721 bytes, document |
| **File counts** | 1 document, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 43 |
