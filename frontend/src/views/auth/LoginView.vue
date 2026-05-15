<!-- src/views/auth/LoginView.vue -->
<template>
  <div class="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="row w-100 justify-content-center">
      <div class="col-12 col-sm-8 col-md-5 col-lg-4">
        <!-- Card principal -->
        <div class="card shadow-sm border-0 rounded-4">
          <div class="card-body p-4">
            <!-- Logo / título -->
            <div class="text-center mb-3">
              <div
                class="rounded-circle d-inline-flex align-items-center justify-content-center mb-2"
                style="width: 52px; height: 52px; background: #e7f5ff;"
              >
                <span style="font-size: 1.8rem">🐾</span>
              </div>
              <h5 class="fw-bold mb-0">VetSystem</h5>
              <p class="text-muted mb-0" style="font-size: 13px">
                Portal para clientes y veterinarios
              </p>
            </div>

            <!-- Mensaje de error -->
            <div v-if="authStore.error" class="alert alert-danger py-2 px-3" style="font-size: 13px">
              {{ authStore.error }}
            </div>

            <!-- Formulario -->
            <form @submit.prevent="alEnviar" novalidate>
              <div class="mb-3">
                <label class="form-label small fw-semibold">Usuario</label>
                <input
                  v-model.trim="form.username"
                  type="text"
                  class="form-control form-control-sm"
                  :class="{ 'is-invalid': enviado && !form.username }"
                  autocomplete="username"
                  placeholder="ej: juan.perez"
                />
                <div v-if="enviado && !form.username" class="invalid-feedback">
                  Ingresá tu usuario.
                </div>
              </div>

              <div class="mb-2">
                <label class="form-label small fw-semibold">Contraseña</label>
                <div class="input-group input-group-sm">
                  <input
                    v-model="form.password"
                    :type="verPassword ? 'text' : 'password'"
                    class="form-control"
                    :class="{ 'is-invalid': enviado && !form.password }"
                    autocomplete="current-password"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="alternarContrasena"
                  >
                    {{ verPassword ? 'Ocultar' : 'Ver' }}
                  </button>
                  <div v-if="enviado && !form.password" class="invalid-feedback">
                    Ingresá tu contraseña.
                  </div>
                </div>
              </div>

              <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="form-check form-check-sm">
                  <input
                    id="recordarme"
                    v-model="recordar"
                    class="form-check-input"
                    type="checkbox"
                    style="transform: scale(0.9)"
                  />
                  <label class="form-check-label small" for="recordarme">
                    Recordarme en este dispositivo
                  </label>
                </div>
                <button
                  type="button"
                  class="btn btn-link btn-sm p-0 small text-decoration-none"
                  @click="alOlvidar"
                >
                  Olvidé mi contraseña
                </button>
              </div>

              <button
                type="submit"
                class="btn btn-success w-100 d-flex justify-content-center align-items-center"
                :disabled="authStore.cargando"
              >
                <span v-if="authStore.cargando" class="spinner-border spinner-border-sm me-2" />
                <span>Ingresar</span>
              </button>
            </form>

            <!-- Separador -->
            <div class="d-flex align-items-center my-3">
              <div class="flex-grow-1 border-bottom"></div>
              <span class="mx-2 text-muted" style="font-size: 11px">o</span>
              <div class="flex-grow-1 border-bottom"></div>
            </div>

            <!-- Tarjetas informativas (mockup-style) -->
            <div class="mb-2">
              <div class="alert alert-info py-2 px-3 mb-2" style="font-size: 12px">
                <strong>Clientes:</strong> podés ver tus mascotas, turnos e internaciones en tiempo real.
              </div>
              <div class="alert alert-secondary py-2 px-3 mb-0" style="font-size: 12px">
                <strong>Veterinarios:</strong> ingresen con su usuario asignado por la clínica.
              </div>
            </div>
          </div>

          <!-- Footer pequeño dentro de la card -->
          <div class="card-footer bg-white border-0 text-center py-3">
            <small class="text-muted d-block" style="font-size: 11px">
              © {{ anioActual }} VetSystem · Clínica Veterinaria
            </small>
          </div>
        </div>

        <!-- Info ambiente (dev only, opcional) -->
        <div class="text-center mt-3" style="font-size: 11px">
          <span class="badge bg-light text-muted">
            Ambiente de pruebas · No usar datos reales de pacientes
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import type { FormularioInicioSesion } from '@/interfaces/usuarioInterface'

const authStore = useAuthStore()

const form = reactive<FormularioInicioSesion>({
  username: '',
  password: '',
})

const enviado = ref(false)
const verPassword = ref(false)
const recordar = ref(true)

const anioActual = computed(() => new Date().getFullYear())

const alternarContrasena = () => {
  verPassword.value = !verPassword.value
}

const alEnviar = async () => {
  enviado.value = true
  if (!form.username || !form.password) return
  // Podés guardar en localStorage si querés persistir usuario
  try {
    await authStore.iniciarSesion(form)
    if (recordar.value && authStore.tokenAcceso) {
      localStorage.setItem('accessToken', authStore.tokenAcceso)
      localStorage.setItem('refreshToken', authStore.tokenRefresco ?? '')
    }
  } catch {
    // el store ya setea el error
  }
}

const alOlvidar = () => {
  // En una versión futura podemos llevar a /recuperar-password
  // Por ahora solo mostramos un alert simple
  window.alert('Contactá con la clínica para restablecer tu contraseña.')
}
</script>