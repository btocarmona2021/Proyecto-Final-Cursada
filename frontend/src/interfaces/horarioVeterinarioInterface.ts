export type DiaSemana = 1 | 2 | 3 | 4 | 5 | 6 | 7

export interface HorarioVeterinario {
  id: number
  veterinario_id: number
  dia_semana: DiaSemana
  dia_semana_display: string
  hora_inicio: string
  hora_fin: string
  created_at: string
  updated_at: string
  activo: boolean
}

export interface HorarioVeterinarioForm {
  veterinario_id: number
  dia_semana: DiaSemana
  hora_inicio: string
  hora_fin: string
}