export interface HorarioVeterinario {
  id: number
  veterinario: number
  nombre_veterinario: string
  dia_semana: 1 | 2 | 3 | 4 | 5 | 6 | 7
  dia_semana_display: string
  hora_inicio: string
  hora_fin: string
}

export interface HorarioVeterinarioForm {
  veterinario: number
  dia_semana: 1 | 2 | 3 | 4 | 5 | 6 | 7
  hora_inicio: string
  hora_fin: string
}
