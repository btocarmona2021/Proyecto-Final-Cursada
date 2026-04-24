// src/services/horarioVeterinarioService.ts
import api from '@/api/api'
import type {
  HorarioVeterinario,
  HorarioVeterinarioForm,
} from '@/interfaces/horarioVeterinario.interface'

const horarioVeterinarioService = {
  async obtenerTodos(): Promise<HorarioVeterinario[]> {
    const response = await api.get<HorarioVeterinario[]>('/horarios/')
    return response.data
  },
  async obtenerUno(id: number): Promise<HorarioVeterinario> {
    const response = await api.get<HorarioVeterinario>(`/horarios/${id}/`)
    return response.data
  },
  async crear(data: HorarioVeterinarioForm): Promise<HorarioVeterinario> {
    const response = await api.post<HorarioVeterinario>('/horarios/', data)
    return response.data
  },
  async actualizar(id: number, data: HorarioVeterinarioForm): Promise<HorarioVeterinario> {
    const response = await api.put<HorarioVeterinario>(`/horarios/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/horarios/${id}/`)
  },
}
export default horarioVeterinarioService
