<template>
  <div>
    <!-- Breadcrumb -->
    <nav class="mb-3">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <RouterLink to="/admin/duenos">Dueños</RouterLink>
        </li>
        <li class="breadcrumb-item active">{{ dueno?.first_name ?? 'Cargando...' }} {{ dueno?.last_name ?? '' }}</li>
      </ol>
    </nav>

    <div v-if="cargando" class="text-center text-muted py-5">Cargando...</div>

    <div v-else-if="!dueno" class="text-center text-muted py-5">Dueño no encontrado</div>

    <div v-else>
      <!-- Header del dueño -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body d-flex align-items-center gap-3">
          <div
            class="rounded-circle d-flex align-items-center justify-content-center fw-bold flex-shrink-0"
            style="width:80px;height:80px;background:#d1e7dd;color:#146c43;font-size:1.8rem"
          >
            {{ iniciales }}
          </div>
          <div class="flex-grow-1">
            <h4 class="fw-bold mb-1">{{ dueno.first_name }} {{ dueno.last_name }}</h4>
            <p class="text-muted small mb-1">
              <strong>Email:</strong> {{ dueno.email || 'Sin email' }}
            </p>
            <p class="text-muted small mb-1">
              <strong>Teléfono:</strong> {{ perfil?.telefono || 'Sin teléfono' }}
            </p>
            <p class="text-muted small mb-0">
              <strong>Dirección:</strong> {{ perfil?.direccion || 'Sin dirección' }}
            </p>
          </div>
          <div>
            <RouterLink :to="`/admin/duenos`" class="btn btn-outline-secondary btn-sm">
              ← Volver
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <!-- Mascotas del dueño -->
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <span class="fw-semibold">Mascotas ({{ mascotasDueno.length }})</span>
              <RouterLink to="/admin/pacientes" class="btn btn-sm btn-success">
                + Agregar mascota
              </RouterLink>
            </div>
            <div class="card-body p-0">
              <div v-if="mascotasDueno.length === 0" class="text-center text-muted py-4 small">
                Este dueño no tiene mascotas registradas
              </div>
              <table v-else class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Nombre</th>
                    <th>Especie</th>
                    <th>Raza</th>
                    <th>Sexo</th>
                    <th>Edad</th>
                    <th>Peso</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="m in mascotasDueno" :key="m.id">
                    <td class="fw-semibold">{{ m.nombre }}</td>
                    <td>{{ m.especie_nombre }}</td>
                    <td class="text-muted small">{{ m.raza_nombre }}</td>
                    <td>
                      <span class="badge" :class="m.sexo === 'M' ? 'bg-primary' : 'bg-danger'">
                        {{ m.sexo_display }}
                      </span>
                    </td>
                    <td class="small">{{ m.edad_anos ? `${m.edad_anos} años` : '—' }}</td>
                    <td class="small">{{ m.peso_actual ? `${m.peso_actual} kg` : '—' }}</td>
                    <td>
                      <RouterLink :to="`/admin/pacientes/${m.id}`" class="btn btn-sm btn-outline-secondary">
                        Ver ficha
                      </RouterLink>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Turnos próximos -->
        <div class="col-md-6">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white">
              <span class="fw-semibold">Próximos turnos</span>
            </div>
            <div class="card-body p-0">
              <div v-if="turnosProximos.length === 0" class="text-center text-muted py-3 small">
                Sin turnos próximos
              </div>
              <table v-else class="table table-sm table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Fecha</th>
                    <th>Mascota</th>
                    <th>Servicio</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="t in turnosProximos.slice(0, 5)" :key="t.id">
                    <td class="small">{{ formatFechaHora(t.fecha_hora) }}</td>
                    <td class="small">{{ t.mascota_nombre }}</td>
                    <td class="small">{{ t.servicio_nombre }}</td>
                    <td>
                      <span class="badge" :class="badgeEstado(t.estado)">
                        {{ t.estado_display }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Historial de turnos -->
        <div class="col-md-6">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white">
              <span class="fw-semibold">Historial de turnos</span>
            </div>
            <div class="card-body p-0">
              <div v-if="turnosPasados.length === 0" class="text-center text-muted py-3 small">
                Sin turnos anteriores
              </div>
              <table v-else class="table table-sm table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Fecha</th>
                    <th>Mascota</th>
                    <th>Servicio</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="t in turnosPasados.slice(0, 5)" :key="t.id">
                    <td class="small">{{ formatFechaHora(t.fecha_hora) }}</td>
                    <td class="small">{{ t.mascota_nombre }}</td>
                    <td class="small">{{ t.servicio_nombre }}</td>
                    <td>
                      <span class="badge" :class="badgeEstado(t.estado)">
                        {{ t.estado_display }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Resumen de consultas -->
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white">
              <span class="fw-semibold">Últimas consultas médicas</span>
            </div>
            <div class="card-body p-0">
              <div v-if="consultasDueno.length === 0" class="text-center text-muted py-3 small">
                Sin consultas registradas
              </div>
              <table v-else class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Fecha</th>
                    <th>Mascota</th>
                    <th>Tipo</th>
                    <th>Veterinario</th>
                    <th>Diagnóstico</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in consultasDueno.slice(0, 10)" :key="c.id">
                    <td class="small">{{ formatFecha(c.fecha) }}</td>
                    <td class="small">{{ obtenerMascotaNombre(c.mascota) }}</td>
                    <td><span class="badge bg-secondary">{{ c.tipo_display }}</span></td>
                    <td class="small">{{ c.veterinario_nombre ?? '—' }}</td>
                    <td class="small">{{ c.diagnostico ?? '—' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUsuarioStore } from '@/stores/usuarioStore'
import { usePerfilClienteStore } from '@/stores/perfilClienteStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useTurnoStore } from '@/stores/turnoStore'
import { useConsultaStore } from '@/stores/consultaStore'
import type { EstadoTurno } from '@/interfaces/turnoInterface'
import type { UsuarioAuth } from '@/interfaces/usuarioInterface'
import type { ConsultaClinica } from '@/interfaces/consultaClinicaInterface'

const route = useRoute()
const usuarioStore = useUsuarioStore()
const perfilClienteStore = usePerfilClienteStore()
const mascotaStore = useMascotaStore()
const turnoStore = useTurnoStore()
const consultaStore = useConsultaStore()

const duenoId = computed(() => Number(route.params.id))

const dueno = computed(() =>
  usuarioStore.usuarios.find((u: UsuarioAuth) => u.id === duenoId.value) ?? null
)

const perfil = computed(() =>
  perfilClienteStore.perfiles.find((p) => p.usuario.id === duenoId.value) ?? null
)

const mascotasDueno = computed(() =>
  mascotaStore.mascotas.filter((m) => m.usuario === duenoId.value)
)

const mascotsIds = computed(() => mascotasDueno.value.map((m) => m.id))

const turnosDueno = computed(() =>
  turnoStore.turnos.filter((t) => mascotsIds.value.includes(t.mascota_id))
)

const turnosProximos = computed(() => {
  const ahora = new Date().toISOString()
  return turnosDueno.value
    .filter((t) => t.fecha_hora >= ahora)
    .sort((a, b) => a.fecha_hora.localeCompare(b.fecha_hora))
})

const turnosPasados = computed(() => {
  const ahora = new Date().toISOString()
  return turnosDueno.value
    .filter((t) => t.fecha_hora < ahora)
    .sort((a, b) => b.fecha_hora.localeCompare(a.fecha_hora))
})

const consultasDueno = computed(() =>
  consultaStore.consultas
    .filter((c: ConsultaClinica) => mascotsIds.value.includes(c.mascota))
    .sort((a: ConsultaClinica, b: ConsultaClinica) => b.fecha.localeCompare(a.fecha))
)

const cargando = computed(() =>
  usuarioStore.cargando ||
  perfilClienteStore.cargando ||
  mascotaStore.cargando ||
  turnoStore.cargando ||
  consultaStore.cargando
)

const iniciales = computed(() => {
  if (!dueno.value) return ''
  const nombre = dueno.value.first_name?.[0] ?? ''
  const apellido = dueno.value.last_name?.[0] ?? ''
  return `${nombre}${apellido}`.toUpperCase()
})

onMounted(async () => {
  await Promise.all([
    usuarioStore.obtenerTodos(),
    perfilClienteStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
    turnoStore.obtenerTodos(),
    consultaStore.obtenerTodos(),
  ])
})

function formatFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function formatFechaHora(fechaHora: string) {
  return (
    new Date(fechaHora).toLocaleDateString('es-AR', { day: '2-digit', month: 'short' }) +
    ' ' +
    new Date(fechaHora).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })
  )
}

function badgeEstado(estado: EstadoTurno) {
  const map: Record<EstadoTurno, string> = {
    reservado: 'bg-primary',
    confirmado: 'bg-success',
    en_espera: 'bg-warning text-dark',
    en_consulta: 'bg-info text-dark',
    atendido: 'bg-secondary',
    cancelado: 'bg-danger',
  }
  return map[estado] ?? 'bg-secondary'
}

function obtenerMascotaNombre(mascotaId: number) {
  return mascotaStore.mascotas.find((m) => m.id === mascotaId)?.nombre ?? '—'
}
</script>