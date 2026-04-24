// src/services/internacionesService.ts
import api from '@/api/api'
import type { Internacion, InternacionForm } from '@/interfaces/internacion.interface'

const internacionesService = {
  async obtenerTodos(): Promise<Internacion[]> {
    const response = await api.get<Internacion[]>('/internaciones/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Internacion> {
    const response = await api.get<Internacion>(`/internaciones/${id}/`)
    return response.data
  },
  async crear(data: InternacionForm): Promise<Internacion> {
    const response = await api.post<Internacion>('/internaciones/', data)
    return response.data
  },
  async actualizar(id: number, data: InternacionForm): Promise<Internacion> {
    const response = await api.put<Internacion>(`/internaciones/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/internaciones/${id}/`)
  },
}
export default internacionesService
