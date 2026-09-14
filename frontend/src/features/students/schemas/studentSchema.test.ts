import { describe, expect, it } from 'vitest'

import { studentFormSchema } from './studentSchema'

const validStudent = {
  firstName: 'Juan',
  lastName: 'Perez',
  dni: '30123456',
  dateOfBirth: '1995-05-20',
  phone: '+549111234-5678',
  email: 'juan.perez@example.com',
}

describe('studentFormSchema', () => {
  it('accepts a fully valid student', () => {
    const result = studentFormSchema.safeParse(validStudent)
    expect(result.success).toBe(true)
  })

  it('accepts optional phone and email as empty strings', () => {
    const result = studentFormSchema.safeParse({
      ...validStudent,
      phone: '',
      email: '',
    })
    expect(result.success).toBe(true)
  })

  it('rejects a DNI with letters', () => {
    const result = studentFormSchema.safeParse({ ...validStudent, dni: '3012345A' })
    expect(result.success).toBe(false)
  })

  it('rejects a DNI shorter than 7 digits', () => {
    const result = studentFormSchema.safeParse({ ...validStudent, dni: '123456' })
    expect(result.success).toBe(false)
  })

  it('rejects an invalid email format', () => {
    const result = studentFormSchema.safeParse({ ...validStudent, email: 'not-an-email' })
    expect(result.success).toBe(false)
  })

  it('requires first name', () => {
    const result = studentFormSchema.safeParse({ ...validStudent, firstName: '' })
    expect(result.success).toBe(false)
  })

  it('requires date of birth', () => {
    const result = studentFormSchema.safeParse({ ...validStudent, dateOfBirth: '' })
    expect(result.success).toBe(false)
  })
})
