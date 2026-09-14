import { apiClient } from './client'
import type {
  CreateStudentInput,
  Student,
  StudentListResult,
  UpdateStudentInput,
} from '../types/student'

interface StudentResponseDto {
  id: string
  first_name: string
  last_name: string
  dni: string
  date_of_birth: string
  phone: string | null
  email: string | null
  created_at: string
}

interface StudentListResponseDto {
  data: StudentResponseDto[]
  total: number
  limit: number
  offset: number
}

function toStudent(dto: StudentResponseDto): Student {
  return {
    id: dto.id,
    firstName: dto.first_name,
    lastName: dto.last_name,
    dni: dto.dni,
    dateOfBirth: dto.date_of_birth,
    phone: dto.phone,
    email: dto.email,
    createdAt: dto.created_at,
  }
}

function toCreateRequest(input: CreateStudentInput) {
  return {
    first_name: input.firstName,
    last_name: input.lastName,
    dni: input.dni,
    date_of_birth: input.dateOfBirth,
    phone: input.phone || null,
    email: input.email || null,
  }
}

function toUpdateRequest(input: UpdateStudentInput) {
  return {
    ...(input.firstName !== undefined && { first_name: input.firstName }),
    ...(input.lastName !== undefined && { last_name: input.lastName }),
    ...(input.dni !== undefined && { dni: input.dni }),
    ...(input.dateOfBirth !== undefined && { date_of_birth: input.dateOfBirth }),
    ...(input.phone !== undefined && { phone: input.phone || null }),
    ...(input.email !== undefined && { email: input.email || null }),
  }
}

export interface ListStudentsParams {
  limit: number
  offset: number
}

export const studentsApi = {
  async list(params: ListStudentsParams): Promise<StudentListResult> {
    const { data } = await apiClient.get<StudentListResponseDto>('/v1/students', {
      params,
    })
    return {
      data: data.data.map(toStudent),
      total: data.total,
      limit: data.limit,
      offset: data.offset,
    }
  },

  async getById(id: string): Promise<Student> {
    const { data } = await apiClient.get<StudentResponseDto>(`/v1/students/${id}`)
    return toStudent(data)
  },

  async getByDni(dni: string): Promise<Student> {
    const { data } = await apiClient.get<StudentResponseDto>(`/v1/students/dni/${dni}`)
    return toStudent(data)
  },

  async create(input: CreateStudentInput): Promise<Student> {
    const { data } = await apiClient.post<StudentResponseDto>(
      '/v1/students',
      toCreateRequest(input),
    )
    return toStudent(data)
  },

  async update(id: string, input: UpdateStudentInput): Promise<Student> {
    const { data } = await apiClient.patch<StudentResponseDto>(
      `/v1/students/${id}`,
      toUpdateRequest(input),
    )
    return toStudent(data)
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`/v1/students/${id}`)
  },
}
