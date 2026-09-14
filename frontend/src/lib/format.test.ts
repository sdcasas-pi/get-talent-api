import { describe, expect, it } from 'vitest'

import { formatDate, formatDni } from './format'

describe('formatDate', () => {
  it('converts ISO date to yyyy/mm/dd', () => {
    expect(formatDate('1995-05-20')).toBe('1995/05/20')
  })

  it('returns the original value if not a valid ISO date', () => {
    expect(formatDate('invalid')).toBe('invalid')
  })
})

describe('formatDni', () => {
  it('adds thousand separators to an 8-digit DNI', () => {
    expect(formatDni('30123456')).toBe('30.123.456')
  })

  it('adds a single separator to a 7-digit DNI', () => {
    expect(formatDni('3123456')).toBe('3.123.456')
  })
})
