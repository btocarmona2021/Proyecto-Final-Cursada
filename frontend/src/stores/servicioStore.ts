// src/stores/servicioStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import serviciosService from '@/services/serviciosService'
import type { Servicio, ServicioForm } from '@/interfaces/servicioInterface'

export const useServicioStore = defineStore('servicio', () => {
  const servicios = ref<Servicio[]>([])
  const servicioSeleccionado = ref<Servicio | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      servicios.value = await serviciosService.obtenerTodos()
    } catch (e) {
      error.value = 'Error al obtener servicios'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      servicioSeleccionado.value = await serviciosService.obtenerUno(id)
    } catch (e) {
      error.value = 'Error al obtener el servicio'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: ServicioForm) => {
    cargando.value = true
    error.value = null
    try {
      const nuevo = await serviciosService.crear(data)
      servicios.value.push(nuevo)
    } catch (e) {
      error.value = 'Error al crear el servicio'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: ServicioForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizado = await serviciosService.actualizar(id, data)
      const index = servicios.value.findIndex((s) => s.id === id)
      if (index !== -1) {
        servicios.value[index] = actualizado
      }
    } catch (e) {
      error.value = 'Error al actualizar el servicio'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await serviciosService.eliminar(id)
      servicios.value = servicios.value.filter((s) => s.id !== id)
    } catch (e) {
      error.value = 'Error al eliminar el servicio'
      throw e
    } finally {
      cargando.value = false
    }
  }

  return {
    servicios,
    servicioSeleccionado,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
