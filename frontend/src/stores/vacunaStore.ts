// src/stores/vacunaStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import vacunasService from '@/services/vacunasService'
import type { Vacuna, VacunaForm } from '@/interfaces/vacuna.interface'

export const useVacunaStore = defineStore('vacuna', () => {
  const vacunas = ref<Vacuna[]>([])
  const vacunaSeleccionada = ref<Vacuna | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      vacunas.value = await vacunasService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener vacunas'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      vacunaSeleccionada.value = await vacunasService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la vacuna'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: VacunaForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await vacunasService.crear(data)
      vacunas.value.push(nueva)
    } catch {
      error.value = 'Error al crear la vacuna'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: VacunaForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await vacunasService.actualizar(id, data)
      const index = vacunas.value.findIndex((v) => v.id === id)
      if (index !== -1) vacunas.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la vacuna'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await vacunasService.eliminar(id)
      vacunas.value = vacunas.value.filter((v) => v.id !== id)
    } catch {
      error.value = 'Error al eliminar la vacuna'
    } finally {
      cargando.value = false
    }
  }

  return {
    vacunas,
    vacunaSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
