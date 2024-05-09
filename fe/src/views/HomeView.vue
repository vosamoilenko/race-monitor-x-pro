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

document.body.addEventListener('click', () => {
  i.value = i.value += 1
  f1(i.value)
})
// const response = await fetch('http://localhost:3000/data/0')
// const data = await response.json()

function f1(id: string | number) {
  fetch('http://localhost:3000/data/' + id)
    .then((response) => response.json())
    .then((_data) => {
      data.value = _data
    })
}
</script>

<template>
  <div class="text text-lg">{{ i }}</div>
  <main>
    <!-- {{ data }} -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard :value="data.monitorStatus" title="Monitor status"></StatCard>
      <StatCard :value="data.engineLoad" title="Engine load"></StatCard>
      <StatCard :value="data.coolantTemperature" title="Coolant temperature"></StatCard>
      <StatCard :value="data.intakeManifoldPressure" title="Intake manifold pressure"></StatCard>
      <StatCard :value="data.engineSpeed" title="Engine speed"></StatCard>
      <StatCard :value="data.vehicleSpeed" title="Vehicle speed"></StatCard>
      <StatCard :value="data.timingAdvance" title="Timing advance"></StatCard>
      <StatCard :value="data.intakeAirTemperature" title="Intake air temperature"></StatCard>
      <StatCard :value="data.mafSensorAirFlowRate" title="Maf sensor air flow rate"></StatCard>
      <StatCard :value="data.throttlePosition" title="Throttle position"></StatCard>
    </div>
  </main>
</template>
