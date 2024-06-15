<script setup lang="ts">
import 'ol/ol.css'
import {
  ref,
  computed,
  watch,
  onMounted,
  onUnmounted,
  defineProps,
  withDefaults,
  nextTick,
  type VNodeRef
} from 'vue'
import Map from 'ol/Map'
import OSM from 'ol/source/OSM.js'
import View from 'ol/View.js'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import { Style, Stroke, Circle as CircleStyle, Fill } from 'ol/style.js'
import { LineString, Point } from 'ol/geom'
import Feature from 'ol/Feature'
import { fromLonLat } from 'ol/proj'
import { useRaceDashboardStore } from '../../stores/race-dashboard.store'
import { useUtilStore } from '../../stores/util.store'

export interface GPSDataPoint {
  lat: number
  lon: number
  ts: number
}

export interface Props {
  gpsDatapoints: GPSDataPoint[]
}

const utilStore = useUtilStore()
const props = withDefaults(defineProps<Props>(), { gpsDatapoints: () => [] })

const raceDashboardStore = useRaceDashboardStore()
const initialZoomLevel = 16
const mapRef = ref<HTMLElement | null>(null)

const items = computed(() => props.gpsDatapoints)

const reversedOrderItems = computed(() => items.value.slice().reverse())

const view = new View({
  center: [0, 0],
  zoom: initialZoomLevel,
  projection: 'EPSG:3857' // Setting the projection to EPSG:3857 for OSM tiles
})

const vectorSource = new VectorSource()
const markerSource = new VectorSource()

const getStrokeColor = (obdData: any) => {
  if (!obdData) return 'rgba(0, 255, 0, 1)' // default green
  const { throttlePosition, vehicleSpeed, engineRpm } = obdData
  return throttlePosition > 30 || vehicleSpeed > 30 || engineRpm > 2000
    ? 'rgba(255, 0, 0, 1)'
    : 'rgba(0, 255, 0, 1)' // red or green
}

const createSegmentsFromPoints = (points: GPSDataPoint[]) => {
  const segments = []
  for (let i = 0; i < points.length - 1; i++) {
    const start = points[i]
    const end = points[i + 1]
    const obdData = raceDashboardStore.getOBDDataAtTimestamp(start.ts)
    const color = getStrokeColor(obdData)
    const segment = new Feature({
      geometry: new LineString([fromLonLat([start.lon, start.lat]), fromLonLat([end.lon, end.lat])])
    })
    segment.set(
      'style',
      new Style({
        stroke: new Stroke({ color, width: 2 })
      })
    )
    segments.push(segment)
  }
  return segments
}

const createMarkerFeature = (point: GPSDataPoint) =>
  new Feature({
    geometry: new Point(fromLonLat([point.lon, point.lat])),
    style: new Style({
      image: new CircleStyle({
        radius: 5,
        fill: new Fill({ color: 'blue' })
      })
    })
  })

let map = new Map({
  layers: [
    new TileLayer({ source: new OSM() }),
    new VectorLayer({
      source: vectorSource,
      style: (feature) => feature.get('style')
    }),
    new VectorLayer({ source: markerSource })
  ],
  view,
  controls: [],
  interactions: []
})

const updateMap = () => {
  console.log('Updating map...')
  const segments = createSegmentsFromPoints(items.value)
  vectorSource.clear()
  vectorSource.addFeatures(segments)
  if (items.value.length > 0) {
    const lastPoint = items.value[items.value.length - 1]
    const markerFeature = createMarkerFeature(lastPoint)
    markerSource.clear()
    markerSource.addFeature(markerFeature)
  }
}

const centerMapOnLastPoint = () => {
  if (reversedOrderItems.value.length === 0) return
  const lastPoint = reversedOrderItems.value[0]
  view.setCenter(fromLonLat([lastPoint.lon, lastPoint.lat]))
}

const calculateMapHeight = async () => {
  await nextTick() // Ensure the DOM is fully rendered
  const canvas = document.querySelector('canvas')
  const canvasHeight = canvas ? canvas.getBoundingClientRect().height : 0
  const calculatedHeight = canvasHeight > 0 ? canvasHeight : 400 // default to 400px if calculation fails
  utilStore.setMapHeight(calculatedHeight)
}

watch(items, (newItems) => {
  updateMap()
  centerMapOnLastPoint()
  calculateMapHeight() // Update height when data changes
})

const store = useRaceDashboardStore()
watch(
  () => store.currentIndex,
  (newIndex) => {
    updateMap()
    centerMapOnLastPoint()
    calculateMapHeight() // Update height when index changes
  }
)

onMounted(async () => {
  await calculateMapHeight()
  window.addEventListener('resize', calculateMapHeight)
  if (mapRef.value) {
    map.setTarget(mapRef.value)
    updateMap()
    centerMapOnLastPoint()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateMapHeight)
  map.setTarget(undefined)
  map = undefined!
})

const assignRef = (el: Element | ComponentPublicInstance | null) => {
  if (!el) return
  mapRef.value = el as unknown as HTMLElement
}
</script>
<template>
  <div
    :ref="assignRef"
    class="map-overlay rounded-lg overflow-hidden shadow-md"
    style="width: 100%; height: 100%"
  ></div>
</template>
s
