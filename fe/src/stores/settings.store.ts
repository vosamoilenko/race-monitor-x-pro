import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useFirestore } from './useFirestore'

export interface SettingsData {
    currentRacerId: string
}

export const useSettingsStore = defineStore('settings', () => {
  const fb = useFirestore()
  const settings = ref<SettingsData>()

  const settingsRef = fb.getUseSettingsDocument()

  watch(settingsRef, (settingsRefData) => {
    if (settingsRefData) {
      settings.value = settingsRefData as SettingsData
    }
  })

  return {
    settings
  }
})
