// src/interfaces/especieInterface.ts

export interface Especie {
  id: number
  nombre: string
  emoji: string | null
  created_at: string
  updated_at: string
  activo: boolean
}

export interface EspecieForm {
  nombre: string
  emoji?: string
  activo?: boolean
}