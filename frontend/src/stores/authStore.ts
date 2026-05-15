// // src/stores/authStore.ts
// import { defineStore } from 'pinia'
// import { ref, computed } from 'vue'
// import { useRouter } from 'vue-router'
// import authService from '@/services/authService'
// import type { LoginCredentials } from '@/interfaces/authInterface'
// import type { RegistroUsuarioForm } from '@/interfaces/usuarioInterface'

// export const useAuthStore = defineStore('auth', () => {
//   const router = useRouter()

//   const accessToken = ref<string | null>(null)
//   const refreshToken = ref<string | null>(null)
//   const grupo = ref<string | null>(null)
//   const cargando = ref(false)
//   const error = ref<string | null>(null)

//   const estaAutenticado = computed(() => !!accessToken.value)
//   const esAdmin = computed(() => grupo.value === 'administradores')
//   const esVeterinario = computed(() => grupo.value === 'veterinarios')
//   const esCliente = computed(() => grupo.value === 'clientes')

//   const redirectByGrupo = (): string => {
//     if (esCliente.value) return '/cliente/inicio'
//     if (esVeterinario.value) return '/admin/agenda'
//     return '/admin/dashboard'
//   }

//   const login = async (credentials: LoginCredentials) => {
//     cargando.value = true
//     error.value = null
//     try {
//       const tokens = await authService.login(credentials)
//       accessToken.value = tokens.access
//       refreshToken.value = tokens.refresh
//       grupo.value = tokens.grupo
//       router.push(redirectByGrupo())
//     } catch (e: any) {
//       error.value = 'Usuario o contraseña incorrectos'
//       throw e
//     } finally {
//       cargando.value = false
//     }
//   }

//   const registrar = async (data: RegistroUsuarioForm) => {
//     cargando.value = true
//     error.value = null
//     try {
//       await authService.registrar(data)
//       router.push('/login')
//     } catch (e: any) {
//       error.value = 'Error al registrar el usuario'
//       throw e
//     } finally {
//       cargando.value = false
//     }
//   }

//   const refresh = async (): Promise<void> => {
//     if (!refreshToken.value) throw new Error('No refresh token')
//     const tokens = await authService.refreshToken(refreshToken.value)
//     accessToken.value = tokens.access
//   }

//   const logout = () => {
//     accessToken.value = null
//     refreshToken.value = null
//     grupo.value = null
//     error.value = null
//     router.push('/login')
//   }

//   return {
//     accessToken,
//     refreshToken,
//     grupo,
//     cargando,
//     error,
//     estaAutenticado,
//     esAdmin,
//     esVeterinario,
//     esCliente,
//     redirectByGrupo,
//     login,
//     registrar,
//     refresh,
//     logout,
//   }
// })
// src/stores/authStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/authService';
import type { LoginForm } from '@/interfaces/usuarioInterface';
import type { RegistroClienteForm } from '@/interfaces/perfilUsuarioInterface';
import type { TokenResponse } from '@/interfaces/usuarioInterface';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();

  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const grupo = ref<string | null>(null);
  const cargando = ref(false);
  const error = ref<string | null>(null);

  const estaAutenticado = computed(() => !!accessToken.value);

  // ─────────────────────────────────────────────
  // ROLES (incluye superadmin como admin)
  // ─────────────────────────────────────────────
  const esAdmin = computed(() => {
    const g = grupo.value ?? '';
    return g === 'administradores' || g === 'superadmin';
  });

  const esVeterinario = computed(() => grupo.value === 'veterinarios');
  const esCliente = computed(() => grupo.value === 'clientes');

  const redirectByGrupo = (): string => {
    if (esCliente.value) return '/cliente/inicio';
    if (esVeterinario.value || esAdmin.value) return '/admin/agenda';
    return '/admin/dashboard';
  };

  // ─────────────────────────────────────────────
  // AUTH
  // ─────────────────────────────────────────────
  const login = async (credentials: LoginForm) => {
    cargando.value = true;
    error.value = null;
    try {
      // TokenResponse original SOLO tiene access y refresh. [file:7]
      const tokens: TokenResponse = await authService.login(credentials);

      accessToken.value = tokens.access;
      refreshToken.value = tokens.refresh;

      // Como el tipo TokenResponse no tiene `grupo`, lo tomamos del backend
      // con un cast explícito, para no romper el tipado global.
      const maybeWithGroup = tokens as TokenResponse & { grupo?: string | null };
      grupo.value = maybeWithGroup.grupo ?? null;

      router.push(redirectByGrupo());
    } catch (e: unknown) {
      error.value = 'Usuario o contraseña incorrectos';
      throw e;
    } finally {
      cargando.value = false;
    }
  };

  // En tu proyecto el registro de usuarios usa RegistroClienteForm
  // (username, password, firstname, lastname, email, etc.). [file:7][file:3]
  const registrar = async (data: RegistroClienteForm) => {
    cargando.value = true;
    error.value = null;
    try {
      await authService.registrar(data);
      router.push('/login');
    } catch (e: unknown) {
      error.value = 'Error al registrar el usuario';
      throw e;
    } finally {
      cargando.value = false;
    }
  };

  const refresh = async (): Promise<void> => {
    if (!refreshToken.value) throw new Error('No refresh token');
    const tokens = await authService.refreshToken(refreshToken.value);
    accessToken.value = tokens.access;
  };

  const logout = () => {
    accessToken.value = null;
    refreshToken.value = null;
    grupo.value = null;
    error.value = null;
    router.push('/login');
  };

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
  };
});