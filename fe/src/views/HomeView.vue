<script setup lang="ts">
let data = ref({
  monitorStatus: null,
  engineLoad: null,
  coolantTemperature: null,
  intakeManifoldPressure: null,
  engineSpeed: null,
  vehicleSpeed: null,
  timingAdvance: null,
  intakeAirTemperature: null,
  mafSensorAirFlowRate: null,
  throttlePosition: null
})
const i = ref(0)
f1(i.value)

setInterval(() => {
  i.value = i.value += 1
  f1(i.value)
}, 1000)
// const response = await fetch('http://localhost:3000/data/0')
// const data = await response.json()

function f1(id: string | number) {
  try {
    fetch('http://localhost:3000/data/' + id)
      .then((response) => response.json())
      .then((_data) => {
        data.value = _data
      })
  } catch (e) {
    console.error(e)
  }
}
</script>

<template>
  <div class="text text-3xl pl-4 my-5">RaceMonitorXPro</div>
  <main class="px-4">
    <!-- {{ data }} -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard :value="data.monitorStatus" title="Monitor status"></StatCard>
      <StatCard postfix="%" :value="data.engineLoad?.toFixed(2)" title="Engine load"></StatCard>
      <StatCard
        postfix="°C"
        :value="data.coolantTemperature"
        title="Coolant temperature"
      ></StatCard>
      <StatCard
        postfix="kPa"
        :value="data.intakeManifoldPressure"
        title="Intake manifold pressure"
      ></StatCard>
      <StatCard postfix="rpm" :value="data.engineSpeed" title="Engine speed"></StatCard>
      <StatCard postfix="km/h" :value="data.vehicleSpeed" title="Vehicle speed"></StatCard>
      <StatCard postfix="degrees" :value="data.timingAdvance" title="Timing advance"></StatCard>
      <StatCard
        postfix="°C"
        :value="data.intakeAirTemperature"
        title="Intake air temperature"
      ></StatCard>
      <StatCard
        postfix="g/s"
        :value="data.mafSensorAirFlowRate"
        title="Maf sensor air flow rate"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="data.throttlePosition?.toFixed(2)"
        title="Throttle position"
      ></StatCard>
    </div>
  </main>
</template>
