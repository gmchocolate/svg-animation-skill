# Contributing

Welcome! SVG Animation Skill is intended as a practical library of motion-design judgments and safely reusable tools.

## Principles

1. Contributions must teach useful visual hierarchy, timing or interaction—not merely add effects.
2. Prefer original, small reproducible examples and permissively licensed source.
3. Don't commit private animation references, scraped source projects, brand assets or screenshots without redistribution rights.
4. Maintain graceful static and reduced-motion behavior.
5. Keep CLI behavior offline and deterministic; state limitations clearly.
6. New integrations should be optional and should not impose another dependency on every user.

## Development

~~~bash
python -m unittest discover -s tests -v
python skills/svg-animation/scripts/check_svg.py skills/svg-animation/examples/line-draw.svg
~~~

When modifying motion_library.py, test invalid input, duplicates, untrusted SVG, local file permissions, selection, feedback and removal. Keep docs bilingual where practical.

For a new motion pattern, include: the semantic purpose, initial and final states, trigger, movement grammar, reduced mode, mobile fallback and browser review notes.
