// src/stores/usuarioStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import usuariosService from '@/services/usuariosService'
import type { UsuarioAuth } from '@/interfaces/usuarioInterface'

export const useUsuarioStore = defineStore('usuario', () => {
  const usuarios = ref<UsuarioAuth[]>([])
  const usuarioSeleccionado = ref<UsuarioAuth | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      usuarios.value = await usuariosService.obtenerTodos()
    } catch (e) {
      error.value = 'Error al obtener usuarios'
      throw e
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      usuarioSeleccionado.value = await usuariosService.obtenerUno(id)
    } catch (e) {
      error.value = 'Error al obtener el usuario'
      throw e
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
  }
})
