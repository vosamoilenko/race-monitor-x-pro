import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUtilStore = defineStore('util', () => {
  const mapHeight = ref(0)

  const setMapHeight = (height: number) => {
    mapHeight.value = height
  }

  return {
    mapHeight,
    setMapHeight
  }
})
