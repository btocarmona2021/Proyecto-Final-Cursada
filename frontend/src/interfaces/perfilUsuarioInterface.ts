// src/interfaces/perfilUsuarioInterface.ts
import type { UsuarioAuth } from './usuarioInterface'

// Perfil de usuario cliente tal como lo devuelve el backend
export interface PerfilUsuario {
  id: number
  usuario: UsuarioAuth
  telefono: string | null
  direccion: string | null
  foto: string | null
  fecha_creacion: string
  fecha_actualizacion: string
}

// Formulario para editar el perfil del usuario
export interface PerfilUsuarioForm {
  telefono?: string
  direccion?: string
  foto?: File | null
}

// ✅ Formulario para registrar un nuevo cliente (snake_case)
export interface RegistroClienteForm {
  username: string
  password: string
  first_name: string  // ← snake_case
  last_name: string   // ← snake_case
  email: string
  telefono?: string
  direccion?: string
}
