export interface EvolucionInternacion {
  id: number
  internacion: number
  fecha: string
  veterinario: number | null
  veterinario_nombre: string | null
  temperatura: string | null
  peso: string | null
  descripcion: string
  indicaciones: string | null
}

export interface EvolucionInternacionForm {
  internacion: number
  veterinario?: number
  temperatura?: number
  peso?: number
  descripcion: string
  indicaciones?: string
}
