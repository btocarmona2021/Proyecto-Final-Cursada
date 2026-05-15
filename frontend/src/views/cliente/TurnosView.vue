<!-- src/views/cliente/TurnosView.vue -->
<template>
  <div class="container-fluid">
    <!-- Encabezado -->
    <div class="mb-3 d-flex justify-content-between align-items-center">
      <div>
        <h4 class="fw-bold mb-1">Mis turnos</h4>
        <p class="text-muted mb-0" style="font-size: 13px">
          Historial y turnos futuros de tus mascotas
        </p>
      </div>
      <RouterLink
        :to="{ name: 'ClienteReservar' }"
        class="btn btn-sm btn-success d-none d-sm-inline-flex align-items-center"
      >
        <span class="me-1">➕</span>
        Reservar turno
      </RouterLink>
    </div>

    <!-- Resumen rápido -->
    <div class="row g-2 mb-3">
      <div class="col-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body py-2 px-3 text-center">
            <div class="text-muted small">Futuros</div>
            <div class="fw-bold fs-5 text-success">{{ totalFuturos }}</div>
          </div>
        </div>
      </div>
      <div class="col-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body py-2 px-3 text-center">
            <div class="text-muted small">Atendidos</div>
            <div class="fw-bold fs-5 text-primary">{{ totalAtendidos }}</div>
          </div>
        </div>
      </div>
      <div class="col-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body py-2 px-3 text-center">
            <div class="text-muted small">Cancelados</div>
            <div class="fw-bold fs-5 text-secondary">{{ totalCancelados }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filtro simple por estado -->
    <div class="d-flex flex-wrap gap-2 mb-3">
      <button
        v-for="op in opcionesEstado"
        :key="op.value"
        class="btn btn-sm"
        :class="filtroEstado === op.value ? 'btn-success' : 'btn-outline-secondary'"
        @click="filtroEstado = op.value"
      >
        {{ op.label }}
      </button>
    </div>

    <!-- Lista de turnos -->
    <div class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div
          v-if="cargando"
          class="text-center text-muted py-4"
          style="font-size: 13px"
        >
          Cargando turnos...
        </div>

        <div
          v-else-if="turnosCliente.length === 0"
          class="text-center text-muted py-4"
          style="font-size: 13px"
        >
          No tenés turnos registrados.
          <RouterLink :to="{ name: 'ClienteReservar' }">
            Reservar ahora
          </RouterLink>.
        </div>

        <ul
          v-else
          class="list-group list-group-flush"
        >
          <li
            v-for="t in turnosFiltrados"
            :key="t.id"
            class="list-group-item"
          >
            <div class="d-flex justify-content-between align-items-start">
              <div class="d-flex gap-2">
                <div
                  class="d-flex flex-column align-items-center justify-content-center px-2"
                  style="min-width: 52px; border-right: 1px solid #eee"
                >
                  <div class="fw-bold" style="font-size: 16px">
                    {{ formatearDia(t.fecha_hora) }}
                  </div>
                  <div
                    class="text-uppercase text-muted"
                    style="font-size: 10px"
                  >
                    {{ formatearMes(t.fecha_hora) }}
                  </div>
                  <span
                    class="badge bg-light text-muted mt-1"
                    style="font-size: 10px"
                  >
                    {{ formatearHora(t.fecha_hora) }}
                  </span>
                </div>
                <div>
                  <div class="fw-semibold" style="font-size: 14px">
                    {{ t.mascota_nombre }} ·
                    <span class="text-muted" style="font-size: 12px">
                      {{ t.servicio_nombre }}
                    </span>
                  </div>
                  <div class="text-muted" style="font-size: 12px">
                    Veterinario: {{ t.veterinario_nombre ?? 'A confirmar' }}
                  </div>
                  <div
                    v-if="t.motivo_consulta"
                    class="text-muted"
                    style="font-size: 12px"
                  >
                    Motivo: {{ t.motivo_consulta }}
                  </div>
                </div>
              </div>

              <div class="text-end">
                <span
                  class="badge"
                  :class="insigniaEstado(t.estado)"
                  style="font-size: 11px"
                >
                  {{ t.estado_display }}
                </span>
              </div>
            </div>

            <div class="d-flex justify-content-end gap-2 mt-2">
              <!-- Acción de cancelar futura, solo preparada, puedes bloquear en permisos backend -->
              <button
                v-if="esFuturo(t)"
                class="btn btn-sm btn-outline-danger"
                type="button"
                disabled
                title="En el futuro podrás cancelar desde aquí"
              >
                Cancelar
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useTurnoStore } from '@/stores/turnoStore'
import type { Turno } from '@/interfaces/turnoInterface'

const turnoStore = useTurnoStore()
const cargando = ref(false)

const filtroEstado = ref<string>('todos')

const opcionesEstado = [
  { value: 'todos', label: 'Todos' },
  { value: 'reservado', label: 'Reservados' },
  { value: 'confirmado', label: 'Confirmados' },
  { value: 'en_consulta', label: 'En consulta' },
  { value: 'atendido', label: 'Atendidos' },
  { value: 'cancelado', label: 'Cancelados' },
]

onMounted(async () => {
  try {
    cargando.value = true
    await turnoStore.obtenerTodos()
  } finally {
    cargando.value = false
  }
})

const turnosCliente = computed<Turno[]>(() => {
  // Aquí asumimos que el backend ya filtra por dueño vía permisos,
  // así que usamos todo el array. Si en el futuro necesitas filtrado
  // adicional por usuario, se puede añadir acá.
  return turnoStore.turnos.slice().sort((a, b) => {
    if (!a.fecha_hora || !b.fecha_hora) return 0
    return new Date(b.fecha_hora).getTime() - new Date(a.fecha_hora).getTime()
  })
})

const turnosFiltrados = computed<Turno[]>(() => {
  if (filtroEstado.value === 'todos') {
    return turnosCliente.value
  }
  return turnosCliente.value.filter((t) => t.estado === filtroEstado.value)
})

const totalFuturos = computed(() => {
  const ahora = new Date()
  return turnosCliente.value.filter(
    (t) => t.fecha_hora && new Date(t.fecha_hora) >= ahora,
  ).length
})

const totalAtendidos = computed(
  () => turnosCliente.value.filter((t) => t.estado === 'atendido').length,
)

const totalCancelados = computed(
  () => turnosCliente.value.filter((t) => t.estado === 'cancelado').length,
)

function esFuturo(t: Turno): boolean {
  if (!t.fecha_hora) return false
  return new Date(t.fecha_hora) >= new Date()
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

function formatearHora(iso: string | null | undefined) {
  if (!iso) return '--:--'
  return new Date(iso).toLocaleTimeString('es-AR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatearDia(iso: string | null | undefined) {
  if (!iso) return '--'
  return new Date(iso).toLocaleDateString('es-AR', {
    day: '2-digit',
  })
}

function formatearMes(iso: string | null | undefined) {
  if (!iso) return '--'
  return new Date(iso).toLocaleDateString('es-AR', {
    month: 'short',
  })
}
</script>