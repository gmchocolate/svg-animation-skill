# SVG Animation Skill · Reference-first web motion design

**Give your AI coding agent motion taste, not just keyframes.** Learn from animations you admire, keep your own private motion-reference library, and produce original, accessible, performance-conscious SVG animations for real websites.

[简体中文](README.zh-CN.md) · [Skill instructions](skills/svg-animation/SKILL.md) · [Motion grammar](skills/svg-animation/references/motion-grammar.md) · [Quality gates](skills/svg-animation/references/quality-gates.md)

## Why

"Make it animated" rarely makes a website better. Good motion communicates hierarchy, causality, and spatial relationships. This [Agent Skill](https://agentskills.io/specification) guides a coding agent to **observe → understand → design → implement → preview → critique**, instead of randomly adding floating particles and glowing circles.

- **Reference-first:** inspect the *actual* reference SVG/GIF/video (not just its tags or a written summary); extract motion patterns and design intent without cloning someone else's work.
- **Personal taste:** explicitly approved references and feedback live in your own local `~/.svg-animation-skill/` directory. The public repository never receives them automatically.
- **Works with your stack:** native SVG / CSS / SMIL by default; Anime.js, GSAP and Motion only when warranted; Vue 3 and Nuxt examples.
- **Production-oriented:** prefers-reduced-motion, SSR safety, performance, legibility, replay/cleanup, responsive behavior and license considerations.
- **Honest execution:** this is an agent instruction set and a local CLI, not an animation model, automatic browser renderer or cloud sync service.

## Install

```bash
npx skills add gmchocolate/svg-animation-skill
```

Or install globally with `-g`. The Agent Skill lives at `skills/svg-animation/SKILL.md`. Compatible agents need filesystem access to run the optional local reference CLI.

## Try it

Ask your coding agent:

> Use svg-animation to design a refined, restrained hero animation for this Nuxt page. Inspect our existing tokens/components, consult my saved motion references if available, implement the SVG as a Vue component, honor reduced motion and check it in the browser.

Or:

> Analyze this attached animation: what moves, when, why, and how? With my permission, save the source file to my local motion taste library. Do not copy the brand or the exact composition.

### Optional local motion library (Python 3.10+, no pip dependencies)

From `skills/svg-animation/`:

```bash
python scripts/motion_library.py add \
  --file /path/to/inspiration.svg \
  --title "Quiet orbital hero" \
  --use-case hero --tag subtle --tag spatial \
  --like "one clear focal point; staggered reveal" \
  --avoid "constant distracting movement" --rating 5

python scripts/motion_library.py list
python scripts/motion_library.py select --use-case hero --tag subtle --top 2
python scripts/motion_library.py prepare --use-case hero --tag subtle \
  --request "A light, premium B2B SaaS hero"
```

This stores actual local copies of supported references (SVG, GIF, MP4, WebM, Lottie JSON, PNG/JPEG/WebP). Static images are **visual-only references**, not evidence of temporal motion. Local files are *not* uploaded anywhere by these scripts. Metadata embedded in non-SVG media is **not stripped**; avoid importing private files you do not intend to store. The CLI uses explainable tags/ratings, not AI embeddings or model training.

**A manifest is not a visual inspection.** The agent must actually open/play the local reference with tools it has. A remote/cloud agent cannot magically read files on your laptop. If real visual inspection is unavailable, disclose that and work from the provided metadata or create an independent design.

## Native SVG starter & static checks

```bash
python scripts/check_svg.py skills/svg-animation/examples/line-draw.svg
python -m unittest discover -s tests -v
```

Check generated standalone SVG files for unsafe active content, missing viewBox, duplicated IDs and motion/reduced-motion concerns. Passing static checks does **not** replace reviewing actual browser rendering.

## Design principles

1. **Purpose before motion:** animate to explain an action, reinforce hierarchy or add measured delight. Sometimes the right animation is none.
2. **Reference → grammar:** extract choreography, timing, easing, density, hierarchy and restraint; don't clone identifiable artwork or logos.
3. **Progressive enhancement:** meaningful content must survive disabled scripts and reduced motion.
4. **Performance-aware:** prefer transforms/opacity, limit simultaneous movement and costly SVG filters; benchmark rather than promise FPS.
5. **Integrate, don't impose:** use existing brand colors, typography, component patterns and framework conventions.
6. **Review real output:** check initial / transition / resting states, desktop/mobile, keyboard navigation and `prefers-reduced-motion`.

## Repo vs personal data

| Asset | Where it lives |
| --- | --- |
| Generic rules, examples, scripts, tests | Public repository |
| Your saved references and personal preferences | `~/.svg-animation-skill/` (or `SVG_ANIMATION_HOME`) |
| Your generated project components | Your website repository |
| Private reference animations | Never committed, synchronized or transmitted by default |

Third-party reference files are not covered by this project's license. Only save assets you have permission to retain and do not redistribute proprietary examples.

## Project map

- [Skill protocol](skills/svg-animation/SKILL.md)
- [Reference-first creative workflow](skills/svg-animation/references/reference-first-workflow.md)
- [Motion grammar](skills/svg-animation/references/motion-grammar.md)
- [Technology selection](skills/svg-animation/references/runtime-selection.md)
- [Vue / Nuxt integration](skills/svg-animation/references/nuxt-vue.md)
- [Quality & safety review](skills/svg-animation/references/quality-gates.md)
- [Local taste library](skills/svg-animation/references/local-taste-library.md)
- [Example SVG](skills/svg-animation/examples/line-draw.svg) · [Example Vue component](skills/svg-animation/examples/hero-orbit.vue)

## License

Original code and docs: [MIT](LICENSE). Third-party tools have their **own** terms (notably GSAP); see [runtime selection](skills/svg-animation/references/runtime-selection.md). Motion references and generated assets may have separate rights.

Contributions and constructive critiques are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).
