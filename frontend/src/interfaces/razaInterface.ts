// interfaces/razaInterface.ts
import type { Especie } from './especieInterface'

export interface Raza {
  id: number
  especie: Especie | null
  especie_id: number
  nombre: string
  created_at: string
  updated_at: string
  activo: boolean
}

export interface RazaForm {
  nombre: string
  especie_id: number  // ← Cambiar de especieId a especie_id
  activo?: boolean
}