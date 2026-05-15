export type EstadoTurno = 
  | 'reservado' 
  | 'confirmado' 
  | 'en_espera' 
  | 'en_consulta' 
  | 'atendido' 
  | 'cancelado'

// Turno con toda la info necesaria para mostrar en el frontend
export interface Turno {
  id: number
  fecha_hora: string
  mascota_id: number
  mascota_nombre: string
  veterinario_id: number
  veterinario_nombre: string | null
  servicio_id: number
  servicio_nombre: string
  estado: EstadoTurno
  estado_display: string
  motivo_consulta: string | null
  notas: string | null
  creado_por_cliente: boolean
  dueno_nombre: string | null
  hora_fin: string | null  // ← NUEVO
  created_at: string
  updated_at: string
  activo: boolean
}

// Formulario para crear/editar turnos
export interface TurnoForm {
  fecha_hora: string
  mascota: number
  veterinario: number
  servicio: number
  estado?: EstadoTurno
  motivo_consulta?: string
  notas?: string
  urgencia: boolean
  creado_por_cliente?: boolean
}
