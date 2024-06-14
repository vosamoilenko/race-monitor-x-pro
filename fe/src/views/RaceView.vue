<script setup lang="ts">
import { useDatapointsStore } from '../stores/datapoints.store'
import { useRaceDashboardStore } from '../stores/race-dashboard.store'
import { useRacingShiftsStore } from '../stores/racing-shifts.store'
import { useSettingsStore } from '../stores/settings.store'
import { useTeamStore } from '../stores/team.store'
import { useFirestore } from '../stores/useFirestore'
import { DateTime } from 'luxon'

const datapointsStore = useDatapointsStore()
const raceStore = useRaceDashboardStore()
const settingsStore = useSettingsStore()
const teamStore = useTeamStore()
const racingShiftsStore = useRacingShiftsStore()

const fb = useFirestore()

const index = ref(0)

const updateIndex = (c: number) => {
  index.value = c
}
const formattedDate = (ts: number): string => {
  return DateTime.fromSeconds(ts).toFormat('dd.MM.yyyy')
}

const formattedTime = (ts: number): string => {
  return DateTime.fromSeconds(ts).toFormat('HH:mm')
}
</script>

<template>
  <RaceDashboardLayout>
    <template #race>
      <div v-if="raceStore.currentData" class="flex flex-col">
        <div class="text-gray-500 text-sm">
          {{ formattedDate(raceStore.currentData.ts) }} /
          {{ raceStore.currentData.ts }}
        </div>
        <div class="text-black text-6xl font-bold">
          {{ formattedTime(raceStore.currentData.ts) }}
        </div>
      </div>
    </template>
    <template #map>
      <RaceMap :gps-datapoints="raceStore.allGPSDateUntilIndex"></RaceMap>
    </template>
    <template #racers>
      <!-- <div class="overflow-hidden h-full"> -->
      <Team :team="teamStore.team" class="h-full overflow-y-scroll" />
      <!-- </div> -->
    </template>
    <template #car>
      <CarStats></CarStats>
    </template>
    <template #seek>
      <RaceSeek
        v-model="raceStore.currentIndex"
        :from="0"
        :to="datapointsStore.datapoints.length - 1"
        @update-index="updateIndex"
      ></RaceSeek>
    </template>
  </RaceDashboardLayout>
</template>
