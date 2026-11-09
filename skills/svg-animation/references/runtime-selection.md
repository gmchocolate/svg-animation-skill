# Choosing an SVG animation engine

Choose the **least complex implementation that satisfies the design**. First inspect the project's existing dependencies and license constraints.

| Need | First choice | When to upgrade |
| --- | --- | --- |
| Hover / fade / scale / translation | CSS transitions / keyframes | precise reversible multi-step orchestration |
| Self-contained animation inside an SVG file | SVG SMIL or CSS in SVG | runtime controls and app state integration |
| Pause / reverse / cancel native effects | Web Animations API | complicated morphing or choreography |
| Timeline, draw, shape morph, motion path | Anime.js 4 | very complex scroll choreography |
| Large, precisely staged campaigns and scroll stories | GSAP | only where its capabilities outweigh complexity |
| Vue/React interaction and layout transitions | Motion | specialized SVG drawing or arbitrary shape morphs |
| Procedurally created SVG shapes/editors | SVG.js | needs separate animation control beyond its API |
| Existing ECharts / charts | chart library's built-in animation | only for custom overlays and narrative layers |
| Designer-delivered motion asset | Lottie-web | only after verifying actual SVG renderer output |

## Official documentation
- SVG and CSS: https://developer.mozilla.org/en-US/docs/Web/SVG
- SVG SMIL: https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_animation_with_SMIL
- Web Animations API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
- Anime.js: https://animejs.com/documentation/svg
- GSAP: https://gsap.com/docs/v3/
- Motion: https://motion.dev/docs/
- SVG.js: https://svgjs.dev/
- Lottie-web: https://github.com/airbnb/lottie-web
- ECharts animation: https://echarts.apache.org/en/index.html

## Licensing note

Anime.js / Motion / SVG.js / Lottie-web are generally MIT licensed (verify the exact version used). GSAP is **not MIT** even when use is free: read the current GSAP standard license and restrictions before bundling in an editor, website builder or redistributed commercial tool. Do not imply that an open source repo makes all dependencies open source.

## Nuxt-specific decision

- Decorative hero SVG: static SVG with scoped CSS keyframes is often enough.
- Interactive visual with state coordination: Vue reactivity + CSS or Motion for Vue.
- Data-driven chart: built-in ECharts transitions first, then coordinate a lightweight SVG overlay.
- GSAP / Anime.js timelines: import client-side if required; cleanly revert/kill on unmount.
- Never rely on a client-only animation to reveal essential SSR content. Hydration must preserve layout and meaning.

## Other good engineering defaults

Keep animation values (durations, easings, transforms) grouped in tokens rather than scattering magic numbers. Animate composite properties (opacity/transform) when possible. Always measure if performance is a claim. Include a final non-animated state that works if JS or observers are unavailable.
