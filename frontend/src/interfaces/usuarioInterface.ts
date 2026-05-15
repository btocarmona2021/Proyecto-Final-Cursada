
// Usuario tal como lo maneja el frontend (normalizado)
export interface UsuarioAuth {
  id: number
  username: string
  first_name: string  // ← snake_case (como viene del backend)
  last_name: string   // ← snake_case
  email: string
  grupo: string | null  // nombre del grupo principal
}

export interface FormularioInicioSesion {
  username: string
  password: string
}

export interface RespuestaToken {
  acceso: string
  refresco: string
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