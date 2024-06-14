<script setup lang="ts">
const tabs = [{ name: 'Racing order', key: 'racingOrder' }]
</script>

<template>
  <TabsContainer :tabs="tabs">
    <template #racingOrder>
      <Card>
        <CardHeader>
          <h2 class="text-lg font-semibold">Team</h2>
        </CardHeader>
        <CardContent>
          <RacingOrder />
        </CardContent>
      </Card>
    </template>
  </TabsContainer>
</template>
