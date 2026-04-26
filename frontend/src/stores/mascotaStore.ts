// src/stores/mascotaStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import mascotasService from '@/services/mascotasService'
import type { Mascota, MascotaForm } from '@/interfaces/mascota.interface'

export const useMascotaStore = defineStore('mascota', () => {
  const mascotas = ref<Mascota[]>([])
  const mascotaSeleccionada = ref<Mascota | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  const obtenerTodos = async () => {
    cargando.value = true
    error.value = null
    try {
      mascotas.value = await mascotasService.obtenerTodos()
    } catch {
      error.value = 'Error al obtener mascotas'
    } finally {
      cargando.value = false
    }
  }

  const obtenerUno = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      mascotaSeleccionada.value = await mascotasService.obtenerUno(id)
    } catch {
      error.value = 'Error al obtener la mascota'
    } finally {
      cargando.value = false
    }
  }

  const crear = async (data: MascotaForm) => {
    cargando.value = true
    error.value = null
    try {
      const nueva = await mascotasService.crear(data)
      mascotas.value.push(nueva)
    } catch {
      error.value = 'Error al crear la mascota'
    } finally {
      cargando.value = false
    }
  }

  const actualizar = async (id: number, data: MascotaForm) => {
    cargando.value = true
    error.value = null
    try {
      const actualizada = await mascotasService.actualizar(id, data)
      const index = mascotas.value.findIndex((m) => m.id === id)
      if (index !== -1) mascotas.value[index] = actualizada
    } catch {
      error.value = 'Error al actualizar la mascota'
    } finally {
      cargando.value = false
    }
  }

  const eliminar = async (id: number) => {
    cargando.value = true
    error.value = null
    try {
      await mascotasService.eliminar(id)
      mascotas.value = mascotas.value.filter((m) => m.id !== id)
    } catch {
      error.value = 'Error al eliminar la mascota'
    } finally {
      cargando.value = false
    }
  }

  return {
    mascotas,
    mascotaSeleccionada,
    cargando,
    error,
    obtenerTodos,
    obtenerUno,
    crear,
    actualizar,
    eliminar,
  }
})
