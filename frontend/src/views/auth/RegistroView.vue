<!-- src/views/auth/RegistroView.vue -->
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
                style="width: 52px; height: 52px; background: #e7f5ff"
              >
                <MarcaClinica :mostrar-nombre="false" :tamano="52" />
              </div>
              <h5 class="fw-bold mb-0">Crear cuenta</h5>
              <p class="text-muted mb-0" style="font-size: 13px">
                Registrate para gestionar las mascotas de tu familia
              </p>
            </div>

            <!-- Mensaje de error -->
            <div
              v-if="authStore.error"
              class="alert alert-danger py-2 px-3"
              style="font-size: 13px"
            >
              {{ authStore.error }}
            </div>

            <!-- Formulario -->
            <form @submit.prevent="alEnviar" novalidate>
              <div class="mb-3">
                <label class="form-label small fw-semibold">Nombre de usuario</label>
                <input
                  v-model.trim="form.username"
                  type="text"
                  class="form-control form-control-sm"
                  :class="{ 'is-invalid': enviado && !form.username }"
                  autocomplete="username"
                  placeholder="ej: juan.perez"
                />
                <div v-if="enviado && !form.username" class="invalid-feedback">
                  Ingresá tu nombre de usuario.
                </div>
              </div>

              <div class="row g-2 mb-3">
                <div class="col-6">
                  <label class="form-label small fw-semibold">Nombre</label>
                  <input
                    v-model.trim="form.first_name"
                    type="text"
                    class="form-control form-control-sm"
                    :class="{ 'is-invalid': enviado && !form.first_name }"
                    autocomplete="given-name"
                    placeholder="Juan"
                  />
                  <div v-if="enviado && !form.first_name" class="invalid-feedback">
                    Nombre requerido.
                  </div>
                </div>
                <div class="col-6">
                  <label class="form-label small fw-semibold">Apellido</label>
                  <input
                    v-model.trim="form.last_name"
                    type="text"
                    class="form-control form-control-sm"
                    :class="{ 'is-invalid': enviado && !form.last_name }"
                    autocomplete="family-name"
                    placeholder="Pérez"
                  />
                  <div v-if="enviado && !form.last_name" class="invalid-feedback">
                    Apellido requerido.
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label small fw-semibold">Correo electrónico</label>
                <input
                  v-model.trim="form.email"
                  type="email"
                  class="form-control form-control-sm"
                  :class="{ 'is-invalid': enviado && !form.email }"
                  autocomplete="email"
                  placeholder="juan@email.com"
                />
                <div v-if="enviado && !form.email" class="invalid-feedback">
                  Ingresá tu correo electrónico.
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label small fw-semibold">Contraseña</label>
                <input
                  v-model="form.password"
                  type="password"
                  class="form-control form-control-sm"
                  :class="{ 'is-invalid': enviado && !form.password }"
                  autocomplete="new-password"
                  placeholder="••••••••"
                />
                <div v-if="enviado && !form.password" class="invalid-feedback">
                  Ingresá una contraseña.
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label small fw-semibold">Teléfono</label>
                <input
                  v-model.trim="form.telefono"
                  type="text"
                  class="form-control form-control-sm"
                  autocomplete="tel"
                  placeholder="Opcional"
                />
              </div>

              <div class="mb-3">
                <label class="form-label small fw-semibold">Dirección</label>
                <input
                  v-model.trim="form.direccion"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="Opcional"
                />
              </div>

              <button type="submit" class="btn btn-success w-100" :disabled="authStore.cargando">
                {{ authStore.cargando ? 'Registrando...' : 'Registrarme' }}
              </button>
            </form>
          </div>

          <div class="card-footer bg-white border-0 text-center py-3">
            <small class="text-muted d-block" style="font-size: 12px">
              ¿Ya tenés cuenta?
              <RouterLink :to="{ name: 'Login' }" class="text-decoration-none">
                Iniciar sesión
              </RouterLink>
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MarcaClinica from '@/components/MarcaClinica.vue'
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import type { RegistroClienteForm } from '@/interfaces/perfilUsuarioInterface'

const authStore = useAuthStore()

const form = reactive<RegistroClienteForm>({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  telefono: '',
  direccion: '',
})

const enviado = ref(false)

const alEnviar = async () => {
  enviado.value = true
  if (!form.username || !form.password || !form.first_name || !form.last_name || !form.email) {
    return
  }
  try {
    await authStore.registrar(form)
  } catch {
    // el store ya setea el error
  }
}
</script>
