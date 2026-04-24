// src/services/veterinariaService.ts
import api from '@/api/api'
import type { Veterinaria, VeterinariaForm } from '@/interfaces/veterinaria.interface'

const veterinariaService = {
  async obtenerTodos(): Promise<Veterinaria[]> {
    const response = await api.get<Veterinaria[]>('/veterinaria/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Veterinaria> {
    const response = await api.get<Veterinaria>(`/veterinaria/${id}/`)
    return response.data
  },
  async crear(data: VeterinariaForm): Promise<Veterinaria> {
    const response = await api.post<Veterinaria>('/veterinaria/', data)
    return response.data
  },
  async actualizar(id: number, data: VeterinariaForm): Promise<Veterinaria> {
    const response = await api.put<Veterinaria>(`/veterinaria/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/veterinaria/${id}/`)
  },
}
export default veterinariaService
