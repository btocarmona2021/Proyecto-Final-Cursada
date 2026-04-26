// src/stores/evolucionInternacionStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import evolucionInternacionService from '@/services/evolucionInternacionService'
import type {
  EvolucionInternacion,
  EvolucionInternacionForm,
} from '@/interfaces/evolucionInternacion.interface'

export const useEvolucionInternacionStore = defineStore('evolucionInternacion', () => {
  const evoluciones = ref<EvolucionInternacion[]>([])
  const evolucionSeleccionada = ref<EvolucionInternacion | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      evoluciones.value = await evolucionInternacionService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener evoluciones'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      evolucionSeleccionada.value = await evolucionInternacionService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la evolucion'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: EvolucionInternacionForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await evolucionInternacionService.crear(data)
      evoluciones.value.push(nueva)
    } catch {
      error.value = 'Error al crear la evolucion'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: EvolucionInternacionForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await evolucionInternacionService.actualizar(id, data)
      const index = evoluciones.value.findIndex((e) => e.id === id)
      if (index !== -1) evoluciones.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la evolucion'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await evolucionInternacionService.eliminar(id)
      evoluciones.value = evoluciones.value.filter((e) => e.id !== id)
    } catch {
      error.value = 'Error al eliminar la evolucion'
    } finally {
      cargando.value = false
    }
  }

  return {
    evoluciones,
    evolucionSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
