# Skill Card: supabase-postgres-best-practices supabase/agent-skills at c9be0e93

## 1. What it does

| Field | Value |
|---|---|
| **Name** | supabase-postgres-best-practices |
| **Description** | A Postgres performance and design guide maintained by Supabase, made of one instruction file and 31 rule files in eight categories ranked by impact, from query performance and connection management to advanced features. Each rule explains why it matters and shows incorrect and correct SQL, with EXPLAIN output or metrics where useful and Supabase notes where they apply. The agent reads the rule files that fit the task and writes or reviews SQL, schemas, indexes, RLS policies and connection settings by them. Use it when writing SQL or designing schemas, optimizing queries, reviewing database performance, configuring connection pooling or working with Row-Level Security. |
| **Tasks** | • add and choose indexes for WHERE, JOIN, JSONB and full-text queries<br>• configure connection pooling, limits and idle timeouts<br>• enable and optimize Row-Level Security and least privilege grants<br>• choose data types, primary keys, partitioning and safe migration constraints<br>• reduce lock contention, deadlocks and N+1 queries<br>• diagnose slow queries with EXPLAIN ANALYZE, pg_stat_statements and VACUUM statistics<br>• for Postgres running anywhere, with Supabase-specific notes |
| **Author's description** | "Postgres best practices maintained by Supabase, for Postgres running anywhere. Load this skill BEFORE writing or changing anything that lives in a Postgres database: creating or altering tables and columns (including choosing column types), schema design, migrations and declarative schema files, RLS policies and the tests that verify them, indexes, triggers, database functions, queues and scheduled jobs (pg_cron, pgmq), vector/semantic search (pgvector), and restoring dumps (pg_restore) or importing data. Also load it when diagnosing slow queries, high CPU, timeouts, EXPLAIN plans, connection exhaustion, locking, bloat, or rows visible to the wrong user or tenant. This is not just a performance guide — schema, migration, security, and SQL authoring tasks need these rules too, even for a one-column change or a single query." |
| **Outputs** | • SQL for tables, indexes, constraints, RLS policies, roles and queries written by the rules (information), SQL text, to the agent's answer or the migration and query files the agent writes<br>• advice on which indexes, pool settings, data types and query rewrites to apply (recommendation), text with incorrect and correct SQL, to the agent's answer to the user<br>• changes to a database when the SQL is run, such as new indexes, policies, roles and server settings (action), database objects and settings, to the Postgres database<br>• diagnostic results from EXPLAIN ANALYZE, pg_stat_statements and pg_stat_activity (information), query plans and result rows, to the agent's context |
| **Sample output** | `Index Scan using orders_customer_id_idx (cost=0.42..8.44 rows=100 width=85)` |
| **Inputs** | • a SQL query or schema to write or review, SQL text, required for every task, example `select * from orders where customer_id = 123;`<br>• a slow query to diagnose, SQL text run under EXPLAIN, conditional for diagnosing slow queries, example `explain (analyze, buffers, format text) select * from orders where customer_id = 123 and status = 'pending';`<br>• the available RAM and CPU cores of the database server, numbers, conditional for setting connection limits and pool size, example `Example for 4 cores: pool_size = 10` |
| **When an input is missing** | not declared |
| **Exclusions** | not declared |
| **Adoption** | • skills.sh: 481.3K installs, counting the skill, first seen 21 January 2026 (read 11 November 2026)<br>• GitHub: 3,040 stars, 267 forks, counting the supabase/agent-skills repository, which holds 2 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 32 characters, description 834 characters, body 53 lines and about 442 tokens<br>• Codex: fits, SKILL.md is 3,231 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 64 lines, listing text 834 characters<br>• ClawHub: fits, folder 62,007 bytes |
| **Software dependencies** | • Postgres (runtime), version not declared, used in an example<br>• pg_stat_statements extension (package), version not declared, used in an example<br>• pg_uuidv7 extension (package), version not declared, used in an example<br>• PgBouncer (binary), version not declared, used in an example<br>• pnpm (binary), version not declared, used in an example |
| **Credentials** | • password, the password of the app_user login role, used for creating a login role that inherits limited privileges, from command argument, goes to the Postgres server the SQL runs on, host not named |
| **Cost, context** | • discovery about 209 tokens<br>• load about 808 tokens<br>• on demand about 11,990 tokens, in references/_sections.md, references/advanced-full-text-search.md, references/advanced-jsonb-indexing.md, references/conn-idle-timeout.md, references/conn-limits.md, references/conn-pooling.md, references/conn-prepared-statements.md, references/data-batch-inserts.md, references/data-n-plus-one.md, references/data-pagination.md, references/data-upsert.md, references/lock-advisory.md, references/lock-deadlock-prevention.md, references/lock-short-transactions.md, references/lock-skip-locked.md, references/monitor-explain-analyze.md, references/monitor-pg-stat-statements.md, references/monitor-vacuum-analyze.md, references/query-composite-indexes.md, references/query-covering-indexes.md, references/query-index-types.md, references/query-missing-indexes.md, references/query-partial-indexes.md, references/schema-constraints.md, references/schema-data-types.md, references/schema-foreign-key-indexes.md, references/schema-lowercase-identifiers.md, references/schema-partitioning.md, references/schema-primary-keys.md, references/security-privileges.md, references/security-rls-basics.md and references/security-rls-performance.md |
| **Cost, per run** | not examined |
| **Cost, services** | none |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• creates or alters tables, indexes, constraints, partitions, RLS policies and functions, affects external service, confirmation not declared, reversible not declared<br>• changes server settings with alter system and pg_reload_conf, affects external service, confirmation not declared, reversible not declared<br>• creates roles and grants or revokes privileges, affects external service, confirmation not declared, reversible not declared<br>• drops old partitions with drop table events_2023_01, affects external service, confirmation not declared, reversible not declared<br>• creates extensions and resets statistics with pg_stat_statements_reset, affects external service, confirmation not declared, reversible not declared<br>• sets pooler timeouts in pgbouncer.ini, affects system, confirmation not declared, reversible not declared |
| **Network access** | • the Postgres database or pooler the agent works with, not named in the files: data source, when the SQL examples or diagnostic queries are run against a database. Sends query text, receives query results, plans, statistics and errors. |
| **Tools and permissions** | allowed-tools: none<br>• SQL and PL/pgSQL statements run in Postgres (program), schema changes, indexes, RLS policies, grants, settings and diagnostics, third party<br>• PgBouncer (program), connection pooling between the application and the database, third party<br>• pnpm test (shell command), checking a new reference file before submitting it, third party<br>• file and database tools of the agent (agent tool), reading the rule files and running the SQL, built in |
| **Machine access, paths** | • references/ rule files in the skill folder, read, skill folder<br>• /path/to/data.csv loaded with copy, read, unknown<br>• pgbouncer.ini, write, unknown |
| **Machine access, settings** | • idle_in_transaction_session_timeout and idle_session_timeout, set, to reclaim idle connections<br>• max_connections and work_mem, set, to keep connection memory within the available RAM<br>• statement_timeout, set, to abort runaway queries<br>• log_lock_waits and deadlock_timeout, set, to log deadlocks<br>• app.current_user_id, set, user context for RLS policies<br>• search_path, set, fixed to empty inside SECURITY DEFINER functions<br>• autovacuum_vacuum_scale_factor and autovacuum_analyze_scale_factor, set, to vacuum and analyze high-churn tables more often<br>• server_idle_timeout and client_idle_timeout in pgbouncer.ini, set, idle timeouts at the pooler level |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 15 September 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 15 September 2026 | the skill's guidance on privileges, RLS, SECURITY DEFINER, migrations and connection limits, as cited in its analysis | pass, risk level SAFE, describes least privilege, RLS and SECURITY DEFINER guidance, idempotent migrations and resource limits, no issue listed | [report](https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 15 September 2026 | the skill package, hash 382ac24032a5e7a18215bef0aef6d65fe88054ad467474bae329956422dcf80f | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • A SECURITY DEFINER function exposes other users' rows when it lacks an identity check, since it runs with the creator's privileges and bypasses RLS. Source: author. Severity: none. Mitigation: explicit auth.uid() check, a non-exposed schema and revoked EXECUTE, shown in the files. Taxonomy: not examined.<br>• SQL examples run unchanged against a live database change server-wide settings or remove data, as with alter system set max_connections = 100 or drop table events_2023_01. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined.<br>• A login role created from the least privilege example keeps the example's placeholder password when the statement is copied unchanged. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | • UUIDv7 primary keys require the pg_uuidv7 extension.<br>• Named prepared statements fail in transaction-mode pooling, and session mode is needed for prepared statements and temp tables.<br>• No dependency carries a version. |
| **Known problems** | • ERROR: prepared statement "get_user" does not exist under transaction-mode pooling: use unnamed prepared statements, deallocate after use, or use session mode pooling<br>• ADD CONSTRAINT IF NOT EXISTS causes a syntax error in migrations: use a DO block that checks pg_constraint before adding the constraint<br>• ERROR: relation "users" does not exist with quoted mixed-case identifiers: use lowercase snake_case, or create views as a compatibility layer<br>• deadlocks when transactions lock rows in different orders: lock rows in a consistent order first, or update in a single statement<br>• duplicate key error from check-then-insert: use insert ... on conflict |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author supabase, organization Supabase, from the frontmatter metadata<br>• publisher the supabase organisation on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: MIT<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 30 July 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 26 January 2026<br>• content changes 16 since first seen<br>• releases 9<br>• last release 28 September 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:7ee0f93df8316c4e9ac54691261ab2c17d8ae8220924938f9a8d530c4199c66f`, files left out none<br>• author version 1.1.1<br>• registry version not declared<br>• commit c9be0e93 |
| **Source** | • repository, GitHub supabase/agent-skills, path skills/supabase-postgres-best-practices, commit c9be0e93, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/supabase/agent-skills/supabase-postgres-best-practices<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • CHANGELOG.md, 5,684 bytes, document<br>• SKILL.md, 3,231 bytes, document<br>• references/_contributing.md, 4,113 bytes, document<br>• references/_sections.md, 1,682 bytes, document<br>• references/_template.md, 1,040 bytes, document<br>• references/advanced-full-text-search.md, 1,468 bytes, document<br>• references/advanced-jsonb-indexing.md, 1,444 bytes, document<br>• references/conn-idle-timeout.md, 1,282 bytes, document<br>• references/conn-limits.md, 1,325 bytes, document<br>• references/conn-pooling.md, 1,382 bytes, document<br>• references/conn-prepared-statements.md, 1,529 bytes, document<br>• references/data-batch-inserts.md, 1,287 bytes, document<br>• references/data-n-plus-one.md, 1,361 bytes, document<br>• references/data-pagination.md, 1,358 bytes, document<br>• references/data-upsert.md, 1,390 bytes, document<br>• references/lock-advisory.md, 1,531 bytes, document<br>• references/lock-deadlock-prevention.md, 1,855 bytes, document<br>• references/lock-short-transactions.md, 1,350 bytes, document<br>• references/lock-skip-locked.md, 1,353 bytes, document<br>• references/monitor-explain-analyze.md, 1,441 bytes, document<br>• references/monitor-pg-stat-statements.md, 1,418 bytes, document<br>• references/monitor-vacuum-analyze.md, 1,506 bytes, document<br>• references/query-composite-indexes.md, 1,454 bytes, document<br>• references/query-covering-indexes.md, 1,287 bytes, document<br>• references/query-index-types.md, 1,521 bytes, document<br>• references/query-missing-indexes.md, 1,218 bytes, document<br>• references/query-partial-indexes.md, 1,347 bytes, document<br>• references/schema-constraints.md, 1,880 bytes, document<br>• references/schema-data-types.md, 1,453 bytes, document<br>• references/schema-foreign-key-indexes.md, 1,679 bytes, document<br>• references/schema-lowercase-identifiers.md, 1,728 bytes, document<br>• references/schema-partitioning.md, 1,548 bytes, document<br>• references/schema-primary-keys.md, 1,821 bytes, document<br>• references/security-privileges.md, 1,566 bytes, document<br>• references/security-rls-basics.md, 1,372 bytes, document<br>• references/security-rls-performance.md, 2,103 bytes, document |
| **File counts** | 36 documents, 0 scripts, 0 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 46 |
