// src/stores/horarioVeterinarioStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import horarioVeterinarioService from '@/services/horarioVeterinarioService'
import type {
  HorarioVeterinario,
  HorarioVeterinarioForm,
} from '@/interfaces/horarioVeterinario.interface'

export const useHorarioVeterinarioStore = defineStore('horarioVeterinario', () => {
  const horarios = ref<HorarioVeterinario[]>([])
  const horarioSeleccionado = ref<HorarioVeterinario | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      horarios.value = await horarioVeterinarioService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener horarios'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      horarioSeleccionado.value = await horarioVeterinarioService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener el horario'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: HorarioVeterinarioForm) => {
    cargando.value = true
    error.value = null
    try {
      const nuevo = await horarioVeterinarioService.crear(data)
      horarios.value.push(nuevo)
    } catch {
      error.value = 'Error al crear el horario'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: HorarioVeterinarioForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizado = await horarioVeterinarioService.actualizar(id, data)
      const index = horarios.value.findIndex((h) => h.id === id)
      if (index !== -1) horarios.value[index] = actualizado
    } catch {
      error.value = 'Error al actualizar el horario'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await horarioVeterinarioService.eliminar(id)
      horarios.value = horarios.value.filter((h) => h.id !== id)
    } catch {
      error.value = 'Error al eliminar el horario'
    } finally {
      cargando.value = false
    }
  }

  return {
    horarios,
    horarioSeleccionado,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
