<template>
  <div
    class="grid gap-3 grid-rows-3 grid-cols-10 h-screen p-2"
    style="grid-template-rows: minmax(0, 2fr) minmax(0, 1fr) 50px"
  >
    <div class="col-span-4">
      <slot name="race"></slot>
    </div>
    <div class="col-span-2">
      <slot name="racers"></slot>
    </div>
    <div class="col-span-4">
      <slot name="map"></slot>
    </div>
    <div class="col-span-10">
      <slot name="car"></slot>
    </div>
    <div class="col-span-10">
      <slot name="seek"></slot>
    </div>
  </div>
</template>
