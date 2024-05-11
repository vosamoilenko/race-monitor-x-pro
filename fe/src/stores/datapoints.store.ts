import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { DateTime } from 'luxon'
import { timestamp } from '@vueuse/core'
import { throttle } from '@unovis/ts'

export interface DataPointEntry {
  value: number | null
  timestamp: DateTime | null
}

export interface DataPoint {
  monitorStatus?: DataPointEntry
  engineLoad?: DataPointEntry
  coolantTemperature?: DataPointEntry
  intakeManifoldPressure?: DataPointEntry
  engineSpeed?: DataPointEntry
  vehicleSpeed?: DataPointEntry
  timingAdvance?: DataPointEntry
  intakeAirTemperature?: DataPointEntry
  mafSensorAirFlowRate?: DataPointEntry
  throttlePosition?: DataPointEntry
}

export const useDatapointsStore = defineStore('datapoints', () => {
  const datapoints = ref<DataPoint[]>([])

  const latestDatapoint = computed(() => {
    return datapoints.value[datapoints.value.length - 1] ?? null
  })

  const allTimingAdvance = computed(() => {
    return datapoints.value.map((datapoint) => ({
      timestamp: datapoint.monitorStatus?.timestamp,
      timingAdvance: datapoint.timingAdvance?.value,
      throttlePosition: datapoint.throttlePosition?.value,
      vehicleSpeed: datapoint.vehicleSpeed?.value,
      engineSpeed: (datapoint.engineSpeed?.value ?? 0) / 100
    })).reverse().slice(0,20)
  })

  const startPooling = () => {
    let i = 0
    setInterval(() => {
      fetchDatapoint(i % 57)
      i += 1
    }, 1000)
  }

  function fetchDatapoint(id: string | number) {
    try {
      fetch('http://localhost:3000/data/' + (Number(id) % 57))
        .then((response) => response.json())
        .then((_data) => {
          datapoints.value.push(_data)
        })
    } catch (e) {
      console.error(e)
    }
  }

  return {
    datapoints,
    latestDatapoint,
    allTimingAdvance,
    startPooling
  }
})
