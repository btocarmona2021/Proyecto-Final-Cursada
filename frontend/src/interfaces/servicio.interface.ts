export interface Servicio {
  id: number
  nombre: string
  descripcion: string | null
  precio: number
  duracion_estimada: number
}

export interface ServicioForm {
  nombre: string
  descripcion?: string
  precio: number
  duracion_estimada: number
}
