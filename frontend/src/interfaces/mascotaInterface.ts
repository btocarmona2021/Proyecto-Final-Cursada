// src/interfaces/mascotaInterface.ts

// Representa una mascota tal como la devuelve el backend Django
export interface Mascota {
  id: number
  nombre: string

  raza: number  // ID de la raza
  raza_nombre: string
  especie_nombre: string

  fecha_nacimiento: string | null
  edad_anos: number | null

  sexo: 'M' | 'H'
  sexo_display: string

  color: string | null
  peso_actual: string | null
  microchip: string | null
  foto: string | null
  observaciones: string | null

  usuario: number  // ID del dueño
  usuario_nombre: string

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
  observaciones?: string
  usuario: number // id del dueño
}
