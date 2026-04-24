// src/services/especiesService.ts
import api from '@/api/api'
import type { Especie, EspecieForm } from '@/interfaces/especie.interface'

const especiesService = {
  async obtenerTodos(): Promise<Especie[]> {
    const response = await api.get<Especie[]>('/especies/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Especie> {
    const response = await api.get<Especie>(`/especies/${id}/`)
    return response.data
  },
  async crear(data: EspecieForm): Promise<Especie> {
    const response = await api.post<Especie>('/especies/', data)
    return response.data
  },
  async actualizar(id: number, data: EspecieForm): Promise<Especie> {
    const response = await api.put<Especie>(`/especies/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/especies/${id}/`)
  },
}
export default especiesService
