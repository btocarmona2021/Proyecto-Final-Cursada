import type { Usuario } from './usuario.interface'

export interface VeterinarioPerfil {
  id: number
  usuario: Usuario
  nombre_completo: string
  matricula: string
  especialidad: string | null
  biografia: string | null
  foto: string | null
  disponible: boolean
}

export interface VeterinariaPerfilForm {
  usuario: number
  matricula: string
  especialidad?: string
  biografia?: string
  foto?: File | null
  disponible?: boolean
}
