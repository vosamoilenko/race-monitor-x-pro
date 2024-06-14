import { DateTime } from 'luxon'
import type { RacingShift } from '../stores/racing-shifts.store'
import { convertISOToMillis, convertTimestampToMillis } from './time'

export function findRacingShift(shifts: RacingShift[], ts: number): RacingShift | null {
  // Convert the timestamp to seconds if it's in milliseconds
  const tsSeconds = ts > 1e10 ? ts / 1000 : ts
  const tsReadable = DateTime.fromSeconds(tsSeconds).toLocaleString(DateTime.DATETIME_MED)
  console.log(`Timestamp to find: ${ts} (${tsReadable})`)

  return (
    shifts.find((shift) => {
      const from = new Date(shift.from).getTime() / 1000
      const to = new Date(shift.to).getTime() / 1000

      const result = tsSeconds >= from && tsSeconds <= to

      return result
    }) ?? null
  )
}

export function filterShiftsByTimestamp(
  shifts: RacingShift[],
  currentTimestamp: number
): RacingShift[] {
  const ts = convertTimestampToMillis(currentTimestamp)

  return shifts.filter((shift) => {
    const shiftFromTimestamp = convertISOToMillis(shift.from)
    return shiftFromTimestamp <= ts
  })
}
