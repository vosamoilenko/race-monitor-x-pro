import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { useRoute } from 'vue-router'
import { useFirestore } from './useFirestore'
import { DateTime } from 'luxon'
import { filterShiftsByTimestamp, findRacingShift } from '../utils/racing-shift-utils'
import { useRaceDashboardStore } from './race-dashboard.store'

export interface RacingShift {
  from: string
  to: string
  racer: string
}

export const useRacingShiftsStore = defineStore('racing-shifts', () => {
  const raceDashboardStore = useRaceDashboardStore()
  const route = useRoute()
  const fb = useFirestore()
  const shifts = ref<RacingShift[]>([])

  watch(
    () => route.params.raceId,
    async (raceId) => {
      const response = fb.getDocument('racing-shifts', raceId as string)

      watch(response, (data) => {
        // @ts-ignore
        shifts.value = data.shifts
      })
    },
    { immediate: true }
  )

  const getCurrentDriverInfo = (timestamp: number) => {
    return findRacingShift(shifts.value, timestamp)
  }
  const getAvailableShiftsBasedOnCurrentDataTimestamp = computed(() => {
    if (!raceDashboardStore.currentData?.ts) {
      return []
    }

    const currentTimestamp = raceDashboardStore.currentData.ts
    return filterShiftsByTimestamp(shifts.value, currentTimestamp).reverse()
  })

  return { shifts, getCurrentDriverInfo, getAvailableShiftsBasedOnCurrentDataTimestamp }
})
