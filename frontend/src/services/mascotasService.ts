// src/services/mascotasService.ts
import api from '@/api/api'
import type { Mascota, MascotaForm } from '@/interfaces/mascota.interface'

const mascotasService = {
  async obtenerTodos(): Promise<Mascota[]> {
    const response = await api.get<Mascota[]>('/mascotas/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Mascota> {
    const response = await api.get<Mascota>(`/mascotas/${id}/`)
    return response.data
  },
  async crear(data: MascotaForm): Promise<Mascota> {
    const response = await api.post<Mascota>('/mascotas/', data)
    return response.data
  },
  async actualizar(id: number, data: MascotaForm): Promise<Mascota> {
    const response = await api.put<Mascota>(`/mascotas/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/mascotas/${id}/`)
  }
}
export default mascotasService
