// src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'
import type { LoginCredentials } from '@/interfaces/auth.interface'
import type { RegistroUsuarioForm } from '@/interfaces/usuario.interface'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()

  // Estado
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const grupo = ref<string | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const estaAutenticado = computed(() => !!accessToken.value)
  const esAdmin = computed(() => grupo.value === 'administradores')
  const esVeterinario = computed(() => grupo.value === 'veterinarios')
  const esCliente = computed(() => grupo.value === 'clientes')

  // Redirige según el grupo del usuario
  const redirectByGrupo = (): string => {
    if (esCliente.value) return '/cliente/inicio'
    if (esVeterinario.value) return '/admin/agenda'
    return '/admin/dashboard'
  }

  // Actions
  const login = async (credentials: LoginCredentials) => {
    cargando.value = true
    error.value = null
    try {
      const tokens = await authService.login(credentials)
      accessToken.value = tokens.access
      refreshToken.value = tokens.refresh
      grupo.value = tokens.grupo
      router.push(redirectByGrupo()) // ← redirige según grupo
    } catch (e: any) {
      error.value = 'Usuario o contraseña incorrectos'
    } finally {
      cargando.value = false
    }
  }

  const registrar = async (data: RegistroUsuarioForm) => {
    cargando.value = true
    error.value = null
    try {
      await authService.registrar(data)
      router.push('/login')
    } catch (e: any) {
      error.value = 'Error al registrar el usuario'
    } finally {
      cargando.value = false
    }
  }

  const refresh = async (): Promise<void> => {
    if (!refreshToken.value) throw new Error('No refresh token')
    const tokens = await authService.refreshToken(refreshToken.value)
    accessToken.value = tokens.access
  }

  const logout = () => {
    accessToken.value = null
    refreshToken.value = null
    grupo.value = null
    error.value = null
    router.push('/login')
  }

  return {
    accessToken,
    refreshToken,
    grupo,
    cargando,
    error,
    estaAutenticado,
    esAdmin,
    esVeterinario,
    esCliente,
    redirectByGrupo,
    login,
    registrar,
    refresh,
    logout,
  }
})
