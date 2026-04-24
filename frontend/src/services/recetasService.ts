// src/services/recetasService.ts
import api from '@/api/api'
import type { RecetaItem, RecetaItemForm } from '@/interfaces/recetaItem.interface'

const recetasService = {
  async obtenerTodos(): Promise<RecetaItem[]> {
    const response = await api.get<RecetaItem[]>('/recetas/')
    return response.data
  },
  async obtenerUno(id: number): Promise<RecetaItem> {
    const response = await api.get<RecetaItem>(`/recetas/${id}/`)
    return response.data
  },
  async crear(data: RecetaItemForm): Promise<RecetaItem> {
    const response = await api.post<RecetaItem>('/recetas/', data)
    return response.data
  },
  async actualizar(id: number, data: RecetaItemForm): Promise<RecetaItem> {
    const response = await api.put<RecetaItem>(`/recetas/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/recetas/${id}/`)
  },
}
export default recetasService

