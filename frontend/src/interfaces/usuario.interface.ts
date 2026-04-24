export interface Usuario {
  id: number
  username: string
  first_name: string
  last_name: string
  email: string
}

export interface PerfilUsuario {
  id: number
  usuario: Usuario
  telefono: string | null
  direccion: string | null
  foto: string | null
}

export interface PerfilUsuarioForm {
  telefono?: string
  direccion?: string
  foto?: File | null
}

export interface RegistroUsuarioForm {
  username: string
  password: string
  first_name: string
  last_name: string
  email: string
  telefono?: string
  direccion?: string
}
