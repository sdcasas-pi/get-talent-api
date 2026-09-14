import axios, { AxiosError } from 'axios'

import type { ApiErrorPayload } from '../types/student'

export class ApiError extends Error {
  readonly code: string
  readonly status: number
  readonly details: string[] | null

  constructor(status: number, payload: ApiErrorPayload) {
    super(payload.message)
    this.name = 'ApiError'
    this.code = payload.error
    this.status = status
    this.details = payload.details ?? null
  }
}

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorPayload>) => {
    if (error.response?.data) {
      return Promise.reject(new ApiError(error.response.status, error.response.data))
    }
    return Promise.reject(
      new ApiError(0, {
        error: 'NETWORK_ERROR',
        message: 'No se pudo conectar con el servidor. Verificá tu conexión.',
      }),
    )
  },
)
