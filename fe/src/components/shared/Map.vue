<script setup lang="ts">
export interface Props {
  history: any[]
}
const props = withDefaults(defineProps<Props>(), { history: () => [] })

const center = computed(() => {
  if (props.history.length === 0) {
    return { lat: 0, lng: 0 }
  }
  const last = props.history[props.history.length - 1]
  console.log({ lat: last.lat, lng: last.lon })
  return { lat: last.lat, lng: last.lon }
})

const items = computed(() => {
  return [...props.history].sort((a, b) => a.ts - b.ts)
})
</script>
<template>
  <GMapMap :center="center" :zoom="7" map-type-id="terrain" style="width: 100vw; height: 100vh">
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
