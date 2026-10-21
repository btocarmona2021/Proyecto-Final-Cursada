import type { UsuarioAuth } from './usuarioInterface'

// Perfil de veterinario tal como lo devuelve el backend
export interface VeterinarioPerfil {
  id: number
  usuario: UsuarioAuth
  matricula: string
  especialidad: string | null
  biografia: string | null
  foto: string | null
  disponible: boolean
  fecha_creacion: string
  fecha_actualizacion: string
}

// interface para crear/editar veterinarios (lado admin)
export interface VeterinarioPerfilForm {
  // Datos de usuario - normalmente solo en alta
  username?: string
  password?: string
  first_name?: string
  last_name?: string
  email?: string
  // Datos específicos del veterinario
  matricula: string
  especialidad?: string
  biografia?: string
  foto?: File | null
  disponible?: boolean
}
