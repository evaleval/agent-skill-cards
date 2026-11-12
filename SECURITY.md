# Security policy

This project reads third-party agent skills, which are untrusted. The pipeline **only reads** a skill's files. It never runs them and never follows links out of the skill folder.

If you find a way for a skill to make the pipeline execute code, read outside the skill folder, or write outside the run folder, please report it privately through GitHub's *Report a vulnerability* button on the Security tab, not in a public issue.
