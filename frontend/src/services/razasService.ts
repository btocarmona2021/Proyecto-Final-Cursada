// src/services/razasService.ts
import api from '@/api/api'
import type { Raza, RazaForm } from '@/interfaces/raza.interface'

const razasService = {
  async obtenerTodos(): Promise<Raza[]> {
    const response = await api.get<Raza[]>('/razas/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Raza> {
    const response = await api.get<Raza>(`/razas/${id}/`)
    return response.data
  },
  async crear(data: RazaForm): Promise<Raza> {
    const response = await api.post<Raza>('/razas/', data)
    return response.data
  },
  async actualizar(id: number, data: RazaForm): Promise<Raza> {
    const response = await api.put<Raza>(`/razas/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/razas/${id}/`)
  },
}
export default razasService
