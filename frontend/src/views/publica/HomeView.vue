<!-- src/views/publica/HomeView.vue -->
<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
      <div class="container">
        <span class="navbar-brand fw-bold">🐾 VetSystem</span>
        <div class="d-flex gap-2">
          <RouterLink to="/login" class="btn btn-outline-light btn-sm">
            Iniciar sesión
          </RouterLink>
          <RouterLink to="/registro" class="btn btn-light btn-sm">
            Registrarse
          </RouterLink>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <div class="bg-success text-white py-5">
      <div class="container text-center">
        <h2 class="fw-bold mb-3">Clínica Veterinaria</h2>
        <p class="mb-0 mx-auto" style="max-width: 520px; font-size: 15px">
          Cuidamos a tus mascotas con amor y profesionalismo. Reservá turnos,
          consultá su historia clínica y mantené al día su salud.
        </p>
      </div>
    </div>

    <!-- Servicios -->
    <div class="container py-5">
      <h4 class="fw-bold text-center mb-1">Nuestros servicios</h4>
      <p class="text-muted text-center mb-4" style="font-size: 14px">
        Todo lo que tu mascota necesita en un solo lugar
      </p>

      <div v-if="cargandoServicios" class="text-center text-muted py-4">
        Cargando servicios...
      </div>

      <div v-else-if="servicios.length === 0" class="text-center text-muted py-4">
        Los servicios se están cargando. Probá recargar la página.
      </div>

      <div v-else class="row g-3">
        <div v-for="s in servicios" :key="s.id" class="col-md-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h6 class="fw-bold">{{ s.nombre }}</h6>
              <p v-if="s.descripcion" class="text-muted mb-2" style="font-size: 13px">
                {{ s.descripcion }}
              </p>
              <div class="d-flex justify-content-between align-items-center">
                <span class="fw-bold text-success">${{ s.precio }}</span>
                <span class="text-muted" style="font-size: 12px">
                  {{ s.duracion_estimada }} min
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sobre la veterinaria -->
    <div class="bg-light py-5">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-8">
            <h4 class="fw-bold text-center mb-3">Sobre nosotros</h4>

            <div v-if="cargandoClinica" class="text-center text-muted py-3">
              Cargando información...
            </div>

            <div v-else-if="clinica">
              <p v-if="clinica.descripcion" class="text-center mb-4">
                {{ clinica.descripcion }}
              </p>

              <div class="row g-3">
                <div class="col-sm-6">
                  <div class="d-flex align-items-start gap-2">
                    <span>📍</span>
                    <div>
                      <div class="fw-semibold small">Dirección</div>
                      <div class="text-muted" style="font-size: 13px">
                        {{ clinica.direccion }}, {{ clinica.ciudad }}, {{ clinica.provincia }}
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="d-flex align-items-start gap-2">
                    <span>📞</span>
                    <div>
                      <div class="fw-semibold small">Teléfono</div>
                      <div class="text-muted" style="font-size: 13px">
                        {{ clinica.telefono ?? 'No disponible' }}
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="d-flex align-items-start gap-2">
                    <span>🕐</span>
                    <div>
                      <div class="fw-semibold small">Horario</div>
                      <div class="text-muted" style="font-size: 13px">
                        {{ clinica.horario_atencion ?? 'Consultar' }}
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="d-flex align-items-start gap-2">
                    <span>✉️</span>
                    <div>
                      <div class="fw-semibold small">Email</div>
                      <div class="text-muted" style="font-size: 13px">
                        {{ clinica.email ?? 'No disponible' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center text-muted py-3">
              Clínica Veterinaria — Cuidando a tus mascotas.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="bg-dark text-white text-center py-3">
      <small>© {{ anioActual }} VetSystem · Clínica Veterinaria</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import serviciosService from '@/services/serviciosService'
import veterinariaService from '@/services/veterinariaService'
import type { Servicio } from '@/interfaces/servicioInterface'
import type { Veterinaria } from '@/interfaces/veterinariaInterface'

const servicios = ref<Servicio[]>([])
const clinica = ref<Veterinaria | null>(null)
const cargandoServicios = ref(false)
const cargandoClinica = ref(false)

const anioActual = computed(() => new Date().getFullYear())

onMounted(async () => {
  cargandoServicios.value = true
  try {
    servicios.value = await serviciosService.obtenerTodos()
  } catch {
    servicios.value = []
  } finally {
    cargandoServicios.value = false
  }

  cargandoClinica.value = true
  try {
    const datos = await veterinariaService.obtenerTodos()
    clinica.value = datos[0] ?? null
  } catch {
    clinica.value = null
  } finally {
    cargandoClinica.value = false
  }
})
</script>
