import { forwardRef } from 'react'
import type { InputHTMLAttributes, ReactNode } from 'react'

import styles from './Field.module.css'

interface FieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
  hint?: string
  suffix?: ReactNode
}

export const Field = forwardRef<HTMLInputElement, FieldProps>(
  ({ label, error, hint, suffix, id, className, ...rest }, ref) => {
    const inputId = id ?? rest.name
    const errorId = error ? `${inputId}-error` : undefined
    const hintId = hint ? `${inputId}-hint` : undefined

    return (
      <div className={[styles.field, className].filter(Boolean).join(' ')}>
        <label htmlFor={inputId} className={styles.label}>
          {label}
          {rest.required && <span className={styles.required}> *</span>}
        </label>
        <div className={styles.inputWrapper}>
          <input
            ref={ref}
            id={inputId}
            className={[styles.input, error && styles.inputError].filter(Boolean).join(' ')}
            aria-invalid={Boolean(error)}
            aria-describedby={errorId ?? hintId}
            {...rest}
          />
          {suffix && <span className={styles.suffix}>{suffix}</span>}
        </div>
        {error ? (
          <p id={errorId} className={styles.errorText} role="alert">
            {error}
          </p>
        ) : hint ? (
          <p id={hintId} className={styles.hintText}>
            {hint}
          </p>
        ) : null}
      </div>
    )
  },
)

Field.displayName = 'Field'
