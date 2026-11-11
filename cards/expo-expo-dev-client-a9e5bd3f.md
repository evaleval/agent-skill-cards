# Skill Card: expo-dev-client expo/skills at a9e5bd3f

## 1. What it does

| Field | Value |
|---|---|
| **Name** | expo-dev-client |
| **Description** | Instructions for building, installing and using Expo development clients, builds of an app that bundle expo-dev-client for testing native code changes on physical devices. They set up a development profile in eas.json, build with EAS Build in the cloud with submission to TestFlight, or locally into .ipa, .apk or .aab files, install the builds on simulators and devices, and connect the client to the Metro bundler. Use it when an app needs local Expo modules, Apple targets, third-party native modules not in Expo Go, config plugins, or testing of remote push notifications and App or Universal Links. |
| **Tasks** | • decide whether a development client is needed instead of Expo Go<br>• configure a development profile in eas.json<br>• build an iOS dev client in the cloud and submit it to TestFlight<br>• build dev clients locally for iOS and Android<br>• install local builds on a simulator, an iOS device or an Android device<br>• check build status and connect the dev client to Metro<br>• launch the dev client without onboarding, dev menu or Tools button |
| **Author's description** | "Build and distribute Expo development clients locally or via TestFlight for internal testing. For production TestFlight releases and store submission, use the eas-app-stores skill." |
| **Outputs** | • a development profile with developmentClient, autoIncrement and appVersionSource settings (information), JSON file, to eas.json in the project<br>• an iOS development client built in the cloud and submitted to App Store Connect (action), a TestFlight build, to TestFlight, with an email when the build is ready<br>• a locally built development client (information), .ipa file for iOS, .apk or .aab file for Android, a .tar.gz with the .app for the simulator, to the machine the build runs on<br>• a development client installed on a simulator or device (action), an installed app, to the booted iOS simulator, an iOS device or an Android device<br>• recent builds and build details (information), terminal text, to the terminal<br>• a feedback report on errors in the skill or on failed Expo tasks (action), a report sent through @expo/agent-cli, to Expo |
| **Sample output** | `build.ipa` |
| **Inputs** | • an Expo project with a development profile in eas.json, a project folder with eas.json, required for every build, example `"development": { "autoIncrement": true, "developmentClient": true }`<br>• the target platform, the -p flag of eas build, optional for building for one platform, both when omitted, example `eas build -p ios --profile development`<br>• the development server URL, a URL entered in the dev client or a QR code, conditional for connecting the dev client to Metro, example `<scheme>://?__expo_url=<encoded dev server URL>&__expo_disable_onboarding=1&__expo_disable_fab=1&__expo_disable_auto_launch=1`<br>• a build file to install, a path to an .app, .ipa or .apk file, conditional for installing a local build, example `adb install build.apk`<br>• feedback text, a command argument with category and subject, conditional for reporting errors in the skill or a failed Expo task, example `npx --yes @expo/agent-cli@latest feedback --category skills --subject "expo-dev-client" "<actionable feedback>"` |
| **When an input is missing** | not declared |
| **Exclusions** | • not for production TestFlight releases and store submission, use the eas-app-stores skill |
| **Adoption** | • skills.sh: 75.0K installs, counting the skill, first seen 19 January 2026 (read 11 November 2026)<br>• GitHub: 4,111 stars, 268 forks, counting the expo/skills repository, which holds 25 skills (read 11 November 2026) |

## 2. What it needs

| Field | Value |
|---|---|
| **Declared requirements** | harnesses, models and capabilities: not declared |
| **Harness limits** | • Agent Skills specification: fits, name 15 characters, description 180 characters, body 178 lines and about 1,303 tokens<br>• Codex: fits, SKILL.md is 5,449 bytes, under the 8,000 byte cut<br>• Claude Code: fits, 183 lines, listing text 180 characters<br>• ClawHub: fits, folder 5,780 bytes |
| **Software dependencies** | • EAS CLI, eas (package), version >= 16.0.1, needed to run<br>• expo-dev-client (package), version not declared, needed to run<br>• Expo CLI, npx expo (package), version SDK 58+ for launches without the dev menu, else not declared, needed to run<br>• Xcode with xcrun simctl (binary), version not declared, needed to run<br>• ideviceinstaller (binary), version not declared, used in an example<br>• adb (binary), version not declared, needed to run<br>• tar (binary), version not declared, used in an example<br>• @expo/agent-cli (package), version latest, needed to run |
| **Credentials** | • certificate, iOS signing credentials, managed with eas credentials, used for signing builds for devices and TestFlight, from unknown, goes to unknown<br>• other, a paid Apple Developer account, used for device and TestFlight distribution, from unknown, goes to App Store Connect, host not named in the files |
| **Cost, context** | • discovery about 45 tokens<br>• load about 1,362 tokens<br>• on demand none |
| **Cost, per run** | not examined |
| **Cost, services** | • EAS Build, needs subscription, price cloud builds are paid, see https://expo.dev/pricing, quota uses your EAS plan's build minutes, calls per use not declared<br>• Apple Developer account, needs account, price paid, amount not declared, quota not declared, calls per use not declared |

## 3. What it touches

| Field | Value |
|---|---|
| **Side effects** | install read only, run changes state<br>• adds a development profile to eas.json, affects workspace, confirmation not declared, reversible not declared<br>• builds in the cloud and submits the build to App Store Connect with eas build --submit, affects external service, confirmation not declared, reversible not declared<br>• increments build numbers on EAS with autoIncrement and appVersionSource remote, affects external service, confirmation not declared, reversible not declared<br>• writes local build files and extracts build-*.tar.gz, affects workspace, confirmation not declared, reversible not declared<br>• installs the app on a simulator or device with xcrun simctl, ideviceinstaller or adb, affects system, confirmation not declared, reversible not declared<br>• clears the build cache with --clear-cache, affects external service, confirmation not declared, reversible not declared<br>• fetches and runs @expo/agent-cli@latest with npx --yes, affects software environment, confirmation no, reversible not declared<br>• sends a feedback report to Expo, affects external service, confirmation not declared, reversible not declared |
| **Network access** | • EAS Build servers, not named in the files: other, cloud builds, build status and credentials commands. Sends file content, receives the build and build details.<br>• App Store Connect and TestFlight, not named in the files: publish, eas build with --submit. Sends file content, receives a TestFlight build and an email when it is ready.<br>• npm registry, not named in the files: install, npx --yes @expo/agent-cli@latest runs. Sends none, receives the @expo/agent-cli package.<br>• Expo feedback service, not named in the files: other, the agent submits feedback on the skill or a failed Expo task. Sends user content, receives not declared.<br>• the local Metro bundler URL: data source, the dev client connects to the development server. Sends none, receives not declared. |
| **Tools and permissions** | allowed-tools: none<br>• eas build, eas build:list, eas build:view, eas credentials, eas update (shell command), building, submitting, checking builds and fixing signing errors, third party<br>• npx expo start --dev-client (shell command), starting the Metro bundler, third party<br>• tar, xcrun simctl, ideviceinstaller, adb (shell command), unpacking and installing local builds, third party<br>• Xcode (program), local iOS builds and installing on devices, third party<br>• npx --yes @expo/agent-cli@latest feedback (shell command), reporting errors in the skill and failed Expo tasks, third party<br>• shell and file tools of the agent (agent tool), running the commands and editing eas.json, built in |
| **Machine access, paths** | • eas.json, write, workspace<br>• build-*.tar.gz and the extracted ./path/to/App.app, write, workspace<br>• local build files, .ipa, .apk or .aab, write, unknown<br>• ../expo-overview/references/launch-without-dev-menu.md, read, unknown |
| **Machine access, settings** | • developmentClient in eas.json, set, bundles expo-dev-client for development builds<br>• autoIncrement in eas.json, set, automatically increments build numbers<br>• appVersionSource in eas.json, set, uses EAS as the source of truth for version numbers<br>• -EXDevMenu* launch arguments, set, skip the dev menu when launching on SDK 57 and earlier |

## 4. What is known about it

**Checks**

| Id | Tool | Date | Scope | Result | Report |
|---|---|---|---|---|---|
| C1 | Snyk, skills.sh audit, version not stated | 28 October 2026 | unknown | pass, risk level LOW, no issues detected | [report](https://skills.sh/expo/skills/expo-dev-client/security/snyk) |
| C2 | Gen Agent Trust Hub, skills.sh audit, version not stated | 28 October 2026 | the commands in the skill instructions, as cited in its analysis | pass, risk level SAFE, three surfaces described, official CLI tools are run, npx --yes @expo/agent-cli@latest is downloaded, and user text reaches the feedback command | [report](https://skills.sh/expo/skills/expo-dev-client/security/agent-trust-hub) |
| C3 | Socket, skills.sh audit, version not stated | 28 October 2026 | the skill package, hash 3440257a11472689881847ec7904cf2b84a154bf4f2b0b0c466b4d44ae7147ef | pass, checks for malicious behavior, security concerns, code obfuscation and suspicious patterns | [report](https://skills.sh/expo/skills/expo-dev-client/security/socket) |

| Field | Value |
|---|---|
| **Vulnerabilities** | none |
| **Risks** | • A changed or compromised release of @expo/agent-cli runs on the machine, since the feedback command fetches the latest version with npx --yes and no pinned version. Source: check C2. Severity: SAFE overall by C2. Mitigation: none stated. Taxonomy: not examined.<br>• Instructions placed in user-provided text reach the feedback command, since that text is passed to it as an argument. Source: check C2. Severity: SAFE overall by C2. Mitigation: none stated, C2 judges it a standard ingestion point for a reporting tool. Taxonomy: https://www.ibm.com/docs/en/watsonx/saas?topic=ai-risk-atlas.<br>• A cloud build uses paid EAS build minutes and a paid Apple Developer account when the agent builds or distributes through EAS Build or TestFlight. Source: author. Severity: none. Mitigation: building locally is free, no confirmation step stated. Taxonomy: not examined.<br>• Task details and project context leave the machine to Expo when the agent submits a feedback report, which the files ask for after repeated failures or user intervention. Source: model. Severity: none. Mitigation: none stated. Taxonomy: not examined. |
| **Limitations** | • Local iOS builds require Xcode.<br>• Installing an iOS build on a device requires signing.<br>• Device and TestFlight distribution needs a paid Apple Developer account.<br>• Expo CLI skips the onboarding sheet and dev menu only on SDK 58+ and only for launches it starts from a non-interactive shell. |
| **Known problems** | • build fails with signing errors: run eas credentials<br>• a stale build cache: rebuild with eas build -p ios --profile development --clear-cache<br>• errors, misleading or outdated information in the skill: report it with the @expo/agent-cli feedback command |
| **Evaluations** | none |

## 5. Who stands behind it

| Field | Value |
|---|---|
| **Authorship** | • author Expo, from the feedback section of SKILL.md<br>• publisher the expo organisation on GitHub<br>• signer none<br>• contact the feedback command npx --yes @expo/agent-cli@latest feedback, from SKILL.md |
| **License** | • SKILL.md frontmatter: MIT<br>• license file: none<br>• skills.sh: not declared<br>• GitHub repository: MIT, as GitHub detects it |
| **Maintenance status** | • last change 28 October 2026<br>• registry update not declared<br>• deprecated not declared<br>• first seen 13 March 2026<br>• content changes 10 since first seen<br>• releases 0<br>• last release none |

## 6. Which files exactly

| Field | Value |
|---|---|
| **Version** | • content hash `sha256:819f7f519fee1f4264b50bf3b650840a7c6265ed2e51ca2066e804acb0e7523d`, files left out none<br>• author version not declared<br>• registry version not declared<br>• commit a9e5bd3f |
| **Source** | • repository, GitHub expo/skills, path plugins/expo/skills/expo-dev-client, commit a9e5bd3f, retrieved 2026-11-11<br>• also listed on skills.sh, https://skills.sh/expo/skills/expo-dev-client<br>• homepage not declared<br>• produced by a tool: none |
| **File list** | • SKILL.md, 5,449 bytes, document<br>• agents/openai.yaml, 331 bytes, data |
| **File counts** | 1 document, 0 scripts, 1 data, 0 binary, instructions only |

## 7. About this card

| Field | Value |
|---|---|
| **Schema** | Skill Card v1.2 |
| **Assembled by** | Claude Opus 5.5, claude-opus-5-5, by hand from the skill files, the skills.sh listing and audits, and GitHub metadata, with the hash, file list, sizes, harness limits and repository figures computed by script, 11 November 2026 |
| **Not done** | • skill run: no<br>• scripts analysed: no<br>• security check run: no<br>• external service contacted: no<br>• registry read: yes |
| **Count of empty values** | 58 |
