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

  const tokenAcceso = ref<string | null>(localStorage.getItem('accessToken'));
  const tokenRefresco = ref<string | null>(localStorage.getItem('refreshToken'));
  const grupo = ref<string | null>(localStorage.getItem('grupo'));
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
  const iniciarSesion = async (credenciales: FormularioInicioSesion) => {
    cargando.value = true;
    error.value = null;
    try {
      const tokens: RespuestaToken = await authService.login(credenciales);

      tokenAcceso.value = tokens.access;
      tokenRefresco.value = tokens.refresh;

      grupo.value = tokens.grupo ?? null;

      localStorage.setItem('accessToken', tokens.access);
      localStorage.setItem('refreshToken', tokens.refresh);
      localStorage.setItem('grupo', grupo.value ?? '');

      router.push(redireccionPorGrupo());
    } catch (e: unknown) {
      const errorHttp = e as { response?: { status?: number } };
      error.value =
        errorHttp.response?.status === 429
          ? 'Demasiados intentos. Esperá un momento y volvé a intentar.'
          : 'Usuario o contraseña incorrectos';
      throw e;
    } finally {
      cargando.value = false;
    }
  };

  // En el registro se usa RegistroClienteForm (username, password, nombres, email, etc.)
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
    tokenAcceso.value = tokens.access;
    tokenRefresco.value = tokens.refresh;
    localStorage.setItem('accessToken', tokens.access);
    localStorage.setItem('refreshToken', tokens.refresh);
  };

  const cerrarSesion = () => {
    const refresh = tokenRefresco.value;
    if (refresh) {
      authService.logout(refresh).catch(() => {});
    }
    tokenAcceso.value = null;
    tokenRefresco.value = null;
    grupo.value = null;
    error.value = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('grupo');
    router.replace('/');
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