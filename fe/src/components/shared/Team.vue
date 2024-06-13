<script setup lang="ts">
import type { Driver } from '../../stores/team.store'

export interface Props {
  team: Driver[]
}
const props = withDefaults(defineProps<Props>(), {})
</script>
<template>
  <div class="space-y-8">
    <div class="flex items-center" v-for="member of props.team" :key="member.name">
      <Avatar class="h-9 w-9">
        <AvatarImage :src="member.pictureUrl" alt="Avatar" />
        <AvatarFallback>OM</AvatarFallback>
      </Avatar>
      <div class="ml-4 space-y-1">
        <p class="text-sm font-medium leading-none">{{ member.name }}</p>
        <p class="text-sm text-muted-foreground">olivia.martin@email.com</p>
      </div>
      <div class="flex flex-col">
        <div class="ml-auto font-medium">{{ member.drivingDuration }}</div>
        <div class="ml-auto font-thin text-xs">{{ member.notDrivingSince }}</div>
      </div>
    </div>
  </div>
</template>
