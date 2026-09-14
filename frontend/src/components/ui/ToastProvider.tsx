import { useCallback, useState } from 'react'
import type { ReactNode } from 'react'

import { ToastContext, type ToastVariant } from './toastContext'
import styles from './ToastProvider.module.css'

interface Toast {
  id: number
  message: string
  variant: ToastVariant
}

let nextId = 0

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const showToast = useCallback((message: string, variant: ToastVariant = 'info') => {
    const id = nextId++
    setToasts((current) => [...current, { id, message, variant }])
    setTimeout(() => {
      setToasts((current) => current.filter((toast) => toast.id !== id))
    }, 4000)
  }, [])

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className={styles.container} aria-live="polite">
        {toasts.map((toast) => (
          <div key={toast.id} className={[styles.toast, styles[toast.variant]].join(' ')}>
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}
