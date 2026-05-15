<!-- src/views/cliente/ReservarView.vue -->
<template>
  <div class="container-fluid">
    <!-- Encabezado -->
    <div class="mb-3 d-flex justify-content-between align-items-center">
      <div>
        <h4 class="fw-bold mb-1">Reservar turno</h4>
        <p class="text-muted mb-0" style="font-size: 13px">
          Elegí mascota, motivo de consulta y horario disponible
        </p>
      </div>
      <RouterLink
        :to="{ name: 'ClienteTurnos' }"
        class="btn btn-sm btn-outline-secondary d-none d-sm-inline-flex align-items-center"
      >
        <span class="me-1">📋</span>
        Mis turnos
      </RouterLink>
    </div>

    <!-- Pasos -->
    <div class="d-flex justify-content-between align-items-center mb-3" style="font-size: 12px">
      <div class="d-flex align-items-center gap-2">
        <div :class="['step-dot', pasoActual >= 1 ? 'active' : '']">1</div>
        <div>
          <div class="fw-semibold">Mascota</div>
          <div class="text-muted" style="font-size: 11px">Elegí con quién es el turno</div>
        </div>
      </div>
      <div class="flex-grow-1 border-top mx-2" style="border-style: dashed !important;"></div>
      <div class="d-flex align-items-center gap-2">
        <div :class="['step-dot', pasoActual >= 2 ? 'active' : '']">2</div>
        <div>
          <div class="fw-semibold">Motivo</div>
          <div class="text-muted" style="font-size: 11px">Tipo de consulta o servicio</div>
        </div>
      </div>
      <div class="flex-grow-1 border-top mx-2" style="border-style: dashed !important;"></div>
      <div class="d-flex align-items-center gap-2">
        <div :class="['step-dot', pasoActual >= 3 ? 'active' : '']">3</div>
        <div>
          <div class="fw-semibold">Profesional y horario</div>
          <div class="text-muted" style="font-size: 11px">Veterinario y turno disponible</div>
        </div>
      </div>
    </div>

    <!-- Paso 1: Mascota -->
    <div v-if="pasoActual === 1" class="card border-0 shadow-sm mb-3">
      <div class="card-body">
        <h6 class="fw-bold mb-2">1. Seleccioná la mascota</h6>
        <p class="text-muted mb-3" style="font-size: 13px">
          Solo se muestran tus mascotas registradas en la clínica.
        </p>

        <div v-if="mascotas.length === 0" class="alert alert-secondary" style="font-size: 13px">
          Todavía no tenés mascotas registradas.
          <RouterLink :to="{ name: 'ClienteMascotas' }">Agregar mascota</RouterLink>.
        </div>

        <div v-else class="row g-2">
          <div
            v-for="m in mascotas"
            :key="m.id"
            class="col-12"
          >
            <button
              type="button"
              class="w-100 text-start btn btn-light d-flex align-items-center p-2 rounded-3 border"
              :class="form.mascota === m.id ? 'border-success bg-success bg-opacity-10' : 'border-light'"
              @click="seleccionarMascota(m.id)"
            >
              <div
                class="rounded-circle d-flex align-items-center justify-content-center me-3"
                style="width: 44px; height: 44px; background: #e7f5ff"
              >
                <span style="font-size: 1.4rem">
                  {{ avatarEmoji(m.especie_nombre) }}
                </span>
              </div>
              <div class="flex-grow-1">
                <div class="fw-bold" style="font-size: 14px">
                  {{ m.nombre }}
                </div>
                <div class="text-muted" style="font-size: 12px">
                  {{ m.especie_nombre }} · {{ m.raza_nombre }}
                </div>
                <div v-if="m.peso_actual" class="text-muted" style="font-size: 12px">
                  Peso: {{ m.peso_actual }} kg
                </div>
              </div>
              <div>
                <span
                  v-if="form.mascota === m.id"
                  class="badge bg-success"
                  style="font-size: 11px"
                >
                  Seleccionada
                </span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Paso 2: Servicio / Motivo -->
    <div v-if="pasoActual === 2" class="card border-0 shadow-sm mb-3">
      <div class="card-body">
        <h6 class="fw-bold mb-2">2. Motivo de la consulta</h6>
        <p class="text-muted mb-3" style="font-size: 13px">
          Elegí el servicio o motivo principal de la consulta.
        </p>

        <div class="mb-3">
          <label class="form-label fw-semibold" style="font-size: 13px">Servicio</label>
          <select
            v-model.number="form.servicio"
            class="form-select form-select-sm"
          >
            <option :value="0">Seleccioná un servicio</option>
            <option
              v-for="s in serviciosActivos"
              :key="s.id"
              :value="s.id"
            >
              {{ s.nombre }} – $ {{ s.precio }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold" style="font-size: 13px">
            Motivo detallado (opcional)
          </label>
          <textarea
            v-model="form.motivo_consulta"
            class="form-control"
            rows="2"
            placeholder="Ej: Control anual, vacunación, consulta por cojeo..."
          ></textarea>
        </div>

        <div class="alert alert-info mb-0" style="font-size: 12px">
          El valor final del turno puede variar según los procedimientos realizados durante la consulta.
        </div>
      </div>
    </div>

    <!-- Paso 3: Veterinario + Fecha y hora -->
    <div v-if="pasoActual === 3" class="card border-0 shadow-sm mb-3">
      <div class="card-body">
        <h6 class="fw-bold mb-2">3. Elegí profesional y horario</h6>
        <p class="text-muted mb-3" style="font-size: 13px">
          Seleccioná el profesional y el horario para tu turno.
        </p>

        <div class="mb-3">
          <label class="form-label fw-semibold" style="font-size: 13px">Veterinario</label>
          <select
            v-model.number="form.veterinario"
            class="form-select form-select-sm"
          >
            <option :value="0">Seleccioná un profesional</option>
            <option
              v-for="v in veterinarios"
              :key="v.id"
              :value="v.id"
            >
              {{ nombreCompletoVet(v) }}
            </option>
          </select>
        </div>

        <div class="row g-2 mb-3">
          <div class="col-12 col-sm-6">
            <label class="form-label fw-semibold" style="font-size: 13px">Fecha</label>
            <input
              v-model="fechaSeleccionada"
              type="date"
              class="form-control form-control-sm"
              :min="hoyInput"
            />
          </div>
          <div class="col-12 col-sm-6">
            <label class="form-label fw-semibold" style="font-size: 13px">Hora</label>
            <input
              v-model="horaSeleccionada"
              type="time"
              class="form-control form-control-sm"
            />
          </div>
        </div>

        <div class="alert alert-secondary mb-0" style="font-size: 12px">
          En una versión futura se limitarán los horarios según la disponibilidad del veterinario.
        </div>
      </div>
    </div>

    <!-- Resumen -->
    <div class="card border-0 shadow-sm mb-3">
      <div class="card-body">
        <h6 class="fw-bold mb-2">Resumen del turno</h6>
        <ul class="list-unstyled mb-0" style="font-size: 13px">
          <li class="d-flex justify-content-between mb-1">
            <span>Mascota</span>
            <strong>{{ resumenMascota }}</strong>
          </li>
          <li class="d-flex justify-content-between mb-1">
            <span>Servicio</span>
            <strong>{{ resumenServicio }}</strong>
          </li>
          <li class="d-flex justify-content-between mb-1">
            <span>Profesional</span>
            <strong>{{ resumenVeterinario }}</strong>
          </li>
          <li class="d-flex justify-content-between mb-1">
            <span>Fecha y hora</span>
            <strong>{{ resumenFechaHora }}</strong>
          </li>
        </ul>
      </div>
    </div>

    <!-- Navegación de pasos -->
    <div class="d-flex justify-content-between mt-3">
      <button
        class="btn btn-outline-secondary"
        type="button"
        :disabled="pasoActual === 1 || guardando"
        @click="pasoAnterior"
      >
        Atrás
      </button>
      <button
        v-if="pasoActual < 3"
        class="btn btn-success"
        type="button"
        :disabled="!puedeAvanzar || guardando"
        @click="pasoSiguiente"
      >
        Siguiente
      </button>
      <button
        v-else
        class="btn btn-success"
        type="button"
        :disabled="!puedeConfirmar || guardando"
        @click="confirmarTurno"
      >
        <span v-if="guardando" class="spinner-border spinner-border-sm me-2"></span>
        Confirmar turno
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTurnoStore } from '@/stores/turnoStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useServicioStore } from '@/stores/servicioStore'
import { useVeterinarioStore } from '@/stores/veterinarioStore'
import type { TurnoForm } from '@/interfaces/turnoInterface'
import type { Mascota } from '@/interfaces/mascotaInterface'
import type { Servicio } from '@/interfaces/servicioInterface'
import type { VeterinarioPerfil } from '@/interfaces/veterinarioPerfilInterface'

const router = useRouter()
const turnoStore = useTurnoStore()
const mascotaStore = useMascotaStore()
const servicioStore = useServicioStore()
const veterinarioStore = useVeterinarioStore()

const pasoActual = ref<number>(1)
const guardando = ref(false)

const form = ref<{
  mascota: number
  servicio: number
  motivo_consulta: string
  veterinario: number
}>({
  mascota: 0,
  servicio: 0,
  motivo_consulta: '',
  veterinario: 0,
})

const hoy = new Date()
const hoyInput = computed(() => {
  const y = hoy.getFullYear()
  const m = String(hoy.getMonth() + 1).padStart(2, '0')
  const d = String(hoy.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
})

const fechaSeleccionada = ref<string>(hoyInput.value)
const horaSeleccionada = ref<string>('09:00')

onMounted(async () => {
  await Promise.all([
    mascotaStore.obtenerTodos(),
    servicioStore.obtenerTodos(),
    veterinarioStore.obtenerTodos(),
  ])
})

const mascotas = computed<Mascota[]>(() => mascotaStore.mascotas)
const serviciosActivos = computed<Servicio[]>(() =>
  servicioStore.servicios.filter((s) => s.activo),
)
const veterinarios = computed<VeterinarioPerfil[]>(() => veterinarioStore.veterinarios)

function seleccionarMascota(id: number) {
  form.value.mascota = id
}

const puedeAvanzar = computed(() => {
  if (pasoActual.value === 1) {
    return form.value.mascota !== 0
  }
  if (pasoActual.value === 2) {
    return form.value.servicio !== 0
  }
  return true
})

const puedeConfirmar = computed(() => {
  return (
    form.value.mascota !== 0 &&
    form.value.servicio !== 0 &&
    form.value.veterinario !== 0 &&
    fechaSeleccionada.value &&
    horaSeleccionada.value
  )
})

function pasoSiguiente() {
  if (pasoActual.value < 3 && puedeAvanzar.value) {
    pasoActual.value += 1
  }
}

function pasoAnterior() {
  if (pasoActual.value > 1) {
    pasoActual.value -= 1
  }
}

const resumenMascota = computed(() => {
  const m = mascotas.value.find((x) => x.id === form.value.mascota)
  if (!m) return 'Sin seleccionar'
  return `${m.nombre} (${m.especie_nombre})`
})

const resumenServicio = computed(() => {
  const s = serviciosActivos.value.find((x) => x.id === form.value.servicio)
  if (!s) return 'Sin seleccionar'
  return s.nombre
})

const resumenVeterinario = computed(() => {
  const v = veterinarios.value.find((x) => x.id === form.value.veterinario)
  if (!v) return 'Sin seleccionar'
  return nombreCompletoVet(v)
})

const resumenFechaHora = computed(() => {
  if (!fechaSeleccionada.value || !horaSeleccionada.value) {
    return 'Sin seleccionar'
  }
  const iso = `${fechaSeleccionada.value}T${horaSeleccionada.value}:00`
  const d = new Date(iso)
  return d.toLocaleString('es-AR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
})

function buildFechaHoraISO(): string | null {
  if (!fechaSeleccionada.value || !horaSeleccionada.value) return null
  return `${fechaSeleccionada.value}T${horaSeleccionada.value}:00`
}

async function confirmarTurno() {
  if (!puedeConfirmar.value) return

  const fechaHoraIso = buildFechaHoraISO()
  if (!fechaHoraIso) return

  const payload: TurnoForm = {
    fecha_hora: fechaHoraIso,
    mascota: form.value.mascota,
    veterinario: form.value.veterinario,
    servicio: form.value.servicio,
    estado: 'reservado',
    motivo_consulta: form.value.motivo_consulta || '',
    urgencia: false,
    creado_por_cliente: true,
  }

  try {
    guardando.value = true
    await turnoStore.crear(payload)
    await turnoStore.obtenerTodos()
    router.push({ name: 'ClienteTurnos' })
  } finally {
    guardando.value = false
  }
}

function avatarEmoji(especieNombre: string | null | undefined) {
  const lower = especieNombre?.toLowerCase() ?? ''
  if (lower.includes('perro')) return '🐶'
  if (lower.includes('gato')) return '🐱'
  if (lower.includes('ave') || lower.includes('pájaro')) return '🦜'
  if (lower.includes('conejo')) return '🐰'
  return '🐾'
}

function nombreCompletoVet(v: VeterinarioPerfil): string {
  const first = v.usuario.first_name ?? ''
  const last = v.usuario.last_name ?? ''
  return `${first} ${last}`.trim() || 'Veterinario'
}
</script>

<style scoped>
.step-dot {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid #ced4da;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #adb5bd;
}
.step-dot.active {
  border-color: #198754;
  background-color: #198754;
  color: #fff;
}
</style>