// src/stores/consultaStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import consultasService from '@/services/consultasService'
import type {
  ConsultaClinica,
  ConsultaClinicaForm,
} from '@/interfaces/consultaClinicaInterface'

export const useConsultaStore = defineStore('consulta', () => {
  // State
  const consultas = ref<ConsultaClinica[]>([])
  const consultaSeleccionada = ref<ConsultaClinica | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  // Actions
  const obtenerTodos = async (): Promise<void> => {
    cargando.value = true
    error.value = null

    try {
      const resp = await consultasService.obtenerTodos()
      consultas.value = resp
    } catch (e) {
      error.value = 'Error al obtener consultas'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number): Promise<void> => {
    cargando.value = true
    error.value = null

    try {
      const resp = await consultasService.obtenerUno(id)
      consultaSeleccionada.value = resp
    } catch (e) {
      error.value = 'Error al obtener la consulta'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: ConsultaClinicaForm): Promise<ConsultaClinica> => {
    cargando.value = true
    error.value = null

    try {
      const nueva = await consultasService.crear(data)
      consultas.value.push(nueva)
      return nueva
    } catch (e) {
      error.value = 'Error al crear la consulta'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (
    id: number,
    data: ConsultaClinicaForm,
  ): Promise<ConsultaClinica> => {
    cargando.value = true
    error.value = null

    try {
      const actualizada = await consultasService.actualizar(id, data)
      const index = consultas.value.findIndex((c) => c.id === id)
      if (index !== -1) {
        consultas.value[index] = actualizada
      }
      if (consultaSeleccionada.value?.id === id) {
        consultaSeleccionada.value = actualizada
      }
      return actualizada
    } catch (e) {
      error.value = 'Error al actualizar la consulta'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number): Promise<void> => {
    cargando.value = true
    error.value = null

    try {
      await consultasService.eliminar(id)
      consultas.value = consultas.value.filter((c) => c.id !== id)
      if (consultaSeleccionada.value?.id === id) {
        consultaSeleccionada.value = null
      }
    } catch (e) {
      error.value = 'Error al eliminar la consulta'
      throw e
    } finally {
      cargando.value = false
    }
  }

  return {
    // state
    consultas,
    consultaSeleccionada,
    cargando,
    error,
    // actions
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})