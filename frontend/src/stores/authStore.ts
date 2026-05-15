
// src/stores/authStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/authService';
import type { FormularioInicioSesion } from '@/interfaces/usuarioInterface';
import type { RegistroClienteForm } from '@/interfaces/perfilUsuarioInterface';
import type { RespuestaToken } from '@/interfaces/usuarioInterface';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();

  const tokenAcceso = ref<string | null>(null);
  const tokenRefresco = ref<string | null>(null);
  const grupo = ref<string | null>(null);
  const cargando = ref(false);
  const error = ref<string | null>(null);

  const estaAutenticado = computed(() => !!tokenAcceso.value);

  // ─────────────────────────────────────────────
  // ROLES (incluye superadmin como admin)
  // ─────────────────────────────────────────────
  const esAdmin = computed(() => {
    const g = grupo.value ?? '';
    return g === 'administradores' || g === 'superadmin';
  });

  const esVeterinario = computed(() => grupo.value === 'veterinarios');
  const esCliente = computed(() => grupo.value === 'clientes');

  const redireccionPorGrupo = (): string => {
    if (esCliente.value) return '/cliente/inicio';
    if (esVeterinario.value || esAdmin.value) return '/admin/agenda';
    return '/admin/dashboard';
  };

  // ─────────────────────────────────────────────
  // AUTH
  // ─────────────────────────────────────────────
  const iniciarSesion = async (credentials: FormularioInicioSesion) => {
    cargando.value = true;
    error.value = null;
    try {
      const tokens: RespuestaToken = await authService.login(credentials);

      tokenAcceso.value = tokens.acceso;
      tokenRefresco.value = tokens.refresco;

      // Como el tipo RespuestaToken no tiene `grupo`, lo tomamos del backend
      // con un cast explícito, para no romper el tipado global.
      const maybeWithGroup = tokens as RespuestaToken & { grupo?: string | null };
      grupo.value = maybeWithGroup.grupo ?? null;

      router.push(redireccionPorGrupo());
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

  const refrescarToken = async (): Promise<void> => {
    if (!tokenRefresco.value) throw new Error('No refresh token');
    const tokens = await authService.refreshToken(tokenRefresco.value);
    tokenAcceso.value = tokens.acceso;
  };

  const cerrarSesion = () => {
    tokenAcceso.value = null;
    tokenRefresco.value = null;
    grupo.value = null;
    error.value = null;
    router.push('/login');
  };

  return {
    tokenAcceso,
    tokenRefresco,
    grupo,
    cargando,
    error,
    estaAutenticado,
    esAdmin,
    esVeterinario,
    esCliente,
    redireccionPorGrupo,
    iniciarSesion,
    registrar,
    refrescarToken,
    cerrarSesion,
  };
});