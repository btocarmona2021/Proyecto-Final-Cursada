export interface Mascota {
  id: number
  nombre: string
  raza: number
  raza_nombre: string
  especie_nombre: string
  fecha_nacimiento: string | null
  sexo: 'M' | 'H' | null
  color: string | null
  peso_actual: number
  microchip: string | null
  foto: string | null
  usuario: number
  usuario_nombre: string
}

export interface MascotaForm {
  nombre: string
  raza: number
  fecha_nacimiento?: string
  sexo?: 'M' | 'H'
  color?: string
  peso_actual?: number
  microchip?: string
  foto?: File | null
  usuario: number
}
