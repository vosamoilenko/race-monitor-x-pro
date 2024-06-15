<script setup lang="ts">
import { watch, ref } from 'vue'
import { DateTime } from 'luxon'
import { useRacingShiftsStore } from '../../stores/racing-shifts.store'

const racingShiftsStore = useRacingShiftsStore()
const data = ref<{ name: string; total: string }[]>([])

onMounted(() => {
  console.log('mounted')
})

watch(
  () => racingShiftsStore.shifts,
  (shifts) => {
    if (!shifts.length) return

    const totalTimeByRacer = shifts.reduce(
      (acc, shift) => {
        const racer = shift.racer
        const duration = DateTime.fromISO(shift.to).diff(
          DateTime.fromISO(shift.from),
          'minutes'
        ).minutes

        if (!acc[racer]) {
          acc[racer] = duration
        } else {
          acc[racer] += duration
        }

        return acc
      },
      {} as Record<string, number>
    )

    // @ts-ignore
    data.value = Object.entries(totalTimeByRacer).map(([name, totalMinutes]) => {
      const totalHours = totalMinutes / 60
      return { name, total: parseFloat(totalHours.toFixed(2)) }
    })
    console.log(data.value)
  },
  { immediate: true }
)
</script>

<template>
  <!-- <div>{{ racingShiftsStore.shifts }}</div>
  <div>{{ data }}</div> -->
  <BarChart
    index="name"
    :data="data"
    :categories="['total']"
    :x-axis-labels="true"
    :showLegend="false"
    :y-formatter="
      (tick, i) => {
        return typeof tick === 'number'
          ? `${new Intl.NumberFormat('us').format(tick).toString()} hours`
          : ''
      }
    "
    :rounded-corners="4"
  />
</template>
