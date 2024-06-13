import { ref, watch } from 'vue';
import { defineStore } from 'pinia';
import { useRoute } from 'vue-router';
import { useFirestore } from './useFirestore';

export interface RacingShift {
  from: string;
  to: string;
}

export const useRacingShiftsStore = defineStore('racing-shifts', () => {
  const route = useRoute();
  const fb = useFirestore();
  const order = ref<string[]>();
  const shifts = ref<Record<string, RacingShift[]>>();

  watch(
    () => route.params.raceId,
    async (raceId) => {
      const response = fb.getDocument('racing-shifts', raceId as string);
      
      watch(response, (data) => {
        order.value = data.order;
        shifts.value = data.shifts;
      });
    },
    { immediate: true }
  );

  const getCurrentDriverInfo = (timestamp: number) => {
    if (!shifts.value || !order.value) return null;
    const currentTimestamp = new Date(timestamp).getTime();

    // Find current shift and driver
    let currentDriver = null;
    let currentShift = null;

    for (const driver in shifts.value) {
      const driverShifts = shifts.value[driver];
      for (const shift of driverShifts) {
        const from = new Date(shift.from).getTime();
        const to = new Date(shift.to).getTime();
        if (currentTimestamp >= from && currentTimestamp <= to) {
          return { currentDriver: driver, currentShift: shift };
        }
      }
    }

    return null;
  };

  return { order, shifts, getCurrentDriverInfo };
});
