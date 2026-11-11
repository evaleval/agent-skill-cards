# Skill Card: google-agents-cli-adk-code google/agents-cli at 896e4719

## 1. What it does

| Field | Value |
|---|---|
| **Name** | google-agents-cli-adk-code |
| **Description** | Reference documents for writing agent code with ADK (Agent Development Kit) in Python and Go. Cheatsheets cover agent types, tools, callbacks, plugins, state, memory, artifacts, multi-agent orchestration, the graph Workflow API and live voice agents, and a topic index maps each capability to a recipe in google/adk-recipes to clone and study. The result is agent code written into a project already scaffolded with agents-cli. Use it when the user wants to write agent code, add a tool, create a callback or define an agent with ADK, not for scaffolding or deployment. |
| **Tasks** | • write ADK agents, tools and callbacks in Python or Go<br>• orchestrate multi-agent systems with sequential, parallel and loop agents<br>• build graph workflows with routing, fan-out, fan-in and human-in-the-loop<br>• build live voice and video agents with run_live<br>• find and study the reference recipe for a capability<br>• look up ADK docs through the llms.txt index or the installed package |
| **Author's description** | "This skill should be used when the user wants to "write agent code", "build an agent with ADK", "add a tool", "create a callback", "define an agent", "use state management" — in a project that needs ADK (Agent Development Kit) API patterns and code examples. It provides a quick reference for agent types, tool definitions, orchestration patterns, callbacks, state management, the graph Workflow API, and reference recipes to study. Do NOT use for scaffolding (use google-agents-cli-scaffold) or deployment (use google-agents-cli-deploy)." |
| **Outputs** | • agent code, tools, callbacks and workflows (information), Python or Go source files, to the scaffolded project, for instance app/agent.py or app/agent.go<br>• integration tests rewritten for a Live agent (information), Python test files, to tests/integration/test_agent.py and tests/integration/test_server_e2e.py<br>• the recipe that implements a needed capability (recommendation), text in the conversation, to the conversation with the user<br>• a sparse clone of google/adk-recipes (information), git checkout, to /tmp/adk-recipes |
| **Sample output** | `agent.py, Contains root_agent definition` |
| **Inputs** | • a project scaffolded with agents-cli, a project directory with agents-cli config, required for writing agent code, example `agents-cli info`<br>• the capability or question the user has, a request in natural language, required for every task, example `how do I build X`<br>• a spec agreed with the user, the spec of workflow Phase 0, conditional for a new project with no code yet, example not declared<br>• the language of the agent, Python or Go, required for choosing the reference to read, example not declared |
| **When an input is missing** | • no project is scaffolded: no agent code is written, /google-agents-cli-workflow is loaded and the spec agreed with the user before scaffolding<br>• existing code without agents-cli config: agents-cli scaffold enhance . is run first<br>• no core recipe covers the capability: check contrib/ or build it yourself, without guessing at a recipe name |
| **Exclusions** | • not for scaffolding, use google-agents-cli-scaffold<br>• not for deployment, use google-agents-cli-deploy<br>• the Live reference is not for turn-based request and response agents, use a normal Agent with run_async |
| **Adoption** | • skills.sh: 564.9K installs, counting the skill, first seen 21 April 2026 (read 11 November 2026)<br>• GitHub: 6,339 stars, 733 forks, counting the google/agents-cli repository, which holds 9 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 26 characters, description 538 characters, body 52 lines and about 909 tokens<br>• Codex: fits, SKILL.md is 4,407 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 73 lines, listing text 538 characters<br>• ClawHub: fits, folder 145,336 bytes |
| **Software dependencies** | • agents-cli (binary), version not declared, needed to run<br>• google-agents-cli (package), version not declared, needed to install<br>• uv (binary), version not declared, needed to install<br>• git (binary), version not declared, needed to run<br>• curl (binary), version not declared, needed to run<br>• google-adk (package), version >= 2.0.0 for the Workflow API, >= 2.4.0 for ManagedAgent, used in an example<br>• Python (runtime), version >= 3.11 for the Workflow API, used in an example<br>• google.golang.org/adk/v2 (package), version v2.1.0 as the adk_go template pins, >= v2.0.0 for workflows, used in an example<br>• Go (runtime), version not declared, used in an example<br>• google-adk[a2a] and the mcp extra (package), version not declared, used in an example<br>• a2ui-agent-sdk (package), version not declared, used in an example<br>• Node.js and npx (runtime), version not declared, used in an example |
| **Credentials** | • API key, GEMINI_API_KEY or GOOGLE_API_KEY, used for Gemini models on AI Studio and managed agents on the Gemini API, from environment variable, goes to the Gemini API, host not named in the files<br>• token, Application Default Credentials from gcloud auth application-default login, used for Gemini platform, Agent Runtime and authenticated MCP toolsets, from unknown, goes to {location}-aiplatform.googleapis.com and the MCP server<br>• API key, OPENAI_API_KEY, used for OpenAI models from ADK Go, from environment variable, goes to the endpoint in OPENAI_BASE_URL<br>• token, ID token from fetch_id_token, used for calling a remote MCP server on Cloud Run, from unknown, goes to the MCP server at MCP_SERVER_URL<br>• other, OAuth2 client_id and client_secret, service account, API key for tools, used for authenticating tools and OpenAPI toolsets, from unknown, goes to the API the tool calls |
| **Cost, context** | • discovery about 135 tokens<br>• load about 1,102 tokens<br>• on demand about 35,234 tokens, in references/recipes.md, references/adk-python.md, references/adk-python-workflows.md, references/adk-python-live.md, references/adk-go.md and references/adk-go-workflows.md |
| **Cost, per run** | not examined |
| **Cost, services** | • Gemini Live API, needs API key, price not declared, quota audio-only sessions 15 min, audio and video 2 min, connection about 10 min, absent compression, calls per use not declared<br>• Agent Runtime in Gemini platform, needs account, price not declared, quota Live sessions 10 min, absent compression, calls per use not declared<br>• Pub/Sub and Eventarc, needs account, price not declared, quota 10-minute processing limit, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install changes state, run changes state<br>• writes and edits agent code, tests and dependencies in the project, affects workspace, confirmation not declared, reversible not declared<br>• deletes app/app_utils/a2a.py and the A2A tests when converting a project to Live, affects workspace, confirmation not declared, reversible not declared<br>• runs agents-cli scaffold enhance . on existing code, affects workspace, confirmation not declared, reversible not declared<br>• clones google/adk-recipes into /tmp/adk-recipes, affects system, confirmation not declared, reversible not declared<br>• installs google-agents-cli with uv tool install, affects software environment, confirmation not declared, reversible not declared<br>• deploys a Live agent with agents-cli deploy, affects external service, confirmation not declared, reversible not declared |
| **Network access** | • adk.dev: data source, when the docs index llms.txt and a docs page are fetched. Sends none, receives the docs index and pages.<br>• github.com: data source, when google/adk-recipes or the google/adk-go examples are cloned. Sends none, receives recipe and example source code.<br>• package index, not named in the files: install, when google-agents-cli is installed with uv. Sends none, receives the package.<br>• {location}-aiplatform.googleapis.com: model call, when an agent deployed to Agent Runtime is called or a Live session runs. Sends credential and user content, receives agent events and audio. |
| **Tools and permissions** | allowed-tools: none<br>• agents-cli info, scaffold enhance, playground, run, eval run, deploy (program), checking the project, enhancing it, testing and evaluating agents, third party<br>• git clone and git sparse-checkout (shell command), fetching a recipe to study, third party<br>• curl https://adk.dev/llms.txt (shell command), fetching the docs index, third party<br>• uv tool install google-agents-cli (shell command), installing agents-cli, third party<br>• python -c "import google.adk; print(google.adk.__path__[0])" (shell command), finding the installed ADK package, third party<br>• WebFetch, Glob, Grep and Read (agent tool), reading docs pages and the installed ADK source, built in |
| **Machine access, paths** | • the project, app/agent.py, app/agent.go, app/fast_api_app.py, tests/ and .env, write, workspace<br>• app/app_utils/a2a.py when converting to Live, delete, workspace<br>• /tmp/adk-recipes, write, system<br>• the installed google/adk package, read, unknown<br>• references/ in the skill folder, read, skill folder |
| **Machine access, settings** | • GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, GOOGLE_GENAI_USE_ENTERPRISE, read, selecting the Gemini platform backend<br>• LIVE_MODEL and LIVE_LOCATION, read, overriding the Live model and its region<br>• ADK_TRIGGER_MAX_CONCURRENT, ADK_TRIGGER_MAX_RETRIES, ADK_TRIGGER_RETRY_BASE_DELAY, ADK_TRIGGER_RETRY_MAX_DELAY, read, limits of the trigger endpoints<br>• OPENAI_BASE_URL, read, the OpenAI-compatible endpoint for ADK Go |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 4 November 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/google/agents-cli/google-agents-cli-adk-code/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 4 November 2026 | SKILL.md, the metadata and the reference files, as cited in its analysis | pass, risk level SAFE, a flagged curl command judged a false positive, vendor domains, uv install and documentation described | [report](https://skills.sh/google/agents-cli/google-agents-cli-adk-code/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 4 November 2026 | the skill package, hash 38719b6fa7220cab4992a697bd902d1e546dbde1527d48cb7574d9e81841b6d4 | pass, checks for malicious behavior, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/google/agents-cli/google-agents-cli-adk-code/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • Instructions hidden in a cloned recipe AGENTS.md or a fetched docs page reach the agent, since these are read before implementing, and contrib recipes are not curated. Source: model. Severity: none. Mitigation: none stated. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• A directory already at /tmp/adk-recipes is read as the recipes without a fresh clone, so content placed there by another process reaches the agent. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | • The Python Workflow API requires google-adk 2.0.0 or later and Python 3.11 or later.<br>• Using output_schema disables tool calling and delegation.<br>• google_search is model-internal grounding, and mixing it with function tools disables automatic function calling for all tools.<br>• Live agents cannot be served over A2A or published to Gemini, and Live models reject text output.<br>• ManagedAgent requires ADK 2.4.0 or later, and client-side tools raise NotImplementedError.<br>• ADK Go has no OpenAPI toolset.<br>• The Go reference reflects google.golang.org/adk/v2 v2.1.0, so a symbol can be missing in another version.<br>• The eleven core Python recipes are the complete set, other capabilities need contrib/ or own code.<br>• InMemoryMemoryService memories do not persist across restarts.<br>• Pub/Sub and Eventarc have a 10-minute processing limit. |
| **Known problems** | • "Session not found" errors during evaluation: set the App name to the basename of the agent directory<br>• "agent already has a parent" errors: build sub-agents with factory functions and call them<br>• importing load_web_page from google.adk.tools imports the module: import it from google.adk.tools.load_web_page<br>• run_live raises "Session not found": create the session before run_live<br>• a Live model fails under the global location: pin the region with client_kwargs location on the model<br>• a client stopping at turnComplete truncates -extended-thinking answers: read interaction_status until IDLE<br>• a Go graph hangs when a route is conditional into a JoinNode: never route conditionally into a JoinNode<br>• Go sample tests break unseen after replacing the sample tools: rewrite app/agent_test.go in the same change and run go test ./... |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author Google, from the SKILL.md frontmatter metadata<br>• publisher the google organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: Apache-2.0, in the metadata block<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: Apache-2.0, as GitHub detects it |
| **Maintenance status** | • last change 4 November 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 14 April 2026<br>• content changes 35 since first seen<br>• releases 29<br>• last release 4 November 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:264b8a44f1545e4b998cd46b07230c371b738b13a6d65e74a73031244912af92`, files left out none<br>• author version 1.13.0<br>• registry version not declared<br>• commit 896e4719 |
| **Source** | • repository, GitHub google/agents-cli, path skills/google-agents-cli-adk-code, commit 896e4719, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/google/agents-cli/google-agents-cli-adk-code<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 4,407 bytes, document<br>• references/adk-go-workflows.md, 17,980 bytes, document<br>• references/adk-go.md, 23,231 bytes, document<br>• references/adk-python-live.md, 34,967 bytes, document<br>• references/adk-python-workflows.md, 17,334 bytes, document<br>• references/adk-python.md, 38,047 bytes, document<br>• references/recipes.md, 9,370 bytes, document |
| **File counts** | 7 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 57 |
