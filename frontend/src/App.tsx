import { Route, Routes } from 'react-router-dom'

import { AppLayout } from './components/layout/AppLayout'
import { StudentsPage } from './features/students/pages/StudentsPage'

function NotFoundPage() {
  return (
    <div style={{ textAlign: 'center', padding: '48px 0' }}>
      <h2>Página no encontrada</h2>
    </div>
  )
}

export function App() {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<StudentsPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AppLayout>
  )
}
