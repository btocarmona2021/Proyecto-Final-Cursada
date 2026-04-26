// src/stores/especieStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import especiesService from '@/services/especiesService'
import type { Especie, EspecieForm } from '@/interfaces/especie.interface'

export const useEspecieStore = defineStore('especie', () => {
  const especies = ref<Especie[]>([])
  const especieSeleccionada = ref<Especie | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      especies.value = await especiesService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener especies'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      especieSeleccionada.value = await especiesService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la especie'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: EspecieForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await especiesService.crear(data)
      especies.value.push(nueva)
    } catch {
      error.value = 'Error al crear la especie'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: EspecieForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await especiesService.actualizar(id, data)
      const index = especies.value.findIndex(e => e.id === id)
      if (index !== -1) especies.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la especie'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await especiesService.eliminar(id)
      especies.value = especies.value.filter(e => e.id !== id)
    } catch {
      error.value = 'Error al eliminar la especie'
    } finally {
      cargando.value = false
    }
  }

  return { especies, especieSeleccionada, cargando, error, obtenerTodos, obtenerUno, crear, actualizar, eliminar }
})
