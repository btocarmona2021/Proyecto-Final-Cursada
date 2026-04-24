export interface Especie {
  id: number
  nombre: string
  emoji: string | null
}

export interface EspecieForm {
  nombre: string
  emoji?: string
}
