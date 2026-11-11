# Skill Card: better-auth-best-practices better-auth/skills at 20c9e88a

## 1. What it does

| Field | Value |
|---|---|
| **Name** | better-auth-best-practices |
| **Description** | A single SKILL.md of instructions for setting up and configuring Better Auth, a TypeScript authentication library, in a project. It covers installing better-auth, setting BETTER_AUTH_SECRET and BETTER_AUTH_URL, creating auth.ts and a route handler and running migrations, with a quick reference for database adapters, sessions, plugins, hooks, security options and the client. It looks up documentation for the installed Better Auth version through the Better Auth MCP or better-auth.com/llms.txt. Use it when users mention Better Auth, betterauth or auth.ts, or need TypeScript authentication with email/password, OAuth or plugins. |
| **Tasks** | • install Better Auth and set its environment variables<br>• create auth.ts and a route handler for the framework<br>• run schema migrations with the built-in adapter, Drizzle or Prisma<br>• configure sessions, cookie cache and secondary storage<br>• add server and client plugins<br>• configure security options, rate limiting and hooks<br>• look up documentation that matches the installed version |
| **Author's description** | "Configure Better Auth server and client, set up database adapters, manage sessions, add plugins, and handle environment variables. Use when users mention Better Auth, betterauth, auth.ts, or need to set up TypeScript authentication with email/password, OAuth, or plugin configuration." |
| **Outputs** | • the Better Auth configuration with database and options (information), TypeScript file, to auth.ts in ./, ./lib, ./utils or under ./src, or a custom path given with --config<br>• a route handler for the project's framework (information), source file, to a path the agent chooses in the project<br>• a generated auth schema for Drizzle or Prisma (information), schema file, to src/db/auth-schema.ts or prisma/schema.prisma<br>• the auth schema applied to the database through migrations (action), database schema change, to the project's database<br>• configuration advice on adapters, sessions, plugins and security options (recommendation), chat text, to the agent's answer to the user |
| **Sample output** | `{ status: "ok" }` |
| **Inputs** | • the Better Auth version of the project, a version named by the user, or the resolved better-auth version in the lockfile or package manifest, optional for choosing the matching documentation, example not declared<br>• the base URL of the app, an environment variable, required for setup, example `https://example.com`<br>• the database to use, a database instance or an ORM adapter, conditional for most features, which need a database, example `drizzleAdapter(db, ...)`<br>• the project's framework, the framework the route handler is created for, required for creating the route handler, example not declared<br>• OAuth client credentials, clientId and clientSecret per provider in the config, conditional for social sign-in, example `{ google: { clientId, clientSecret }, ... }` |
| **When an input is missing** | • the user names no version: the resolved better-auth version in the lockfile is used, or the package manifest when there is no lockfile<br>• the project version cannot be determined: the latest documentation is used<br>• the Better Auth MCP is not available: lookup starts at better-auth.com/llms.txt and follows the matching version index<br>• BETTER_AUTH_URL or BETTER_AUTH_SECRET is not set: baseURL or secret is defined in the config instead<br>• auth.ts is not in ./, ./lib, ./utils or under ./src: the CLI is given the path with --config |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 131.6K installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 229 stars, 37 forks, counting the better-auth/skills repository, which holds 6 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: does not fit, the name does not match the folder name best-practices<br>• Codex: does not fit, SKILL.md is 8,231 bytes, 231 over the 8,000 byte cut on the injected file, and 7,891 bytes if only the body counts<br>• Claude Code: fits, 192 lines, listing text 284 characters<br>• ClawHub: fits, folder 8,231 bytes |
| **Software dependencies** | • better-auth (package), version not declared, needed to install<br>• auth CLI, run as npx auth@latest (package), version latest, needed to run<br>• npm and npx (runtime), version not declared, needed to run<br>• drizzle-kit (package), version not declared, used in an example<br>• prisma (package), version not declared, used in an example<br>• pg, mysql2, better-sqlite3, postgres or @neondatabase/serverless, as alternatives (package), version not declared, used in an example<br>• openssl (binary), version not declared, used in an example |
| **Credentials** | • other, BETTER_AUTH_SECRET, used for encryption secret of Better Auth, min 32 chars, from environment variable, stays on the machine<br>• other, clientSecret, used for OAuth sign-in through socialProviders, from file, goes to the OAuth provider, host not named in the files<br>• other, DB credentials, used for drizzle-kit commands reaching the database, from file, goes to the database server, host not named in the files |
| **Cost, context** | • discovery about 71 tokens<br>• load about 2,058 tokens<br>• on demand none |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• installs the better-auth package with npm install, affects software environment, confirmation not declared, reversible not declared<br>• creates auth.ts, a route handler and generated schema files, affects workspace, confirmation not declared, reversible not declared<br>• applies schema migrations to the database, affects external service, confirmation not declared, reversible not declared<br>• sets BETTER_AUTH_SECRET and BETTER_AUTH_URL, affects shell environment, confirmation not declared, reversible not declared<br>• adds the Better Auth MCP to AI tools with npx auth@latest mcp --cursor, affects software environment, confirmation not declared, reversible not declared |
| **Network access** | • better-auth.com: data source, when the Better Auth MCP is not available, to read llms.txt and the version index. Sends none, receives documentation and version indices.<br>• the Better Auth MCP, host not named in the files: data source, when the MCP is available, through get_doc and search_docs. Sends query text, receives documentation identifiers and pages.<br>• the npm registry, not named in the files: install, on npm install better-auth and on each npx auth@latest, drizzle-kit or prisma call. Sends none, receives the packages.<br>• the project's database, host not named in the files: other, when migrations are run. Sends credential and file content, receives the migration result. |
| **Tools and permissions** | allowed-tools: none<br>• Better Auth MCP with get_doc and search_docs (external server), resolving the version and searching the documentation, third party<br>• npm install (shell command), installing better-auth, third party<br>• npx auth@latest migrate, generate and mcp (shell command), applying or generating the schema and adding the MCP to AI tools, third party<br>• npx drizzle-kit push, generate and migrate, npx prisma migrate dev (shell command), migrations with Drizzle or Prisma, third party<br>• openssl rand -base64 32 (shell command), generating BETTER_AUTH_SECRET, third party<br>• shell and file tools of the agent (agent tool), running the commands and writing auth.ts and the route handler, built in |
| **Machine access, paths** | • the lockfile and the package manifest, read, workspace<br>• auth.ts in ./, ./lib, ./utils or under ./src, write, workspace<br>• src/db/auth-schema.ts or prisma/schema.prisma, write, workspace<br>• drizzle.config.ts, read, workspace<br>• the route handler at a path the agent chooses, write, unknown |
| **Machine access, settings** | • BETTER_AUTH_URL, set, base URL of the app<br>• MCP configuration of AI tools such as Cursor, set, add MCP to AI tools |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 14 September 2026 | unknown | warn, risk level MEDIUM, 1 issue, W011 third-party content exposure, indirect prompt injection risk, scored low risk 0.10 | [report](https://skills.sh/better-auth/skills/better-auth-best-practices/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 14 September 2026 | SKILL.md, as cited in its analysis | pass, risk level SAFE, external downloads, command execution and indirect prompt injection described, content from better-auth.com/llms.txt reaches the agent without boundary markers or sanitisation | [report](https://skills.sh/better-auth/skills/better-auth-best-practices/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 14 September 2026 | the skill package, hash 2ca64e870d2b84b9f769fad6b322ac5e1eb3765db26a01f98f3fdb0b2a22cb56 | pass, checks for malicious behaviour, credential exposure, obfuscated code and suspicious patterns | [report](https://skills.sh/better-auth/skills/better-auth-best-practices/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | • Third-party content exposure, indirect prompt injection risk, W011 (C1, MEDIUM, open), location not stated. Fix: not stated |
| **Risks** | • Instructions placed in fetched documentation reach the agent, since content from better-auth.com/llms.txt and the MCP is read without boundary markers or sanitisation. Source: check C1, check C2. Severity: MEDIUM by C1, SAFE overall by C2. Mitigation: none in the files, C2 notes that no boundary markers or sanitisation are defined. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• A changed or compromised release of the auth CLI runs with the agent's privileges, since npx auth@latest fetches and runs the latest version unpinned. Source: check C2. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• Setting disableCSRFCheck or disableOriginCheck in advanced removes CSRF or origin protection from the auth endpoints. Source: author. Severity: none. Mitigation: both options are marked as a security risk. Taxonomy: not examined.<br>• The auth secret ends up in source control when it is set as secret in auth.ts, which the config allows when BETTER_AUTH_SECRET is not set. Source: model. Severity: none. Mitigation: env vars are named as the first place for the secret, as guidance only. Taxonomy: not examined. |
| **Limitations** | • APIs and plugin names can differ across maintained release lines, so documentation must match the installed version.<br>• Custom session fields are not cached in the cookie cache and are always re-fetched.<br>• In stateless mode with no database the session lives only in the cookie, and the user is logged out when the cache expires.<br>• Email verification works only when emailVerification.sendVerificationEmail is defined.<br>• With secondaryStorage defined, sessions go there and not to the database by default. |
| **Known problems** | • model vs table name: use the ORM model name in the config, not the database table name<br>• plugin schema missing after adding plugins: re-run the CLI after adding or changing plugins<br>• Drizzle: db not initialized: pass a db instance from drizzle() to drizzleAdapter, see the create-auth skill<br>• Drizzle: missing drizzle.config.ts: add a drizzle.config.ts pointing to the generated schema file and DB credentials<br>• sessions not stored in the database when secondaryStorage is set: set session.storeSessionInDatabase: true |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the better-auth organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: none |
| **Maintenance status** | • last change 1 September 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 14 January 2026<br>• content changes 11 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:7bfd18c412988ff45696bb656a14b2b2422fe5a2aa20a6f090f969d45fba358e`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit 20c9e88a |
| **Source** | • repository, GitHub better-auth/skills, path better-auth/best-practices, commit 20c9e88a, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/better-auth/skills/better-auth-best-practices<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 8,231 bytes, document |
| **File counts** | 1 document, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 52 |
