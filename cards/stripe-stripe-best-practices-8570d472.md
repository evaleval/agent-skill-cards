# Skill Card: stripe-best-practices stripe/ai at 8570d472

## 1. What it does

| Field | Value |
|---|---|
| **Name** | stripe-best-practices |
| **Description** | Instructions and six reference documents for planning, building and reviewing Stripe integrations. A routing table sends each kind of integration, payments, Connect, billing, tax, Treasury or security, to a recommended API and a reference file, and critical rules set the latest API version 2026-10-28.endive, restricted API keys, dynamic payment methods and required webhooks. What comes out is advice and integration code, and with Stripe CLI or MCP access also checks run on the account, such as a test tax calculation. Use it when planning, building, modifying, testing or reviewing any Stripe integration. |
| **Tasks** | • choose between Checkout Sessions, PaymentIntents and Setup Intents<br>• set up Connect platforms and marketplaces with Accounts v2<br>• plan subscriptions and usage-based billing with Billing APIs and Metronome<br>• set up Stripe Tax registrations and automatic_tax<br>• secure API keys, webhooks, OAuth flows and Dashboard access<br>• migrate from deprecated Stripe APIs<br>• use separate sandboxes for development and testing |
| **Outputs** | • recommended APIs, account configurations and remaining integration steps (recommendation), answer text, to the conversation<br>• integration code that instantiates a StripeClient and calls the recommended APIs (information), source code, to the user's project<br>• a brief Stripe Tax note at the end of every Billing setup or subscription answer (information), answer text, to the conversation<br>• results of a test Tax Calculation and threshold monitoring, reported with taxability_reason (information), answer text, to the conversation<br>• a sandbox test account with test API keys from stripe sandbox create (action), Stripe sandbox, to Stripe<br>• tax registrations created or expired after the user confirms (action), registration through the Tax Registrations API, to the user's Stripe account |
| **Sample output** | `Stripe Tax doesn’t support that region yet` |
| **Inputs** | • the integration the user is planning, building or reviewing, a request in natural language or existing code, required for every task, example not declared<br>• the business model of a Connect platform, a description of who owns the customer relationship, conditional for choosing a Connect charge pattern, example `buyers purchase through our platform`<br>• the jurisdictions where the business sells and is registered, a list of jurisdictions confirmed by the user, conditional for Stripe Tax setup and registrations, example not declared<br>• a Stripe account with execution access, MCP tools or the Stripe CLI with a valid token, optional for reading Tax Settings, running test calculations and threshold monitoring, example `stripe whoami --format json`<br>• an API version, a version string, optional for every task, example `2026-10-28.endive` |
| **When an input is missing** | • the user has no Stripe account: the Stripe CLI creates a sandbox test account with test API keys through stripe sandbox create<br>• the user specifies no API version or SDK: the latest API version and SDK are used<br>• the jurisdictions are unknown: ask where the business sells, direct the user to their tax advisor, then record only confirmed registrations<br>• only read or advisory access to the account: do not claim the tax setup is verified and point the user to Testing Stripe Tax<br>• the metronome skill is not installed: read it from https://docs.stripe.com/.well-known/skills/metronome/SKILL.md before continuing<br>• the request does not clearly fit a single domain: consult Integration Options, API Tour and the Go Live Checklist |
| **Exclusions** | • not for Metronome implementation questions, which go to the metronome skill<br>• not for deciding where a user must register for tax or whether they are legally obligated<br>• unsupported tax types such as customs duties and excise taxes are out of scope |
| **Adoption** | • skills.sh: 101.8K installs, counting the skill, first seen 21 January 2026 (read 11 November 2026)<br>• GitHub: 2,055 stars, 387 forks, counting the stripe/ai repository, which holds 10 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 21 characters, description 893 characters, body 62 lines and about 1,319 tokens<br>• Codex: fits, SKILL.md is 6,247 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 79 lines, listing text 893 characters<br>• ClawHub: fits, folder 71,355 bytes |
| **Software dependencies** | • Stripe CLI, @stripe/cli (package), version not declared, needed to run<br>• npm (binary), version not declared, needed to install<br>• Stripe SDKs for Ruby, Python, Node.js, PHP, Java, Go and .NET (package), version latest versions Ruby 20.0.0, Python 16.0.0, Node.js 23.0.0, PHP 22.0.0, Java 34.0.0, Go 87.0.0, .NET 53.0.0, used in an example |
| **Credentials** | • API key, restricted API key (RAK) with rk_ prefix, or secret key with sk_ prefix, used for calling the Stripe API from the integration and the CLI, from unknown, goes to Stripe, host not named in the files<br>• token, a valid token of the Stripe CLI, used for execution access to the account through the CLI, from unknown, goes to Stripe, host not named in the files<br>• other, webhook signing secret, used for verifying webhook signatures, from unknown, stays on the machine |
| **Cost, context** | • discovery about 223 tokens<br>• load about 1,562 tokens<br>• on demand about 16,277 tokens, in references/payments.md, references/connect.md, references/billing.md, references/tax.md, references/treasury.md and references/security.md |
| **Cost, per run** | not examined |
| **Cost, services** | • Stripe, needs account, price not declared, quota not declared, calls per use not declared<br>• Stripe Tax with Tax Complete, for Register for me and automated filing, needs subscription, price not declared, quota not declared, calls per use not declared<br>• Taxually, needs subscription, price not declared, quota availability varies by country and plan, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install changes state, run changes state<br>• writes or changes integration code in the user's project, affects workspace, confirmation not declared, reversible not declared<br>• installs the Stripe CLI globally with npm i -g @stripe/cli, affects software environment, confirmation not declared, reversible not declared<br>• creates a sandbox test account and test API keys with stripe sandbox create, affects external service, confirmation not declared, reversible not declared<br>• runs a test Tax Calculation on the account, affects external service, confirmation not declared, reversible not declared<br>• sets a head office address in Tax Settings and passes automatic_tax on objects, affects external service, confirmation not declared, reversible not declared<br>• creates a tax registration, prepared and confirmed by the user, affects external service, confirmation yes, reversible not declared<br>• expires a tax registration, prepared and confirmed by the user, affects external service, confirmation yes, reversible no<br>• sets up a pre-commit hook that catches keys in source code, affects workspace, confirmation not declared, reversible not declared |
| **Network access** | • Stripe API, host not named in the files: data source, with execution access through MCP tools or the Stripe CLI. Sends credential and user content, receives account data, Tax Settings, tax calculations, threshold monitoring results and test API keys.<br>• docs.stripe.com: data source, when the metronome skill is not installed, or a request does not fit a single domain. Sends none, receives the metronome skill's SKILL.md and Stripe documentation pages.<br>• npm registry, not named in the files: install, once, when the Stripe CLI is installed. Sends none, receives the @stripe/cli package. |
| **Tools and permissions** | allowed-tools: none<br>• stripe sandbox create, stripe sandbox claim, stripe whoami --format json, stripe logs tail (shell command), creating and claiming a sandbox, auth checks and watching logs, third party<br>• get_tax_threshold_monitoring CLI tool (shell command), retrieving threshold monitoring results, third party<br>• npm i -g @stripe/cli (shell command), installing the Stripe CLI, third party<br>• Stripe MCP tools, including the GetTaxThresholdMonitoring dynamic tool (external server), execution access to the account and threshold monitoring, third party<br>• metronome skill (other), Metronome implementation questions and code, third party<br>• shell and file tools of the agent (agent tool), running the CLI and reading and writing integration code, built in |
| **Machine access, paths** | • references/*.md in the skill folder, read, skill folder<br>• the user's integration source code, read, workspace<br>• integration source files the agent writes or changes, write, workspace<br>• a pre-commit hook in the repository under version control, write, workspace |
| **Machine access, settings** | none |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 30 October 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/stripe/ai/stripe-best-practices/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 30 October 2026 | unknown | pass, risk level SAFE, only official Stripe domains and cloud secret managers referenced, warns against hardcoded keys, standard Stripe CLI and SDK tooling | [report](https://skills.sh/stripe/ai/stripe-best-practices/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 30 October 2026 | the skill package, hash 7ea7861a310af85029fda32154d777cf9cca79f425f00f697db76c82bc95d0d3 | pass, checks for malicious behaviour, credential exposure, obfuscated code and suspicious patterns | [report](https://skills.sh/stripe/ai/stripe-best-practices/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • Stripe collects no tax while the user believes tax is on, when automatic_tax is enabled without an active registration. Source: author. Severity: none. Mitigation: confirm an active registration first, in the instructions. Taxonomy: not examined.<br>• A Stripe API key committed to a source code repository can be taken over and seriously harm the user's business. Source: author. Severity: none. Mitigation: secrets vault, restricted keys, pre-commit hook and key rolling, in the instructions. Taxonomy: not examined.<br>• Orders are silently dropped when fulfillment logic runs only on the success page and the customer never reaches it. Source: author. Severity: none. Mitigation: webhook handler for checkout.session.completed and checkout.session.async_payment_succeeded, in the instructions. Taxonomy: not examined.<br>• Platform operators bear financial liability for fraud and disputes on Express and Custom connected accounts. Source: author. Severity: none. Mitigation: Standard named as the safer default, in the instructions. Taxonomy: not examined.<br>• Instructions read at run time from docs.stripe.com/.well-known/skills/metronome/SKILL.md steer the agent without being part of the files this card describes. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• With execution access through MCP tools or a CLI token, the agent changes Tax Settings and runs calls on a live Stripe account. Source: model. Severity: none. Mitigation: user confirmation is required for registrations only, existing head office address and tax code are not to be overwritten. Taxonomy: not examined. |
| **Limitations** | • Stripe Tax does not process payments outside Stripe, automatically file every tax return, or support every jurisdiction.<br>• Threshold monitoring only processes live-mode transactions and does not cover physical-presence obligations.<br>• Threshold notifications are not real time and arrive within 1 or 2 days after a threshold is crossed.<br>• The taxability_reason not_collecting cannot tell a missing registration from a Nontaxable product tax code.<br>• Tax registrations and Tax Settings in a sandbox are scoped to that sandbox and do not appear in live mode.<br>• Metronome does not support usage prices that must work with Connect, Adaptive Pricing or Workflows. |
| **Known problems** | • automatic_tax collects zero tax: check the product tax code, add a registration, then run a test transaction<br>• customer_tax_location_invalid: correct the invalid higher-priority address<br>• invalid_request_error when adding a registration: set a head office address in Tax Settings first<br>• enabling automatic_tax is rejected while manual tax_rates remain: clear all tax_rates first, or use the Tax migration tool<br>• 403 errors when testing a restricted API key: add the missing permissions to the RAK<br>• MCP used after sandbox creation: run stripe sandbox claim first<br>• an API key is exposed or compromised: roll the key immediately, check activity logs and contact Stripe support |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the stripe organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 30 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 20 January 2026<br>• content changes 58 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:fd9066ab19b3cd371c7860dd36dd296f042bed872df2fea75901aae9c637e105`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 8570d472 |
| **Source** | • repository, GitHub stripe/ai, path skills/stripe-best-practices, commit 8570d472, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/stripe/ai/stripe-best-practices<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 6,247 bytes, document<br>• references/billing.md, 10,134 bytes, document<br>• references/connect.md, 11,017 bytes, document<br>• references/payments.md, 9,072 bytes, document<br>• references/security.md, 10,056 bytes, document<br>• references/tax.md, 24,036 bytes, document<br>• references/treasury.md, 793 bytes, document |
| **File counts** | 7 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
