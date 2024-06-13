import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useSettingsStore } from './settings.store'
import { useFirestore } from './useFirestore'

export interface GPSDataPoint {
  lat: number
  lon: number
  ts: number
}

export interface OBDDataPoint {
  bank1Sensor1OxygenSensorVoltage: number
  bank1Sensor2OxygenSensorVoltage: number
  calculatedEngineLoad: number
  commandedSecondaryAirStatus: string
  engineCoolantTemperature: number
  engineRpm: number
  fuelSystemStatus: string
  intakeAirTemperature: number
  longTermFuelTrimBank1: number
  mafAirFlowRate: number
  monitorStatusSinceDtcsCleared: string | number | null
  obdStandardsVehicleConformsTo: string | null
  oxygenSensorsPresent: number
  shortTermFuelTrimBank1: number
  throttlePosition: number
  timingAdvance: number
  ts: number
  vehicleSpeed: number
}

export type CarDataPoint = OBDDataPoint | GPSDataPoint
export type JoinedCarDataPoint = OBDDataPoint & GPSDataPoint

export function isGPSDataPoint(data: OBDDataPoint | GPSDataPoint): data is GPSDataPoint {
  return (data as GPSDataPoint).lat !== undefined
}

export function isOBDDataPoint(data: OBDDataPoint | GPSDataPoint): data is OBDDataPoint {
  return (data as OBDDataPoint).vehicleSpeed !== undefined
}

export const useDatapointsStore = defineStore('datapoints', () => {
  const route = useRoute()
  const settingsStore = useSettingsStore()
  const fb = useFirestore()
  const settingsRef = ref(null)

  watch(
    () => route.params.raceId,
    async (raceId) => {
      console.log({ raceId })
      const value = await fb.getDataDocumentData(raceId as string)
      const data = value[0].data()
      datapoints.value = data.entries
    },
    { immediate: true }
  )

  const datapoints = ref<CarDataPoint[]>([])

  const obdDatapoints = computed(() => {
    return datapoints.value.filter(isOBDDataPoint)
  })
  const gpsDatapoints = computed(() => {
    return datapoints.value.filter(isGPSDataPoint)
  })

  const latestOBDDatapoint = computed(() => {
    return obdDatapoints.value[obdDatapoints.value.length - 1] ?? null
  })
  const latestGPSDatapoint = computed(() => {
    return gpsDatapoints.value[gpsDatapoints.value.length - 1] ?? null
  })

  const allTimingAdvance = computed(() => {
    return datapoints.value
      .filter(isOBDDataPoint)
      .map((datapoint) => ({
        timestamp: datapoint.ts,
        timingAdvance: datapoint.timingAdvance,
        throttlePosition: datapoint.throttlePosition,
        vehicleSpeed: datapoint.vehicleSpeed,
        engineSpeed: (datapoint.engineRpm ?? 0) / 100
      }))
      .reverse()
      .slice(0, 20)
  })

  return {
    datapoints,
    latestOBDDatapoint,
    latestGPSDatapoint,
    obdDatapoints,
    gpsDatapoints,
    allTimingAdvance
  }
})
