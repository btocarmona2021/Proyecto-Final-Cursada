export type EstadoTurno =
  | 'reservado'
  | 'confirmado'
  | 'en_espera'
  | 'en_consulta'
  | 'atendido'
  | 'cancelado'

export interface Turno {
  id: number
  fecha_hora: string
  mascota: number
  mascota_nombre: string
  veterinario: number
  veterinario_nombre: string
  servicio: number
  servicio_nombre: string
  estado: EstadoTurno
  estado_display: string
  motivo_consulta: string | null
  notas: string | null
  creado_por_cliente: boolean
}

export interface TurnoForm {
  fecha_hora: string
  mascota: number
  veterinario: number
  servicio: number
  estado?: EstadoTurno
  motivo_consulta?: string
  notas?: string
  creado_por_cliente?: boolean
}
