// src/services/notificacionesService.ts
import api from '@/api/api'
import type { Notificacion, NotificacionForm } from '@/interfaces/notificacion.interface'

const notificacionesService = {
  async obtenerTodos(): Promise<Notificacion[]> {
    const response = await api.get<Notificacion[]>('/notificaciones/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Notificacion> {
    const response = await api.get<Notificacion>(`/notificaciones/${id}/`)
    return response.data
  },
  async crear(data: NotificacionForm): Promise<Notificacion> {
    const response = await api.post<Notificacion>('/notificaciones/', data)
    return response.data
  },
  async actualizar(id: number, data: NotificacionForm): Promise<Notificacion> {
    const response = await api.put<Notificacion>(`/notificaciones/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/notificaciones/${id}/`)
  },
}
export default notificacionesService
