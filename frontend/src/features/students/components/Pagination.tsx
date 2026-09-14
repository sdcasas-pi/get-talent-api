import { Button } from '../../../components/ui/Button'
import styles from './Pagination.module.css'

interface PaginationProps {
  total: number
  limit: number
  offset: number
  onOffsetChange: (offset: number) => void
}

export function Pagination({ total, limit, offset, onOffsetChange }: PaginationProps) {
  if (total === 0) return null

  const currentPage = Math.floor(offset / limit) + 1
  const totalPages = Math.max(1, Math.ceil(total / limit))
  const rangeStart = offset + 1
  const rangeEnd = Math.min(offset + limit, total)

  return (
    <div className={styles.wrapper}>
      <span className={styles.summary}>
        Mostrando {rangeStart}–{rangeEnd} de {total}
      </span>
      <div className={styles.controls}>
        <Button
          variant="ghost"
          onClick={() => onOffsetChange(Math.max(0, offset - limit))}
          disabled={offset === 0}
        >
          Anterior
        </Button>
        <span className={styles.page}>
          Página {currentPage} de {totalPages}
        </span>
        <Button
          variant="ghost"
          onClick={() => onOffsetChange(offset + limit)}
          disabled={offset + limit >= total}
        >
          Siguiente
        </Button>
      </div>
    </div>
  )
}
