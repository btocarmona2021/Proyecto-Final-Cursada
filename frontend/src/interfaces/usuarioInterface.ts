
// Usuario tal como lo maneja el frontend (normalizado)
export interface UsuarioAuth {
  id: number
  username: string
  first_name: string  // ← snake_case (como viene del backend)
  last_name: string   // ← snake_case
  email: string
  grupo: string | null  // nombre del grupo principal
}

export interface LoginForm {
  username: string
  password: string
}

export interface TokenResponse {
  access: string
  refresh: string
}