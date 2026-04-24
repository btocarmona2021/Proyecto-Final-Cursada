export interface Vacuna {
  id: number
  mascota: number
  mascota_nombre: string
  nombre: string
  fecha_aplicacion: string
  fecha_proxima: string | null
  observaciones: string | null
  veterinario: number | null
  veterinario_nombre: string | null
}

export interface VacunaForm {
  mascota: number
  nombre: string
  fecha_aplicacion: string
  fecha_proxima?: string
  observaciones?: string
  veterinario?: number
}
