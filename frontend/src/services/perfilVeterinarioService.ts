// src/services/perfilVeterinarioService.ts
import api from '@/api/api'
import type {
  VeterinarioPerfil,
  VeterinariaPerfilForm,
} from '@/interfaces/veterinarioPerfil.interface'

const perfilVeterinarioService = {
  async obtenerTodos(): Promise<VeterinarioPerfil[]> {
    const response = await api.get<VeterinarioPerfil[]>('/veterinarios/')
    return response.data
  },
  async obtenerUno(id: number): Promise<VeterinarioPerfil> {
    const response = await api.get<VeterinarioPerfil>(`/veterinarios/${id}/`)
    return response.data
  },
  async crear(data: VeterinariaPerfilForm): Promise<VeterinarioPerfil> {
    const response = await api.post<VeterinarioPerfil>('/veterinarios/', data)
    return response.data
  },
  async actualizar(id: number, data: VeterinariaPerfilForm): Promise<VeterinarioPerfil> {
    const response = await api.put<VeterinarioPerfil>(`/veterinarios/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/veterinarios/${id}/`)
  },
}
export default perfilVeterinarioService

