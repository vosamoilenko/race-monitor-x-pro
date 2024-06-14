import { ref, watch } from 'vue';
import { defineStore } from 'pinia';
import { useRoute } from 'vue-router';
import { useFirestore } from './useFirestore';
import { DateTime } from 'luxon';

export interface RacingShift {
  from: string;
  to: string;
  racer: string;
}

export const useRacingShiftsStore = defineStore('racing-shifts', () => {
  const route = useRoute();
  const fb = useFirestore();
  const shifts = ref<RacingShift[]>([]);

  watch(
    () => route.params.raceId,
    async (raceId) => {
      const response = fb.getDocument('racing-shifts', raceId as string);
      
      watch(response, (data) => {
        shifts.value = data.shifts;
      });
    },
    { immediate: true }
  );

  const getCurrentDriverInfo = (timestamp: string, timeZone: string) => {
    if (!shifts.value) return null;
    const currentTimestamp = DateTime.fromISO(timestamp, { zone: timeZone });

    for (const shift of shifts.value) {
      const from = DateTime.fromISO(shift.from, { zone: timeZone });
      const to = DateTime.fromISO(shift.to, { zone: timeZone });
      if (currentTimestamp >= from && currentTimestamp <= to) {
        return {
          currentDriver: shift.racer,
          currentShift: {
            from: from.toISO(),
            to: to.toISO()
          }
        };
      }
    }

    return null;
  };

  return { shifts, getCurrentDriverInfo };
});
