import api from '@/api/api'
import type {
  PerfilUsuario,
  PerfilUsuarioForm,
  RegistroClienteForm,
} from '@/interfaces/perfilUsuarioInterface'

// FormData permite enviar los datos y la imagen juntos como multipart.
function formularioCliente(data: PerfilUsuarioForm): FormData {
  const formulario = new FormData()

  if (data.username != null) formulario.append('username', data.username)
  if (data.first_name != null) formulario.append('first_name', data.first_name)
  if (data.last_name != null) formulario.append('last_name', data.last_name)
  if (data.email != null) formulario.append('email', data.email)
  if (data.telefono != null) formulario.append('telefono', data.telefono)
  if (data.direccion != null) formulario.append('direccion', data.direccion)

  if (data.foto) formulario.append('foto', data.foto)

  return formulario
}

const perfilClienteService = {
  async obtenerTodos(): Promise<PerfilUsuario[]> {
    const response = await api.get<PerfilUsuario[]>('/clientes/')
    return response.data
  },

  async obtenerUno(id: number): Promise<PerfilUsuario> {
    const response = await api.get<PerfilUsuario>(`/clientes/${id}/`)
    return response.data
  },

  async crear(data: RegistroClienteForm): Promise<PerfilUsuario> {
    const formulario = formularioCliente(data)
    formulario.append('password', data.password)
    const response = await api.post<PerfilUsuario>('/clientes/', formulario)
    return response.data
  },

  async actualizar(id: number, data: PerfilUsuarioForm): Promise<PerfilUsuario> {
    const response = await api.put<PerfilUsuario>(`/clientes/${id}/`, formularioCliente(data))
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/clientes/${id}/`)
  },
}

export default perfilClienteService
