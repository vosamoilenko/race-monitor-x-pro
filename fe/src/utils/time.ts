import { DateTime } from 'luxon'

export function convertTimestampToMillis(timestamp: number): number {
  return DateTime.fromSeconds(timestamp).toUTC().toMillis()
}

export function convertISOToMillis(isoString: string): number {
  return DateTime.fromISO(isoString, { zone: 'utc' }).toMillis()
}
