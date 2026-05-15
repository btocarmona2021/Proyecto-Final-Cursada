<!-- src/views/cliente/InternacionView.vue -->
<template>
  <div class="container-fluid">
    <!-- Breadcrumb simple -->
    <div class="mb-2">
      <RouterLink
        :to="{ name: 'ClienteInicio' }"
        class="small text-decoration-none text-muted"
      >
        ← Volver al inicio
      </RouterLink>
    </div>

    <!-- Estado de carga -->
    <div
      v-if="cargando"
      class="text-center text-muted py-4"
      style="font-size: 13px"
    >
      Cargando información de internación...
    </div>

    <!-- No encontrada -->
    <div
      v-else-if="!internacion"
      class="alert alert-secondary"
      style="font-size: 13px"
    >
      No se encontró ninguna internación activa para tus mascotas.
    </div>

    <!-- Detalle internación -->
    <div v-else>
      <!-- Header -->
      <div class="card border-0 shadow-sm mb-3">
        <div class="card-body d-flex align-items-center gap-3">
          <div
            class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
            style="width: 56px; height: 56px; background: #fde2e4"
          >
            <span style="font-size: 2rem">🏥</span>
          </div>
          <div class="flex-grow-1">
            <h4 class="fw-bold mb-1">
              Internación de {{ internacion.mascota_nombre }}
            </h4>
            <div class="text-muted" style="font-size: 13px">
              Estado:
              <span
                class="badge"
                :class="insigniaInternacion(internacion.estado)"
                style="font-size: 11px"
              >
                {{ internacion.estado_display }}
              </span>
            </div>
            <div class="text-muted" style="font-size: 12px">
              Veterinario responsable:
              <strong>{{ internacion.veterinario_nombre ?? 'A asignar' }}</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Fechas y motivo -->
      <div class="row g-3 mb-3">
        <div class="col-12 col-md-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-2">Fechas</h6>
              <ul class="list-unstyled mb-0" style="font-size: 13px">
                <li class="d-flex justify-content-between mb-1">
                  <span>Ingreso</span>
                  <strong>{{ formatearFecha(internacion.fecha_ingreso) }}</strong>
                </li>
                <li class="d-flex justify-content-between mb-1">
                  <span>Egreso</span>
                  <strong>
                    {{
                      internacion.fecha_egreso
                        ? formatearFecha(internacion.fecha_egreso)
                        : 'Aún internado'
                    }}
                  </strong>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Motivo y diagnóstico -->
        <div class="col-12 col-md-8">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-2">Motivo y diagnóstico</h6>
              <p class="mb-1" style="font-size: 13px">
                <strong>Motivo de internación:</strong>
              </p>
              <p class="text-muted" style="font-size: 13px">
                {{ internacion.motivo || 'Sin detalle cargado.' }}
              </p>

              <p class="mb-1" style="font-size: 13px">
                <strong>Diagnóstico inicial:</strong>
              </p>
              <p class="text-muted mb-0" style="font-size: 13px">
                {{ internacion.diagnostico_ingreso || 'Sin diagnóstico registrado aún.' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Observaciones simples -->
      <div
        v-if="internacion.observaciones"
        class="card border-0 shadow-sm mb-3"
      >
        <div class="card-body">
          <h6 class="fw-bold mb-2">Observaciones</h6>
          <p class="text-muted mb-0" style="font-size: 13px">
            {{ internacion.observaciones }}
          </p>
        </div>
      </div>

      <!-- Evoluciones (placeholder simple) -->
      <div class="card border-0 shadow-sm mb-3">
        <div class="card-body">
          <h6 class="fw-bold mb-2">Evolución durante la internación</h6>
          <p class="text-muted mb-1" style="font-size: 13px">
            En esta sección, en futuras versiones, vas a poder ver las notas de evolución
            que registra el equipo veterinario (controles, medicación, observaciones).
          </p>
          <p class="text-muted mb-0" style="font-size: 13px">
            Ante cualquier duda sobre el estado de tu mascota, contactá directamente a la clínica.
          </p>
        </div>
      </div>

      <!-- CTA -->
      <div class="d-flex justify-content-end">
        <RouterLink
          :to="{ name: 'ClienteTurnos' }"
          class="btn btn-outline-success"
        >
          Ver turnos de control
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useInternacionStore } from '@/stores/internacionStore'
import type { Internacion } from '@/interfaces/internacionInterface'

const route = useRoute()
const internacionStore = useInternacionStore()

const cargando = ref(false)

/**
 * Si viene un id por ruta, lo usamos.
 * Si no, o si no existe, mostraremos la internación activa más reciente.
 */
const idInternacion = computed(() => Number(route.params.id || 0))

onMounted(async () => {
  cargando.value = true
  try {
    await internacionStore.obtenerTodos()
  } finally {
    cargando.value = false
  }
})

const internaciones = computed<Internacion[]>(() => internacionStore.internaciones)

/**
 * Lógica de selección:
 * 1. Intentar encontrar por ID (si la ruta lo trae).
 * 2. Si no existe, tomar la internación activa más reciente
 *    (estado internado u observacion, o activo=true).
 */
const internacion = computed<Internacion | undefined>(() => {
  const data = internaciones.value

  // 1) Buscar por ID de ruta
  if (idInternacion.value) {
    const byId = data.find((i) => i.id === idInternacion.value)
    if (byId) return byId
  }

  // 2) Fallback: internación activa más reciente
  const activas = data.filter(
    (i) =>
      i.estado === 'internado' ||
      i.estado === 'observacion' ||
      i.activo,
  )

  if (activas.length === 0) return undefined

  return activas
    .slice()
    .sort(
      (a, b) =>
        new Date(b.fecha_ingreso).getTime() -
        new Date(a.fecha_ingreso).getTime(),
    )[0]
})

function formatearFecha(iso: string | null | undefined) {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function insigniaInternacion(estado: string) {
  switch (estado) {
    case 'internado':
      return 'bg-danger'
    case 'observacion':
      return 'bg-warning text-dark'
    case 'alta':
      return 'bg-success'
    default:
      return 'bg-secondary'
  }
}
</script>