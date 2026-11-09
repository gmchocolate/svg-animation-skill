# Reference-first motion creation

## Why screenshots are insufficient

A screenshot teaches visual hierarchy but cannot reveal acceleration, delay, repeats, handoff timing or interaction states. For SVG motion, **the timeline is part of the design asset**. A still PNG/WebP may inform palette/line weight only; NEVER infer animation speed or easing from one still.

## Analyze a real source

When an approved, accessible animation is provided, use the best available viewer/browser/player. Observe:

| Phase | Questions |
| --- | --- |
| Initial / 0% | What is visible before anything moves? Does layout remain understandable? |
| First movement | Which object moves first? What attention does it invite? |
| 25–50% | Is there anticipation, progressive disclosure or synchronization? |
| 50–100% | Do parts converge, resolve into a state, or start the next cycle? |
| Rest / repeat | Is there a genuine resting state? What happens on hover/scroll/reentry? |
| Interruption | Does it respond correctly to reduced motion, resize, tab hiding or route changes? |

Record only observed facts; estimated timing must be explicitly called approximate. If you cannot play the file, say "temporal behavior not verified" and don't claim a visual motion analysis.

## Motion DNA record (agent may draft, user confirms preference)

~~~yaml
reference_id: ref-example
purpose: establish spatial relationships
visual:
  line_weight: thin
  color_treatment: restrained, low contrast
motion:
  trigger: enter-viewport
  stages:
    - reveal frame
    - draw connecting paths
    - reveal endpoints
  easing: decelerating
  loop: false
liked_for:
  - sequence communicates causality
avoid_copying:
  - reference logo and exact geometry
adapt_to:
  - existing site tokens and accessible copy
confidence:
  temporal_review: directly_observed
~~~

For an animation from another project, reuse **the timing grammar**, not the source paths/illustration's recognizable expression.

## Reference selection order

1. Explicit user-provided references for this task.
2. Explicitly approved private library sources tagged for the same use case.
3. Project's already-established motion vocabulary (existing UI).
4. Original design based on general principles, clearly labeled as such.

Select at most 1–3 references and explain their relevance. CLI tag ranking is NOT model vision or a vector index; the agent must then inspect the actual media. Do not download remote sources or upload local sources without permission.

## Deliverable storyboard (minimum)

- Semantic objective (one sentence)
- 0% fallback/initial state
- Transition phases, trigger and timing
- 100% / resting state
- Reduced-motion equivalent
- Chosen mechanism and integration context
- Review criteria and browser observation notes

## Feedback loop

After user has seen real playback, invite specific feedback such as "entry too fast", "title competes with moving grid", "love the way paths converge" or "keep the resting state static". Only when asked to save that feedback, update personal taste metadata. Never auto-learn preferences by silently saving private files.
