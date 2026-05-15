// interfaces/servicioInterface.ts
export interface Servicio {
  id: number
  nombre: string
  descripcion: string | null
  precio: number
  duracion_estimada: number
  activo: boolean
  created_at: string
  updated_at: string
}

export interface ServicioForm {
  nombre: string
  descripcion: string
  precio: number
  duracion_estimada: number
  activo: boolean
}