<script setup lang="ts">
import { useRaceDashboardStore } from '../../stores/race-dashboard.store'

const store = useRaceDashboardStore()
</script>
<template>
  <div class="grid grid-cols-3 gap-3">
    <div class="flex flex-col gap-3">
      <StatCard
        postfix="RPM"
        :value="`${store?.lastOBDData?.engineRpm ?? '-'}`"
        title="Engine RPM"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="`${store?.lastOBDData?.calculatedEngineLoad?.toFixed(2) ?? '-'}`"
        title="Calculated Engine Load"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="`${store?.lastOBDData?.throttlePosition?.toFixed(2) ?? '-'}`"
        title="Throttle Position"
      ></StatCard>
      <StatCard
        postfix="°"
        :value="`${store?.lastOBDData?.timingAdvance.toFixed(2) ?? '-'}`"
        title="Timing Advance"
      ></StatCard>
      <StatCard
        postfix="km/h"
        :value="`${store?.lastOBDData?.vehicleSpeed ?? '-'}`"
        title="Vehicle Speed"
      ></StatCard>
    </div>
    <div class="flex flex-col gap-3">
      <StatCard
        postfix="°C"
        :value="`${store?.lastOBDData?.engineCoolantTemperature ?? '-'}`"
        title="Engine Coolant Temperature"
      ></StatCard>
      <StatCard
        postfix="°C"
        :value="`${store?.lastOBDData?.intakeAirTemperature ?? '-'}`"
        title="Intake Air Temperature"
      ></StatCard>
      <StatCard
        postfix="g/s"
        :value="`${store?.lastOBDData?.mafAirFlowRate ?? '-'}`"
        title="MAF Air Flow Rate"
      ></StatCard>
    </div>
    <div class="flex flex-col gap-3">
      <StatCard
        postfix="%"
        :value="`${store?.lastOBDData?.longTermFuelTrimBank1?.toFixed(2) ?? '-'}`"
        title="Long Term Fuel Trim Bank 1"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="`${store?.lastOBDData?.shortTermFuelTrimBank1?.toFixed(2) ?? '-'}`"
        title="Short Term Fuel Trim Bank 1"
      ></StatCard>
      <StatCard
        postfix="V"
        :value="`${store?.lastOBDData?.bank1Sensor1OxygenSensorVoltage?.toFixed(2) ?? '-'}`"
        title="Bank 1 Sensor 1 Oxygen Sensor Voltage"
      ></StatCard>
      <StatCard
        postfix="V"
        :value="`${store?.lastOBDData?.bank1Sensor2OxygenSensorVoltage?.toFixed(2) ?? '-'}`"
        title="Bank 1 Sensor 2 Oxygen Sensor Voltage"
      ></StatCard>
      <StatCard
        postfix="%"
        :value="`${store?.lastOBDData?.oxygenSensorsPresent ?? '-'}`"
        title="Oxygen Sensors Present"
      ></StatCard>
    </div>
  </div>
</template>
