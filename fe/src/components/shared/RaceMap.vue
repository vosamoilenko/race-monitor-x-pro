<template>
  <div :ref="(el) => (mapRef = el)" class="map-overlay" style="width: 100%; height: 100%"></div>
</template>

<script setup lang="ts">
import 'ol/ol.css'
import { ref, computed, watch, onMounted, onUnmounted, defineProps, withDefaults } from 'vue'
import Map from 'ol/Map'
import OSM from 'ol/source/OSM.js'
import View from 'ol/View.js'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import { Style, Stroke } from 'ol/style.js'
import { LineString } from 'ol/geom'
import Feature from 'ol/Feature'
import { fromLonLat } from 'ol/proj'
import { useRaceDashboardStore } from '../../stores/race-dashboard.store'

export interface GPSDataPoint {
  lat: number
  lon: number
  ts: number
}

export interface Props {
  gpsDatapoints: GPSDataPoint[]
}

const props = withDefaults(defineProps<Props>(), { gpsDatapoints: () => [] })

const initialZoomLevel = 16

const mapRef = ref<HTMLElement | null>(null)

const items = computed(() => {
  return props.gpsDatapoints
})

const reversedOrderItems = computed(() => {
  return items.value.slice().reverse()
})

const view = new View({
  center: [0, 0],
  zoom: initialZoomLevel,
  projection: 'EPSG:3857' // Setting the projection to EPSG:3857 for OSM tiles
})

const vectorSource = new VectorSource()
const vectorLayer = new VectorLayer({
  source: vectorSource,
  style: new Style({
    stroke: new Stroke({
      color: 'rgba(255, 61, 61, 1)',
      width: 2
    })
  })
})

let map = new Map({
  layers: [
    new TileLayer({
      source: new OSM()
    }),
    vectorLayer
  ],
  view,
  controls: [],
  interactions: []
})

const createLineStringFromPoints = (points: GPSDataPoint[]) => {
  const coordinates = points.map((point) => fromLonLat([point.lon, point.lat]))
  return new LineString(coordinates)
}

const updateMap = () => {
  const lineString = createLineStringFromPoints(items.value)
  const lineFeature = new Feature({
    geometry: lineString
  })

  vectorSource.clear()
  vectorSource.addFeature(lineFeature)
}

const centerMapOnLastPoint = () => {
  if (reversedOrderItems.value.length === 0) {
    return
  }

  const lastPoint = reversedOrderItems.value[0]
  view.setCenter(fromLonLat([lastPoint.lon, lastPoint.lat]))
}

watch(items, (newItems) => {
  updateMap()
  centerMapOnLastPoint()
})

const store = useRaceDashboardStore()
watch(
  () => store.currentIndex,
  (newIndex) => {
    updateMap()
    centerMapOnLastPoint()
  }
)

onMounted(() => {
  if (mapRef.value) {
    map.setTarget(mapRef.value)
    updateMap()
    centerMapOnLastPoint()
  }
})

onUnmounted(() => {
  map.setTarget(undefined)
  map = undefined!
})
</script>

<style scoped>
.map-overlay {
  width: 100%;
  height: 100%;
}
</style>
