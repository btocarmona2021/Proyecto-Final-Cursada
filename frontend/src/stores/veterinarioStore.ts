// src/stores/veterinarioStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import perfilVeterinarioService from '@/services/perfilVeterinarioService'
import type {
  VeterinarioPerfil,
  VeterinariaPerfilForm,
} from '@/interfaces/veterinarioPerfil.interface'

export const useVeterinarioStore = defineStore('veterinario', () => {
  const veterinarios = ref<VeterinarioPerfil[]>([])
  const veterinarioSeleccionado = ref<VeterinarioPerfil | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      veterinarios.value = await perfilVeterinarioService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener veterinarios'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      veterinarioSeleccionado.value = await perfilVeterinarioService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener el veterinario'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: VeterinariaPerfilForm) => {
    cargando.value = true
    error.value = null
    try {
      const nuevo = await perfilVeterinarioService.crear(data)
      veterinarios.value.push(nuevo)
    } catch {
      error.value = 'Error al crear el veterinario'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: VeterinariaPerfilForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizado = await perfilVeterinarioService.actualizar(id, data)
      const index = veterinarios.value.findIndex((v) => v.id === id)
      if (index !== -1) veterinarios.value[index] = actualizado
    } catch {
      error.value = 'Error al actualizar el veterinario'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await perfilVeterinarioService.eliminar(id)
      veterinarios.value = veterinarios.value.filter((v) => v.id !== id)
    } catch {
      error.value = 'Error al eliminar el veterinario'
    } finally {
      cargando.value = false
    }
  }

  return {
    veterinarios,
    veterinarioSeleccionado,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
