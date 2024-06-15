<script setup lang="ts">
import { useDatapointsStore } from '../stores/datapoints.store'
import { useSettingsStore } from '../stores/settings.store'
import { useTeamStore } from '../stores/team.store'
import { useFirestore } from '../stores/useFirestore'

const store = useDatapointsStore()
const settingsStore = useSettingsStore()
const teamStore = useTeamStore()

const fb = useFirestore()

const updateIndex = (c: number) => {
  console.log(c)
}
</script>

<template>
  <RaceDashboardLayout>
    <template #seek>
      <RaceSeek @update-index="updateIndex" :from="0" :to="23"></RaceSeek>
    </template>
  </RaceDashboardLayout>
  <div class="text text-3xl pl-4 my-5">RaceMonitorXPro</div>
  <div class="px-4 flex flex-wrap">
    <div class="flex gap-4 mb-4">
      <Card>
        <CardHeader>
          <CardTitle>Kerosinen Racing</CardTitle>
          <!-- <CardDescription> Team time {{ props.totalTime }} </CardDescription> -->
        </CardHeader>
        <CardContent>
          <Team :team="teamStore.team" />
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Map :gps-datapoints="store.gpsDatapoints"></Map>
        </CardContent>
      </Card>
    </div>
    <!-- {{ data }} -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <!-- <StatCard
        :value="store?.latestOBDDatapoint?.monitorStatus"
        title="Monitor status"
      ></StatCard> -->
      <div class="flex gap-4 flex flex-col">
        <StatCard
          postfix="RPM"
          :value="`${store?.latestOBDDatapoint?.engineRpm}`"
          title="Engine RPM"
        ></StatCard>
        <StatCard
          postfix="°C"
          :value="`${store?.latestOBDDatapoint?.engineCoolantTemperature}`"
          title="Engine Coolant Temperature"
        ></StatCard>
        <StatCard
          postfix="kPa"
          :value="`${store?.latestOBDDatapoint?.intakeAirTemperature}`"
          title="Intake Air Temperature"
        ></StatCard>
        <StatCard
          postfix="V"
          :value="`${store?.latestOBDDatapoint?.bank1Sensor1OxygenSensorVoltage.toFixed(2)}`"
          title="Bank 1 Sensor 1 Oxygen Sensor Voltage"
        ></StatCard>
      </div>
      <StatCard
        postfix="V"
        :value="`${store?.latestOBDDatapoint?.bank1Sensor2OxygenSensorVoltage.toFixed(2)}`"
        title="Bank 1 Sensor 2 Oxygen Sensor Voltage"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="`${store?.latestOBDDatapoint?.calculatedEngineLoad.toFixed(2)}`"
        title="Calculated Engine Load"
      ></StatCard>
      <!-- <StatCard
        :value="`${store?.latestOBDDatapoint?.commandedSecondaryAirStatus}`"
        title="Commanded Secondary Air Status"
      ></StatCard> -->
      <!-- <StatCard
        :value="`${store?.latestOBDDatapoint?.fuelSystemStatus}`"
        title="Fuel System Status"
      ></StatCard> -->
      <StatCard
        postfix="%"
        :value="`${store?.latestOBDDatapoint?.longTermFuelTrimBank1}`"
        title="Long Term Fuel Trim Bank 1"
      ></StatCard>
      <StatCard
        postfix="g/s"
        :value="`${store?.latestOBDDatapoint?.mafAirFlowRate}`"
        title="MAF Air Flow Rate"
      ></StatCard>
      <StatCard
        :value="`${store?.latestOBDDatapoint?.monitorStatusSinceDtcsCleared}`"
        title="Monitor Status Since DTCs Cleared"
      ></StatCard>
      <StatCard
        :value="`${store?.latestOBDDatapoint?.oxygenSensorsPresent.toFixed(2)}`"
        title="Oxygen Sensors Present"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="`${store?.latestOBDDatapoint?.shortTermFuelTrimBank1.toFixed(2)}`"
        title="Short Term Fuel Trim Bank 1"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="`${store?.latestOBDDatapoint?.throttlePosition.toFixed(2)}`"
        title="Throttle Position"
      ></StatCard>
      <StatCard
        postfix="°"
        :value="`${store?.latestOBDDatapoint?.timingAdvance}`"
        title="Timing Advance"
      ></StatCard>
      <StatCard
        postfix="km/h"
        :value="`${store?.latestOBDDatapoint?.vehicleSpeed}`"
        title="Vehicle Speed"
      ></StatCard>
      <!-- <StatCard
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
      ></StatCard> -->
    </div>
  </div>
</template>
