<!-- src/views/cliente/MascotaDetalleView.vue -->
<template>
  <div class="container-fluid">
    <!-- Breadcrumb simple -->
    <div class="mb-2">
      <RouterLink :to="{ name: 'ClienteMascotas' }" class="small text-decoration-none text-muted">
        ← Volver a mis mascotas
      </RouterLink>
    </div>

    <!-- Estado de carga -->
    <div v-if="cargando" class="text-center text-muted py-4" style="font-size: 13px">
      Cargando información de la mascota...
    </div>

    <!-- No encontrada -->
    <div v-else-if="!mascota" class="alert alert-warning" style="font-size: 13px">
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
            <img
              v-if="mascota.foto"
              :src="urlImagen(mascota.foto)"
              :alt="mascota.nombre"
              class="rounded-circle"
              style="width: 100%; height: 100%; object-fit: cover"
            />
            <span v-else style="font-size: 2rem">
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
              <div v-if="turnosMascota.length === 0" class="text-muted" style="font-size: 13px">
                No hay turnos registrados para esta mascota.
              </div>
              <ul v-else class="list-group list-group-flush" style="font-size: 13px">
                <li v-for="t in turnosMascota.slice(0, 5)" :key="t.id" class="list-group-item px-0">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <div class="fw-semibold">
                        {{ formatearFechaHora(t.fecha_hora) }}
                      </div>
                      <div class="text-muted">
                        {{ t.servicio_nombre }}
                        <span v-if="t.veterinario_nombre"> · {{ t.veterinario_nombre }} </span>
                      </div>
                    </div>
                    <span class="badge" :class="insigniaEstado(t.estado)" style="font-size: 11px">
                      {{ t.estado_display }}
                    </span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Historial clínico -->
      <div class="row g-3 mb-3">
        <div class="col-12 col-md-6">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-2">Vacunas</h6>
              <div v-if="vacunasMascota.length === 0" class="text-muted" style="font-size: 13px">
                Sin vacunas registradas.
              </div>
              <ul v-else class="list-group list-group-flush" style="font-size: 13px">
                <li v-for="v in vacunasMascota" :key="v.id" class="list-group-item px-0">
                  <div class="d-flex justify-content-between">
                    <span class="fw-semibold">{{ v.nombre }}</span>
                    <span class="text-muted">
                      {{ formatearFecha(v.fecha_aplicacion) }}
                    </span>
                  </div>
                  <div v-if="v.fecha_proxima" class="text-muted">
                    Próxima: {{ formatearFecha(v.fecha_proxima) }}
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-6">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h6 class="fw-bold mb-2">Consultas</h6>
              <div v-if="consultasMascota.length === 0" class="text-muted" style="font-size: 13px">
                Sin consultas registradas.
              </div>
              <ul v-else class="list-group list-group-flush" style="font-size: 13px">
                <li v-for="c in consultasMascota" :key="c.id" class="list-group-item px-0">
                  <div class="d-flex justify-content-between">
                    <span class="fw-semibold">{{ c.tipo_display }}</span>
                    <span class="text-muted">
                      {{ formatearFecha(c.fecha) }}
                    </span>
                  </div>
                  <div v-if="c.diagnostico" class="text-muted">
                    {{ c.diagnostico }}
                  </div>
                  <details v-if="c.recetas?.length" class="mt-2">
                    <summary class="text-success">Ver receta ({{ c.recetas.length }})</summary>
                    <RecetaDetalle :items="c.recetas" class="mt-2" />
                  </details>
                  <div v-if="c.veterinario_nombre" class="text-muted small">
                    Dr/a: {{ c.veterinario_nombre }}
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA -->
      <div class="d-flex justify-content-end">
        <RouterLink :to="{ name: 'ClienteReservar' }" class="btn btn-success">
          Reservar turno para {{ mascota.nombre }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import RecetaDetalle from '@/components/RecetaDetalle.vue'
import { urlImagen } from '@/utils/imagenes'
import { computed, onMounted, ref } from 'vue'
import { fechaDesdeAPI } from '@/utils/fechas'
import { useRoute } from 'vue-router'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useTurnoStore } from '@/stores/turnoStore'
import { useConsultaStore } from '@/stores/consultaStore'
import { useVacunaStore } from '@/stores/vacunaStore'
import type { Mascota } from '@/interfaces/mascotaInterface'
import type { Turno } from '@/interfaces/turnoInterface'
import type { ConsultaClinica } from '@/interfaces/consultaClinicaInterface'
import type { Vacuna } from '@/interfaces/vacunaInterface'

const route = useRoute()
const mascotaStore = useMascotaStore()
const turnoStore = useTurnoStore()
const consultaStore = useConsultaStore()
const vacunaStore = useVacunaStore()

const cargando = ref(false)

const idMascota = computed(() => Number(route.params.id || 0))

onMounted(async () => {
  cargando.value = true
  try {
    await Promise.all([
      mascotaStore.obtenerTodos(),
      turnoStore.obtenerTodos(),
      consultaStore.obtenerTodos(),
      vacunaStore.obtenerTodos(),
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

const consultasMascota = computed<ConsultaClinica[]>(() =>
  consultaStore.consultas.filter((c) => c.mascota === idMascota.value),
)

const vacunasMascota = computed<Vacuna[]>(() =>
  vacunaStore.vacunas.filter((v) => v.mascota === idMascota.value),
)

function formatearFecha(iso: string | null | undefined) {
  if (!iso) return '—'
  return fechaDesdeAPI(iso).toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

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
