<script setup lang="ts">
import { defineProps, ref, watch, withDefaults } from 'vue'
import { gsap } from 'gsap'

export interface Props {
  value: number
}
const props = withDefaults(defineProps<Props>(), {})
const a = ref(-40)

watch(
  () => props.value,
  (v) => {
    const newValue = calculateRotation(v, 260)
    gsap.to(a, {
      value: newValue,
      duration: 1,
      ease: 'power1.out'
    })
  }
)

function calculateRotation(currentValue: number, maxValue: number) {
  const startAngle = -40
  const endAngle = 235

  currentValue = Math.min(currentValue, maxValue)
  const valueFraction = currentValue / maxValue
  const rotationAngle = startAngle + valueFraction * (endAngle - startAngle)

  return rotationAngle
}
</script>
<template>
  <div class="speedometr w-full h-full">
    <svg class="speed" viewBox="0 0 360 342">
      <path
        id="path"
        style="
          fill: none;
          fill-rule: evenodd;
          stroke-width: 38;
          stroke-miterlimit: 4;
          stroke: hsla(var(--muted-foreground));
          stroke-opacity: 0.5;
        "
        d="m 66.906305,293.33748 a 160.10918,160.10918 0 0 1 10e-7,-226.428566 a 160.10918,160.10918 0 0 1 226.428574,10e-7 a 160.10918,160.10918 0 0 1 -10e-6,226.428565"
      />

      <!-- <line class="line" x1="53" y1="306" x2="180" y2="180" style="stroke:rgb(255,0,0);stroke-width:2;transform-origin:63px 0px"
        /> -->
      <polygon
        id="bigLine"
        class="line"
        fill="url(#linear2)"
        points="180,168 180,192  65,188  65,172"
        style="
          fill-opacity: 0.9;
          transform-origin: 50% 50%;
          stroke: black;
          transition: 'transform 0.5s ease-out';
        "
        :style="{ transform: `rotate(${a}deg)` }"
      />

      <line class="metka" x1="180" y1="14" x2="180" y2="26" transform="rotate(226 180 180)"></line>
      <line class="metka" x1="180" y1="14" x2="180" y2="26" transform="rotate(270 180 180)"></line>
      <line class="metka" x1="180" y1="14" x2="180" y2="26" transform="rotate(315 180 180)"></line>
      <line class="metka" x1="180" y1="14" x2="180" y2="26" transform="rotate(405 180 180)"></line>
      <line class="metka" x1="180" y1="14" x2="180" y2="26" transform="rotate(450 180 180)"></line>
      <line class="metka" x1="180" y1="14" x2="180" y2="26" transform="rotate(494 180 180)"></line>
      <line class="metka" x1="180" y1="14" x2="180" y2="26"></line>

      <text x="85" y="275" class="number">0</text>
      <!-- <text x="50" y="187" class="number">5</text>
      <text x="82" y="100" class="number">10</text>
      <text x="170" y="60" class="number">15</text>
      <text x="255" y="100" class="number">20</text>
      <text x="292" y="187" class="number">25</text> -->
      <text x="255" y="275" class="number">260</text>
    </svg>
  </div>
</template>
<style>
.metka {
  stroke: hsla(var(--primary));
  stroke-width: 5;
}
.number {
  fill: hsla(var(--primary));
  font-weight: 700;
  font-size: 16px;
  opacity: 0.8;
  font-family: 'Open Sans', sans-serif;
}
.speedometr {
  position: relative;
  max-width: 350px;
}
.speed-number {
  color: hsla(var(--primary));
  font-family: 'Tulpen One', cursive;
  font-size: 82px;
  font-weight: 400;
  text-align: center;
  position: absolute;
  top: 240px;
  width: 100%;
}
</style>
