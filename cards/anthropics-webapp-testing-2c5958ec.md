# Skill Card: webapp-testing anthropics/skills at 2c5958ec

## 1. What it does

| Field | Value |
|---|---|
| **Name** | webapp-testing |
| **Description** | Instructions, one helper script and three example scripts for testing local web applications with native Python Playwright scripts. The helper with_server.py starts one or more servers, waits until their ports answer, runs an automation command and then stops the servers. The automation navigates to the app, waits for networkidle, takes screenshots or inspects the rendered DOM to find selectors, and then acts with those selectors, with examples for element discovery, static HTML through file:// URLs and console log capture. Use it to verify frontend functionality, debug UI behavior, capture browser screenshots and view browser logs. |
| **Tasks** | • start one or more local servers, run an automation command, then stop them<br>• inspect the rendered DOM and take screenshots to find selectors<br>• click, fill and submit forms with Playwright<br>• automate static HTML files through file:// URLs<br>• capture browser console logs<br>• works on local web applications |
| **Author's description** | "Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs." |
| **Outputs** | • Playwright automation scripts written for the task (information), Python file, to a path the agent chooses, for instance your_automation.py<br>• screenshots of the page, full page (information), PNG file, to /tmp/inspect.png, /tmp/page_discovery.png or /mnt/user-data/outputs/static_page.png<br>• browser console messages (information), text file and terminal text, to /mnt/user-data/outputs/console.log and the terminal<br>• lists of buttons, links and input fields found on the page (information), terminal text, to the terminal the agent runs the script in<br>• server start, readiness and stop messages (information), terminal text, to the terminal the agent runs the script in<br>• clicks, form entries and form submissions in the app under test (action), browser interaction, to the web application under test |
| **Sample output** | `Screenshot saved to /tmp/page_discovery.png` |
| **Inputs** | • the address of a running local web application, a localhost URL, conditional for testing a dynamic webapp, example `page.goto('http://localhost:5173')`<br>• a static HTML file, a path turned into a file:// URL, conditional for testing static HTML, example `html_file_path = os.path.abspath('path/to/your/file.html')`<br>• a command that starts a server, a --server argument, repeatable, conditional for a server that is not already running, example `--server "cd backend && python server.py"`<br>• the port of each server, a --port argument, an integer, one per --server, conditional for a server that is not already running, example `--port 5173`<br>• the command to run once the servers are ready, arguments after --, conditional for a server that is not already running, example `-- python your_automation.py`<br>• a timeout per server in seconds, a --timeout argument, an integer, default 30, optional for a server that starts slowly, example not declared |
| **When an input is missing** | • no command follows the server arguments: with_server.py prints Error: No command specified to run and exits<br>• the counts of --server and --port arguments differ: with_server.py prints Error: Number of --server and --port arguments must match and exits<br>• a server does not open its port within the timeout: with_server.py raises Server failed to start on port and stops the servers it started<br>• reading a static HTML file fails or is incomplete: the app is treated as dynamic |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 202.4K installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 192,784 stars, 22,682 forks, counting the anthropics/skills repository, which holds 20 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 14 characters, description 204 characters, body 91 lines and about 907 tokens<br>• Codex: fits, SKILL.md is 3,913 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 96 lines, listing text 204 characters<br>• ClawHub: fits, folder 22,394 bytes |
| **Software dependencies** | • Python (runtime), version not declared, needed to run<br>• playwright, sync_api (package), version not declared, needed to run<br>• Chromium, launched headless through Playwright (binary), version not declared, needed to run<br>• npm (binary), version not declared, used in an example |
| **Credentials** | none |
| **Cost, context** | • discovery about 51 tokens<br>• load about 978 tokens<br>• on demand about 861 tokens, in examples/element_discovery.py, examples/static_html_automation.py and examples/console_logging.py |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• starts server processes from shell commands and stops them after the run, affects system, confirmation not declared, reversible yes<br>• writes screenshots to /tmp, affects system, confirmation not declared, reversible not declared<br>• writes screenshots and console.log to /mnt/user-data/outputs, affects system, confirmation not declared, reversible not declared<br>• creates Playwright automation scripts, affects workspace, confirmation not declared, reversible not declared<br>• clicks, fills and submits forms in the app under test, affects other, confirmation not declared, reversible not declared |
| **Network access** | • localhost, on the ports given, for instance 5173 and 3000: other, every run, for the readiness check and the browser session. Sends user content, receives the rendered pages and console messages of the app under test. |
| **Tools and permissions** | allowed-tools: none<br>• python scripts/with_server.py (program), starting servers, waiting for their ports, running the automation, stopping the servers, skill<br>• Playwright with headless Chromium (program), navigating, inspecting, screenshotting and acting on pages, third party<br>• server commands such as npm run dev or python server.py (shell command), starting the app under test, run through the shell, third party<br>• shell and file tools of the agent (agent tool), running the scripts and writing the automation scripts, built in |
| **Machine access, paths** | • scripts/with_server.py, run from the skill folder, read, skill folder<br>• local HTML files the user names, such as path/to/your/file.html, read, workspace<br>• automation scripts such as your_automation.py, write, workspace<br>• /tmp/inspect.png and /tmp/page_discovery.png, write, system<br>• /mnt/user-data/outputs/, console.log, static_page.png and after_submit.png, write, system |
| **Machine access, settings** | none |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 14 September 2026 | unknown | warn, risk level MEDIUM, 1 issue, W011 third-party content exposure, indirect prompt injection risk, scored low risk 0.10 | [report](https://skills.sh/anthropics/skills/webapp-testing/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 14 September 2026 | scripts/with_server.py, examples/element_discovery.py and examples/console_logging.py, as cited in its analysis | pass, risk level SAFE, two surfaces described, with_server.py runs shell commands with shell=True, and web content reaches the agent without delimiters or sanitisation | [report](https://skills.sh/anthropics/skills/webapp-testing/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 14 September 2026 | the skill package, hash cfb23ef0c399c36e9247142a7ab5ac0e03c03e1c9f047b0f7502232a2c50b564 | warn, 1 alert, Anomaly LOW in scripts/with_server.py, shell=True with command strings from the command line, confidence 60%, severity 55% | [report](https://skills.sh/anthropics/skills/webapp-testing/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Third-party content exposure, indirect prompt injection risk, W011 (C1, MEDIUM, open), location not stated. Fix: not stated<br>• Anomaly, subprocess.Popen with shell=True on command strings from the command line (C3, LOW, confidence 60%, severity 55%, open), location scripts/with_server.py. Fix: not stated |
| **Risks** | • Instructions hidden in a tested page reach the agent, since DOM content and console logs are read into its context without delimiters or sanitisation. Source: check C1, check C2. Severity: MEDIUM by C1, SAFE overall by C2. Mitigation: none in the files, C2 notes that no boundary markers or filtering are used. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• A --server command built from untrusted input runs arbitrary code with the agent's privileges, since with_server.py passes it to the shell with shell=True. Source: check C3, check C2. Severity: LOW by C3, SAFE overall by C2. Mitigation: none stated. Taxonomy: not examined.<br>• Running the automation against an app connected to real data can change that data, since the examples click buttons and submit forms without asking. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• Screenshots and logs written to /tmp and /mnt/user-data/outputs can hold data shown by the app and stay there after the run. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | • The bundled scripts can be very large, and reading their source fills the context window, so they are run as black boxes with --help first.<br>• with_server.py checks readiness only by polling the given port on localhost, 30 seconds per server by default.<br>• Inspecting the DOM of a dynamic app before networkidle gives an incomplete picture of the page.<br>• No dependency carries a version. |
| **Known problems** | • DOM inspected before a dynamic app finished loading: wait for page.wait_for_load_state('networkidle') before inspection<br>• selectors from a static HTML file fail or are incomplete: treat the app as dynamic and use reconnaissance-then-action<br>• a server fails to start on its port within the timeout: raise the limit with --timeout |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author Anthropic, PBC, from the license file<br>• publisher the anthropics organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: Complete terms in LICENSE.txt<br>• license file: LICENSE.txt, Apache License Version 2.0, January 2004, copyright 2026 Anthropic, PBC<br>• skills.sh: not declared<br>• GitHub repository: none |
| **Maintenance status** | • last change 20 April 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 1 December 2025<br>• content changes 1 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:31ebb48bce8e86083126a45fe62f42d1352259f07a410807d07f038bb1c954a3`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 2c5958ec |
| **Source** | • repository, GitHub anthropics/skills, path skills/webapp-testing, commit 2c5958ec, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/anthropics/skills/webapp-testing<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • LICENSE.txt, 11,345 bytes, document<br>• SKILL.md, 3,913 bytes, document<br>• examples/console_logging.py, 1,027 bytes, script<br>• examples/element_discovery.py, 1,463 bytes, script<br>• examples/static_html_automation.py, 953 bytes, script<br>• scripts/with_server.py, 3,693 bytes, script, executable |
| **File counts** | 2 documents, 4 scripts, 0 data, 0 binary, instructions with scripts |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 42 |
