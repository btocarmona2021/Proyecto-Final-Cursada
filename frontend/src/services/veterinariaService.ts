import api from '@/api/api'
import type { Veterinaria, VeterinariaForm } from '@/interfaces/veterinariaInterface'

// FormData permite enviar los datos y la imagen juntos como multipart.
function formularioClinica(data: VeterinariaForm): FormData {
  const formulario = new FormData()

  formulario.append('razon_social', data.razon_social)
  if (data.nombre_fantasia != null) formulario.append('nombre_fantasia', data.nombre_fantasia)
  formulario.append('cuit', data.cuit)
  formulario.append('direccion', data.direccion)
  formulario.append('ciudad', data.ciudad)
  formulario.append('provincia', data.provincia)
  if (data.codigo_postal != null) formulario.append('codigo_postal', data.codigo_postal)
  if (data.telefono != null) formulario.append('telefono', data.telefono)
  if (data.email != null) formulario.append('email', data.email)
  if (data.sitio_web != null) formulario.append('sitio_web', data.sitio_web)
  if (data.descripcion != null) formulario.append('descripcion', data.descripcion)
  if (data.horario_atencion != null) formulario.append('horario_atencion', data.horario_atencion)
  if (data.instagram != null) formulario.append('instagram', data.instagram)
  if (data.facebook != null) formulario.append('facebook', data.facebook)

  if (data.logo) formulario.append('logo', data.logo)

  return formulario
}

const veterinariaService = {
  async obtenerTodos(): Promise<Veterinaria[]> {
    const response = await api.get<Veterinaria[]>('/veterinaria/')
    return response.data
  },

  async obtenerUno(id: number): Promise<Veterinaria> {
    const response = await api.get<Veterinaria>(`/veterinaria/${id}/`)
    return response.data
  },

  async crear(data: VeterinariaForm): Promise<Veterinaria> {
    const response = await api.post<Veterinaria>('/veterinaria/', formularioClinica(data))
    return response.data
  },

  async actualizar(id: number, data: VeterinariaForm): Promise<Veterinaria> {
    const response = await api.put<Veterinaria>(`/veterinaria/${id}/`, formularioClinica(data))
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/veterinaria/${id}/`)
  },
}

export default veterinariaService
