# Guidance for coding agents contributing to this repository

Read skills/svg-animation/SKILL.md before changing the Skill.

- Preserve the Agent Skills entry point skills/svg-animation/SKILL.md and frontmatter name/description.
- Keep the repository independent of a particular framework; offer Vue/Nuxt examples without requiring them.
- Reference-first means ACTUALLY inspecting motion. Never claim that tags/metadata alone constitute watching a clip.
- Save user references outside the Git repo by default. Any persistent save/delete requires explicit user permission.
- No network access, telemetry, model calls or external downloads in the local CLI.
- Do not use binary reference examples from third-party websites without permission.
- Python 3.10+ standard library only for scripts and tests; don't add runtime dependencies without justification.
- Static checking is not visual verification; say what was and wasn't tested.
- Maintain security checks for untrusted SVG/JSON input and avoid embedding/playing arbitrary user-supplied code.
- Document changes in both READMEs when user-facing commands or behavior change.
- Run python -m unittest discover -s tests -v and check the bundled SVG before submitting.
