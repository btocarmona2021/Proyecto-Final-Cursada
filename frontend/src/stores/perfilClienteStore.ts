// src/stores/perfilClienteStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import perfilClienteService from '@/services/perfilClienteService'
import type { PerfilUsuario, PerfilUsuarioForm } from '@/interfaces/usuario.interface'

export const usePerfilClienteStore = defineStore('perfilCliente', () => {
  const perfiles = ref<PerfilUsuario[]>([])
  const perfilSeleccionado = ref<PerfilUsuario | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      perfiles.value = await perfilClienteService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener perfiles'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      perfilSeleccionado.value = await perfilClienteService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener el perfil'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: PerfilUsuarioForm) => {
    cargando.value = true
    error.value = null
    try {
      const nuevo = await perfilClienteService.crear(data)
      perfiles.value.push(nuevo)
    } catch {
      error.value = 'Error al crear el perfil'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: PerfilUsuarioForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizado = await perfilClienteService.actualizar(id, data)
      const index = perfiles.value.findIndex((p) => p.id === id)
      if (index !== -1) perfiles.value[index] = actualizado
    } catch {
      error.value = 'Error al actualizar el perfil'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await perfilClienteService.eliminar(id)
      perfiles.value = perfiles.value.filter((p) => p.id !== id)
    } catch {
      error.value = 'Error al eliminar el perfil'
    } finally {
      cargando.value = false
    }
  }

  return {
    perfiles,
    perfilSeleccionado,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
