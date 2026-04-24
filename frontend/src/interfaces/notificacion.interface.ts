export type TipoNotificacion = 'turno' | 'vacuna' | 'internacion' | 'sistema'

export interface Notificacion {
  id: number
  usuario: number
  usuario_nombre: string
  tipo: TipoNotificacion
  titulo: string
  mensaje: string
  leida: boolean
  fecha_lectura: string | null
  fecha_creacion: string
}

export interface NotificacionForm {
  usuario: number
  tipo: TipoNotificacion
  titulo: string
  mensaje: string
  leida?: boolean
}
