<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Internaciones</h4>
      <p class="text-muted small mb-0">Pacientes hospitalizados y en observación</p>
    </div>

    <div class="d-flex gap-2 mb-3">
      <button class="btn btn-success" @click="abrirModalNueva">+ Nueva internación</button>
      <select class="form-select form-select-sm ms-auto" style="width:180px" v-model="filtroEstado">
        <option value="">Todos los estados</option>
        <option value="internado">Internado</option>
        <option value="observacion">Observación</option>
        <option value="alta">Alta</option>
      </select>
    </div>

    <div v-if="internacionStore.cargando" class="text-center text-muted py-5">
      Cargando internaciones...
    </div>

    <div v-else-if="internacionesFiltradas.length === 0" class="text-center text-muted py-5">
      No se encontraron internaciones
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Paciente</th>
              <th>Veterinario</th>
              <th>Ingreso</th>
              <th>Egreso</th>
              <th>Motivo</th>
              <th>Estado</th>
              <th style="width:220px"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in internacionesFiltradas" :key="i.id">
              <td class="fw-semibold">{{ i.mascota_nombre }}</td>
              <td class="small">{{ i.veterinario_nombre }}</td>
              <td class="small">{{ formatFecha(i.fecha_ingreso) }}</td>
              <td class="small">{{ i.fecha_egreso ? formatFecha(i.fecha_egreso) : '—' }}</td>
              <td class="small">{{ i.motivo }}</td>
              <td>
                <span class="badge" :class="badgeEstado(i.estado)">
                  {{ i.estado_display }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-1">
                  <button class="btn btn-sm btn-outline-info" @click="verEvoluciones(i)">
                    Evoluciones
                  </button>
                  <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditar(i)">
                    Editar
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminar(i)">
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL CREAR/EDITAR -->
    <div class="modal fade" id="modalInternacion" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicion ? 'Editar internación' : 'Nueva internación' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Paciente</label>
              <select class="form-select" v-model="form.mascota">
                <option :value="0">Seleccioná un paciente</option>
                <option v-for="m in mascotaStore.mascotas" :key="m.id" :value="m.id">
                  {{ m.nombre }} ({{ m.especie_nombre }})
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Veterinario responsable</label>
              <select class="form-select" v-model="form.veterinario_responsable">
                <option :value="0">Seleccioná un veterinario</option>
                <option v-for="v in veterinarioStore.veterinarios" :key="v.id" :value="v.id">
                  {{ v.usuario.first_name }} {{ v.usuario.last_name }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Motivo de internación</label>
              <textarea class="form-control" rows="2" v-model="form.motivo"></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Diagnóstico inicial</label>
              <textarea class="form-control" rows="2" v-model="form.diagnostico_ingreso"></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Estado</label>
              <select class="form-select" v-model="form.estado">
                <option value="internado">Internado</option>
                <option value="observacion">Observación</option>
                <option value="alta">Alta</option>
              </select>
            </div>
            <div class="mb-3" v-if="form.estado === 'alta'">
              <label class="form-label fw-semibold">Fecha de egreso</label>
              <input type="date" class="form-control" v-model="form.fecha_egreso" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Observaciones</label>
              <textarea class="form-control" rows="2" v-model="form.observaciones"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-success" @click="guardar" :disabled="guardando">
              {{ guardando ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL EVOLUCIONES -->
    <div class="modal fade" id="modalEvoluciones" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content" v-if="internacionSeleccionada">
          <div class="modal-header">
            <h5 class="modal-title">
              Evoluciones - {{ internacionSeleccionada.mascota_nombre }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <button class="btn btn-sm btn-success mb-3" @click="abrirModalNuevaEvolucion">
              + Nueva evolución
            </button>

            <div v-if="evolucionStore.cargando" class="text-center text-muted py-3">
              Cargando evoluciones...
            </div>
            <div v-else-if="evolucionesActuales.length === 0" class="text-muted text-center py-3">
              Sin evoluciones registradas
            </div>
            <div v-else>
              <div v-for="e in evolucionesActuales" :key="e.id" class="card mb-2">
                <div class="card-body">
                  <div class="d-flex justify-content-between mb-2">
                    <span class="fw-semibold small">{{ formatFecha(e.fecha) }}</span>
                    <span class="text-muted small">{{ e.veterinario_nombre || 'Sin veterinario' }}</span>
                  </div>
                  <div class="small mb-1"><strong>Descripción:</strong> {{ e.descripcion }}</div>
                  <div class="small text-muted" v-if="e.temperatura">Temp: {{ e.temperatura }}°C</div>
                  <div class="small text-muted" v-if="e.peso">Peso: {{ e.peso }} kg</div>
                  <div class="small text-muted" v-if="e.indicaciones">
                    <strong>Indicaciones:</strong> {{ e.indicaciones }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cerrar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL NUEVA EVOLUCIÓN -->
    <div class="modal fade" id="modalNuevaEvolucion" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Nueva evolución</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Veterinario</label>
              <select class="form-select" v-model="formEvolucion.veterinario">
                <option :value="undefined">Sin especificar</option>
                <option v-for="v in veterinarioStore.veterinarios" :key="v.id" :value="v.id">
                  {{ v.usuario.first_name }} {{ v.usuario.last_name }}
                </option>
              </select>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Temperatura (°C)</label>
                <input type="number" step="0.1" class="form-control" v-model.number="formEvolucion.temperatura" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Peso (kg)</label>
                <input type="number" step="0.1" class="form-control" v-model.number="formEvolucion.peso" />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Descripción</label>
              <textarea class="form-control" rows="3" v-model="formEvolucion.descripcion"></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Indicaciones</label>
              <textarea class="form-control" rows="2" v-model="formEvolucion.indicaciones"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-success" @click="guardarEvolucion" :disabled="guardandoEvolucion">
              {{ guardandoEvolucion ? 'Guardando...' : 'Guardar' }}
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
import { useInternacionStore } from '@/stores/internacionStore'
import { useEvolucionInternacionStore } from '@/stores/evolucionInternacionStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useVeterinarioStore } from '@/stores/veterinarioStore'
import type { Internacion, EstadoInternacion } from '@/interfaces/internacionInterface'

const internacionStore = useInternacionStore()
const evolucionStore = useEvolucionInternacionStore()
const mascotaStore = useMascotaStore()
const veterinarioStore = useVeterinarioStore()

const filtroEstado = ref<EstadoInternacion | ''>('')
const guardando = ref(false)
const guardandoEvolucion = ref(false)
const modoEdicion = ref(false)
const internacionEditando = ref<Internacion | null>(null)
const internacionSeleccionada = ref<Internacion | null>(null)

const formVacio = () => ({
  mascota: 0,
  veterinario_responsable: 0,
  motivo: '',
  diagnostico_ingreso: '',
  estado: 'internado' as EstadoInternacion,
  observaciones: '',
  fecha_egreso: '',
})

const formEvolucionVacio = () => ({
  internacion: 0,
  veterinario: undefined as number | undefined,
  temperatura: undefined as number | undefined,
  peso: undefined as number | undefined,
  descripcion: '',
  indicaciones: '',
})

const form = ref(formVacio())
const formEvolucion = ref(formEvolucionVacio())

onMounted(async () => {
  await Promise.all([
    internacionStore.obtenerTodos(),
    evolucionStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
    veterinarioStore.obtenerTodos(),
  ])
})

const internacionesFiltradas = computed(() => {
  return internacionStore.internaciones.filter(i => {
    if (!filtroEstado.value) return true
    return i.estado === filtroEstado.value
  })
})

const evolucionesActuales = computed(() => {
  if (!internacionSeleccionada.value) return []
  return evolucionStore.evoluciones
    .filter(e => e.internacion === internacionSeleccionada.value!.id)
    .sort((a, b) => b.fecha.localeCompare(a.fecha))
})

function getModal() {
  return Modal.getOrCreateInstance(document.getElementById('modalInternacion')!)
}

function getModalEvoluciones() {
  return Modal.getOrCreateInstance(document.getElementById('modalEvoluciones')!)
}

function getModalNuevaEvolucion() {
  return Modal.getOrCreateInstance(document.getElementById('modalNuevaEvolucion')!)
}

function abrirModalNueva() {
  modoEdicion.value = false
  internacionEditando.value = null
  form.value = formVacio()
  getModal().show()
}

function abrirModalEditar(i: Internacion) {
  modoEdicion.value = true
  internacionEditando.value = i
  form.value = {
    mascota: i.mascota,
    veterinario_responsable: i.veterinario_responsable,
    motivo: i.motivo,
    diagnostico_ingreso: i.diagnostico_ingreso || '',
    estado: i.estado,
    observaciones: i.observaciones || '',
    fecha_egreso: i.fecha_egreso || '',
  }
  getModal().show()
}

function verEvoluciones(i: Internacion) {
  internacionSeleccionada.value = i
  getModalEvoluciones().show()
}

function abrirModalNuevaEvolucion() {
  formEvolucion.value = formEvolucionVacio()
  formEvolucion.value.internacion = internacionSeleccionada.value!.id
  getModalNuevaEvolucion().show()
}

async function guardar() {
  if (!form.value.mascota || !form.value.veterinario_responsable || !form.value.motivo) {
    Swal.fire('Campos requeridos', 'Completá mascota, veterinario y motivo.', 'warning')
    return
  }

  guardando.value = true
  try {
    const payload = {
      mascota: form.value.mascota,
      veterinario_responsable: form.value.veterinario_responsable,
      motivo: form.value.motivo,
      diagnostico_ingreso: form.value.diagnostico_ingreso || undefined,
      estado: form.value.estado,
      observaciones: form.value.observaciones || undefined,
      fecha_egreso: form.value.fecha_egreso || undefined,
    }

    if (modoEdicion.value && internacionEditando.value) {
      await internacionStore.actualizar(internacionEditando.value.id, payload)
      Swal.fire({ icon: 'success', title: 'Internación actualizada', timer: 1500, showConfirmButton: false })
    } else {
      await internacionStore.crear(payload)
      Swal.fire({ icon: 'success', title: 'Internación creada', timer: 1500, showConfirmButton: false })
    }
    await internacionStore.obtenerTodos()
    getModal().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar la internación.', 'error')
  } finally {
    guardando.value = false
  }
}

async function guardarEvolucion() {
  if (!formEvolucion.value.descripcion) {
    Swal.fire('Campo requerido', 'La descripción es obligatoria.', 'warning')
    return
  }

  guardandoEvolucion.value = true
  try {
    await evolucionStore.crear(formEvolucion.value)
    await evolucionStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Evolución registrada', timer: 1500, showConfirmButton: false })
    getModalNuevaEvolucion().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar la evolución.', 'error')
  } finally {
    guardandoEvolucion.value = false
  }
}

async function confirmarEliminar(i: Internacion) {
  const result = await Swal.fire({
    title: '¿Eliminar internación?',
    text: i.mascota_nombre,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })

  if (result.isConfirmed) {
    await internacionStore.eliminar(i.id)
    await internacionStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Internación eliminada', timer: 1500, showConfirmButton: false })
  }
}

function formatFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function badgeEstado(estado: EstadoInternacion) {
  const map: Record<EstadoInternacion, string> = {
    internado: 'bg-danger',
    observacion: 'bg-warning text-dark',
    alta: 'bg-success',
  }
  return map[estado] ?? 'bg-secondary'
}
</script>