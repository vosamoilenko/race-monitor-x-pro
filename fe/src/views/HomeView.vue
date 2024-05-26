<script setup lang="ts">
import { useDatapointsStore } from '../stores/datapoints.store'
import { useFirestore } from '../stores/useFirestore'

const store = useDatapointsStore()

const fb = useFirestore()
// const doc = fb.getDocument('vova')
const col = fb.doc1('vova')
</script>

<template>
  
  <Map :history="col?.history"></Map>

  <div class="text text-3xl pl-4 my-5">RaceMonitorXPro</div>
  <main class="px-4">
    <!-- {{ data }} -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard
        :value="store?.latestDatapoint?.monitorStatus.value"
        title="Monitor status"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="store?.latestDatapoint?.engineLoad.value?.toFixed(2)"
        title="Engine load"
      ></StatCard>
      <StatCard
        postfix="°C"
        :value="store?.latestDatapoint?.coolantTemperature.value"
        title="Coolant temperature"
      ></StatCard>
      <StatCard
        postfix="kPa"
        :value="store?.latestDatapoint?.intakeManifoldPressure.value"
        title="Intake manifold pressure"
      ></StatCard>
      <StatCard
        postfix="rpm"
        :value="store?.latestDatapoint?.engineSpeed.value"
        title="Engine speed"
      ></StatCard>
      <StatCard
        postfix="km/h"
        :value="store?.latestDatapoint?.vehicleSpeed.value"
        title="Vehicle speed"
      >
        <Speedometer :value="store?.latestDatapoint?.vehicleSpeed.value"></Speedometer
      ></StatCard>
      <StatCard
        postfix="degrees"
        :value="store?.latestDatapoint?.timingAdvance.value"
        title="Timing advance"
      >
        <Ch :data="store?.allTimingAdvance"></Ch>
      </StatCard>
      <StatCard
        postfix="°C"
        :value="store?.latestDatapoint?.intakeAirTemperature.value"
        title="Intake air temperature"
      ></StatCard>
      <StatCard
        postfix="g/s"
        :value="store?.latestDatapoint?.mafSensorAirFlowRate.value"
        title="Maf sensor air flow rate"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="store?.latestDatapoint?.throttlePosition.value?.toFixed(2)"
        title="Throttle position"
      ></StatCard>
    </div>
  </main>
</template>
