import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'

import { Button } from '../../../components/ui/Button'
import { Field } from '../../../components/ui/Field'
import {
  studentFormDefaultValues,
  studentFormSchema,
  type StudentFormValues,
} from '../schemas/studentSchema'
import styles from './StudentForm.module.css'

interface StudentFormProps {
  defaultValues?: StudentFormValues
  isSubmitting: boolean
  submitLabel: string
  onSubmit: (values: StudentFormValues) => void
  onCancel: () => void
}

export function StudentForm({
  defaultValues = studentFormDefaultValues,
  isSubmitting,
  submitLabel,
  onSubmit,
  onCancel,
}: StudentFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<StudentFormValues>({
    resolver: zodResolver(studentFormSchema),
    defaultValues,
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div className={styles.grid}>
        <Field
          label="Nombre"
          required
          autoFocus
          placeholder="Juan"
          error={errors.firstName?.message}
          {...register('firstName')}
        />
        <Field
          label="Apellido"
          required
          placeholder="Pérez"
          error={errors.lastName?.message}
          {...register('lastName')}
        />
        <Field
          label="DNI"
          required
          inputMode="numeric"
          placeholder="30123456"
          hint="7 u 8 dígitos, sin puntos"
          error={errors.dni?.message}
          {...register('dni')}
        />
        <Field
          label="Fecha de nacimiento"
          required
          type="date"
          error={errors.dateOfBirth?.message}
          {...register('dateOfBirth')}
        />
        <Field
          label="Teléfono"
          type="tel"
          placeholder="+54 9 11 1234-5678"
          error={errors.phone?.message}
          {...register('phone')}
        />
        <Field
          label="Email"
          type="email"
          placeholder="juan.perez@example.com"
          error={errors.email?.message}
          {...register('email')}
        />
      </div>

      <div className={styles.actions}>
        <Button type="button" variant="ghost" onClick={onCancel} disabled={isSubmitting}>
          Cancelar
        </Button>
        <Button type="submit" variant="primary" isLoading={isSubmitting}>
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}
