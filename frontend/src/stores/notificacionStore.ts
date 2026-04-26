// src/stores/notificacionStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import notificacionesService from '@/services/notificacionesService'
import type { Notificacion, NotificacionForm } from '@/interfaces/notificacion.interface'

export const useNotificacionStore = defineStore('notificacion', () => {
  const notificaciones = ref<Notificacion[]>([])
  const notificacionSeleccionada = ref<Notificacion | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  // Getter útil para el badge
  const noLeidas = computed(() => notificaciones.value.filter((n) => !n.leida).length)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      notificaciones.value = await notificacionesService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener notificaciones'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      notificacionSeleccionada.value = await notificacionesService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la notificacion'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: NotificacionForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await notificacionesService.crear(data)
      notificaciones.value.push(nueva)
    } catch {
      error.value = 'Error al crear la notificacion'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: NotificacionForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await notificacionesService.actualizar(id, data)
      const index = notificaciones.value.findIndex((n) => n.id === id)
      if (index !== -1) notificaciones.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la notificacion'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await notificacionesService.eliminar(id)
      notificaciones.value = notificaciones.value.filter((n) => n.id !== id)
    } catch {
      error.value = 'Error al eliminar la notificacion'
    } finally {
      cargando.value = false
    }
  }

  return {
    notificaciones,
    notificacionSeleccionada,
    noLeidas,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
