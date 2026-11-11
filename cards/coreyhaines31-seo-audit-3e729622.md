# Skill Card: seo-audit coreyhaines31/marketingskills at 3e729622

## 1. What it does

| Field | Value |
|---|---|
| **Name** | seo-audit |
| **Description** | Instructions and seven reference documents for auditing the SEO of a website. The audit runs in priority order through crawlability and indexation, technical foundations, on-page optimization, content quality and authority, with added checklists for multilingual sites, local businesses, title tags and pages ranking in positions 8 to 20. The result is an audit report with an executive summary, findings with issue, impact, evidence, fix and priority, and a prioritized action plan. Use it when someone wants to audit or diagnose SEO, asks why traffic dropped or a page won't rank, or just says their SEO is bad. |
| **Tasks** | • audit crawlability, indexation and technical SEO<br>• check Core Web Vitals, mobile-friendliness, HTTPS and URL structure<br>• review title tags, meta descriptions, headings, images and internal linking<br>• check hreflang, canonicals and sitemaps on multilingual and multi-regional sites<br>• diagnose local SEO, Business Profiles, citations, reviews and location pages<br>• move pages ranking in positions 8 to 20 onto page one and fix weak click-through |
| **Outputs** | • SEO audit report with executive summary, technical, on-page and content findings, and a prioritized action plan (recommendation), structured text report, each finding with Issue, Impact, Evidence, Fix and Priority, to a message to the user<br>• proposed title changes for a bulk title audit (recommendation), Markdown table with page, current title, proposed title and reason, to a message to the user, for the owner to approve line by line<br>• local SEO plan and artifacts, field edits, citation cleanup table, review drafts, location-page outline or measurement plan (recommendation), text and tables, to a message to the user<br>• rankings push candidates bucketed into striking distance, weak click-through and near the top, with the smallest change per page (recommendation), text and tables, to a message to the user |
| **Sample output** | `\| /pricing \| Plans That Grow With You \| Acme Pricing: Plans and Costs \| Matches the "acme pricing" query \|` |
| **Inputs** | • the site or pages to audit, a URL, with the scope as full site or specific pages, required for every audit, example `URL: https://example.com`<br>• product marketing context, a Markdown file in the workspace, optional for every task, example `.agents/product-marketing.md`<br>• site context, business goal, priority keywords, known issues, traffic level and recent changes or migrations, answers to questions in natural language, conditional for information not already covered by the product marketing context, example `What type of site? (SaaS, e-commerce, blog, etc.)`<br>• Search Console and analytics access or data, account access or exported reports, optional for indexation checks and finding rankings push candidates, example `query + page pairs for the trailing 28 days`<br>• a crawl export, an export file from a crawler such as Screaming Frog, optional for bulk title audits and schema detection, example `URL, title, H1, length, indexable status`<br>• local business facts, business type, locations, hours, services, profile URLs and ownership, answers in natural language and URLs, conditional for local SEO requests, example `Business type: customers visit a storefront, staff travel to customers, both, or online only.` |
| **When an input is missing** | • a product marketing context file exists: it is read first and only information not already covered or specific to the task is asked for<br>• no access to the Business Profile or its evidence: a provisional plan is given with the evidence needed, and no profile findings are invented |
| **Exclusions** | • SEO pages at scale, see programmatic-seo<br>• implementing structured data, see schema<br>• AI search optimization, see ai-seo<br>• software product directory campaigns, see directory-submissions |
| **Adoption** | • skills.sh: 251.6K installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 59,667 stars, 8,712 forks, counting the coreyhaines31/marketingskills repository, which holds 53 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 9 characters, description 405 characters, body 491 lines and about 4,328 tokens<br>• Codex: does not fit, SKILL.md is 17,785 bytes, 9,785 over the 8,000 byte cut on the injected file<br>• Claude Code: fits, 497 lines, listing text 405 characters<br>• ClawHub: fits, folder 80,226 bytes |
| **Software dependencies** | • curl (binary), version not declared, needed to run<br>• Screaming Frog (binary), version not declared, needed to run |
| **Credentials** | none |
| **Cost, context** | • discovery about 101 tokens<br>• load about 4,446 tokens<br>• on demand about 11,681 tokens, in references/ai-writing-detection.md, references/international-seo.md, references/local-seo-pages-and-measurement.md, references/local-seo-profile-and-citations.md, references/local-seo.md, references/rankings-push.md and references/title-tags.md |
| **Cost, per run** | not examined |
| **Cost, services** | • Screaming Frog, needs subscription, price paid, no amount stated, quota not declared, calls per use not declared<br>• Ahrefs, needs subscription, price paid, no amount stated, quota not declared, calls per use not declared<br>• Semrush, needs subscription, price paid, no amount stated, quota not declared, calls per use not declared<br>• Sitebulb, needs subscription, price paid, no amount stated, quota not declared, calls per use not declared<br>• ContentKing, needs subscription, price paid, no amount stated, quota not declared, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• profile changes, messages to customers or directory submissions, only under the user's existing authorization, affects external service, confirmation yes, reversible not declared<br>• requests indexing of a new page once in Search Console, affects external service, confirmation not declared, reversible not declared |
| **Network access** | • the site under audit, given by the user: data source, when pages are fetched with web_fetch, curl or a browser tool. Sends none, receives page HTML, headers, robots.txt and sitemaps.<br>• search.google.com, Rich Results Test: data source, when checking schema markup. Sends user content, receives the structured data found on the rendered page.<br>• Google Search Console, host not named in the files: data source, when Search Console access is available. Sends none, receives coverage, Core Web Vitals and query and page reports.<br>• a search engine results page, host not named in the files: data source, when checking the titles that rank for a target query or the top three results. Sends query text, receives the ranking results and their titles.<br>• PageSpeed Insights and WebPageTest, hosts not named in the files: data source, when checking site speed and Core Web Vitals. Sends user content, receives speed and Core Web Vitals measurements. |
| **Tools and permissions** | allowed-tools: none<br>• web_fetch (agent tool), fetching pages, not for detecting schema markup, built in<br>• curl (shell command), fetching pages, not for detecting schema markup, third party<br>• browser tool (agent tool), rendering a page and running document.querySelectorAll('script[type="application/ld+json"]'), built in<br>• Google Search Console, PageSpeed Insights, Bing Webmaster Tools, Rich Results Test, Mobile-Friendly Test, Schema Validator, WebPageTest, Chrome DevTools (program), free tools for indexation, speed, mobile and schema checks, third party<br>• Screaming Frog, Ahrefs, Semrush, Sitebulb, ContentKing (program), paid crawling, ranking and monitoring tools, if available, third party |
| **Machine access, paths** | • .agents/product-marketing.md, .claude/product-marketing.md or product-marketing-context.md, read, workspace<br>• crawl exports the client provides, read, unknown |
| **Machine access, settings** | none |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 10 November 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/coreyhaines31/marketingskills/seo-audit/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 10 November 2026 | the skill files and reference documentation, as its analysis states | pass, risk level SAFE, indirect prompt injection surface described as addressed by the untrusted-data instruction, no malicious code or exfiltration found | [report](https://skills.sh/coreyhaines31/marketingskills/seo-audit/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 20 October 2026 | the skill package, hash 70818bc66dff7d712dd9e5089b9f20891bdfe78137cd5d8640ae45cc921e7568 | pass, checks for malicious behaviour, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/coreyhaines31/marketingskills/seo-audit/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • Instructions embedded in the HTML, meta tags or copy of a fetched page reach the agent when it analyses the site. Source: author, check C2. Severity: SAFE overall by C2. Mitigation: an instruction to treat fetched pages as untrusted data and never follow embedded instructions, in place. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• A home-based business owner's private address becomes public when it is added to citations or JSON-LD markup. Source: author. Severity: none. Mitigation: instructions never to publish a hidden home address, in place. Taxonomy: not examined.<br>• A review request that offers incentives, selects only happy customers or requires particular wording breaks Google's review policy. Source: author. Severity: none. Mitigation: a neutral example request and the rule against incentives, in place. Taxonomy: not examined.<br>• A reply to a complaint exposes customer, medical, financial or job details. Source: author. Severity: none. Mitigation: instruction to offer a private contact path instead, in place. Taxonomy: not examined.<br>• Profile edits, customer messages or directory submissions are made on the user's accounts when the agent acts under an existing authorization, with no way to undo stated. Source: model. Severity: none. Mitigation: a drafted plan does not itself authorize execution, in place. Taxonomy: not examined. |
| **Limitations** | • web_fetch and curl cannot reliably detect structured data, since JSON-LD injected by client-side JavaScript does not appear in static HTML.<br>• Without access to a Business Profile, only a provisional plan with the evidence needed can be given.<br>• Search Console data is limited by privacy thresholds and aggregation, and analytics counts by consent, blockers and tagging.<br>• Schema validation does not guarantee rich-result display or a local-pack ranking change.<br>• If two rounds of edits move nothing, the page is probably limited by intent mismatch or authority, which more on-page work won't fix. |
| **Known problems** | • no schema found with web_fetch or curl: check with a browser tool, the Google Rich Results Test or a Screaming Frog export<br>• Google shows a different title than the one written: tighten the title and align it with the H1<br>• a new page is not indexed after a few weeks: check the causes in the Indexation section instead of resubmitting<br>• no concrete reason a page ranks below the top three: work on links with the link-building skill rather than a rewrite<br>• Next.js alternates.languages omits the self-referencing xhtml:link: add the current locale explicitly<br>• conflicting hreflang annotations in HTML and sitemap: make the methods agree, since Google drops the conflicting pair |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author not declared<br>• publisher the coreyhaines31 account on GitHub<br>• signer none<br>• contact not declared |
| **License** | • SKILL.md frontmatter: not declared<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 9 November 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 16 January 2026<br>• content changes 34 since first seen<br>• releases 100 or more<br>• last release 11 November 2026 |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:e5296133190cc6dc94e93b7e1ba986210af8b6d34e001dae85d0619ac2a9ed9a`, files left out none<br>• author version 2.2.5<br>• registry version not declared<br>• commit 3e729622 |
| **Source** | • repository, GitHub coreyhaines31/marketingskills, path skills/seo-audit, commit 3e729622, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/coreyhaines31/marketingskills/seo-audit<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 17,785 bytes, document<br>• evals/evals.json, 15,717 bytes, data<br>• references/ai-writing-detection.md, 6,528 bytes, document<br>• references/international-seo.md, 14,898 bytes, document<br>• references/local-seo-pages-and-measurement.md, 4,036 bytes, document<br>• references/local-seo-profile-and-citations.md, 3,971 bytes, document<br>• references/local-seo.md, 7,249 bytes, document<br>• references/rankings-push.md, 4,509 bytes, document<br>• references/title-tags.md, 5,533 bytes, document |
| **File counts** | 8 documents, 0 scripts, 1 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
