// Las fechas sin hora representan un día del calendario, no un instante UTC.
export function fechaDesdeAPI(iso: string): Date {
  return new Date(/^\d{4}-\d{2}-\d{2}$/.test(iso) ? `${iso}T00:00:00` : iso)
}

export function fechaParaFormulario(fecha = new Date()): string {
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const dia = String(fecha.getDate()).padStart(2, '0')
  return `${fecha.getFullYear()}-${mes}-${dia}`
}

export function diasHastaFecha(iso: string, hoy = new Date()): number {
  const fecha = fechaDesdeAPI(iso)
  // Comparar días de calendario evita diferencias por horas o cambios de horario.
  const destino = Date.UTC(fecha.getFullYear(), fecha.getMonth(), fecha.getDate())
  const origen = Date.UTC(hoy.getFullYear(), hoy.getMonth(), hoy.getDate())
  return (destino - origen) / 86400000
}
