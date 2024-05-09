<script setup lang="ts">
export interface Props {
  title: string
  value: string
  postfix?: string
}
const props = withDefaults(defineProps<Props>(), {})
</script>
<template>
  <Card>
    <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle class="text-sm font-medium"> {{ title }} </CardTitle>
    </CardHeader>
    <CardContent>
      <span class="text-2xl font-bold">{{ value }}</span
      ><span v-if="postfix">{{ postfix }}</span>
      <!-- <p class="text-xs text-muted-foreground">{{  }}</p> -->
    </CardContent>
  </Card>
</template>
