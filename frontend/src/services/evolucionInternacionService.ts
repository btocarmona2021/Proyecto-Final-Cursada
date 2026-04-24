// src/services/evolucionInternacionService.ts
import api from '@/api/api'
import type {
  EvolucionInternacion,
  EvolucionInternacionForm,
} from '@/interfaces/evolucionInternacion.interface'

const evolucionInternacionService = {
  async obtenerTodos(): Promise<EvolucionInternacion[]> {
    const response = await api.get<EvolucionInternacion[]>('/evoluciones/')
    return response.data
  },
  async obtenerUno(id: number): Promise<EvolucionInternacion> {
    const response = await api.get<EvolucionInternacion>(`/evoluciones/${id}/`)
    return response.data
  },
  async crear(data: EvolucionInternacionForm): Promise<EvolucionInternacion> {
    const response = await api.post<EvolucionInternacion>('/evoluciones/', data)
    return response.data
  },
  async actualizar(id: number, data: EvolucionInternacionForm): Promise<EvolucionInternacion> {
    const response = await api.put<EvolucionInternacion>(`/evoluciones/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/evoluciones/${id}/`)
  },
}
export default evolucionInternacionService

