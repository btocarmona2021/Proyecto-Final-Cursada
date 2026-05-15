<template>
  <div>
    <!-- Encabezado -->
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Agenda de Turnos</h4>
      <p class="text-muted small mb-0">Gestión de citas y calendario</p>
    </div>

    <!-- Controles -->
    <div class="d-flex flex-wrap gap-2 mb-4 align-items-center">
      <button class="btn btn-success" @click="abrirModalNuevo">
        ➕ Nuevo turno
      </button>
      <button class="btn btn-outline-secondary" @click="irHoy">Hoy</button>
      <button class="btn btn-outline-secondary" @click="cambiarMes(-1)">◀</button>
      <button class="btn btn-outline-secondary" @click="cambiarMes(1)">▶</button>
      <span class="fw-bold">{{ mesAnioLabel }}</span>

      <input 
        type="date" 
        class="form-control form-control-sm ms-auto" 
        style="width: 180px"
        v-model="fechaSeleccionada"
      />
    </div>

    <!-- Filtros de estado -->
    <div class="d-flex gap-2 mb-3 flex-wrap">
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

    <!-- Tabla de turnos -->
    <div class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <div v-if="turnoStore.cargando" class="text-center text-muted py-5">
          Cargando turnos...
        </div>
        <div v-else-if="turnosFiltrados.length === 0" class="text-center text-muted py-5">
          No hay turnos para la fecha seleccionada
        </div>
        <table v-else class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th style="width: 100px">Fecha</th>
              <th style="width: 80px">Inicio</th>
              <th style="width: 80px">Fin</th>
              <th>Paciente</th>
              <th>Dueño</th>
              <th>Servicio</th>
              <th>Veterinario</th>
              <th style="width: 120px">Estado</th>
              <th style="width: 140px"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="turno in turnosFiltrados" :key="turno.id">
              <td class="small text-muted">{{ formatFecha(turno.fecha_hora) }}</td>
              <td class="fw-bold">{{ formatHora(turno.fecha_hora) }}</td>
              <td class="fw-bold text-success">{{ formatHora(turno.hora_fin) }}</td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <span class="badge bg-success-subtle text-success-emphasis rounded-circle" style="width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-size: 14px;">
                    🐾
                  </span>
                  <span class="fw-semibold">{{ turno.mascota_nombre }}</span>
                </div>
              </td>
              <td class="text-muted small">{{ turno.dueno_nombre || 'Sin dueño' }}</td>
              <td>{{ turno.servicio_nombre }}</td>
              <td>{{ turno.veterinario_nombre }}</td>
              <td>
                <span class="badge" :class="badgeEstado(turno.estado)">
                  {{ turno.estado_display }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-1">
                  <button class="btn btn-sm btn-outline-secondary" @click="abrirModalEditar(turno)">
                    Editar
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminar(turno)">
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL NUEVO/EDITAR TURNO -->
    <div class="modal fade" id="modalTurno" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicion ? 'Editar turno' : 'Nuevo turno' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <!-- Fecha y hora -->
            <div class="mb-3">
              <label class="form-label fw-semibold">Fecha y hora</label>
              <input 
                type="datetime-local" 
                class="form-control" 
                v-model="form.fecha_hora"
              />
            </div>

            <!-- Mascota -->
            <div class="mb-3">
              <label class="form-label fw-semibold">Mascota</label>
              <select class="form-select" v-model="form.mascota">
                <option :value="0">Seleccioná una mascota</option>
                <option 
                  v-for="m in mascotaStore.mascotas" 
                  :key="m.id" 
                  :value="m.id"
                >
                  {{ m.nombre }} ({{ m.especie_nombre }})
                </option>
              </select>
            </div>

            <!-- Veterinario -->
            <div class="mb-3">
              <label class="form-label fw-semibold">Veterinario</label>
              <select class="form-select" v-model="form.veterinario">
                <option :value="0">Seleccioná un veterinario</option>
                <option 
                  v-for="v in veterinarioStore.veterinarios" 
                  :key="v.id" 
                  :value="v.id"
                >
                  {{ nombreCompletoVet(v) }}
                </option>
              </select>
            </div>

            <!-- Servicio -->
            <div class="mb-3">
              <label class="form-label fw-semibold">Servicio</label>
              <select class="form-select" v-model="form.servicio">
                <option :value="0">Seleccioná un servicio</option>
                <option 
                  v-for="s in servicioStore.servicios" 
                  :key="s.id" 
                  :value="s.id"
                >
                  {{ s.nombre }}
                </option>
              </select>
            </div>

            <!-- Estado -->
            <div class="mb-3">
              <label class="form-label fw-semibold">Estado</label>
              <select class="form-select" v-model="form.estado">
                <option value="reservado">Reservado</option>
                <option value="confirmado">Confirmado</option>
                <option value="en_espera">En espera</option>
                <option value="en_consulta">En consulta</option>
                <option value="atendido">Atendido</option>
                <option value="cancelado">Cancelado</option>
              </select>
            </div>

            <!-- Motivo consulta -->
            <div class="mb-3">
              <label class="form-label fw-semibold">Motivo de consulta</label>
              <textarea 
                class="form-control" 
                rows="2" 
                v-model="form.motivo_consulta"
                placeholder="Descripción del motivo de la consulta"
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button 
              class="btn btn-success" 
              @click="guardar" 
              :disabled="guardando"
            >
              {{ guardando ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import Swal from 'sweetalert2'
import { useTurnoStore } from '@/stores/turnoStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useServicioStore } from '@/stores/servicioStore'
import { useVeterinarioStore } from '@/stores/veterinarioStore'
import type { Turno, EstadoTurno, TurnoForm } from '@/interfaces/turnoInterface'
import type { VeterinarioPerfil } from '@/interfaces/veterinarioPerfilInterface'

const turnoStore = useTurnoStore()
const mascotaStore = useMascotaStore()
const servicioStore = useServicioStore()
const veterinarioStore = useVeterinarioStore()

const fechaSeleccionada = ref(obtenerFechaLocal())
const filtroEstado = ref<string>('')
const modoEdicion = ref(false)
const turnoEditando = ref<Turno | null>(null)
const guardando = ref(false)

const formVacio: TurnoForm = {
  fecha_hora: '',
  mascota: 0,
  veterinario: 0,
  servicio: 0,
  estado: 'reservado',
  motivo_consulta: '',
  urgencia: false,
}

const form = ref<TurnoForm>({ ...formVacio })

const opcionesEstado = [
  { value: '', label: 'Todos' },
  { value: 'reservado', label: 'Reservado' },
  { value: 'confirmado', label: 'Confirmado' },
  { value: 'en_espera', label: 'En espera' },
  { value: 'en_consulta', label: 'En consulta' },
  { value: 'atendido', label: 'Atendido' },
  { value: 'cancelado', label: 'Cancelado' },
]

onMounted(async () => {
  await Promise.all([
    turnoStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
    servicioStore.obtenerTodos(),
    veterinarioStore.obtenerTodos(),
  ])
})

function obtenerFechaLocal(): string {
  const hoy = new Date()
  const year = hoy.getFullYear()
  const month = String(hoy.getMonth() + 1).padStart(2, '0')
  const day = String(hoy.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const mesAnioLabel = computed(() => {
  const [yearStr, monthStr, dayStr] = fechaSeleccionada.value.split('-')
  const year = parseInt(yearStr || '0')
  const month = parseInt(monthStr || '0')
  const day = parseInt(dayStr || '0')
  
  const d = new Date(year, month - 1, day)
  return d.toLocaleDateString('es-AR', { month: 'long', year: 'numeric' })
    .replace(/^\w/, (c) => c.toUpperCase())
})

const turnosFiltrados = computed(() => {
  return turnoStore.turnos
    .filter((t) => {
      if (!t.fecha_hora) return false

      const mismaFecha = t.fecha_hora.startsWith(fechaSeleccionada.value)
      const mismoEstado = filtroEstado.value ? t.estado === filtroEstado.value : true
      return mismaFecha && mismoEstado
    })
    .sort((a, b) => a.fecha_hora!.localeCompare(b.fecha_hora!))
})

function cambiarMes(n: number) {
  const [yearStr, monthStr, dayStr] = fechaSeleccionada.value.split('-')
  const year = parseInt(yearStr || '0')
  const month = parseInt(monthStr || '0')
  const day = parseInt(dayStr || '0')
  
  const d = new Date(year, month - 1 + n, day)
  
  const newYear = d.getFullYear()
  const newMonth = String(d.getMonth() + 1).padStart(2, '0')
  const newDay = String(d.getDate()).padStart(2, '0')
  
  fechaSeleccionada.value = `${newYear}-${newMonth}-${newDay}`
}

function irHoy() {
  fechaSeleccionada.value = obtenerFechaLocal()
}

function formatFecha(fecha_hora: string) {
  return new Date(fecha_hora).toLocaleDateString('es-AR', {
    day: '2-digit',
    month: '2-digit',
  })
}

function formatHora(fecha_hora: string | null | undefined) {
  if (!fecha_hora) return '-'
  return new Date(fecha_hora).toLocaleTimeString('es-AR', {
    hour: '2-digit',
    minute: '2-digit',
  })
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

function nombreCompletoVet(vet: VeterinarioPerfil): string {
  return `${vet.usuario.first_name} ${vet.usuario.last_name}`
}

function getModal() {
  return Modal.getOrCreateInstance(document.getElementById('modalTurno')!)
}

function abrirModalNuevo() {
  modoEdicion.value = false
  turnoEditando.value = null
  form.value = { ...formVacio }
  form.value.fecha_hora = `${fechaSeleccionada.value}T09:00`
  getModal().show()
}

function abrirModalEditar(turno: Turno) {
  modoEdicion.value = true
  turnoEditando.value = turno
  form.value = {
    fecha_hora: turno.fecha_hora.slice(0, 16),
    mascota: turno.mascota_id,
    veterinario: turno.veterinario_id,
    servicio: turno.servicio_id,
    estado: turno.estado,
    motivo_consulta: turno.motivo_consulta ?? '',
    urgencia: false,
  }
  getModal().show()
}

async function guardar() {
  if (guardando.value) return
  
  const mascota = Number(form.value.mascota)
  const veterinario = Number(form.value.veterinario)
  const servicio = Number(form.value.servicio)

  if (!form.value.fecha_hora || mascota === 0 || veterinario === 0 || servicio === 0) {
    Swal.fire('Campos requeridos', 'Completá todos los campos obligatorios.', 'warning')
    return
  }

  guardando.value = true
  const payload: TurnoForm = {
    ...form.value,
    mascota,
    veterinario,
    servicio,
  }

  try {
    if (modoEdicion.value && turnoEditando.value) {
      await turnoStore.actualizar(turnoEditando.value.id, payload)
    } else {
      await turnoStore.crear(payload)
    }
    
    await turnoStore.obtenerTodos()
    getModal().hide()
    
    Swal.fire({
      icon: 'success',
      title: modoEdicion.value ? 'Turno actualizado' : 'Turno creado',
      timer: 1500,
      showConfirmButton: false,
    })
    
  } catch (error: unknown) {
    let mensajeError = 'No se pudo guardar el turno.'
    
    if (error && typeof error === 'object' && 'response' in error) {
      const axiosError = error as { response?: { data?: Record<string, unknown> } }
      if (axiosError.response?.data) {
        const errores = axiosError.response.data
        const mensajes = Object.entries(errores)
          .map(([campo, msgs]) => {
            const textos = Array.isArray(msgs) ? msgs.join(', ') : String(msgs)
            return `<strong>${campo}:</strong> ${textos}`
          })
          .join('<br>')
        
        mensajeError = mensajes
      }
    }
    
    Swal.fire({
      icon: 'error',
      title: 'Error al guardar',
      html: mensajeError,
    })
  } finally {
    guardando.value = false
  }
}

async function confirmarEliminar(turno: Turno) {
  const result = await Swal.fire({
    title: 'Eliminar turno?',
    text: `${turno.mascota_nombre} — ${formatHora(turno.fecha_hora)}`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })

  if (result.isConfirmed) {
    await turnoStore.eliminar(turno.id)
    await turnoStore.obtenerTodos()
    Swal.fire({
      icon: 'success',
      title: 'Turno eliminado',
      timer: 1500,
      showConfirmButton: false,
    })
  }
}
</script>