// src/interfaces/mascotaInterface.ts

// Representa una mascota tal como la devuelve el backend Django
export interface Mascota {
  id: number
  nombre: string

  raza: number  // ID de la raza
  raza_nombre: string  // ← snake_case
  especie_nombre: string  // ← snake_case

  fecha_nacimiento: string | null
  edad_anos: number | null

  sexo: 'M' | 'H'
  sexo_display: string  // ← snake_case

  color: string | null
  peso_actual: string | null  // ← snake_case
  microchip: string | null
  foto: string | null

  usuario: number  // ID del dueño
  usuario_nombre: string  // ← snake_case

  created_at: string
  updated_at: string
  activo: boolean
}

// Formulario para crear/editar mascotas (lo que envías al backend)
export interface MascotaForm {
  nombre: string
  raza: number
  fecha_nacimiento?: string
  sexo: 'M' | 'H'
  color?: string
  peso_actual?: number
  microchip?: string
  foto?: File | null
  usuario: number // id del dueño
}
