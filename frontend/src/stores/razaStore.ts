// src/stores/razaStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import razasService from '@/services/razasService'
import type { Raza, RazaForm } from '@/interfaces/raza.interface'

export const useRazaStore = defineStore('raza', () => {
  const razas = ref<Raza[]>([])
  const razaSeleccionada = ref<Raza | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      razas.value = await razasService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener razas'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      razaSeleccionada.value = await razasService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la raza'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: RazaForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await razasService.crear(data)
      razas.value.push(nueva)
    } catch {
      error.value = 'Error al crear la raza'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: RazaForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await razasService.actualizar(id, data)
      const index = razas.value.findIndex((r) => r.id === id)
      if (index !== -1) razas.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la raza'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await razasService.eliminar(id)
      razas.value = razas.value.filter((r) => r.id !== id)
    } catch {
      error.value = 'Error al eliminar la raza'
    } finally {
      cargando.value = false
    }
  }

  return {
    razas,
    razaSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
