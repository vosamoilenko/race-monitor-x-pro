<template>
  <div class="seek-container flex items-center border p-2">
    {{ currentIndex }}
    <button @click="prev" class="mr-2">Prev</button>
    <button @click="playPause" class="mr-2">{{ isPlaying ? 'Pause' : 'Play' }}</button>
    <button @click="next" class="mr-2">Next</button>
    <div id="seek-bar" class="relative w-full h-4 bg-gray-200" @click="onSeekBarClick">
      <div
        id="seek-progress"
        class="absolute h-4 bg-blue-500"
        :style="{ width: progressWidth }"
      ></div>
      <div
        id="seek-control"
        class="absolute w-6 h-6 bg-blue-700 rounded-full -mt-1 -ml-3 cursor-pointer"
        :style="{ left: controlLeft }"
        @mousedown="onMouseDown"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, defineProps, defineEmits } from 'vue'

const props = defineProps<{
  from: number
  to: number
}>()

const emit = defineEmits(['updateIndex', 'prev', 'playPause', 'next'])

const currentIndex = defineModel<number>()
const isDragging = ref(false)
const isPlaying = ref(false)
const seekBar = ref<HTMLElement | null>(null)
const intervalId = ref<number | null>(null)

const progressWidth = ref('0%')
const controlLeft = ref('0%')

const updateProgress = () => {
  const percentage = ((currentIndex.value - props.from) / (props.to - props.from)) * 100
  progressWidth.value = `${percentage}%`
  controlLeft.value = `${percentage}%`
}

const onSeekBarClick = (e: MouseEvent) => {
  if (seekBar.value) {
    const rect = seekBar.value.getBoundingClientRect()
    const offsetX = e.clientX - rect.left
    const width = rect.width
    const newIndex = Math.round((offsetX / width) * (props.to - props.from) + props.from)
    currentIndex.value = Math.max(props.from, Math.min(newIndex, props.to))
    emit('updateIndex', currentIndex.value)
  }
}

const onMouseMove = (e: MouseEvent) => {
  if (isDragging.value && seekBar.value) {
    const rect = seekBar.value.getBoundingClientRect()
    const offsetX = e.clientX - rect.left
    const width = rect.width
    const newIndex = Math.round((offsetX / width) * (props.to - props.from) + props.from)
    currentIndex.value = Math.max(props.from, Math.min(newIndex, props.to))
    emit('updateIndex', currentIndex.value)
    updateProgress()
  }
}

const onMouseUp = () => {
  if (isDragging.value) {
    isDragging.value = false
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
  }
}

const onMouseDown = () => {
  isDragging.value = true
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

const prev = () => {
  if (currentIndex.value > props.from) {
    currentIndex.value--
    emit('updateIndex', currentIndex.value)
    emit('prev')
  }
}

const next = () => {
  if (currentIndex.value < props.to) {
    currentIndex.value++
    emit('updateIndex', currentIndex.value)
    emit('next')
  }
}

const playPause = () => {
  if (isPlaying.value) {
    clearInterval(intervalId.value!)
    intervalId.value = null
    isPlaying.value = false
    emit('playPause', isPlaying.value)
  } else {
    isPlaying.value = true
    emit('playPause', isPlaying.value)
    intervalId.value = setInterval(() => {
      if (currentIndex.value < props.to) {
        currentIndex.value++
        emit('updateIndex', currentIndex.value)
      } else {
        clearInterval(intervalId.value!)
        isPlaying.value = false
        emit('playPause', isPlaying.value)
      }
    }, 500) // Change the interval time as needed
  }
}

watch(currentIndex, updateProgress)

onMounted(() => {
  seekBar.value = document.getElementById('seek-bar') as HTMLElement
  updateProgress()
})

onUnmounted(() => {
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', onMouseUp)
  if (intervalId.value) {
    clearInterval(intervalId.value)
  }
})
</script>

<style scoped>
.seek-container {
  width: 100%;
}
</style>
