// src/stores/consultaStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import consultasService from '@/services/consultasService'
import type { ConsultaClinica, ConsultaClinicaForm } from '@/interfaces/consulta.interface'

export const useConsultaStore = defineStore('consulta', () => {
  const consultas = ref<ConsultaClinica[]>([])
  const consultaSeleccionada = ref<ConsultaClinica | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      consultas.value = await consultasService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener consultas'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      consultaSeleccionada.value = await consultasService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la consulta'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: ConsultaClinicaForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await consultasService.crear(data)
      consultas.value.push(nueva)
    } catch {
      error.value = 'Error al crear la consulta'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: ConsultaClinicaForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await consultasService.actualizar(id, data)
      const index = consultas.value.findIndex((c) => c.id === id)
      if (index !== -1) consultas.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la consulta'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await consultasService.eliminar(id)
      consultas.value = consultas.value.filter((c) => c.id !== id)
    } catch {
      error.value = 'Error al eliminar la consulta'
    } finally {
      cargando.value = false
    }
  }

  return {
    consultas,
    consultaSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
