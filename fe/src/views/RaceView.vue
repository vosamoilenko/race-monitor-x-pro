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

const iconComponent = computed(() => {
  return `i-back`
})
</script>

<template>
  <RaceDashboardLayout>
    <template #race>
      <div v-if="raceStore.currentData" class="flex flex-col">
        <div>
          {{ DateTime.fromSeconds(raceStore.currentData.ts).toISO() }}
        </div>
        <div v-if="raceStore.lastEntry">
          {{ racingShiftsStore.getCurrentDriverInfo(raceStore.lastEntry.ts) }}
        </div>
      </div>
    </template>
    <template #map>
      <RaceMap :gps-datapoints="raceStore.allGPSDateUntilIndex"></RaceMap>
    </template>
    <template #racers>
      <Team :team="teamStore.team" />
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
