import type { UsuarioAuth } from './usuarioInterface'

// Perfil de veterinario tal como lo devuelve el backend
export interface VeterinarioPerfil {
  id: number
  usuario: UsuarioAuth  // ← Contiene first_name, last_name
  matricula: string
  especialidad: string | null
  biografia: string | null
  foto: string | null
  disponible: boolean
  fecha_creacion: string
  fecha_actualizacion: string
}

// Formulario para crear/editar veterinarios (lado admin)
export interface VeterinarioPerfilForm {
  // Datos de usuario - normalmente solo en alta
  username?: string
  password?: string
  primer_nombre?: string
  apellido?: string
  correo?: string

  // Datos específicos del veterinario
  matricula: string
  especialidad?: string
  biografia?: string
  foto?: File | null
  disponible?: boolean
}