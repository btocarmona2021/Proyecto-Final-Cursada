// src/stores/recetaStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import recetasService from '@/services/recetasService'
import type { RecetaItem, RecetaItemForm } from '@/interfaces/recetaItem.interface'

export const useRecetaStore = defineStore('receta', () => {
  const recetas = ref<RecetaItem[]>([])
  const recetaSeleccionada = ref<RecetaItem | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      recetas.value = await recetasService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener recetas'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      recetaSeleccionada.value = await recetasService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la receta'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: RecetaItemForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await recetasService.crear(data)
      recetas.value.push(nueva)
    } catch {
      error.value = 'Error al crear la receta'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: RecetaItemForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await recetasService.actualizar(id, data)
      const index = recetas.value.findIndex((r) => r.id === id)
      if (index !== -1) recetas.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la receta'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await recetasService.eliminar(id)
      recetas.value = recetas.value.filter((r) => r.id !== id)
    } catch {
      error.value = 'Error al eliminar la receta'
    } finally {
      cargando.value = false
    }
  }

  return {
    recetas,
    recetaSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
