<template>
  <div>
    <!-- Breadcrumb -->
    <nav class="mb-3">
      <ol class="breadcrumb">
        <li class="breadcrumb-item">
          <RouterLink to="/admin/pacientes">Pacientes</RouterLink>
        </li>
        <li class="breadcrumb-item active">{{ mascota?.nombre ?? 'Cargando...' }}</li>
      </ol>
    </nav>

    <div v-if="mascotaStore.cargando" class="text-center text-muted py-5">Cargando...</div>

    <div v-else-if="!mascota" class="text-center text-muted py-5">Paciente no encontrado</div>

    <div v-else>
      <!-- Header -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body d-flex align-items-center gap-3">
          <div
            class="rounded-circle bg-success bg-opacity-10 d-flex align-items-center justify-content-center flex-shrink-0"
            style="width:64px;height:64px;font-size:2rem"
          >
            🐾
          </div>
          <div class="flex-grow-1">
            <h5 class="fw-bold mb-1">{{ mascota.nombre }}</h5>
            <p class="text-muted small mb-1">
              {{ mascota.especie_nombre }} · {{ mascota.raza_nombre }} · {{ mascota.sexo_display }}
            </p>
            <p class="text-muted small mb-0">
              Dueño: <strong>{{ mascota.usuario_nombre }}</strong>
              <span v-if="mascota.peso_actual"> · Peso: {{ mascota.peso_actual }} kg</span>
              <span v-if="mascota.microchip"> · Microchip: {{ mascota.microchip }}</span>
            </p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-outline-secondary btn-sm" @click="abrirModalEditar">Editar</button>
            <button class="btn btn-success btn-sm" @click="abrirModalConsulta">+ Consulta</button>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <!-- Vacunas -->
        <div class="col-md-6">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <span class="fw-semibold">Vacunas</span>
              <button class="btn btn-sm btn-success" @click="abrirModalVacuna">+ Agregar</button>
            </div>
            <div class="card-body p-0">
              <div v-if="vacunaStore.cargando" class="text-center text-muted py-3">Cargando...</div>
              <div v-else-if="vacunasMascota.length === 0" class="text-center text-muted py-3 small">
                Sin vacunas registradas
              </div>
              <table v-else class="table table-sm table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Vacuna</th>
                    <th>Aplicada</th>
                    <th>Próxima</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="v in vacunasMascota" :key="v.id">
                    <td>{{ v.nombre }}</td>
                    <td class="small">{{ formatearFecha(v.fecha_aplicacion) }}</td>
                    <td class="small">{{ v.fecha_proxima ? formatearFecha(v.fecha_proxima) : '—' }}</td>
                    <td>
                      <span class="badge" :class="estadoVacuna(v.fecha_proxima)">
                        {{ etiquetaVacuna(v.fecha_proxima) }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Turnos -->
        <div class="col-md-6">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white">
              <span class="fw-semibold">Últimos turnos</span>
            </div>
            <div class="card-body p-0">
              <div v-if="turnosMascota.length === 0" class="text-center text-muted py-3 small">
                Sin turnos registrados
              </div>
              <table v-else class="table table-sm table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Fecha</th>
                    <th>Servicio</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="t in turnosMascota.slice(0, 5)" :key="t.id">
                    <td class="small">{{ t.fecha_hora ? formatearFechaHora(t.fecha_hora) : '—' }}</td>
                    <td class="small">{{ t.servicio_nombre }}</td>
                    <td>
                      <span class="badge" :class="insigniaEstado(t.estado)">{{ t.estado_display }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Consultas -->
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white">
              <span class="fw-semibold">Historia clínica</span>
            </div>
            <div class="card-body p-0">
              <div v-if="consultaStore.cargando" class="text-center text-muted py-3">Cargando...</div>
              <div v-else-if="consultasMascota.length === 0" class="text-center text-muted py-3 small">
                Sin consultas registradas
              </div>
              <table v-else class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Veterinario</th>
                    <th>Diagnóstico</th>
                    <th>Peso</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in consultasMascota" :key="c.id">
                    <td class="small">{{ formatearFecha(c.fecha) }}</td>
                    <td><span class="badge bg-secondary">{{ c.tipo_display }}</span></td>
                    <td class="small">{{ c.veterinario_nombre ?? '—' }}</td>
                    <td class="small">{{ c.diagnostico ?? '—' }}</td>
                    <td class="small">{{ c.peso_actual ? c.peso_actual + ' kg' : '—' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL VACUNA -->
    <div class="modal fade" id="modalVacuna" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Registrar vacuna</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Nombre vacuna</label>
              <input type="text" class="form-control" v-model="formVacuna.nombre" />
            </div>
            <div class="row">
              <div class="col mb-3">
                <label class="form-label fw-semibold">Fecha aplicación</label>
                <input type="date" class="form-control" v-model="formVacuna.fecha_aplicacion" />
              </div>
              <div class="col mb-3">
                <label class="form-label fw-semibold">Próxima dosis</label>
                <input type="date" class="form-control" v-model="formVacuna.fecha_proxima" />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Observaciones</label>
              <textarea class="form-control" rows="2" v-model="formVacuna.observaciones"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-success" @click="guardarVacuna" :disabled="guardando">
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
import { useRoute } from 'vue-router'
import { Modal } from 'bootstrap'
import Swal from 'sweetalert2'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useVacunaStore } from '@/stores/vacunaStore'
import { useTurnoStore } from '@/stores/turnoStore'
import { useConsultaStore } from '@/stores/consultaStore'
import type { EstadoTurno } from '@/interfaces/turnoInterface'
import type { ConsultaClinica } from '@/interfaces/consultaClinicaInterface'

const route = useRoute()
const mascotaStore = useMascotaStore()
const vacunaStore = useVacunaStore()
const turnoStore = useTurnoStore()
const consultaStore = useConsultaStore()

const guardando = ref(false)

const formVacuna = ref({
  mascota: 0,
  nombre: '',
  fecha_aplicacion: new Date().toISOString().slice(0, 10),
  fecha_proxima: '',
  observaciones: '',
})

const idMascota = computed(() => Number(route.params.id))

const mascota = computed(() =>
  mascotaStore.mascotas.find((m) => m.id === idMascota.value) ?? null
)

const vacunasMascota = computed(() =>
  vacunaStore.vacunas.filter((v) => v.mascota === idMascota.value)
)

const turnosMascota = computed(() =>
  turnoStore.turnos
    .filter((t) => t.mascota_id === idMascota.value && t.fecha_hora)
    .sort((a, b) => b.fecha_hora!.localeCompare(a.fecha_hora!))
)

const consultasMascota = computed(() =>
  consultaStore.consultas
    .filter((c: ConsultaClinica) => c.mascota === idMascota.value)
    .sort((a: ConsultaClinica, b: ConsultaClinica) => b.fecha.localeCompare(a.fecha))
)

onMounted(async () => {
  await Promise.all([
    mascotaStore.obtenerTodos(),
    vacunaStore.obtenerTodos(),
    turnoStore.obtenerTodos(),
    consultaStore.obtenerTodos(),
  ])
})

function formatearFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString('es-AR', { day: 'numeric', month: 'short', year: 'numeric' })
}

function formatearFechaHora(fechaHora: string) {
  return new Date(fechaHora).toLocaleDateString('es-AR', { day: 'numeric', month: 'short' }) +
    ' ' + new Date(fechaHora).toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })
}

function estadoVacuna(fechaProxima: string | null) {
  if (!fechaProxima) return 'bg-secondary'
  const dias = Math.ceil((new Date(fechaProxima).getTime() - new Date().setHours(0,0,0,0)) / 86400000)
  if (dias < 0) return 'bg-danger'
  if (dias <= 30) return 'bg-warning text-dark'
  return 'bg-success'
}

function etiquetaVacuna(fechaProxima: string | null) {
  if (!fechaProxima) return 'Sin próxima'
  const dias = Math.ceil((new Date(fechaProxima).getTime() - new Date().setHours(0,0,0,0)) / 86400000)
  if (dias < 0) return 'Vencida'
  if (dias <= 30) return `${dias} días`
  return 'Al día'
}

function insigniaEstado(estado: EstadoTurno) {
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

function obtenerModalVacuna() {
  return Modal.getOrCreateInstance(document.getElementById('modalVacuna')!)
}

function abrirModalVacuna() {
  formVacuna.value = {
    mascota: idMascota.value,
    nombre: '',
    fecha_aplicacion: new Date().toISOString().slice(0, 10),
    fecha_proxima: '',
    observaciones: '',
  }
  obtenerModalVacuna().show()
}

function abrirModalEditar() {
  Swal.fire('Info', 'Editá el paciente desde el listado de Pacientes.', 'info')
}

function abrirModalConsulta() {
  Swal.fire('Info', 'Creá la consulta desde Historia Clínica.', 'info')
}

async function guardarVacuna() {
  if (!formVacuna.value.nombre || !formVacuna.value.fecha_aplicacion) {
    Swal.fire('Campos requeridos', 'Nombre y fecha de aplicación son obligatorios.', 'warning')
    return
  }
  guardando.value = true
  try {
    await vacunaStore.crear(formVacuna.value)
    await vacunaStore.obtenerTodos()
    obtenerModalVacuna().hide()
    Swal.fire({ icon: 'success', title: 'Vacuna registrada', timer: 1500, showConfirmButton: false })
  } catch {
    Swal.fire('Error', 'No se pudo registrar la vacuna.', 'error')
  } finally {
    guardando.value = false
  }
}
</script>