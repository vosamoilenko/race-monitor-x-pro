<script setup lang="ts">
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export interface TabItem {
  name: string
  key: string
}

export interface Props {
  tabs: TabItem[]
}
const props = withDefaults(defineProps<Props>(), {
  tabs: () => []
})
</script>
<template>
  <Tabs :default-value="props.tabs[0]?.key" class="w-[400px]">
    <TabsList>
      <TabsTrigger v-for="item in props.tabs" :key="item.key" :value="item.key">
        {{ item.name }}
      </TabsTrigger>
    </TabsList>

    <TabsContent v-for="item in props.tabs" :key="item.key" :value="item.key">
      <slot :name="item.key"></slot>
    </TabsContent>
  </Tabs>
</template>
