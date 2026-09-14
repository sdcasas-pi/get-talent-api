import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { StudentForm } from './StudentForm'

describe('StudentForm', () => {
  it('shows validation errors and blocks submit when fields are invalid', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()

    render(
      <StudentForm
        isSubmitting={false}
        submitLabel="Registrar"
        onSubmit={onSubmit}
        onCancel={vi.fn()}
      />,
    )

    await user.type(screen.getByLabelText(/dni/i), '123')
    await user.click(screen.getByRole('button', { name: 'Registrar' }))

    expect(await screen.findByText(/el dni debe tener 7 u 8 dígitos/i)).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('submits normalized values when the form is valid', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()

    render(
      <StudentForm
        isSubmitting={false}
        submitLabel="Registrar"
        onSubmit={onSubmit}
        onCancel={vi.fn()}
      />,
    )

    await user.type(screen.getByLabelText(/nombre/i), 'Juan')
    await user.type(screen.getByLabelText(/apellido/i), 'Perez')
    await user.type(screen.getByLabelText(/dni/i), '30123456')
    await user.type(screen.getByLabelText(/fecha de nacimiento/i), '1995-05-20')
    await user.click(screen.getByRole('button', { name: 'Registrar' }))

    expect(onSubmit).toHaveBeenCalledTimes(1)
    expect(onSubmit.mock.calls[0][0]).toMatchObject({
      firstName: 'Juan',
      lastName: 'Perez',
      dni: '30123456',
      dateOfBirth: '1995-05-20',
    })
  })
})
