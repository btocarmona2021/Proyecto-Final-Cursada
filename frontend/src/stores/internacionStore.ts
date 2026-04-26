// src/stores/internacionStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import internacionesService from '@/services/internacionesService'
import type { Internacion, InternacionForm } from '@/interfaces/internacion.interface'

export const useInternacionStore = defineStore('internacion', () => {
  const internaciones = ref<Internacion[]>([])
  const internacionSeleccionada = ref<Internacion | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      internaciones.value = await internacionesService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener internaciones'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      internacionSeleccionada.value = await internacionesService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la internacion'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: InternacionForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await internacionesService.crear(data)
      internaciones.value.push(nueva)
    } catch {
      error.value = 'Error al crear la internacion'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: InternacionForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await internacionesService.actualizar(id, data)
      const index = internaciones.value.findIndex((i) => i.id === id)
      if (index !== -1) internaciones.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la internacion'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await internacionesService.eliminar(id)
      internaciones.value = internaciones.value.filter((i) => i.id !== id)
    } catch {
      error.value = 'Error al eliminar la internacion'
    } finally {
      cargando.value = false
    }
  }

  return {
    internaciones,
    internacionSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
