import type { Student } from '../../../types/student'
import { formatDate, formatDni } from '../../../lib/format'
import styles from './StudentTable.module.css'

interface StudentTableProps {
  students: Student[]
  onEdit: (student: Student) => void
  onDelete: (student: Student) => void
}

export function StudentTable({ students, onEdit, onDelete }: StudentTableProps) {
  return (
    <div className={styles.wrapper}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Apellido y nombre</th>
            <th>DNI</th>
            <th>Nacimiento</th>
            <th>Contacto</th>
            <th aria-label="Acciones" />
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.id}>
              <td>
                <span className={styles.fullName}>
                  {student.lastName}, {student.firstName}
                </span>
              </td>
              <td>{formatDni(student.dni)}</td>
              <td>{formatDate(student.dateOfBirth)}</td>
              <td>
                <div className={styles.contact}>
                  {student.email && <span>{student.email}</span>}
                  {student.phone && <span className={styles.muted}>{student.phone}</span>}
                  {!student.email && !student.phone && <span className={styles.muted}>—</span>}
                </div>
              </td>
              <td>
                <div className={styles.actions}>
                  <button
                    type="button"
                    className={styles.actionButton}
                    onClick={() => onEdit(student)}
                  >
                    Editar
                  </button>
                  <button
                    type="button"
                    className={[styles.actionButton, styles.danger].join(' ')}
                    onClick={() => onDelete(student)}
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
