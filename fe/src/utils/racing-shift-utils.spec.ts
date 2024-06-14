import { filterShiftsByTimestamp, findRacingShift } from './racing-shift-utils'

function getMockData() {
  return [
    { racer: 'vova', from: '2024-06-08T10:00:00.000Z', to: '2024-06-08T11:46:00.000Z' },
    { racer: 'norbert', from: '2024-06-08T11:50:00.000Z', to: '2024-06-08T14:00:00.000Z' },
    { racer: 'flo', from: '2024-06-08T13:50:00.000Z', to: '2024-06-08T15:50:00.000Z' },
    { racer: 'max', from: '2024-06-08T15:55:00.000Z', to: '2024-06-08T18:33:00.000Z' },
    { racer: 'niki', from: '2024-06-08T18:40:00.000Z', to: '2024-06-08T20:10:00.000Z' }
  ]
}

describe('RacingShiftUtils:findRacingShift', () => {
  it('should return the correct shift for a given timestamp within a shift', () => {
    const shifts = getMockData()
    const ts = new Date('2024-06-08T10:30:00.000Z').getTime() / 1000
    const result = findRacingShift(shifts, ts)
    console.log(result)

    expect(result).toEqual(shifts[0])
  })

  it('should return null for a timestamp outside of any shift', () => {
    const shifts = getMockData()
    const ts = new Date('2024-06-08T09:00:00.000Z').getTime() / 1000
    const result = findRacingShift(shifts, ts)
    console.log(result)

    expect(result).toBeNull()
  })
})
describe('RacingShiftUtils:filterShiftsByTimestamp', () => {
  it('should return all shifts up to the current timestamp', () => {
    const shifts = getMockData()
    const currentTimestamp = Math.floor(new Date('2024-06-08T14:00:00.000Z').getTime() / 1000) // Use seconds
    const result = filterShiftsByTimestamp(shifts, currentTimestamp)
    console.log('Filtered Shifts:', result)

    expect(result).toEqual([shifts[0], shifts[1], shifts[2]])
  })

  it('should return an empty array if current timestamp is before any shifts', () => {
    const shifts = getMockData()
    const currentTimestamp = Math.floor(new Date('2024-06-08T09:00:00.000Z').getTime() / 1000) // Use seconds
    const result = filterShiftsByTimestamp(shifts, currentTimestamp)

    expect(result).toEqual([])
  })

  it('should return all shifts if current timestamp is after all shifts', () => {
    const shifts = getMockData()
    const currentTimestamp = Math.floor(new Date('2024-06-08T20:30:00.000Z').getTime() / 1000) // Use seconds
    const result = filterShiftsByTimestamp(shifts, currentTimestamp)

    expect(result).toEqual(shifts)
  })
})
