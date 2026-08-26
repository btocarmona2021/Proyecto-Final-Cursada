// src/services/turnosService.ts
import api from '@/api/api'
import type { Turno, TurnoForm } from '@/interfaces/turnoInterface'

const turnosService = {
  async obtenerTodos(): Promise<Turno[]> {
    const response = await api.get<Turno[]>('/turnos/')
    return response.data
  },

  async obtenerUno(id: number): Promise<Turno> {
    const response = await api.get<Turno>(`/turnos/${id}/`)
    return response.data
  },

  async crear(data: TurnoForm): Promise<Turno> {
    const response = await api.post<Turno>('/turnos/', data)
    return response.data
  },

  async actualizar(id: number, data: TurnoForm): Promise<Turno> {
    const response = await api.put<Turno>(`/turnos/${id}/`, data)
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/turnos/${id}/`)
  },

  async cancelar(id: number): Promise<Turno> {
    const response = await api.post<Turno>(`/turnos/${id}/cancelar/`)
    return response.data
  },

  async atender(id: number): Promise<Turno> {
    const response = await api.post<Turno>(`/turnos/${id}/atender/`)
    return response.data
  },
}

export default turnosService