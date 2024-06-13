<template>
  <div class="grid grid-rows-3 grid-cols-10 h-screen border">
    <div class="col-span-3">
      <!-- race overview -->
      <slot name="race"></slot>
    </div>
    <div class="col-span-2">
      <!-- racers overview -->
      <slot name="racers"></slot>
    </div>
    <div class="col-span-2"></div>
    <div class="col-span-3 border">
        <slot name="map"></slot>
    </div>
    <div class="col-span-10">
      <!-- car stats -->
    </div>
    <div class="col-span-10">
        <slot name="seek"></slot>
      <!-- seek control stats -->
    </div>
  </div>
</template>
