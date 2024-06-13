<script setup lang="ts">
import { useDatapointsStore } from '../stores/datapoints.store'
import { useRaceDashboardStore } from '../stores/race-dashboard.store'
import { useSettingsStore } from '../stores/settings.store'
import { useTeamStore } from '../stores/team.store'
import { useFirestore } from '../stores/useFirestore'
import { DateTime } from 'luxon'

const datapointsStore = useDatapointsStore()
const raceStore = useRaceDashboardStore()
const settingsStore = useSettingsStore()
const teamStore = useTeamStore()

const fb = useFirestore()

const index = ref(0)

const updateIndex = (c: number) => {
  index.value = c
}
</script>

<template>
  <RaceDashboardLayout>
    <template #race>
      <div v-if="raceStore.currentData">
        <!-- {{ DateTime.fromSeconds(raceStore.currentData.ts).toISO() }} -->
      </div>
    </template>
    <template #map>
      <!-- <Map :gps-datapoints="raceStore.allGPSDateUntilIndex"></Map> -->
      <RaceMap :gps-datapoints="raceStore.allGPSDateUntilIndex"></RaceMap>
    </template>
    <template #racers>
      {{ raceStore.allGPSDateUntilIndex }}
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
