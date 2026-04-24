// src/services/consultasService.ts
import api from '@/api/api'
import type { ConsultaClinica, ConsultaClinicaForm } from '@/interfaces/consulta.interface'

const consultasService = {
  async obtenerTodos(): Promise<ConsultaClinica[]> {
    const response = await api.get<ConsultaClinica[]>('/consultas/')
    return response.data
  },
  async obtenerUno(id: number): Promise<ConsultaClinica> {
    const response = await api.get<ConsultaClinica>(`/consultas/${id}/`)
    return response.data
  },
  async crear(data: ConsultaClinicaForm): Promise<ConsultaClinica> {
    const response = await api.post<ConsultaClinica>('/consultas/', data)
    return response.data
  },
  async actualizar(id: number, data: ConsultaClinicaForm): Promise<ConsultaClinica> {
    const response = await api.put<ConsultaClinica>(`/consultas/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/consultas/${id}/`)
  },
}
export default consultasService

