// src/services/vacunasService.ts
import api from '@/api/api'
import type { Vacuna, VacunaForm } from '@/interfaces/vacuna.interface'

const vacunasService = {
  async obtenerTodos(): Promise<Vacuna[]> {
    const response = await api.get<Vacuna[]>('/vacunas/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Vacuna> {
    const response = await api.get<Vacuna>(`/vacunas/${id}/`)
    return response.data
  },
  async crear(data: VacunaForm): Promise<Vacuna> {
    const response = await api.post<Vacuna>('/vacunas/', data)
    return response.data
  },
  async actualizar(id: number, data: VacunaForm): Promise<Vacuna> {
    const response = await api.put<Vacuna>(`/vacunas/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/vacunas/${id}/`)
  },
}
export default vacunasService

