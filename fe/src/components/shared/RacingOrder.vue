<script setup lang="ts">
import { DateTime, Interval } from 'luxon'
import { useRacingShiftsStore } from '../../stores/racing-shifts.store'
import { useTeamStore } from '../../stores/team.store'
import { useUtilStore } from '../../stores/util.store'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

const teamStore = useTeamStore()
const racingShiftsStore = useRacingShiftsStore()
const utilStore = useUtilStore()

function formatDuration(from: string, to: string) {
  const fromDate = DateTime.fromISO(from)
  const toDate = DateTime.fromISO(to)
  const duration = Interval.fromDateTimes(fromDate, toDate).toDuration(['hours', 'minutes'])

  return `${duration.hours}h ${Math.round(duration.minutes)}m`
}

const getMapHeightStyles = () => {
  return {
    'max-height': `${utilStore.mapHeight - 48}px`,
    'min-height': `${utilStore.mapHeight - 48}px`
  }
}
</script>
<template>
  <div v-if="racingShiftsStore.getAvailableShiftsBasedOnCurrentDataTimestamp.length">
    <div
      class="overflow-container p-2 overflow-y-scroll border rounded-lg w-full shadow-md"
      :style="getMapHeightStyles()"
    >
      <div
        class="flex items-center p-1 w-full"
        v-for="shift in racingShiftsStore.getAvailableShiftsBasedOnCurrentDataTimestamp"
        :key="shift.from"
      >
        <Avatar class="h-9 w-9">
          <AvatarImage
            v-if="teamStore.getTeamMemberByName(shift.racer)"
            :src="teamStore.getTeamMemberByName(shift.racer)?.pictureUrl!"
            alt="Avatar"
          />
          <AvatarFallback>{{ shift.racer }}</AvatarFallback>
        </Avatar>
        <div class="ml-4 space-y-1">
          <p class="text-sm font-medium leading-none">{{ shift.racer }}</p>
        </div>
        <div class="flex flex-col ml-auto items-end">
          <div class="font-medium">
            {{ DateTime.fromISO(shift.from).toFormat('HH:mm') }} -
            {{ DateTime.fromISO(shift.to).toFormat('HH:mm') }}
          </div>
          <div class="font-thin text-xs">{{ formatDuration(shift.from, shift.to) }}</div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="!racingShiftsStore.getAvailableShiftsBasedOnCurrentDataTimestamp.length">
    <Alert variant="destructive">
      <AlertTitle>No Data Available</AlertTitle>
      <AlertDescription>
        Data for the current timestamp is not available. Please use the seek controls to adjust the
        timestamp.
      </AlertDescription>
    </Alert>
  </div>
</template>

<style scoped>
.overflow-container::-webkit-scrollbar {
  display: none;
}

.overflow-container {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
</style>
