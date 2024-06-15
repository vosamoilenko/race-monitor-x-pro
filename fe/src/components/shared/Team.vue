<script setup lang="ts">
const tabs = [
  { name: 'Racing order', key: 'racingOrder' },
  { name: 'Time overview', key: 'timeOverview' }
]
</script>

<template>
  <TabsContainer :tabs="tabs">
    <template #racingOrder>
      <RacingOrder class="racing-order" />
    </template>
    <template #timeOverview>
      <Card>
        <CardContent>
          <RacingTimeBarChart />
        </CardContent>
      </Card>
    </template>
  </TabsContainer>
</template>

<style scoped>
.racing-order > div {
  border: 1px solid red;
}
</style>
