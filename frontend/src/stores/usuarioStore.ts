// src/stores/usuarioStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import usuariosService from '@/services/usuariosService'
import type { Usuario } from '@/interfaces/usuario.interface'
import type { RegistroUsuarioForm } from '@/interfaces/usuario.interface'

export const useUsuarioStore = defineStore('usuario', () => {
  const usuarios = ref<Usuario[]>([])
  const usuarioSeleccionado = ref<Usuario | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      usuarios.value = await usuariosService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener usuarios'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      usuarioSeleccionado.value = await usuariosService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener el usuario'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: RegistroUsuarioForm) => {
    cargando.value = true
    error.value = null
    try {
      const nuevo = await usuariosService.crear(data)
      usuarios.value.push(nuevo)
    } catch {
      error.value = 'Error al crear el usuario'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: Partial<RegistroUsuarioForm>) => {
    cargando.value = true
    error.value = null
    try {
      const actualizado = await usuariosService.actualizar(id, data)
      const index = usuarios.value.findIndex((u) => u.id === id)
      if (index !== -1) usuarios.value[index] = actualizado
    } catch {
      error.value = 'Error al actualizar el usuario'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await usuariosService.eliminar(id)
      usuarios.value = usuarios.value.filter((u) => u.id !== id)
    } catch {
      error.value = 'Error al eliminar el usuario'
    } finally {
      cargando.value = false
    }
  }

  return {
    usuarios,
    usuarioSeleccionado,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
