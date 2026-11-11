# Skill Card: firecrawl firecrawl/cli at 06b371f0

## 1. What it does

| Field | Value |
|---|---|
| **Name** | firecrawl |
| **Description** | Instructions for doing live-web tasks through the Firecrawl CLI. It searches the web, scrapes static and JS-rendered pages, maps and crawls sites, interacts with pages through clicks, forms and login, downloads sites and sets monitors for changes, and returns clean markdown optimized for LLM context windows. Results are written to files in .firecrawl/ and read in bounded parts. Use it for ordinary web research and content gathering, web only, with local files going to firecrawl-parse. |
| **Tasks** | • search the web and gather sources<br>• scrape a page or a list of known URLs<br>• map a site to find a subpage and crawl a site section<br>• interact with a page through clicks, form fills, pagination or login<br>• download a site to local files<br>• watch pages for changes with a monitor<br>• find US law or regulation with gov search |
| **Author's description** | "Any live-web task via the Firecrawl CLI — including ordinary web research: searching the web, reading or extracting pages, gathering sources, discovering site URLs, bulk extraction, downloading a site, change alerts, or pages needing clicks/login — web only; local files route to firecrawl-parse. For US legal or regulatory questions use gov; for papers use firecrawl-research-index; for library, API, error, or bug questions use firecrawl-developer-index." |
| **Outputs** | • search results, with page content when scraped (information), JSON file, to .firecrawl/search-{query}.json or .firecrawl/search-{query}-scraped.json<br>• page content (information), markdown file, or JSON for several formats, to .firecrawl/{site}-{path}.md, or the agent's context when the user asks for it<br>• a downloaded site (information), local files, destination not declared<br>• auth state, concurrency limit, remaining credits and credit usage (information), terminal text or JSON file, to the terminal or .firecrawl/credits.json<br>• a monitor that runs recurring scrapes or crawls and alerts on changes (action), a scheduled job at Firecrawl, to the Firecrawl account, with alerts by webhook or email<br>• clicks, form submissions and multi-step navigation on a page (action), browser actions, to the website being interacted with<br>• feedback on a search or a job (action), a feedback call, to Firecrawl, through /v2/feedback for job feedback |
| **Sample output** | `.firecrawl/search-react-hooks.json` |
| **Inputs** | • a question or search query, text in a command, conditional for search, gov and research tasks, example `firecrawl search "react hooks" -o .firecrawl/search-react-hooks.json --json`<br>• a URL, a quoted URL in a command, conditional for scraping, mapping, crawling and interacting with a known page or site, example `firecrawl scrape "<url>" -o .firecrawl/page.md`<br>• an output file, the -o flag, optional for every command that returns results, example `-o .firecrawl/page.md`<br>• options for a provider capability, a JSON string, conditional for running a structured-data tool found by search, example `scrape <provider/capability> --options '<JSON>'`<br>• a jurisdiction and date for a legal question, text in a command, conditional for US legal or regulatory search, example `firecrawl gov "<question, jurisdiction, and date>" --limit 10`<br>• a Firecrawl API key, a command argument, optional for authentication when browser login fails, example `firecrawl login --api-key "<key>"` |
| **When an input is missing** | • a legal question names no jurisdiction: the agent asks for the jurisdiction before identifying the governing rule<br>• no credentials are set: search, scrape and interact run on the keyless free tier, and crawl, map, download, agent, monitor, credit-usage and feedback prompt an interactive login<br>• authentication fails: the agent asks the user to log in with the browser or enter an API key<br>• an Unauthorized: Invalid token or insufficient-credits error: the agent checks firecrawl --status once, reports the blocking reason and stops |
| **Exclusions** | • not for local files, which route to firecrawl-parse<br>• not for research papers, which go to firecrawl-research-index<br>• not for library, API, error or bug questions, which go to firecrawl-developer-index<br>• not for tasks needing capabilities Firecrawl lacks<br>• not for integrating Firecrawl into an app, which goes to the firecrawl-build skills |
| **Adoption** | • skills.sh: 104.3K installs, counting the skill, first seen 21 January 2026 (read 11 November 2026)<br>• GitHub: 683 stars, 122 forks, counting the firecrawl/cli repository, which holds 13 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | • harnesses: not declared<br>• models: not declared<br>• capabilities: tool calling |
| **Harness limits** | • Agent Skills specification: fits, name 9 characters, description 456 characters, body 154 lines and about 2,873 tokens<br>• Codex: does not fit, SKILL.md is 12,060 bytes, 4,060 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 162 lines, listing text 456 characters<br>• ClawHub: fits, folder 16,344 bytes |
| **Software dependencies** | • firecrawl-cli (package), version latest, needed to run<br>• npm and npx (runtime), version not declared, needed to install<br>• jq (binary), version not declared, used in an example |
| **Credentials** | • API key, a key from firecrawl.dev, used for authenticating the CLI when browser login fails, from command argument, goes to Firecrawl, host not named in the files<br>• token, credentials from firecrawl login --browser, used for authenticating the CLI through browser OAuth, from unknown, goes to Firecrawl, host not named in the files |
| **Cost, context** | • discovery about 115 tokens<br>• load about 3,015 tokens<br>• on demand about 1,071 tokens, in rules/install.md and rules/security.md |
| **Cost, per run** | not examined |
| **Cost, services** | • Firecrawl, needs account, price not declared, quota API credits and a concurrency limit, a rate-limited keyless free tier, and feedback refunds of 1 credit up to 10 per website and 100 per team each UTC day, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install changes state, run changes state<br>• installs firecrawl-cli globally with npm or npx, affects software environment, confirmation not declared, reversible not declared<br>• installs core and workflow skills globally across all detected coding editors, affects user home, confirmation not declared, reversible not declared<br>• stores login credentials through the CLI, affects user home, confirmation not declared, reversible not declared<br>• writes result files to .firecrawl/ and adds .firecrawl/ to .gitignore, affects workspace, confirmation not declared, reversible not declared<br>• clicks, fills and submits forms on websites through interact, affects external service, confirmation not declared, reversible not declared<br>• creates monitors that schedule recurring scrapes or crawls, affects external service, confirmation not declared, reversible not declared<br>• uses API credits and sends feedback to Firecrawl, affects external service, confirmation not declared, reversible not declared |
| **Network access** | • the Firecrawl API, host not named in the files: data source, every search, scrape, map, crawl, interact, agent, monitor and download command. Sends credential, query text and user content, receives search results, page content as markdown or JSON, job and credit status.<br>• the Firecrawl feedback endpoint /v2/feedback, host not named in the files: other, after search results are used and after search, scrape, parse or map jobs, unless FIRECRAWL_NO_ENDPOINT_FEEDBACK is set. Sends credential and user content, receives a credit refund for the first feedback per search.<br>• the npm registry, not named in the files: install, when firecrawl-cli is installed or updated. Sends none, receives the firecrawl-cli package.<br>• Firecrawl login in the browser, host not named in the files: auth, on firecrawl login --browser or init --browser. Sends credential, receives credentials stored by the CLI.<br>• firecrawl.dev: other, once, to verify the install. Sends none, receives the page, saved to .firecrawl/install-check.md. |
| **Tools and permissions** | allowed-tools: Bash(firecrawl *), Bash(npx firecrawl-cli *)<br>• firecrawl (program), search, scrape, map, crawl, interact, monitor, download, login, status, feedback and credit usage, third party<br>• npx firecrawl-cli and npm install -g firecrawl-cli (shell command), installing, updating and setting up the CLI and skills, third party<br>• grep, head, wc and jq (shell command), reading output files in bounded parts and working with JSON output, third party<br>• Bash (agent tool), running firecrawl and npx firecrawl-cli commands, built in |
| **Machine access, paths** | • .firecrawl/, write, workspace<br>• .firecrawl/, read, workspace<br>• .gitignore, write, workspace<br>• the npm global install location, write, unknown<br>• skill folders of all detected coding editors, write, unknown<br>• credentials stored by the CLI, write, unknown |
| **Machine access, settings** | • FIRECRAWL_NO_ENDPOINT_FEEDBACK, read, set to 1, the CLI skips every endpoint feedback call<br>• PATH, read, the npm global bin must be in it for firecrawl to be found |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 22 October 2026 | unknown | warn, risk level MEDIUM, 1 issue, W011 third-party content exposure, indirect prompt injection risk, scored low risk 0.10 | [report](https://skills.sh/firecrawl/cli/firecrawl/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 22 October 2026 | SKILL.md, rules/install.md and rules/security.md, as cited in its analysis | pass, risk level SAFE, three categories described, indirect prompt injection, external downloads through npm and npx, and command execution through Bash | [report](https://skills.sh/firecrawl/cli/firecrawl/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 22 October 2026 | the skill package, hash b45d85dc544afeb07d168380a4f00d55e4e37b32f1ab5f06a62df42591d81312 | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/firecrawl/cli/firecrawl/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Third-party content exposure, indirect prompt injection risk, W011 (C1, MEDIUM, open), location not stated. Fix: not stated |
| **Risks** | • Instructions hidden in fetched web pages reach the agent, since search, scrape, crawl and map bring outsider-authored text into its context. Source: author, check C1, check C2. Severity: MEDIUM by C1, SAFE overall by C2. Mitigation: in place as instructions, output isolated in .firecrawl/, read in bounded parts, and instructions in page content not followed. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• An unquoted URL in a shell command can lead to command injection. Source: author. Severity: none. Mitigation: in place as an instruction to always quote URLs. Taxonomy: not examined.<br>• Installing with npx -y firecrawl-cli@latest or npm install -g runs whatever version npm serves at that time with the user's privileges. Source: check C2. Severity: none. Mitigation: none stated, C2 notes the package comes from the official vendor. Taxonomy: not examined.<br>• Clicks, form fills and logins through interact can submit data or change accounts on third-party websites. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• An API key passed with firecrawl login --api-key stays in shell history or logs. Source: model. Severity: none. Mitigation: none stated, browser login is the recommended path. Taxonomy: not examined. |
| **Limitations** | • Gov search filters keep only pages the index has labeled, so a filtered search can leave out relevant pages.<br>• Gov results are excerpts, not a guarantee of official-only sources or current governing law, and no hits does not establish that no applicable law exists.<br>• The keyless free tier is rate-limited, and crawl, map, download, agent, monitor, credit-usage and the feedback commands need an account.<br>• The client cannot be assumed to signal an overflow back to the tool, and Bash cannot be assumed to support search IDs or every provider's retained data.<br>• search --categories research is a website filter, not the paper index. |
| **Known problems** | • Unauthorized: Invalid token or insufficient-credits error: verify config once with firecrawl --status, report the blocking reason and stop, since retrying yields the same error<br>• authentication fails: log in with firecrawl login --browser or firecrawl login --api-key<br>• firecrawl is not found after installation: put the npm global bin in PATH, try npx firecrawl-cli@latest --version, or reinstall<br>• the CLI is missing, stale or only partially configured: re-run npx -y firecrawl-cli@latest init -y --browser<br>• a client context or output error: keep the request or scrape ID and inspect saved output or use scrape firecrawl/bash before repeating the request |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the firecrawl organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: none |
| **Maintenance status** | • last change 22 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 18 August 2026<br>• content changes 17 since first seen<br>• releases 98<br>• last release 6 November 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:6792d1a7a58a75a56aaeafb879f221294663e0f2a432b4e6c0a67ed27c800dd8`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 06b371f0 |
| **Source** | • repository, GitHub firecrawl/cli, path skills/firecrawl, commit 06b371f0, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/firecrawl/cli/firecrawl<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 12,060 bytes, document<br>• rules/install.md, 2,889 bytes, document<br>• rules/security.md, 1,395 bytes, document |
| **File counts** | 3 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 52 |
