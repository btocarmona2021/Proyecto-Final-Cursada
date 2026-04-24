// src/services/serviciosService.ts
import api from '@/api/api'
import type { Servicio, ServicioForm } from '@/interfaces/servicio.interface'

const serviciosService = {
  async obtenerTodos(): Promise<Servicio[]> {
    const response = await api.get<Servicio[]>('/servicios/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Servicio> {
    const response = await api.get<Servicio>(`/servicios/${id}/`)
    return response.data
  },
  async crear(data: ServicioForm): Promise<Servicio> {
    const response = await api.post<Servicio>('/servicios/', data)
    return response.data
  },
  async actualizar(id: number, data: ServicioForm): Promise<Servicio> {
    const response = await api.put<Servicio>(`/servicios/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/servicios/${id}/`)
  },
}
export default serviciosService
