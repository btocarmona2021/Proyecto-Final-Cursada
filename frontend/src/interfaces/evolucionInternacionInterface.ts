export interface EvolucionInternacion {
  id: number
  internacion: number
  internacion_info: {
    id: number
    mascota_nombre: string
    mascota_id: number
    motivo: string
    estado: string
  } | null
  veterinario: number | null
  veterinario_nombre: string | null
  fecha: string
  temperatura: string | null
  peso: string | null
  descripcion: string
  indicaciones: string | null
  created_at: string
  updated_at: string
  activo: boolean
}

export interface EvolucionInternacionForm {
  internacion: number
  veterinario?: number
  temperatura?: number
  peso?: number
  descripcion: string
  indicaciones?: string
}