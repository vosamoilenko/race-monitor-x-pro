<script setup lang="ts">
import type { GPSDataPoint } from '../../stores/datapoints.store';

export interface Props {
  gpsDatapoints: GPSDataPoint[]
}
const props = withDefaults(defineProps<Props>(), { gpsDatapoints: () => [] })

const center = computed(() => {
  if (props.gpsDatapoints.length === 0) {
    return { lat: 0, lng: 0 }
  }
  const last = props.gpsDatapoints[props.gpsDatapoints.length - 1]
  return { lat: last.lat, lng: last.lon }
})

const items = computed(() => {
  return [...props.gpsDatapoints].sort((a, b) => a.ts - b.ts)
})
</script>
<template>
  <GMapMap :center="center" :zoom="16" map-type-id="terrain" style="width: 100%; height: 100%">
    <GMapCluster v-if="items.length">
      <GMapMarker
        v-for="value in items"
        :key="value.ts"
        :position="{ lat: value.lat, lng: value.lon }"
        :clickable="true"
        :draggable="true"
        @click="center = { lat: value.lat, lng: value.lon }"
      />
    </GMapCluster>
  </GMapMap>
</template>
