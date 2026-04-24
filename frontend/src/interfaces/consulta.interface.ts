import type { RecetaItem } from './recetaItem.interface'

export type TipoConsulta =
  | 'control'
  | 'vacunacion'
  | 'cirugia'
  | 'urgencia'
  | 'post_operatorio'
  | 'desparasitacion'
  | 'otro'

export interface ConsultaClinica {
  id: number
  mascota: number
  mascota_nombre: string
  veterinario: number | null
  veterinario_nombre: string | null
  turno: number | null
  fecha: string
  tipo: TipoConsulta
  tipo_display: string
  motivo_consulta: string | null
  diagnostico: string | null
  tratamiento: string | null
  observaciones: string | null
  peso_actual: string | null
  temperatura: string | null
  frecuencia_cardiaca: number | null
  frecuencia_respiratoria: number | null
  proxima_visita: string | null
  recetas: RecetaItem[]
}

export interface ConsultaClinicaForm {
  mascota: number
  turno?: number
  veterinario?: number
  tipo?: TipoConsulta
  motivo_consulta?: string
  diagnostico?: string
  tratamiento?: string
  observaciones?: string
  peso_actual?: number
  temperatura?: number
  frecuencia_cardiaca?: number
  frecuencia_respiratoria?: number
  proxima_visita?: string
}
