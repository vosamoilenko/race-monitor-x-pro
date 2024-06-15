import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { useFirestore } from './useFirestore'

export interface Track {
  id: string
  lan: string
  lon: string
  name: string
  website: string
  startTime: string
  endTime: string
}

export const useTracksStore = defineStore('tracks', () => {
  const route = useRoute()

  const fb = useFirestore()
  const tracks = ref<Track[]>()

  const response = fb.getDocument('tracks', 'tracks')
  watch(
    () => response.value,
    (value) => {
      if (!value) return
      tracks.value = value.tracks
    },
    { immediate: true }
  )

  const currentTrack = computed(() => {
    return tracks.value?.find((track) => route.params.raceId.includes(track.id)) ?? null
  })

  return {
    currentTrack,
    tracks
  }
})
