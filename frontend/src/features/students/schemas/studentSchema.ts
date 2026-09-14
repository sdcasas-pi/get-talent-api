import { z } from 'zod'

const emailPattern = /^[\w.-]+@[\w.-]+\.\w+$/

export const studentFormSchema = z.object({
  firstName: z.string().trim().min(1, 'El nombre es obligatorio').max(100, 'Máximo 100 caracteres'),
  lastName: z
    .string()
    .trim()
    .min(1, 'El apellido es obligatorio')
    .max(100, 'Máximo 100 caracteres'),
  dni: z
    .string()
    .trim()
    .regex(/^\d{7,8}$/, 'El DNI debe tener 7 u 8 dígitos numéricos'),
  dateOfBirth: z.string().min(1, 'La fecha de nacimiento es obligatoria'),
  phone: z.string().trim().max(30, 'Máximo 30 caracteres').optional().or(z.literal('')),
  email: z
    .string()
    .trim()
    .regex(emailPattern, 'Ingresá un email válido')
    .optional()
    .or(z.literal('')),
})

export type StudentFormValues = z.infer<typeof studentFormSchema>

export const studentFormDefaultValues: StudentFormValues = {
  firstName: '',
  lastName: '',
  dni: '',
  dateOfBirth: '',
  phone: '',
  email: '',
}
