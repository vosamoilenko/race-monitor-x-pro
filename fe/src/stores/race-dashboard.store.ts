import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import {
  isGPSDataPoint,
  useDatapointsStore,
  type CarDataPoint,
  type JoinedCarDataPoint
} from './datapoints.store'

export const useRaceDashboardStore = defineStore('race-dashboard', () => {
  const datapointStore = useDatapointsStore()

  const entries = ref<CarDataPoint[]>([])
  const currentIndex = ref(0)
  const state = ref<JoinedCarDataPoint | null>(null)

  watch(
    () => datapointStore.datapoints,
    (datapoints) => {
      entries.value = datapoints
    }
  )

  const allGPSDateUntilIndex = computed(() => {
    const filteredEntries = entries.value.slice(0, currentIndex.value + 1).filter(isGPSDataPoint)

    return filteredEntries.slice(Math.max(filteredEntries.length - 100, 0))
  })

  // Helper function to perform binary search
  const binarySearchClosest = (key: string, index: number) => {
    let low = 0
    let high = index

    while (low <= high) {
      const mid = Math.floor((low + high) / 2)
      if (
        // @ts-ignore
        entries.value[mid][key] !== undefined &&
        // @ts-ignore
        (mid === index || entries.value[mid + 1][key] === undefined)
      ) {
        return entries.value[mid]
        // @ts-ignore
      } else if (entries.value[mid][key] !== undefined) {
        low = mid + 1
      } else {
        high = mid - 1
      }
    }

    return null
  }

  // Find the closest values without exceeding the index
  const findClosestValues = (index: number) => {
    const closestGPS = binarySearchClosest('lat', index)
    const closestOBD = binarySearchClosest('engineRpm', index)

    return { closestGPS, closestOBD }
  }

  const currentData = computed(() => {
    if (!entries.value.length) {
      return null
    }

    const { closestGPS, closestOBD } = findClosestValues(currentIndex.value)

    return {
      ...closestGPS,
      ...closestOBD,
      ts: entries.value[currentIndex.value]?.ts
    }
  })

  const incrementIndex = () => {
    if (currentIndex.value < entries.value.length - 1) {
      currentIndex.value++
    }
  }

  const decrementIndex = () => {
    if (currentIndex.value > 0) {
      currentIndex.value--
    }
  }

  const setIndex = (index: number) => {
    if (index >= 0 && index < entries.value.length) {
      currentIndex.value = index
    }
  }

  return {
    entries,
    currentIndex,
    currentData,
    incrementIndex,
    decrementIndex,
    setIndex,
    allGPSDateUntilIndex
  }
})
