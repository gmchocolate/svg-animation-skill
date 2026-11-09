# Production Vue 3 / Nuxt practices

## Integration contract

1. Keep informational text and controls semantic HTML, not SVG text unless the visual is inherently a diagram.
2. Do not read window/document/matchMedia during SSR module evaluation or setup without guards.
3. For JS-driven sequences: create them in onMounted, destroy or revert in onBeforeUnmount, and interrupt cleanly on route changes.
4. Avoid initial invisible content: the page should be useful even when animation never runs or hydration fails.
5. Give SVG a stable viewBox and aspect-ratio; place it behind content when decorative and use aria-hidden="true" focusable="false".
6. Component styles should use the site's theme tokens (e.g. currentColor / CSS variables), not an unrelated palette.
7. Respect prefers-reduced-motion in CSS AND JS; if it changes during a session, adjust correctly.
8. Avoid animation that intercepts pointer events or scroll; do not obscure keyboard focus.
9. If IDs are required for gradients/clipPaths, generate unique IDs per component instance (Vue useId() in supported versions) or namespace deterministically; repeated SVG IDs can collide.
10. Mobile and high-DPI preview are required for visual acceptance.

## Prefer CSS for simple decorative motion

See ../examples/hero-orbit.vue. It is SSR-safe, needs no dependency, reserves layout, hides decoration from assistive tech and stops ambient motion under reduced-motion.

## JS-driven timeline pseudocode

~~~ts
import { onMounted, onBeforeUnmount, ref } from "vue";

const svgRoot = ref<SVGSVGElement | null>(null);
let cleanup: (() => void) | undefined;

onMounted(async () => {
  if (!svgRoot.value) return;
  const query = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (query.matches) return; // static fallback must already be readable

  // Import GSAP/Anime.js client-side only if this component truly needs it.
  // Scope selectors to svgRoot.value; do not grab other components' IDs.
  // Create the timeline and register any event listeners here.
  cleanup = () => {
    // kill/cancel/revert timeline; remove listeners/observers
  };
});

onBeforeUnmount(() => {
  cleanup?.();
});
~~~

This is intentionally a contract, not runnable GSAP code. Choose the actual library and cleanup API based on the project's installed version. For `prefers-reduced-motion` changes during playback, listen for the media-query change event and cancel or settle animations, then remove that listener in cleanup.

## Testing checklist

- SSR render and hydration have no console warnings.
- The visual has a well-defined width, height and viewBox.
- Entrance plays once on the appropriate trigger and doesn't flicker on route back.
- Multiple component instances do not share IDs or accidentally target each other.
- A mobile viewport does not crop meaningful nodes.
- Reduced-motion mode is meaningful and not hidden/invisible.
- Route navigation and unmount free observers, timelines, raf and event listeners.
- Semantic keyboard behavior and screen-reader names remain correct.
