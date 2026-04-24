export interface RecetaItem {
  id: number
  consulta: number
  medicamento: string
  dosis: string
  frecuencia: string | null
  dias: number | null
  indicaciones: string | null
}

export interface RecetaItemForm {
  consulta: number
  medicamento: string
  dosis: string
  frecuencia?: string
  dias?: number
  indicaciones?: string
}
