<!-- src/views/cliente/InicioView.vue -->
<template>
  <div class="container-fluid">
    <!-- Encabezado -->
    <div class="mb-3">
      <h4 class="fw-bold mb-1">Hola de nuevo 👋</h4>
      <p class="text-muted mb-0" style="font-size: 13px">
        Resumen de tu clínica y tus mascotas
      </p>
    </div>

    <!-- Banner próximo turno -->
    <div v-if="proximo_turno" class="card border-0 shadow-sm mb-3">
      <div class="card-body d-flex">
        <div
          class="me-3 d-flex flex-column align-items-center justify-content-center px-2"
          style="border-right: 1px solid #eee"
        >
          <div class="fw-bold" style="font-size: 24px">
            {{ format_dia(proximo_turno.fecha_hora) }}
          </div>
          <div class="text-uppercase text-muted" style="font-size: 11px">
            {{ format_mes(proximo_turno.fecha_hora) }}
          </div>
          <span class="badge bg-success mt-2" style="font-size: 11px">
            {{ format_hora(proximo_turno.fecha_hora) }}
          </span>
        </div>
        <div class="flex-grow-1">
          <div class="d-flex justify-content-between align-items-start mb-1">
            <div class="fw-bold" style="font-size: 14px">
              Próximo turno con
              {{ proximo_turno.veterinario_nombre ?? 'Veterinario' }}
            </div>
            <span
              class="badge rounded-pill"
              :class="badge_estado_turno(proximo_turno.estado)"
              style="font-size: 11px"
            >
              {{ proximo_turno.estado_display }}
            </span>
          </div>
          <div class="text-muted mb-1" style="font-size: 13px">
            Mascota:
            <strong>{{ proximo_turno.mascota_nombre }}</strong>
          </div>
          <div class="text-muted mb-2" style="font-size: 13px">
            Servicio: {{ proximo_turno.servicio_nombre }}
          </div>
          <RouterLink
            class="btn btn-sm btn-outline-success"
            :to="{ name: 'ClienteTurnos' }"
          >
            Ver todos los turnos
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Aviso si no hay turnos -->
    <div v-else class="alert alert-info d-flex align-items-center mb-3">
      <span class="me-2">📅</span>
      <div style="font-size: 13px">
        No tenés turnos próximos.
        <RouterLink :to="{ name: 'ClienteReservar' }">
          Reservar ahora
        </RouterLink>.
      </div>
    </div>

    <!-- Bloque mascotas -->
    <div class="mb-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h6 class="mb-0 fw-bold">Tus mascotas</h6>
        <RouterLink
          v-if="mascotas.length > 0"
          :to="{ name: 'ClienteMascotas' }"
          class="small text-success text-decoration-none"
        >
          Ver todas
        </RouterLink>
      </div>

      <div v-if="mascotas.length > 0" class="row g-2">
        <div
          v-for="m in mascotas_preview"
          :key="m.id"
          class="col-12"
        >
          <div
            class="d-flex align-items-center p-2 rounded-3 border bg-white shadow-sm"
            role="button"
            @click="ir_mascota(m.id)"
          >
            <div
              class="rounded-circle d-flex align-items-center justify-content-center me-3"
              style="width: 48px; height: 48px; background: #e7f5ff"
            >
              <span style="font-size: 1.5rem">
                {{ avatar_emoji(m.especie_nombre) }}
              </span>
            </div>
            <div class="flex-grow-1">
              <div class="fw-bold" style="font-size: 14px">
                {{ m.nombre }}
              </div>
              <div class="text-muted" style="font-size: 12px">
                {{ m.especie_nombre }} · {{ m.raza_nombre }}
              </div>
              <div
                v-if="m.peso_actual"
                class="text-muted"
                style="font-size: 12px"
              >
                Peso: {{ m.peso_actual }} kg
              </div>
            </div>
            <div class="text-end">
              <span class="badge bg-light text-muted" style="font-size: 11px">
                {{ m.sexo_display }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div
        v-else
        class="alert alert-secondary d-flex align-items-center"
        style="font-size: 13px"
      >
        <span class="me-2">🐾</span>
        <div>
          Todavía no cargaste ninguna mascota.
          <RouterLink :to="{ name: 'ClienteMascotas' }">
            Agregar mascota
          </RouterLink>.
        </div>
      </div>
    </div>

    <!-- Accesos rápidos -->
    <div class="mb-3">
      <h6 class="mb-2 fw-bold">Acciones rápidas</h6>
      <div class="row g-2">
        <div class="col-6">
          <RouterLink
            :to="{ name: 'ClienteReservar' }"
            class="btn btn-success w-100 d-flex flex-column align-items-center py-3"
          >
            <span class="mb-1" style="font-size: 1.6rem">🗓️</span>
            <span style="font-size: 12px; font-weight: 600">
              Reservar turno
            </span>
          </RouterLink>
        </div>
        <div class="col-6">
          <RouterLink
            :to="{ name: 'ClienteTurnos' }"
            class="btn btn-outline-success w-100 d-flex flex-column align-items-center py-3"
          >
            <span class="mb-1" style="font-size: 1.6rem">📋</span>
            <span style="font-size: 12px; font-weight: 600">
              Ver mis turnos
            </span>
          </RouterLink>
        </div>
        <div class="col-6">
          <RouterLink
            :to="{ name: 'ClienteMascotas' }"
            class="btn btn-outline-secondary w-100 d-flex flex-column align-items-center py-3"
          >
            <span class="mb-1" style="font-size: 1.6rem">🐶</span>
            <span style="font-size: 12px; font-weight: 600">
              Gestionar mascotas
            </span>
          </RouterLink>
        </div>
        <div class="col-6">
          <RouterLink
            :to="{ name: 'ClienteInternacion', params: { id: 1 } }"
            class="btn btn-outline-danger w-100 d-flex flex-column align-items-center py-3"
          >
            <span class="mb-1" style="font-size: 1.6rem">🏥</span>
            <span style="font-size: 12px; font-weight: 600">
              Ver internación
            </span>
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Resumen de estado -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <h6 class="fw-bold mb-2">Resumen de tu cuenta</h6>
        <ul class="list-unstyled mb-0" style="font-size: 13px">
          <li class="d-flex justify-content-between mb-1">
            <span>Mascotas registradas</span>
            <strong>{{ mascotas.length }}</strong>
          </li>
          <li class="d-flex justify-content-between mb-1">
            <span>Turnos futuros</span>
            <strong>{{ turnos_futuros }}</strong>
          </li>
          <li class="d-flex justify-content-between mb-1">
            <span>Turnos atendidos</span>
            <strong>{{ turnos_atendidos }}</strong>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTurnoStore } from '@/stores/turnoStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import type { Turno } from '@/interfaces/turnoInterface'
import type { Mascota } from '@/interfaces/mascotaInterface'

const router = useRouter()
const turno_store = useTurnoStore()
const mascota_store = useMascotaStore()

onMounted(async () => {
  await Promise.all([turno_store.obtenerTodos(), mascota_store.obtenerTodos()])
})

const hoy = new Date()

const turnos_futuros_lista = computed<Turno[]>(() =>
  turno_store.turnos
    .filter((t) => {
      if (!t.fecha_hora) return false
      return new Date(t.fecha_hora) >= hoy
    })
    .sort((a, b) => {
      const a_time = a.fecha_hora ? new Date(a.fecha_hora).getTime() : 0
      const b_time = b.fecha_hora ? new Date(b.fecha_hora).getTime() : 0
      return a_time - b_time
    }),
)

const proximo_turno = computed<Turno | null>(
  () => turnos_futuros_lista.value[0] ?? null,
)

const turnos_futuros = computed(
  () => turnos_futuros_lista.value.length,
)

const turnos_atendidos = computed(
  () => turno_store.turnos.filter((t) => t.estado === 'atendido').length,
)

const mascotas = computed<Mascota[]>(() => mascota_store.mascotas)
const mascotas_preview = computed<Mascota[]>(() => mascotas.value.slice(0, 3))

function ir_mascota(id: number) {
  router.push({ name: 'ClienteMascotaDetalle', params: { id } })
}

function avatar_emoji(especie_nombre: string | null | undefined) {
  const lower = especie_nombre?.toLowerCase() ?? ''
  if (lower.includes('perro')) return '🐶'
  if (lower.includes('gato')) return '🐱'
  if (lower.includes('ave') || lower.includes('pájaro')) return '🦜'
  if (lower.includes('conejo')) return '🐰'
  return '🐾'
}

function badge_estado_turno(estado: string) {
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
    default:
      return 'bg-light text-muted'
  }
}

function format_hora(iso: string | null | undefined) {
  if (!iso) return '--:--'
  return new Date(iso).toLocaleTimeString('es-AR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

function format_dia(iso: string | null | undefined) {
  if (!iso) return '--'
  return new Date(iso).toLocaleDateString('es-AR', {
    day: '2-digit',
  })
}

function format_mes(iso: string | null | undefined) {
  if (!iso) return '--'
  return new Date(iso).toLocaleDateString('es-AR', {
    month: 'short',
  })
}
</script>