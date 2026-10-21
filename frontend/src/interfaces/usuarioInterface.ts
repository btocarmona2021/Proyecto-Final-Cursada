
// Usuario tal como lo maneja el frontend (normalizado)
export interface UsuarioAuth {
  id: number
  username: string
  first_name: string
  last_name: string
  email: string
  grupo: string | null
}

export interface FormularioInicioSesion {
  username: string
  password: string
}

export interface RespuestaToken {
  access: string
  refresh: string
  grupo?: string | null
}

export type Usuario = UsuarioAuth

export interface RegistroUsuarioForm {
  username: string
  password?: string
  first_name: string
  last_name: string
  email: string
  telefono?: string
  direccion?: string
}
