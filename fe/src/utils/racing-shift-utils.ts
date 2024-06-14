import type { RacingShift } from '../stores/racing-shifts.store'

export function findRacingShift(shifts: RacingShift[], ts: number): RacingShift | null {
  return (
    shifts.find((shift) => {
      const from = new Date(shift.from).getTime()
      const to = new Date(shift.to).getTime()
      return ts >= from && ts <= to
    }) ?? null
  )
}
