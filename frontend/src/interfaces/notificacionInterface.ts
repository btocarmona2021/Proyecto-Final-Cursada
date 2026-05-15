export type TipoNotificacion = 'turno' | 'vacuna' | 'internacion' | 'sistema'

export interface Notificacion {
  id: number
  usuario: number
  tipo: TipoNotificacion
  titulo: string
  mensaje: string
  leida: boolean
  fecha_lectura: string | null
  created_at: string
  updated_at: string
}

export interface NotificacionForm {
  usuario: number
  tipo: TipoNotificacion
  titulo: string
  mensaje: string
  leida?: boolean
}