<template>
  <div
    class="grid gap-3 grid-rows-3 grid-cols-10 h-screen p-2"
    style="grid-template-rows: minmax(0, 1fr) minmax(0, 1fr) 50px"
  >
    <div class="col-span-3">
      <!-- race overview -->
      <slot name="race"></slot>
    </div>
    <div class="col-span-3">
      <!-- racers overview -->
      <slot name="racers"></slot>
    </div>
    <div class="col-span-4">
      <slot name="map"></slot>
    </div>
    <div class="col-span-10">
      <slot name="car"></slot>
      <!-- car stats -->
    </div>
    <div class="col-span-10">
      <slot name="seek"></slot>
      <!-- seek control stats -->
    </div>
  </div>
</template>
