export interface Vacuna {
  id: number
  mascota: number
  nombre: string
  fecha_aplicacion: string
  fecha_proxima: string | null
  observaciones: string | null
  veterinario: number | null
  created_at: string
  updated_at: string
  activo: boolean
}

export interface VacunaForm {
  mascota: number
  nombre: string
  fecha_aplicacion: string
  fecha_proxima?: string
  observaciones?: string
  veterinario?: number
}