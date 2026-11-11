# Skill Card: hf-cli huggingface/skills at 25910b3d

## 1. What it does

| Field | Value |
|---|---|
| **Name** | hf-cli |
| **Description** | A single SKILL.md, generated with huggingface_hub v2.4.0, that lists the commands and options of the Hugging Face Hub CLI hf. It covers downloading and uploading files, managing repos, buckets, collections, discussions and pull requests, browsing models, datasets, spaces and papers, querying datasets with SQL, running jobs and sandboxes on Hugging Face infrastructure, and deploying Inference Endpoints. Results are files on disk, changes on the Hub, and command output in auto, human, agent, json or quiet format. Use it whenever the user mentions hf, huggingface or Hugging Face, or wants to do anything in the Hugging Face ecosystem. |
| **Tasks** | • download, upload, copy and sync files between local paths, repos and buckets<br>• manage repos, branches, tags, collections, discussions and pull requests on the Hub<br>• browse and search models, datasets, spaces and papers, and query datasets with DuckDB SQL<br>• run and schedule Jobs and sandboxes on Hugging Face infrastructure<br>• deploy and manage Inference Endpoints and configure Spaces<br>• manage authentication, the local cache, webhooks, extensions and skills |
| **Author's description** | "Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datasets, spaces, buckets, repos, papers, jobs, and more on the Hugging Face Hub. Use when: handling authentication; managing local cache; managing Hugging Face Buckets; running or scheduling jobs on Hugging Face infrastructure; managing Hugging Face repos; discussions and pull requests; browsing models, datasets and spaces; reading, searching, or browsing academic papers; managing collections; querying datasets; configuring spaces; setting up webhooks; or deploying and managing HF Inference Endpoints. Make sure to use this skill whenever the user mentions 'hf', 'huggingface', 'Hugging Face', 'huggingface-cli', or 'hugging face cli', or wants to do anything related to the Hugging Face ecosystem and to AI and ML in general. Also use for cloud storage needs like training checkpoints, data pipelines, or agent traces. Use even if the user doesn't explicitly ask for a CLI command. Replaces the deprecated `huggingface-cli`." |
| **Outputs** | • files downloaded from Hub repos and buckets (information), model, dataset or space files, to the Hugging Face cache, --cache-dir or --local-dir<br>• listings, info, cards, papers, logs and query results (information), terminal text in auto, human, agent, json or quiet format, to the terminal the agent runs hf in<br>• files uploaded, synced, copied or deleted on the Hub and in buckets (action), commits, pull requests and bucket changes, to Hub repos and Hugging Face Buckets<br>• repos, collections, discussions, webhooks and settings created, changed or deleted (action), changes to the user's Hub account, to the Hugging Face Hub<br>• Jobs, scheduled Jobs, sandboxes and Inference Endpoints started, paused, scaled or deleted (action), running workloads on Hugging Face infrastructure, to Hugging Face Jobs and Inference Endpoints |
| **Sample output** | not declared |
| **Inputs** | • a repo, bucket, collection, job, endpoint or space identifier, a positional argument, required for every command that acts on one item, example `hf-mount start repo openai-community/gpt2 /tmp/gpt2`<br>• a User Access Token, the HF_TOKEN environment variable or the --token option, conditional for authenticated and write operations, example `hf-mount start --hf-token $HF_TOKEN bucket myuser/my-bucket /tmp/data`<br>• local files or a folder, a path argument, conditional for uploading, copying and syncing, example not declared<br>• a container image and command, or a UV script, positional arguments, the script a local file or URL, conditional for running and scheduling Jobs, example not declared<br>• a SQL query, a positional argument, conditional for querying datasets with hf datasets sql, example not declared<br>• environment variables and secrets for remote workloads, --env, --secrets, --env-file or --secrets-file options, optional for Jobs, sandboxes, Spaces, repos and Inference Endpoints, example not declared |
| **When an input is missing** | not declared |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 3.6K installs, counting the skill, first seen 6 March 2026 (read 11 November 2026)<br>• GitHub: 11,333 stars, 792 forks, counting the huggingface/skills repository, which holds 26 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 6 characters, description 1,008 characters, body 239 lines and about 8,288 tokens, over the recommended 5,000 tokens<br>• Codex: does not fit, SKILL.md is 34,197 bytes, 26,197 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 243 lines, listing text 1,008 characters<br>• ClawHub: fits, folder 34,197 bytes |
| **Software dependencies** | • hf CLI from huggingface_hub (package), version v2.4.0, the version the command list was generated with, needed to run<br>• curl and bash (binary), version not declared, needed to install<br>• hf-mount (binary), version not declared, used in an example<br>• brew (binary), version not declared, used in an example |
| **Credentials** | • token, User Access Token, HF_TOKEN, used for authenticating to the Hugging Face Hub, from environment variable, goes to huggingface.co<br>• password, --container-registry-password, used for pulling a custom image for an Inference Endpoint, from command argument, goes to huggingface.co<br>• other, --secrets and --secrets-file, used for secrets for Jobs, sandboxes, Spaces, repos and Inference Endpoints, from command argument, goes to huggingface.co<br>• other, webhook --secret, used for signing webhook calls, from command argument, goes to huggingface.co |
| **Cost, context** | • discovery about 252 tokens<br>• load about 8,549 tokens<br>• on demand none |
| **Cost, per run** | not examined |
| **Cost, services** | • Hugging Face Jobs and sandboxes, with hardware flavors from cpu-basic to h200x8, needs account, price not declared, quota not declared, calls per use not declared<br>• Hugging Face Inference Endpoints, needs account, price not declared, quota not declared, calls per use not declared<br>• ZeroGPU on Spaces, needs account, price not declared, quota remaining GPU time and reset date, shown by hf spaces zero-gpu quota, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install changes state, run changes state<br>• installs the hf CLI by piping https://hf.co/cli/install.sh to bash, affects software environment, confirmation not declared, reversible not declared<br>• updates the CLI, installs extensions from GitHub and installs skills, affects software environment, confirmation not declared, reversible not declared<br>• downloads files into the cache or a local directory, and removes cached files with hf cache rm and prune, affects user home, confirmation not declared, reversible not declared<br>• uploads, copies, syncs and deletes files in Hub repos and buckets, affects external service, confirmation not declared, reversible not declared<br>• deletes a repo from the Hub, an irreversible operation, affects external service, confirmation not declared, reversible no<br>• deletes an Inference Endpoint or a webhook permanently, affects external service, confirmation not declared, reversible no<br>• creates, moves and changes repos, buckets, collections, discussions, settings, secrets and variables, affects external service, confirmation not declared, reversible not declared<br>• runs Jobs and sandboxes and deploys, scales or pauses Inference Endpoints, affects external service, confirmation not declared, reversible not declared<br>• stores the token in the git credential store with --add-to-git-credential, affects user home, confirmation not declared, reversible not declared |
| **Network access** | • hf.co: install, once, when the CLI is installed with the install script. Sends none, receives the install script install.sh.<br>• huggingface.co: other, every Hub command, for reading, uploading, syncing, running Jobs and deploying endpoints. Sends credential, query text, file content and user content, receives files, listings, cards, papers, logs and job output.<br>• github.com: install, when extensions are searched, installed or updated, or hf-mount is downloaded. Sends query text, receives extension code and hf-mount binaries.<br>• the Homebrew package host, not named in the files: install, when hf-mount is installed with brew. Sends none, receives the hf-mount package. |
| **Tools and permissions** | allowed-tools: none<br>• hf (program), every Hub, cache, job, endpoint and auth operation, third party<br>• curl -LsSf https://hf.co/cli/install.sh \| bash -s (shell command), installing the hf CLI, third party<br>• hf-mount (program), mounting repos and buckets as local filesystems, third party<br>• brew install hf-mount (shell command), installing hf-mount, third party<br>• hf extensions (program), installing and executing extensions from public GitHub repositories, third party<br>• shell tool of the agent (agent tool), running hf and hf-mount commands, built in |
| **Machine access, paths** | • the Hugging Face cache or the directory given with --cache-dir, write, unknown<br>• cached repositories, revisions and incomplete downloads removed by hf cache rm and prune, delete, unknown<br>• the directory given with --local-dir, write, unknown<br>• local files and folders uploaded, copied or synced, read, unknown<br>• local files deleted by hf sync --delete, delete, unknown<br>• files given with --env-file, --secrets-file, --body-file and --identity-file, read, unknown<br>• mount points such as /tmp/gpt2 and /tmp/data, write, system<br>• the skill destination given with --dest or --global, write, unknown |
| **Machine access, settings** | • git credential store, set, with --add-to-git-credential, so git can use the access token |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 30 October 2026 | unknown | warn, risk level MEDIUM, 1 issue, W011 third-party content exposure, indirect prompt injection risk, scored medium risk 0.30 | [report](https://skills.sh/huggingface/skills/hf-cli/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 30 October 2026 | the commands of SKILL.md, as cited in its analysis | pass, risk level SAFE, tags EXTERNAL_DOWNLOADS, REMOTE_CODE_EXECUTION, COMMAND_EXECUTION, CREDENTIALS_UNSAFE and INDIRECT_PROMPT_INJECTION, six surfaces described | [report](https://skills.sh/huggingface/skills/hf-cli/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 30 October 2026 | the skill package, hash 5e956f66479b98cb38530a42a0b71ef535c0f5ca15b265dcd079241b21a4b5e9 | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/huggingface/skills/hf-cli/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Third-party content exposure, indirect prompt injection risk, W011 (C1, MEDIUM, scored 0.30, open), location not stated. Fix: not stated |
| **Risks** | • Instructions hidden in outsider-authored discussions, pull requests, model cards, dataset info or papers reach the agent when it reads them through hf. Source: check C1, check C2. Severity: MEDIUM by C1, SAFE overall by C2. Mitigation: none in the files. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• The install command pipes a script fetched from hf.co straight into bash, so whatever that script contains runs on the machine. Source: check C2. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• hf auth token prints the current access token to stdout, where it enters the agent's context and terminal logs. Source: check C2. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• hf extensions install downloads third-party code from public GitHub repositories, which then runs through hf extensions exec. Source: check C2. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• hf jobs run, hf jobs uv run and hf sandbox exec execute arbitrary code on Hugging Face infrastructure under the user's account. Source: check C2. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• A repo removed with hf repos delete is lost, since the operation is irreversible. Source: author. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• Jobs, sandboxes and Inference Endpoints started on GPU flavors such as a100x8 or h200x8 keep incurring charges until they are cancelled, paused or deleted. Source: model. Severity: none. Mitigation: none stated, --timeout and --scale-to-zero-timeout exist as options. Taxonomy: not examined.<br>• An access token passed with --token stays in shell history or logs. Source: model. Severity: none. Mitigation: the files recommend setting HF_TOKEN instead of passing --token. Taxonomy: not examined. |
| **Limitations** | • Secret values of a Space are write-only and are not returned by hf spaces secrets list.<br>• Sandboxes on Hugging Face Jobs are experimental.<br>• A repo mounted with hf-mount is read-only, a bucket is read-write.<br>• The command list reflects huggingface_hub v2.4.0, full options and examples come from hf &lt;command> --help. |
| **Known problems** | • the huggingface-cli command is deprecated: use hf, with auth commands under hf auth |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the huggingface organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: Apache-2.0, as GitHub detects it |
| **Maintenance status** | • last change 29 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 6 March 2026<br>• content changes 45 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:ed52172e86a292ddbeac3aa34cc899adeb2b4f5f4000cb7368cb40360d8155de`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 25910b3d |
| **Source** | • repository, GitHub huggingface/skills, path skills/hf-cli, commit 25910b3d, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/huggingface/skills/hf-cli<br>• homepage not declared<br>• produced by a tool: huggingface_hub v2.4.0, as SKILL.md states, regenerated with hf skills add --force |
| **File list** | • SKILL.md, 34,197 bytes, document |
| **File counts** | 1 document, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 78 |
