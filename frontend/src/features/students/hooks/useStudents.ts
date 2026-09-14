import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { studentsApi, type ListStudentsParams } from '../../../api/students'
import type { CreateStudentInput, UpdateStudentInput } from '../../../types/student'

const studentsKeys = {
  all: ['students'] as const,
  list: (params: ListStudentsParams) => [...studentsKeys.all, 'list', params] as const,
  detail: (id: string) => [...studentsKeys.all, 'detail', id] as const,
}

export function useStudentsList(params: ListStudentsParams) {
  return useQuery({
    queryKey: studentsKeys.list(params),
    queryFn: () => studentsApi.list(params),
    placeholderData: (previous) => previous,
  })
}

export function useCreateStudent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (input: CreateStudentInput) => studentsApi.create(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: studentsKeys.all })
    },
  })
}

export function useUpdateStudent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, input }: { id: string; input: UpdateStudentInput }) =>
      studentsApi.update(id, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: studentsKeys.all })
    },
  })
}

export function useDeleteStudent() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => studentsApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: studentsKeys.all })
    },
  })
}
