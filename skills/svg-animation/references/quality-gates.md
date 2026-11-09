# Quality gates for SVG web motion

## Acceptance scorecard (0–2 each, 20 total)

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Purpose | random decoration | recognizable intent | clearly supports understanding/action |
| Hierarchy | competing motion | partial focus | one obvious focus |
| Timing | awkward or jittery | acceptable | coherent staging, easing and rest |
| Restraint | excessive loops | some clutter | calm, deliberate composition |
| Visual integration | alien to product | mostly aligned | matches typography, palette, spacing |
| Responsiveness | clipped or breaks | minor defects | excellent mobile/desktop behavior |
| Accessibility | inaccessible | reduced mode incomplete | static/reduced equivalent works |
| Performance | costly repeated work | mostly acceptable | efficient, verified in browser |
| Technical safety | untrusted code/links | unresolved risks | safe input and lifecycle behavior |
| Craft | crude geometry or artifacts | workable | crisp and polished across states |

Do not invent a score for a non-rendered animation. For a project review, evaluate the actual playback. A draft may pass static code checks but still fail visual hierarchy.

## Hard failures regardless of score

- Essential page content is invisible without JS.
- Reduced-motion preference is ignored for intense, continuous motion, or its replacement hides required information.
- SVG is injected from untrusted sources with script, foreignObject or external resources.
- User data, labels, map metrics or chart values are fabricated or distorted by the animation.
- The animation blocks keyboard focus, scrolling or clicks.
- Third-party branding or proprietary artwork is copied from a reference.
- A cloud-hosted agent claims local file access it doesn't have.

## Static check (standalone .svg only)

~~~bash
python skills/svg-animation/scripts/check_svg.py path/to/file.svg
python skills/svg-animation/scripts/check_svg.py --strict path/to/file.svg
~~~

The checker detects basic unsafe constructs and common markup concerns, not visual quality, script-defined behavior in an external page, or complete XSS safety. Never interpret a pass as a security audit.

## Browser review protocol

Inspect three frames (entry, transition, rest), plus a full repeat if looping. Test at least one desktop and one small/mobile viewport; use prefers-reduced-motion; interact with keyboard where appropriate. If tooling supports performance inspection, measure scripting/paint and compare the page with motion disabled. Do not claim "60fps" without evidence.

Look for:
- noticeable layout shift or initial-state flash;
- collisions with text, excessive contrast/blur or moving backgrounds;
- a path that draws backward or morphs through nonsensical geometry;
- loops restarting unexpectedly after route changes;
- excessive SVG filters or large numbers of animated nodes;
- missing pause when offscreen;
- invisible focus outlines or click overlays.

## Error correction priority

1. Broken semantics, factual accuracy and accessibility.
2. Timing/interaction bugs and movement stealing focus.
3. Strongest aesthetic mismatches (composition, hierarchy, rhythm).
4. Minor easing/decoration.

Prefer deleting effects to adding more.
