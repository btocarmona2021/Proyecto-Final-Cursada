export interface Veterinaria {
  id: number
  razon_social: string
  nombre_fantasia: string | null
  cuit: string
  direccion: string
  ciudad: string
  provincia: string
  codigo_postal: string | null
  telefono: string | null
  email: string | null
  sitio_web: string | null
  logo: string | null
  descripcion: string | null
  horario_atencion: string | null
  instagram: string | null
  facebook: string | null
}

export interface VeterinariaForm {
  razon_social: string
  nombre_fantasia?: string
  cuit: string
  direccion: string
  ciudad: string
  provincia: string
  codigo_postal?: string
  telefono?: string
  email?: string
  sitio_web?: string
  logo?: File | null
  descripcion?: string
  horario_atencion?: string
  instagram?: string
  facebook?: string
}

