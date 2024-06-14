<script setup lang="ts">
import { useRaceDashboardStore } from '../../stores/race-dashboard.store'
import { useRacingShiftsStore } from '../../stores/racing-shifts.store'
import { useTeamStore } from '../../stores/team.store'

const teamStore = useTeamStore()
const racingShiftsStore = useRacingShiftsStore()
const raceDashboardStore = useRaceDashboardStore()
</script>
<template>
  <div class="space-y-8 p-4 overflow-hidden">
    <div
      class="flex items-center"
      v-for="shift of racingShiftsStore.getAvailableShiftsBasedOnCurrentDataTimestamp"
      :key="shift.from"
    >
      <Avatar class="h-9 w-9">
        <AvatarImage
          v-if="teamStore.getTeamMemberByName(shift.racer)?.pictureUrl"
          :src="teamStore.getTeamMemberByName(shift.racer)?.pictureUrl"
          alt="Avatar"
        />
        <AvatarFallback>{{ shift.racer }}</AvatarFallback>
      </Avatar>
      <div class="ml-4 space-y-1">
        <p class="text-sm font-medium leading-none">{{ shift.racer }}</p>
      </div>
      <!-- <div class="flex flex-col">
        <div class="ml-auto font-medium">{{ member.drivingDuration }}</div>
        <div class="ml-auto font-thin text-xs">{{ member.notDrivingSince }}</div>
      </div> -->
    </div>
  </div>
</template>
