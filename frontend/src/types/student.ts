export interface Student {
  id: string
  firstName: string
  lastName: string
  dni: string
  dateOfBirth: string
  phone: string | null
  email: string | null
  createdAt: string
}

export interface StudentListResult {
  data: Student[]
  total: number
  limit: number
  offset: number
}

export interface CreateStudentInput {
  firstName: string
  lastName: string
  dni: string
  dateOfBirth: string
  phone?: string
  email?: string
}

export type UpdateStudentInput = Partial<CreateStudentInput>

export interface ApiErrorPayload {
  error: string
  message: string
  details?: string[] | null
}
