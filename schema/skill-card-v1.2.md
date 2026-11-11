# Skill Card schema v1.2

## 1. What it does

This section lets readers grasp what the skill is, what it does and produces, what it needs to be given, what it is not for, and how widely it is used.

| Field | Description |
|---|---|
| name | What is the skill called? The name as it appears where the skill is listed or installed. This allows all readers to match the card to the skill they have. |
| description | What does the skill do? A summary of what the skill does and produces, the tasks it covers, and the author's own description as the agent sees it when it selects a skill. This gives all readers a first picture of the skill before the details. |
| outputs | What does the skill produce or do? Each kind of result with its form and where it ends up, whether it is information, a recommendation or an action, and one sample of it. This is useful for all readers to know what to expect from a run. |
| inputs | What must the skill be given to do its job? Each input with its form, whether it is required, an example, and what happens when it is missing. This allows an agent to judge whether it has what the skill needs, and a person to prepare it. |
| exclusions | What should the skill not be used for? Tasks, domains, situations and settings the author rules out, and cases where another skill is the better choice. This is useful for all readers to tell an intended limit of use from a risk that a check found. |
| adoption | How widely is the skill used? Downloads, installs, stars or likes as the registry shows them, with the date they were read and what they count. This is useful for a person to see what others have done with the skill, and the card draws no conclusion from it. |

## 2. What it needs

This section lets readers judge whether the skill can run with their model, runtime and machine, and what using it costs.

| Field | Description |
|---|---|
| compatibility | Which models and runtimes can run the skill? The models, capabilities and harnesses the files name as needed, and whether the skill stays within the limits each common harness enforces. This is useful for all readers to tell where the skill will load as intended, and where it will be cut or refused. |
| software dependencies | What do the skill's scripts need on the machine? Packages, runtimes, binaries and hardware the bundled code needs, with versions where known. This is useful for a person to see what has to be installed before the skill can run, and what the skill brings into the environment. |
| credentials | Which secrets does the skill need? The kinds of secret it reads or asks for, never their values, with what each is used for and where it goes. This is useful for a person to know which sensitive values the skill handles and where they can end up. |
| cost | What does using the skill cost? The context it takes up at discovery, at load and on demand, the tokens a run consumed where measured, and paid or limited services the files name. This allows an agent to judge whether the skill fits its budget, and a person to compare one skill with another. |

## 3. What it touches

This section lets readers see what a run can change, where data goes, and what the skill can reach through the agent and on the machine.

| Field | Description |
|---|---|
| side effects | What does a run change, and can it be undone? Whether the skill only reads or also changes state, what it can destroy, whether a change asks for confirmation first, and whether it can be reversed. This is useful for all readers to judge what is at stake in letting the skill act. |
| network access | Which hosts does the skill contact, and what goes where? Each host with what the connection is for, what is sent to it and what comes back. This is useful for a person to see what leaves the machine, and for an agent to tell whether the skill needs a network. |
| tools and permissions | Which tools and permissions does the skill use? The agent tools, permissions, servers, commands and programs it uses, with what each is for. This is useful for all readers to see what the skill can do through the agent, and for a runtime to know what it must provide. |
| machine access | Which files, folders and settings does the skill read or change? The paths it touches with the operation and whether they lie in the workspace, and the settings it reads or sets. This is useful for a person to see what the skill can reach on the machine beyond the task's own files. |

## 4. What is known about it

This section lists what has been checked, found, measured and stated about the skill, so that readers can see what is known and by whom.

### Checks

Every skill checker that ran on this version of the skill, one row per check. A check is a run of a skill checker, a static analysis, a registry audit or a manual review of the files. A producer's own tests of its output are not checks.

| Field | Description |
|---|---|
| id | Which check does this row record? A short identifier that values in other rows cite. This allows a reader to trace any detected value back to the check that produced it. |
| tool | Which tool ran the check? The skill checker or process, with its version. This is useful for readers to know what kind of examination the result comes from, and to look the tool up. |
| date | When did the check run? The date of the run. This is useful for readers to judge how current the result is for the version the card describes. |
| scope | What did the check examine? The files or artefacts it covered, as the tool states them. This is useful for readers to judge how far a result reaches, since a check that did not look at the scripts says nothing about them. |
| result | What did the check conclude? The verdict, scores, findings and recommendation as the tool gave them. This is the check's own bottom line, before anyone interprets it. |
| report | Where is the full output? A link to the complete report. This allows a reader to go beyond what the card carries. |

### Findings

| Field | Description |
|---|---|
| vulnerabilities | What have checks found in the skill? Each finding with the tool that found it, where in the files it sits, how severe and how certain the tool rated it, and its status. This gives readers what was actually detected, as distinct from a risk that someone judged possible. |
| risks | What harm could using the skill cause? Each risk with a short name, a description, a link to a risk taxonomy, who or what identified it, and what mitigates it. This allows readers to weigh a risk by its source, since a risk the skill's maker states carries different weight from one a tool or a model proposed. The card carries no overall score. |
| limitations | Where does the skill fall short? Known limits of what it can do, cases where it fails or degrades, and known problems with the way around them. This is useful for readers to know what not to expect, and to tell the skill's limit from a fault in their own use. |

### Evaluations

Every benchmark run in which an agent used the skill on a set of tasks and someone measured the outcome, one row per run. Most cards read none, which tells readers that nobody has measured the skill in use. A producer's tests of its own code are not evaluations.

| Field | Description |
|---|---|
| id | Which run does this row record? A short identifier that values in other rows cite. This allows a reader to trace an observed behaviour back to the run that showed it. |
| tasks | What was the skill tested on? The benchmark or task set with a link to it, and the number of tasks and attempts. This is useful for readers to judge how broad the evidence is, and to inspect or rerun the tasks. |
| setup | In which runtime and with which model did the agent run? The harness and the model, with versions. This is useful for readers to know for which setup the result holds, since the same skill can behave differently across runtimes and models. |
| result | How did the agent perform with the skill, and without it where that was measured? The scores or observations as the evaluator gave them. This is the measured outcome, before anyone interprets it. |
| date, by | When did the run take place, and who ran it? The date and the party. This is useful for readers to judge how current the result is, and whether it came from the skill's maker or from an independent party. |
| report | Where is the full record? A link to the run record. This allows a reader to go beyond what the card carries. |

## 5. Who stands behind it

This section lets readers see whom they trust when they install the skill, under which terms they may use it, and whether it is still maintained.

| Field | Description |
|---|---|
| authorship | Who made the skill, and who stands behind it? The author, the publisher or owner, the signer if the files are signed, and where to send questions or problems. This is useful for a person to know whom they are trusting when they install the skill, and whom to contact. |
| license | Under which terms may the skill be used? The license or terms of use the skill comes with, as stated. This is useful for a person to tell whether they may use, change and redistribute the skill, and whether any terms are stated at all. The card records the terms and does not interpret them. |
| maintenance status | Is the skill still maintained? The last change to its content, any deprecation notice, and how often releases appear. This is useful for a person to judge whether to expect fixes, and whether the skill is likely to keep working with current models and runtimes. |

## 6. Which files exactly

This section pins the card to the exact files it describes, so that readers can match them to what they have and a reviewer can fetch them.

| Field | Description |
|---|---|
| version | Which version of the skill does this card describe? A hash over the exact files the card was made from, the author's version number where there is one, and the commit. This is useful for all readers to check that the card matches the files they have, and to compare one version with another. |
| source | Where do the skill files come from? The location from which the identical files can be fetched, and the tool that produced them where one did. This allows a reviewer to check the card against the same files, and a person to judge the origin of what they are about to run. |
| file list | Which files make up the skill? Every file with its path, size, hash and kind, and the count of files per kind. This is useful for readers to see whether the skill is only instructions or also ships scripts, programs or data, which is a first indication of what it can do when it runs. |

## 7. About this card

This closing section says how the card itself was made.

| Field | Description |
|---|---|
| card stamp | When was this card made, by whom, and following which version of this schema? The assembler, the date, the schema version, and what the assembly did not do. This is useful for readers to judge how current the information is, and to see what the card cannot speak to. |
