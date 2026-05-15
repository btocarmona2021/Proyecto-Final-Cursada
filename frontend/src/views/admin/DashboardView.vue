<template>
  <div>
    <!-- Encabezado -->
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Dashboard</h4>
      <p class="text-muted small mb-0">Resumen rápido de la clínica para hoy · {{ fechaHoy }}</p>
    </div>

    <!-- KPIs -->
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="text-muted small mb-1">Turnos de hoy</div>
            <div class="fs-3 fw-bold text-primary">{{ turnosHoy.length }}</div>
            <div class="text-muted small">agendados</div>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="text-muted small mb-1">Pacientes activos</div>
            <div class="fs-3 fw-bold text-success">{{ mascotaStore.mascotas.length }}</div>
            <div class="text-muted small">registrados</div>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="text-muted small mb-1">Vacunas vencidas</div>
            <div class="fs-3 fw-bold text-warning">{{ vacunasVencidas.length }}</div>
            <div class="text-muted small">requieren atención</div>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="text-muted small mb-1">Internaciones activas</div>
            <div class="fs-3 fw-bold text-danger">{{ internacionesActivas.length }}</div>
            <RouterLink
              to="/admin/internaciones"
              class="small text-decoration-none"
            >
              Ver internaciones →
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Turnos + Vacunas -->
    <div class="row g-3 mb-4">
      <!-- Turnos de hoy -->
      <div class="col-md-6">
        <div class="card border-0 shadow-sm h-100">
          <div
            class="card-header bg-white d-flex justify-content-between align-items-center"
          >
            <span class="fw-semibold">Próximos turnos de hoy</span>
            <RouterLink
              to="/admin/agenda"
              class="btn btn-sm btn-outline-secondary"
            >
              Ver agenda
            </RouterLink>
          </div>
          <div class="card-body p-0">
            <div
              v-if="turnoStore.cargando"
              class="text-center text-muted py-4"
            >
              Cargando...
            </div>
            <div
              v-else-if="turnosHoy.length === 0"
              class="text-center text-muted py-4"
            >
              No hay turnos para hoy
            </div>
            <ul v-else class="list-group list-group-flush">
              <li
                v-for="turno in turnosHoy.slice(0, 6)"
                :key="turno.id"
                class="list-group-item d-flex align-items-center gap-2"
              >
                <span
                  class="text-muted small fw-bold"
                  style="min-width: 48px"
                >
                  {{ formatHora(turno.fecha_hora) }}
                </span>
                <div class="flex-grow-1">
                  <div class="fw-semibold small">
                    {{ turno.mascota_nombre }}
                  </div>
                  <div class="text-muted" style="font-size: 11px">
                    {{ turno.servicio_nombre }} ·
                    {{ turno.veterinario_nombre || 'Sin asignar' }}
                  </div>
                </div>
                <span
                  class="badge"
                  :class="badgeEstado(turno.estado)"
                >
                  {{ turno.estado_display }}
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Vacunas alertas -->
      <div class="col-md-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white">
            <span class="fw-semibold">Vacunas — alertas próximas</span>
          </div>
          <div class="card-body p-0">
            <div
              v-if="vacunaStore.cargando"
              class="text-center text-muted py-4"
            >
              Cargando...
            </div>
            <div
              v-else-if="alertasVacunas.length === 0"
              class="text-center text-muted py-4"
            >
              Sin alertas de vacunas
            </div>
            <table
              v-else
              class="table table-sm table-hover mb-0"
            >
              <thead class="table-light">
                <tr>
                  <th>Paciente</th>
                  <th>Vacuna</th>
                  <th>Próxima</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="v in alertasVacunas" :key="v.id">
                  <td>{{ obtenerNombreMascota(v.mascota) }}</td>
                  <td>{{ v.nombre }}</td>
                  <td>{{ formatFecha(v.fecha_proxima!) }}</td>
                  <td>
                    <span
                      class="badge"
                      :class="v.vencida ? 'bg-danger' : 'bg-warning text-dark'"
                    >
                      {{
                        v.vencida
                          ? 'Vencida'
                          : diasRestantes(v.fecha_proxima!) + ' días'
                      }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Internaciones activas -->
    <div
      v-if="internacionesActivas.length > 0"
      class="card border-0 shadow-sm"
    >
      <div
        class="card-header bg-white d-flex justify-content-between align-items-center"
      >
        <span class="fw-semibold">Internaciones activas</span>
        <RouterLink
          to="/admin/internaciones"
          class="btn btn-sm btn-outline-secondary"
        >
          Ver todas
        </RouterLink>
      </div>
      <div class="card-body p-0">
        <table class="table table-sm table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Paciente</th>
              <th>Veterinario</th>
              <th>Ingreso</th>
              <th>Motivo</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in internacionesActivas" :key="i.id">
              <td>{{ i.mascota_nombre }}</td>
              <td>{{ i.veterinario_nombre || '-' }}</td>
              <td>{{ formatFecha(i.fecha_ingreso) }}</td>
              <td>{{ i.motivo }}</td>
              <td>
                <span
                  class="badge"
                  :class="badgeInternacion(i.estado)"
                >
                  {{ i.estado_display }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useTurnoStore } from '@/stores/turnoStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useVacunaStore } from '@/stores/vacunaStore'
import { useInternacionStore } from '@/stores/internacionStore'
import type { EstadoTurno } from '@/interfaces/turnoInterface'
import type { EstadoInternacion } from '@/interfaces/internacionInterface'

const turnoStore = useTurnoStore()
const mascotaStore = useMascotaStore()
const vacunaStore = useVacunaStore()
const internacionStore = useInternacionStore()

onMounted(async () => {
  await Promise.all([
    turnoStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
    vacunaStore.obtenerTodos(),
    internacionStore.obtenerTodos(),
  ])
})

const fechaHoy = computed(() =>
  new Date().toLocaleDateString('es-AR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }),
)

const hoy = new Date().toISOString().slice(0, 10)

const turnosHoy = computed(() =>
  turnoStore.turnos
    .filter((t) => t.fecha_hora && t.fecha_hora.startsWith(hoy))
    .sort((a, b) => a.fecha_hora.localeCompare(b.fecha_hora)),
)

const vacunasVencidas = computed(() =>
  vacunaStore.vacunas.filter(
    (v) => v.fecha_proxima && new Date(v.fecha_proxima) < new Date(),
  ),
)

const alertasVacunas = computed(() =>
  vacunaStore.vacunas
    .filter((v) => {
      if (!v.fecha_proxima) return false
      const dias = diasRestantes(v.fecha_proxima)
      return dias < 0 || (dias >= 0 && dias <= 30)
    })
    .map((v) => ({
      ...v,
      vencida: diasRestantes(v.fecha_proxima!) < 0,
    }))
    .slice(0, 6),
)

const internacionesActivas = computed(() =>
  internacionStore.internaciones.filter((i) => i.estado !== 'alta'),
)

function obtenerNombreMascota(mascotaId: number): string {
  const mascota = mascotaStore.mascotas.find((m) => m.id === mascotaId)
  return mascota?.nombre || 'Desconocido'
}

const formatFecha = (iso: string) =>
  new Date(iso).toLocaleDateString('es-AR')

const formatHora = (iso: string) =>
  new Date(iso).toLocaleTimeString('es-AR', {
    hour: '2-digit',
    minute: '2-digit',
  })

const diasRestantes = (iso: string) => {
  const hoyDate = new Date()
  const target = new Date(iso)
  const diff = target.getTime() - hoyDate.getTime()
  return Math.round(diff / (1000 * 60 * 60 * 24))
}

const badgeEstado = (estado: EstadoTurno) => {
  switch (estado) {
    case 'confirmado':
      return 'bg-success'
    case 'en_espera':
      return 'bg-warning text-dark'
    case 'cancelado':
      return 'bg-secondary'
    case 'atendido':
      return 'bg-primary'
    default:
      return 'bg-light text-dark'
  }
}

const badgeInternacion = (estado: EstadoInternacion) => {
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