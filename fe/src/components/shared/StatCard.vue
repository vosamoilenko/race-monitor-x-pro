<script setup lang="ts">
export interface Props {
  title: string
  value: string
  postfix?: string
}
const props = withDefaults(defineProps<Props>(), {})
</script>
<template>
  <Card class="stat-card shadow-sm">
    <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-1">
      <CardTitle class="text-sm font-medium"> {{ title }} </CardTitle>
    </CardHeader>
    <CardContent>
      <div>
        <span class="text-xl font-bold">{{ value === null || value === 'null' ? '-' : value }}</span
        ><span v-if="postfix">&nbsp;{{ postfix }}</span>
      </div>
      <div class="relative flex">
        <slot></slot>
      </div>
      <!-- <p class="text-xs text-muted-foreground">{{  }}</p> -->
    </CardContent>
  </Card>
</template>

<style>
  .stat-card > div {
    padding: 8px;
    padding-bottom: 0px;
  }
</style>
