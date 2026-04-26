// src/stores/veterinariaStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import veterinariaService from '@/services/veterinariaService'
import type { Veterinaria, VeterinariaForm } from '@/interfaces/veterinaria.interface'

export const useVeterinariaStore = defineStore('veterinaria', () => {
  const veterinarias = ref<Veterinaria[]>([])
  const veterinariaSeleccionada = ref<Veterinaria | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      veterinarias.value = await veterinariaService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener veterinarias'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      veterinariaSeleccionada.value = await veterinariaService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la veterinaria'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: VeterinariaForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await veterinariaService.crear(data)
      veterinarias.value.push(nueva)
    } catch {
      error.value = 'Error al crear la veterinaria'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: VeterinariaForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await veterinariaService.actualizar(id, data)
      const index = veterinarias.value.findIndex((v) => v.id === id)
      if (index !== -1) veterinarias.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la veterinaria'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await veterinariaService.eliminar(id)
      veterinarias.value = veterinarias.value.filter((v) => v.id !== id)
    } catch {
      error.value = 'Error al eliminar la veterinaria'
    } finally {
      cargando.value = false
    }
  }

  return {
    veterinarias,
    veterinariaSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
