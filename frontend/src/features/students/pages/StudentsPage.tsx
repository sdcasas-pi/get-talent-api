import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'

import { ApiError } from '../../../api/client'
import { studentsApi } from '../../../api/students'
import { Button } from '../../../components/ui/Button'
import { ConfirmDialog } from '../../../components/ui/ConfirmDialog'
import { EmptyState } from '../../../components/ui/EmptyState'
import { Field } from '../../../components/ui/Field'
import { Modal } from '../../../components/ui/Modal'
import { useToast } from '../../../components/ui/useToast'
import type { Student } from '../../../types/student'
import { Pagination } from '../components/Pagination'
import { StudentForm } from '../components/StudentForm'
import { StudentTable } from '../components/StudentTable'
import {
  useCreateStudent,
  useDeleteStudent,
  useStudentsList,
  useUpdateStudent,
} from '../hooks/useStudents'
import type { StudentFormValues } from '../schemas/studentSchema'
import styles from './StudentsPage.module.css'

const PAGE_SIZE = 10

type ModalState = { mode: 'create' } | { mode: 'edit'; student: Student } | null

function toApiErrorMessage(error: unknown, fallback: string): string {
  if (error instanceof ApiError) return error.message
  return fallback
}

export function StudentsPage() {
  const [offset, setOffset] = useState(0)
  const [modalState, setModalState] = useState<ModalState>(null)
  const [studentToDelete, setStudentToDelete] = useState<Student | null>(null)
  const [dniQuery, setDniQuery] = useState('')
  const [searchResult, setSearchResult] = useState<Student | 'not-found' | null>(null)
  const [isSearching, setIsSearching] = useState(false)

  const { showToast } = useToast()

  const listParams = useMemo(() => ({ limit: PAGE_SIZE, offset }), [offset])
  const { data, isLoading, isError, error } = useStudentsList(listParams)

  const createStudent = useCreateStudent()
  const updateStudent = useUpdateStudent()
  const deleteStudent = useDeleteStudent()

  function closeModal() {
    setModalState(null)
  }

  function handleCreateSubmit(values: StudentFormValues) {
    createStudent.mutate(
      {
        firstName: values.firstName,
        lastName: values.lastName,
        dni: values.dni,
        dateOfBirth: values.dateOfBirth,
        phone: values.phone,
        email: values.email,
      },
      {
        onSuccess: () => {
          showToast('Alumno registrado correctamente', 'success')
          closeModal()
        },
        onError: (err) => {
          showToast(toApiErrorMessage(err, 'No se pudo registrar el alumno'), 'error')
        },
      },
    )
  }

  function handleEditSubmit(studentId: string, values: StudentFormValues) {
    updateStudent.mutate(
      {
        id: studentId,
        input: {
          firstName: values.firstName,
          lastName: values.lastName,
          dni: values.dni,
          dateOfBirth: values.dateOfBirth,
          phone: values.phone,
          email: values.email,
        },
      },
      {
        onSuccess: () => {
          showToast('Cambios guardados', 'success')
          closeModal()
        },
        onError: (err) => {
          showToast(toApiErrorMessage(err, 'No se pudo actualizar el alumno'), 'error')
        },
      },
    )
  }

  function handleConfirmDelete() {
    if (!studentToDelete) return
    deleteStudent.mutate(studentToDelete.id, {
      onSuccess: () => {
        showToast('Alumno eliminado', 'success')
        setStudentToDelete(null)
      },
      onError: (err) => {
        showToast(toApiErrorMessage(err, 'No se pudo eliminar el alumno'), 'error')
      },
    })
  }

  async function handleSearchByDni(event: FormEvent) {
    event.preventDefault()
    if (!dniQuery.trim()) {
      setSearchResult(null)
      return
    }
    setIsSearching(true)
    try {
      const student = await studentsApi.getByDni(dniQuery.trim())
      setSearchResult(student)
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setSearchResult('not-found')
      } else {
        showToast(toApiErrorMessage(err, 'Error al buscar el alumno'), 'error')
      }
    } finally {
      setIsSearching(false)
    }
  }

  function clearSearch() {
    setDniQuery('')
    setSearchResult(null)
  }

  const isMutating = createStudent.isPending || updateStudent.isPending

  return (
    <div className={styles.page}>
      <div className={styles.pageHeader}>
        <div>
          <h1>Alumnos</h1>
          <p className={styles.subtitle}>Gestión de inscripciones del curso</p>
        </div>
        <Button variant="primary" onClick={() => setModalState({ mode: 'create' })}>
          + Nuevo alumno
        </Button>
      </div>

      <form className={styles.searchBar} onSubmit={handleSearchByDni}>
        <Field
          label="Buscar por DNI"
          placeholder="30123456"
          value={dniQuery}
          inputMode="numeric"
          onChange={(event) => setDniQuery(event.target.value)}
        />
        <div className={styles.searchActions}>
          <Button type="submit" variant="secondary" isLoading={isSearching}>
            Buscar
          </Button>
          {searchResult && (
            <Button type="button" variant="ghost" onClick={clearSearch}>
              Limpiar
            </Button>
          )}
        </div>
      </form>

      {searchResult === 'not-found' && (
        <p className={styles.searchFeedback}>No se encontró ningún alumno con ese DNI.</p>
      )}

      {searchResult && searchResult !== 'not-found' && (
        <div className={styles.searchResult}>
          <StudentTable
            students={[searchResult]}
            onEdit={(student) => setModalState({ mode: 'edit', student })}
            onDelete={(student) => setStudentToDelete(student)}
          />
        </div>
      )}

      {!searchResult && (
        <>
          {isLoading && <p className={styles.status}>Cargando alumnos…</p>}

          {isError && (
            <p className={[styles.status, styles.errorStatus].join(' ')}>
              {toApiErrorMessage(error, 'No se pudo cargar el listado de alumnos')}
            </p>
          )}

          {data && data.data.length === 0 && (
            <EmptyState
              title="Todavía no hay alumnos registrados"
              description="Registrá el primer alumno del curso para empezar."
              action={
                <Button variant="primary" onClick={() => setModalState({ mode: 'create' })}>
                  + Nuevo alumno
                </Button>
              }
            />
          )}

          {data && data.data.length > 0 && (
            <>
              <StudentTable
                students={data.data}
                onEdit={(student) => setModalState({ mode: 'edit', student })}
                onDelete={(student) => setStudentToDelete(student)}
              />
              <Pagination
                total={data.total}
                limit={data.limit}
                offset={data.offset}
                onOffsetChange={setOffset}
              />
            </>
          )}
        </>
      )}

      <Modal
        title={modalState?.mode === 'edit' ? 'Editar alumno' : 'Nuevo alumno'}
        isOpen={modalState !== null}
        onClose={closeModal}
      >
        {modalState && (
          <StudentForm
            submitLabel={modalState.mode === 'edit' ? 'Guardar cambios' : 'Registrar'}
            isSubmitting={isMutating}
            defaultValues={
              modalState.mode === 'edit'
                ? {
                    firstName: modalState.student.firstName,
                    lastName: modalState.student.lastName,
                    dni: modalState.student.dni,
                    dateOfBirth: modalState.student.dateOfBirth,
                    phone: modalState.student.phone ?? '',
                    email: modalState.student.email ?? '',
                  }
                : undefined
            }
            onCancel={closeModal}
            onSubmit={(values) =>
              modalState.mode === 'edit'
                ? handleEditSubmit(modalState.student.id, values)
                : handleCreateSubmit(values)
            }
          />
        )}
      </Modal>

      <ConfirmDialog
        title="Eliminar alumno"
        description={
          studentToDelete
            ? `¿Confirmás eliminar a ${studentToDelete.firstName} ${studentToDelete.lastName}? Esta acción no se puede deshacer.`
            : ''
        }
        isOpen={studentToDelete !== null}
        isLoading={deleteStudent.isPending}
        confirmLabel="Eliminar"
        onConfirm={handleConfirmDelete}
        onClose={() => setStudentToDelete(null)}
      />
    </div>
  )
}
