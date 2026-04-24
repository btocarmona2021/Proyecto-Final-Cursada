export type EstadoInternacion = 'internado' | 'observacion' | 'alta'

export interface Internacion {
  id: number
  mascota: number
  mascota_nombre: string
  veterinario_responsable: number
  veterinario_nombre: string
  fecha_ingreso: string
  fecha_egreso: string | null
  motivo: string
  diagnostico_ingreso: string | null
  estado: EstadoInternacion
  estado_display: string
  observaciones: string | null
}

export interface InternacionForm {
  mascota: number
  veterinario_responsable: number
  motivo: string
  diagnostico_ingreso?: string
  estado?: EstadoInternacion
  observaciones?: string
  fecha_egreso?: string
}
