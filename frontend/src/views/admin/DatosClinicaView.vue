<template>
  <div class="datos-clinica">
    <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap mb-4">
      <div>
        <h1 class="h4 fw-bold mb-1">Datos de la clínica</h1>
        <p class="text-muted mb-0">
          Configurá la información y el contacto que se muestran en la portada.
        </p>
      </div>
      <RouterLink to="/" target="_blank" rel="noopener" class="btn btn-outline-success"
        >Ver portada</RouterLink
      >
    </div>

    <p v-if="cargando" class="text-muted py-4" role="status">Cargando datos de la clínica…</p>
    <div v-else-if="errorCarga" class="alert alert-danger" role="alert">
      <p>{{ errorCarga }}</p>
      <button type="button" class="btn btn-outline-danger" @click="cargar">Reintentar</button>
    </div>

    <form v-else @submit.prevent="guardar">
      <p v-if="idClinica === null" class="alert alert-info">
        Todavía no registraste la clínica. Completá sus datos para publicarlos en la portada.
      </p>
      <div v-if="errorGuardado" id="error-clinica" class="alert alert-danger" role="alert">
        {{ errorGuardado }}
      </div>
      <p v-if="mensaje" class="alert alert-success" role="status">{{ mensaje }}</p>

      <fieldset :disabled="guardando">
        <section class="card border-0 shadow-sm mb-4" aria-labelledby="identidad-clinica">
          <div class="card-body p-4">
            <h2 id="identidad-clinica" class="h6 fw-bold mb-4">Información de la clínica</h2>
            <ImagenSelector
              v-model="form.logo"
              :actual="logoActual"
              etiqueta="Logo de la clínica"
              id="logo-clinica"
            />
            <div class="row g-3">
              <div class="col-md-6">
                <label for="razon-social" class="form-label">Razón social *</label>
                <input
                  id="razon-social"
                  v-model="form.razon_social"
                  class="form-control"
                  maxlength="200"
                  required
                />
              </div>
              <div class="col-md-6">
                <label for="nombre-clinica" class="form-label">Nombre de la clínica</label>
                <input
                  id="nombre-clinica"
                  v-model="form.nombre_fantasia"
                  class="form-control"
                  maxlength="200"
                  aria-describedby="ayuda-nombre"
                />
                <p id="ayuda-nombre" class="form-text mb-0">
                  Es el nombre que aparece en la portada.
                </p>
              </div>
              <div class="col-md-6">
                <label for="cuit-clinica" class="form-label">CUIT *</label>
                <input
                  id="cuit-clinica"
                  v-model="form.cuit"
                  class="form-control"
                  maxlength="13"
                  required
                />
              </div>
              <div class="col-12">
                <label for="descripcion-clinica" class="form-label"
                  >Presentación de la clínica</label
                >
                <textarea
                  id="descripcion-clinica"
                  v-model="form.descripcion"
                  class="form-control"
                  rows="3"
                  aria-describedby="ayuda-descripcion"
                ></textarea>
                <p id="ayuda-descripcion" class="form-text mb-0">
                  Una descripción breve de la atención que brindan.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section class="card border-0 shadow-sm mb-4" aria-labelledby="ubicacion-clinica">
          <div class="card-body p-4">
            <h2 id="ubicacion-clinica" class="h6 fw-bold mb-4">Ubicación</h2>

            <div class="row g-3">
              <div class="col-12">
                <label for="direccion-clinica" class="form-label">Dirección *</label>
                <input
                  id="direccion-clinica"
                  v-model="form.direccion"
                  class="form-control"
                  autocomplete="street-address"
                  maxlength="255"
                  required
                />
              </div>
              <div class="col-md-5">
                <label for="ciudad-clinica" class="form-label">Ciudad *</label>
                <input
                  id="ciudad-clinica"
                  v-model="form.ciudad"
                  class="form-control"
                  autocomplete="address-level2"
                  maxlength="100"
                  required
                />
              </div>
              <div class="col-md-5">
                <label for="provincia-clinica" class="form-label">Provincia *</label>
                <input
                  id="provincia-clinica"
                  v-model="form.provincia"
                  class="form-control"
                  autocomplete="address-level1"
                  maxlength="100"
                  required
                />
              </div>
              <div class="col-md-2">
                <label for="cp-clinica" class="form-label">Código postal</label>
                <input
                  id="cp-clinica"
                  v-model="form.codigo_postal"
                  class="form-control"
                  autocomplete="postal-code"
                  maxlength="10"
                />
              </div>
            </div>
          </div>
        </section>

        <section class="card border-0 shadow-sm mb-4" aria-labelledby="contacto-clinica">
          <div class="card-body p-4">
            <h2 id="contacto-clinica" class="h6 fw-bold mb-4">Contacto y atención</h2>

            <div class="row g-3">
              <div class="col-md-6">
                <label for="telefono-clinica" class="form-label">Teléfono</label>
                <input
                  id="telefono-clinica"
                  v-model="form.telefono"
                  type="tel"
                  class="form-control"
                  autocomplete="tel"
                  maxlength="30"
                />
              </div>
              <div class="col-md-6">
                <label for="email-clinica" class="form-label">Email</label>
                <input
                  id="email-clinica"
                  v-model="form.email"
                  type="email"
                  class="form-control"
                  autocomplete="email"
                  maxlength="254"
                />
              </div>
              <div class="col-12">
                <label for="horario-clinica" class="form-label">Horario de atención</label>
                <textarea
                  id="horario-clinica"
                  v-model="form.horario_atencion"
                  class="form-control"
                  rows="2"
                  maxlength="255"
                  aria-describedby="ayuda-horario"
                ></textarea>
                <p id="ayuda-horario" class="form-text mb-0">
                  Este texto informa a los clientes. Los horarios para reservar turnos se configuran
                  en Veterinarios.
                </p>
              </div>
            </div>
          </div>
        </section>

        <div class="d-flex align-items-center justify-content-between gap-3 flex-wrap pb-4">
          <p class="text-muted small mb-0">Los campos con * son obligatorios.</p>
          <button class="btn btn-success px-4" type="submit">
            {{
              guardando
                ? 'Guardando…'
                : idClinica === null
                  ? 'Guardar datos de la clínica'
                  : 'Guardar cambios'
            }}
          </button>
        </div>
      </fieldset>
    </form>
  </div>
</template>

<script setup lang="ts">
import ImagenSelector from '@/components/ImagenSelector.vue'
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useVeterinariaStore } from '@/stores/veterinariaStore'
import type { VeterinariaForm } from '@/interfaces/veterinariaInterface'

const auth = useAuthStore()
const clinicaStore = useVeterinariaStore()
const cargando = ref(true)
const guardando = ref(false)
const errorCarga = ref('')
const errorGuardado = ref('')
const mensaje = ref('')
const logoActual = ref<string | null>(null)
const idClinica = ref<number | null>(null)
const form = ref<VeterinariaForm>({
  razon_social: '',
  nombre_fantasia: '',
  cuit: '',
  descripcion: '',
  direccion: '',
  ciudad: '',
  provincia: '',
  codigo_postal: '',
  telefono: '',
  email: '',
  horario_atencion: '',
})

async function cargar() {
  cargando.value = true
  errorCarga.value = ''
  try {
    await clinicaStore.obtenerTodos()
    const clinica = clinicaStore.veterinarias[0]
    if (clinica) {
      idClinica.value = clinica.id
      logoActual.value = clinica.logo
      form.value = {
        razon_social: clinica.razon_social,
        nombre_fantasia: clinica.nombre_fantasia ?? '',
        cuit: clinica.cuit,
        descripcion: clinica.descripcion ?? '',
        direccion: clinica.direccion,
        ciudad: clinica.ciudad,
        provincia: clinica.provincia,
        codigo_postal: clinica.codigo_postal ?? '',
        telefono: clinica.telefono ?? '',
        email: clinica.email ?? '',
        horario_atencion: clinica.horario_atencion ?? '',
      }
    }
  } catch {
    errorCarga.value = 'No se pudieron cargar los datos de la clínica. Reintentá antes de guardar.'
  } finally {
    cargando.value = false
  }
}

async function guardar() {
  if (guardando.value || cargando.value || errorCarga.value) return
  errorGuardado.value = ''
  mensaje.value = ''
  if (!auth.esAdmin) {
    errorGuardado.value = 'Solo el administrador puede modificar los datos de la clínica.'
    return
  }
  guardando.value = true
  try {
    if (idClinica.value === null) {
      await clinicaStore.crear({ ...form.value })
      idClinica.value = clinicaStore.veterinarias[0]?.id ?? null
    } else {
      await clinicaStore.actualizar(idClinica.value, { ...form.value })
    }
    logoActual.value = clinicaStore.veterinarias[0]?.logo ?? null
    form.value.logo = null
    document.title =
      form.value.nombre_fantasia?.trim() || form.value.razon_social.trim() || 'VetSystem'
    mensaje.value = 'Datos guardados. Ya podés verlos en la portada.'
  } catch (error: unknown) {
    const datos = (error as { response?: { data?: Record<string, unknown> } })?.response?.data
    errorGuardado.value = datos
      ? Object.entries(datos)
          .map(
            ([campo, valor]) =>
              `${campo === 'non_field_errors' || campo === 'detail' ? '' : campo + ': '}${Array.isArray(valor) ? valor.join(' ') : String(valor)}`,
          )
          .join(' ')
      : 'No se pudieron guardar los datos. Revisá la conexión e intentá nuevamente.'
  } finally {
    guardando.value = false
  }
}

onMounted(cargar)
</script>

<style scoped>
.datos-clinica {
  max-width: 1000px;
}
fieldset {
  min-width: 0;
}
</style>
