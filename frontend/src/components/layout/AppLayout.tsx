import type { ReactNode } from 'react'

import styles from './AppLayout.module.css'

export function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <div className={styles.brand}>
          <span className={styles.mark} aria-hidden="true">
            π
          </span>
          <div className={styles.brandText}>
            <span className={styles.brandName}>Pi Consulting</span>
            <span className={styles.brandProduct}>Get Talent</span>
          </div>
        </div>
      </header>
      <main className={styles.content}>{children}</main>
    </div>
  )
}
