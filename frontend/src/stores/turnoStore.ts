// src/stores/turnoStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import turnosService from '@/services/turnosService'
import type { Turno, TurnoForm } from '@/interfaces/turno.interface'

export const useTurnoStore = defineStore('turno', () => {
  const turnos = ref<Turno[]>([])
  const turnoSeleccionado = ref<Turno | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      turnos.value = await turnosService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener turnos'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      turnoSeleccionado.value = await turnosService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener el turno'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: TurnoForm) => {
    cargando.value = true
    error.value = null
    try {
      const nuevo = await turnosService.crear(data)
      turnos.value.push(nuevo)
    } catch {
      error.value = 'Error al crear el turno'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: TurnoForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizado = await turnosService.actualizar(id, data)
      const index = turnos.value.findIndex((t) => t.id === id)
      if (index !== -1) turnos.value[index] = actualizado
    } catch {
      error.value = 'Error al actualizar el turno'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await turnosService.eliminar(id)
      turnos.value = turnos.value.filter((t) => t.id !== id)
    } catch {
      error.value = 'Error al eliminar el turno'
    } finally {
      cargando.value = false
    }
  }

  return {
    turnos,
    turnoSeleccionado,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
