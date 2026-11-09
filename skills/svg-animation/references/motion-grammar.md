# Motion grammar: a practical design language

Animation is communication over time. Decide **what changes, why now, and what the viewer learns**.

## Useful pattern vocabulary

| Pattern | Use it for | Avoid |
| --- | --- | --- |
| Draw / trace | explain connections, routes, causal graphs | overly long paths that delay information |
| Reveal / stagger | progressive information hierarchy | animating every card independently |
| Morph | relationship between two related shapes or states | arbitrary shape change that obscures meaning |
| Follow path | movement along a known flow | endless movement with no semantic goal |
| Orbit / drift | subdued ambient spatial context | too many moving dots behind important text |
| Expand / collapse | show ownership or disclosure | layout jumps and broken focus |
| Spring feedback | direct response to user input | slow rebounds on productivity controls |
| Scroll sequence | step-by-step story tied to reading | scroll-jacking and inaccessible core content |
| Data transition | explain a value/shape comparison | ambiguous or misleading interpolation |

## Timing as a design decision

These are starting points, not standards or hard rules:

- Direct interactive response: roughly 100–220 ms; immediately acknowledge input.
- Entrance / short reveal: roughly 250–600 ms.
- Narrative beat: roughly 600–1400 ms if it carries a real story.
- Ambient movement: slow and low amplitude, only if it does not compete with content.

Prefer a shared timeline to independent random durations. Stagger only enough to establish sequence. A brief pause can communicate more than another effect. For dashboards, keep core reading fast.

## Easing

- ease-out: arrives naturally into stable state; useful for entrances.
- ease-in-out: calm travel between two states.
- linear: uniform progress, tracing, loading or rotations where constant speed is intentional.
- spring: physically suggestive direct manipulation; clamp overshoot around precise labels.
- custom Bézier: tune only when a visual reference or brand system justifies it.

Avoid bounce/everywhere; motion should not make factual labels or data feel unstable.

## SVG-specific mechanisms

**Stroke drawing:** normalize with pathLength="1" then animate stroke-dasharray / stroke-dashoffset, or compute getTotalLength() in browser for a specific path. Test paths with markers/dash patterns. For stroke reveal, avoid filling until the reveal is complete unless intentionally choreographed.

**Morph:** path d represents a geometric sequence of points/commands, not a semantic shape. Different shapes may require path normalization/point sampling, orientation checks and careful correspondence. SVG path interpolation isn't universally smooth by itself.

**Motion path:** use SVG animateMotion, CSS offset-path or a JS library; if orientation matters, align rotation to tangent and test boundaries.

**Transform origin:** SVG CSS transforms have browser-specific coordinate expectations; define transform-box: fill-box / view-box and transform-origin explicitly, then visually verify.

**Filters:** blur, turbulence and displacement can be expensive when continuously updated. Use sparingly and check mobile rendering.

## Motion density budget

Classify every moving object as primary (meaning), secondary (support) or ambient (decoration). A page should have one dominant motion idea in any visual area. Ambient loops should stop being the most noticeable thing after the first few seconds; if uncertain, remove them.

## Three stages, not one continuous trick

1. **Establish:** a readable static composition or an intentional entrance.
2. **Explain:** the smallest motion that reveals relationship or state.
3. **Rest:** settle; user can read and interact.

Design reduced motion as another valid state, not an error condition.
