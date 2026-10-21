import api from '@/api/api'
import type {
  VeterinarioPerfil,
  VeterinarioPerfilForm,
} from '@/interfaces/veterinarioPerfilInterface'

// FormData permite enviar los datos y la imagen juntos como multipart.
function formularioVeterinario(data: VeterinarioPerfilForm): FormData {
  const formulario = new FormData()

  if (data.username != null) formulario.append('username', data.username)
  if (data.password != null) formulario.append('password', data.password)
  if (data.first_name != null) formulario.append('first_name', data.first_name)
  if (data.last_name != null) formulario.append('last_name', data.last_name)
  if (data.email != null) formulario.append('email', data.email)
  formulario.append('matricula', data.matricula)
  if (data.especialidad != null) formulario.append('especialidad', data.especialidad)
  if (data.biografia != null) formulario.append('biografia', data.biografia)
  if (data.disponible != null) formulario.append('disponible', String(data.disponible))

  if (data.foto) formulario.append('foto', data.foto)

  return formulario
}

const perfilVeterinarioService = {
  async obtenerTodos(): Promise<VeterinarioPerfil[]> {
    const response = await api.get<VeterinarioPerfil[]>('/veterinarios/')
    return response.data
  },

  async obtenerUno(id: number): Promise<VeterinarioPerfil> {
    const response = await api.get<VeterinarioPerfil>(`/veterinarios/${id}/`)
    return response.data
  },

  async crear(data: VeterinarioPerfilForm): Promise<VeterinarioPerfil> {
    const response = await api.post<VeterinarioPerfil>(
      '/veterinarios/',
      formularioVeterinario(data),
    )
    return response.data
  },

  async actualizar(id: number, data: VeterinarioPerfilForm): Promise<VeterinarioPerfil> {
    const response = await api.put<VeterinarioPerfil>(
      `/veterinarios/${id}/`,
      formularioVeterinario(data),
    )
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/veterinarios/${id}/`)
  },
}

export default perfilVeterinarioService
