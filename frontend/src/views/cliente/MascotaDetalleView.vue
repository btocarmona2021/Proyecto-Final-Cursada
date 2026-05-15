<!-- src/views/cliente/MascotaDetalleView.vue -->
<template>
  <div class="container-fluid">
    <!-- Breadcrumb simple -->
    <div class="mb-2">
      <RouterLink
        :to="{ name: 'ClienteMascotas' }"
        class="small text-decoration-none text-muted"
      >
        ← Volver a mis mascotas
      </RouterLink>
    </div>

    <!-- Estado de carga -->
    <div
      v-if="cargando"
      class="text-center text-muted py-4"
      style="font-size: 13px"
    >
      Cargando información de la mascota...
    </div>

    <!-- No encontrada -->
    <div
      v-else-if="!mascota"
      class="alert alert-warning"
      style="font-size: 13px"
    >
      Mascota no encontrada. Es posible que haya sido desactivada o no tengas acceso.
    </div>

    <!-- Detalle -->
    <div v-else>
      <!-- Header -->
      <div class="card border-0 shadow-sm mb-3">
        <div class="card-body d-flex align-items-center gap-3">
          <div
            class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
            style="width: 64px; height: 64px; background: #e7f5ff"
          >
            <span style="font-size: 2rem">
              {{ emojiAvatar(mascota.especie_nombre) }}
            </span>
          </div>
          <div class="flex-grow-1">
            <h4 class="fw-bold mb-1">{{ mascota.nombre }}</h4>
            <div class="text-muted" style="font-size: 13px">
              {{ mascota.especie_nombre }} · {{ mascota.raza_nombre }}
            </div>
            <div class="text-muted" style="font-size: 12px">
              Sexo:
              <span
                class="badge"
                :class="mascota.sexo === 'M' ? 'bg-primary' : 'bg-danger'"
                style="font-size: 11px"
              >
                {{ mascota.sexo_display }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Datos básicos -->
      <div class="row g-3 mb-3">
        <div class="col-12 col-md-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-2">Datos generales</h6>
              <ul class="list-unstyled mb-0" style="font-size: 13px">
                <li class="d-flex justify-content-between mb-1">
                  <span>Edad</span>
                  <strong>
                    {{ mascota.edad_anos ? mascota.edad_anos + ' años' : '—' }}
                  </strong>
                </li>
                <li class="d-flex justify-content-between mb-1">
                  <span>Peso actual</span>
                  <strong>
                    {{ mascota.peso_actual ? mascota.peso_actual + ' kg' : '—' }}
                  </strong>
                </li>
                <li class="d-flex justify-content-between mb-1">
                  <span>Identificador</span>
                  <strong>{{ mascota.id }}</strong>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Últimos turnos -->
        <div class="col-12 col-md-8">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-2">Últimos turnos</h6>
              <div
                v-if="turnosMascota.length === 0"
                class="text-muted"
                style="font-size: 13px"
              >
                No hay turnos registrados para esta mascota.
              </div>
              <ul
                v-else
                class="list-group list-group-flush"
                style="font-size: 13px"
              >
                <li
                  v-for="t in turnosMascota.slice(0, 5)"
                  :key="t.id"
                  class="list-group-item px-0"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <div class="fw-semibold">
                        {{ formatearFechaHora(t.fecha_hora) }}
                      </div>
                      <div class="text-muted">
                        {{ t.servicio_nombre }}
                        <span v-if="t.veterinario_nombre">
                          · {{ t.veterinario_nombre }}
                        </span>
                      </div>
                    </div>
                    <span
                      class="badge"
                      :class="insigniaEstado(t.estado)"
                      style="font-size: 11px"
                    >
                      {{ t.estado_display }}
                    </span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumen simple clínico (placeholder) -->
      <div class="card border-0 shadow-sm mb-3">
        <div class="card-body">
          <h6 class="fw-bold mb-2">Resumen clínico</h6>
          <p class="text-muted mb-1" style="font-size: 13px">
            En futuras versiones vas a poder ver el detalle de vacunas, consultas y
            resultados clínicos directamente desde aquí.
          </p>
        </div>
      </div>

      <!-- CTA -->
      <div class="d-flex justify-content-end">
        <RouterLink
          :to="{ name: 'ClienteReservar' }"
          class="btn btn-success"
        >
          Reservar turno para {{ mascota.nombre }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useTurnoStore } from '@/stores/turnoStore'
import type { Mascota } from '@/interfaces/mascotaInterface'
import type { Turno } from '@/interfaces/turnoInterface'

const route = useRoute()
const mascotaStore = useMascotaStore()
const turnoStore = useTurnoStore()

const cargando = ref(false)

const idMascota = computed(() => Number(route.params.id || 0))

onMounted(async () => {
  cargando.value = true
  try {
    await Promise.all([
      mascotaStore.obtenerTodos(),
      turnoStore.obtenerTodos(),
    ])
  } finally {
    cargando.value = false
  }
})

const mascotas = computed<Mascota[]>(() => mascotaStore.mascotas)

const mascota = computed<Mascota | undefined>(() =>
  mascotas.value.find((m) => m.id === idMascota.value),
)

const turnosMascota = computed<Turno[]>(() =>
  turnoStore.turnos
    .filter((t) => t.mascota_id === idMascota.value)
    .sort((a, b) => {
      if (!a.fecha_hora || !b.fecha_hora) return 0
      return new Date(b.fecha_hora).getTime() - new Date(a.fecha_hora).getTime()
    }),
)

function emojiAvatar(especieNombre: string | null | undefined) {
  const lower = especieNombre?.toLowerCase() ?? ''
  if (lower.includes('perro')) return '🐶'
  if (lower.includes('gato')) return '🐱'
  if (lower.includes('ave') || lower.includes('pájaro')) return '🦜'
  if (lower.includes('conejo')) return '🐰'
  return '🐾'
}

function formatearFechaHora(iso: string | null | undefined) {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleString('es-AR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function insigniaEstado(estado: string) {
  switch (estado) {
    case 'confirmado':
      return 'bg-success'
    case 'en_espera':
      return 'bg-warning text-dark'
    case 'en_consulta':
      return 'bg-info text-dark'
    case 'reservado':
      return 'bg-secondary'
    case 'cancelado':
      return 'bg-light text-muted'
    case 'atendido':
      return 'bg-primary'
    default:
      return 'bg-light text-muted'
  }
}
</script>