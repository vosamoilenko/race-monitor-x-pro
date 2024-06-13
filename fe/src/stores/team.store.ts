import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { useFirestore } from './useFirestore'
import { useSettingsStore } from './settings.store'
import { DateTime, Duration } from 'luxon'

export interface Driver {
  name: string
  drivingDuration: string | null
  notDrivingSince: string | null
  pictureUrl: string | null
}

export interface TeamData {
  drivers: Driver[]
}

export const useTeamStore = defineStore('team', () => {
  const fb = useFirestore()
  const team = ref<Driver[]>()

  const settingsStore = useSettingsStore()
  const teamRef = fb.getUseTeamDocument()

  watch(teamRef, (teamData) => {
    // map to human readable format the drivingDuration that is in duration iso format
    // and notDrivingSince that is in iso format
    const teamMappedData = teamData?.team.map((driver) => {
      const drivingDuration = driver.drivingDuration
        ? Duration.fromISO(driver.drivingDuration)
        : null

      const notDrivingSince = driver.notDrivingSince
        ? DateTime.fromISO(driver.notDrivingSince)
        : null

      return {
        ...driver,
        drivingDuration: drivingDuration?.isValid
          ? `${drivingDuration.hours}h ${drivingDuration.minutes}m`
          : '-',
        notDrivingSince: notDrivingSince?.isValid
          ? `${notDrivingSince.hour}h ${notDrivingSince.minute}m`
          : '-'
      }
    })

    team.value = (teamMappedData ?? []) as Driver[]
  })

  const currentDriver = computed(() => {
    if (!team.value?.length) {
      return null
    }
    if (!settingsStore.settings?.currentRacerId) {
      return null
    }

    return team.value.find((m) => m.name === settingsStore.settings?.currentRacerId) ?? null
  })

  return {
    team,
    currentDriver
  }
})
