// src/services/mascotasService.ts
import api from '@/api/api'
import type { Mascota, MascotaForm } from '@/interfaces/mascotaInterface'

// FormData permite enviar los datos y la imagen juntos como multipart.
function formularioMascota(data: MascotaForm): FormData {
  const formulario = new FormData()

  formulario.append('nombre', data.nombre)
  formulario.append('raza', String(data.raza))
  formulario.append('usuario', String(data.usuario))
  formulario.append('sexo', data.sexo)
  if (data.fecha_nacimiento != null) formulario.append('fecha_nacimiento', data.fecha_nacimiento)
  if (data.color != null) formulario.append('color', data.color)
  if (data.peso_actual != null) formulario.append('peso_actual', String(data.peso_actual))
  if (data.microchip != null) formulario.append('microchip', data.microchip)
  if (data.observaciones != null) formulario.append('observaciones', data.observaciones)

  if (data.foto) formulario.append('foto', data.foto)

  return formulario
}

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
    const response = await api.post<Mascota>('/mascotas/', formularioMascota(data))
    return response.data
  },

  async actualizar(id: number, data: MascotaForm): Promise<Mascota> {
    const response = await api.put<Mascota>(`/mascotas/${id}/`, formularioMascota(data))
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/mascotas/${id}/`)
  },
}

export default mascotasService
