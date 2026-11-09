<script setup lang="ts">
withDefaults(defineProps<{
  eyebrow?: string
  title?: string
  description?: string
}>(), {
  eyebrow: 'SPATIAL INTELLIGENCE',
  title: 'See relationships clearly',
  description: 'A quiet visual system that supports the message instead of competing with it.',
})
</script>

<template>
  <section class="motion-hero">
    <div class="motion-copy">
      <p class="eyebrow">{{ eyebrow }}</p>
      <h1>{{ title }}</h1>
      <p class="description">{{ description }}</p>
    </div>

    <svg
      class="motion-visual"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 540 420"
      aria-hidden="true"
      focusable="false"
      preserveAspectRatio="xMidYMid meet"
    >
      <circle class="halo" cx="270" cy="210" r="150" />
      <circle class="ring" cx="270" cy="210" r="116" />
      <circle class="ring secondary" cx="270" cy="210" r="74" />
      <g class="orbit orbit-primary">
        <circle cx="270" cy="94" r="9" class="point" />
        <circle cx="270" cy="94" r="20" class="point-glow" />
      </g>
      <g class="orbit orbit-secondary">
        <circle cx="344" cy="210" r="6" class="point light" />
      </g>
      <path class="axis" d="M120 210 H420 M270 60 V360" />
      <circle class="core" cx="270" cy="210" r="36" />
      <circle class="core-center" cx="270" cy="210" r="7" />
    </svg>
  </section>
</template>

<style scoped>
.motion-hero {
  --motion-accent: var(--color-primary, #645dc8);
  --motion-ink: var(--color-text, #1c2440);
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  align-items: center;
  gap: clamp(2rem, 5vw, 5rem);
  padding: clamp(3rem, 8vw, 7rem) clamp(1.5rem, 5vw, 6rem);
  background: var(--color-surface, transparent);
  color: var(--motion-ink);
}
.motion-copy { max-width: 35rem; position: relative; z-index: 1; }
.eyebrow { letter-spacing: .15em; font-size: .75rem; font-weight: 700; color: var(--motion-accent); }
h1 { font-size: clamp(2.3rem, 4.5vw, 4.6rem); line-height: 1.08; letter-spacing: -.035em; }
.description { font-size: clamp(1rem, 1.4vw, 1.2rem); opacity: .72; line-height: 1.65; }
.motion-visual { width: 100%; height: auto; overflow: visible; color: var(--motion-accent); }
.halo { fill: currentColor; opacity: .045; }
.ring, .axis { fill: none; stroke: currentColor; stroke-width: 1.5; opacity: .23; }
.ring.secondary { opacity: .14; }
.axis { opacity: .12; }
.core { fill: currentColor; opacity: .13; }
.core-center, .point { fill: currentColor; }
.point-glow { fill: currentColor; opacity: .13; }
.point.light { opacity: .6; }
.orbit {
  transform-box: view-box;
  transform-origin: center;
  animation: turn 16s linear infinite;
}
.orbit-secondary { animation-duration: 25s; animation-direction: reverse; }
@keyframes turn { to { transform: rotate(360deg); } }
@media (max-width: 760px) {
  .motion-hero { grid-template-columns: 1fr; }
  .motion-visual { max-width: 480px; margin: -1rem auto 0; }
}
@media (prefers-reduced-motion: reduce) {
  .orbit { animation: none; }
}
</style>
