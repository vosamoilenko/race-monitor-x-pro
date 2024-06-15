import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { useFirestore } from './useFirestore'
import { useSettingsStore } from './settings.store'
import { DateTime, Duration } from 'luxon'

export interface Driver {
  name: string
  pictureUrl: string | null
}

export interface TeamData {
  drivers: Driver[]
}

export const useTeamStore = defineStore('team', () => {
  const fb = useFirestore()
  const team = ref<Driver[]>()

  const response = fb.getDocument('team', 'team')

  watch(response, (data) => {
    // @ts-ignore
    team.value = data.team
  })

  const getTeamMemberByName = (name: string): Driver | null => {
    return team.value?.find((driver) => driver.name === name) ?? null
  }

  return {
    team,
    getTeamMemberByName
  }
})
