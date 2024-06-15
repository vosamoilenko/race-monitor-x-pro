<script setup lang="ts">
import { computed } from 'vue'
import { useTracksStore } from '../../stores/tracks.store'
import { useTeamStore } from '../../stores/team.store'
import { DateTime } from 'luxon'

const tracksStore = useTracksStore()
const teamStore = useTeamStore()

function formatDuration(startTime: string, endTime: string) {
  const start = DateTime.fromISO(startTime)
  const end = DateTime.fromISO(endTime)

  if (!start.isValid || !end.isValid) {
    return 'Invalid DateTime'
  }

  const duration = end.diff(start, ['hours', 'minutes'])
  return `${duration.hours}h ${Math.round(duration.minutes)}m`
}

const raceStatus = computed(() => {
  const now = DateTime.now()
  const start = DateTime.fromISO(tracksStore.currentTrack?.startTime || '')
  const end = DateTime.fromISO(tracksStore.currentTrack?.endTime || '')

  if (!start.isValid || !end.isValid) {
    return 'Invalid DateTime'
  }

  if (now > end) {
    return 'Race status: Finished'
  } else if (now >= start && now <= end) {
    return 'Race status: Racing'
  } else {
    const daysUntilStart = start.diff(now, 'days').days
    return `Race status: Expected in ${Math.ceil(daysUntilStart)} days`
  }
})
</script>

<template>
  <div class="shadow-md rounded-lg flex items-center justify-center border h-full">
    <div class="w-full max-w-4xl">
      <div class="p-6">
        <a class="text-3xl font-bold hover:underline" :href="tracksStore.currentTrack?.website">
          {{ tracksStore.currentTrack?.name }}
        </a>
        <div class="text-gray-500 mt-1">{{ raceStatus }}</div>
        <div class="text-gray-600 mt-2">
          <div v-if="tracksStore.currentTrack?.startTime">
            Start Time:
            {{ DateTime.fromISO(tracksStore.currentTrack.startTime).toFormat('dd MMM yyyy HH:mm') }}
          </div>
          <div v-if="tracksStore.currentTrack?.endTime">
            End Time:
            {{ DateTime.fromISO(tracksStore.currentTrack.endTime).toFormat('dd MMM yyyy HH:mm') }}
          </div>
          <div v-if="tracksStore.currentTrack?.startTime && tracksStore.currentTrack?.endTime">
            Duration:
            {{
              formatDuration(tracksStore.currentTrack.startTime, tracksStore.currentTrack.endTime)
            }}
          </div>
        </div>
        <div class="mt-4">
          <div class="text-lg font-semibold text-gray-800">Participants:</div>
          <div class="flex space-x-2 mt-2">
            <div
              v-for="member in teamStore.team"
              :key="member.name"
              class="w-10 h-10 rounded-full overflow-hidden bg-gray-200"
            >
              <img
                v-if="member.pictureUrl"
                :src="member.pictureUrl"
                alt="Avatar"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-500">
                {{ member.name.charAt(0).toUpperCase() }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
