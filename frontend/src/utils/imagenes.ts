export function urlImagen(ruta?: string | null): string {
  if (!ruta) return ''
  const api = new URL(
    import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
    window.location.origin,
  )
  const url = new URL(ruta, api.origin)
  return ['http:', 'https:'].includes(url.protocol) ? url.href : ''
}
