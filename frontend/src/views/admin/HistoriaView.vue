<!-- src/views/admin/HistoriaView.vue -->
<template>
  <div class="container-fluid">
    <!-- Encabezado -->
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Historia Clínica</h4>
      <p class="text-muted small mb-0">
        Registro de consultas clínicas, diagnósticos y tratamientos de todos los pacientes.
      </p>
    </div>

    <!-- Filtros -->
    <div class="card border-0 shadow-sm mb-3">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-12 col-md-4">
            <label class="form-label small fw-semibold">Buscar</label>
            <input
              v-model="busqueda"
              type="text"
              class="form-control form-control-sm"
              placeholder="Paciente, dueño, diagnóstico..."
            />
          </div>

          <div class="col-6 col-md-3">
            <label class="form-label small fw-semibold">Fecha desde</label>
            <input
              v-model="filtros.fechaDesde"
              type="date"
              class="form-control form-control-sm"
            />
          </div>

          <div class="col-6 col-md-3">
            <label class="form-label small fw-semibold">Fecha hasta</label>
            <input
              v-model="filtros.fechaHasta"
              type="date"
              class="form-control form-control-sm"
            />
          </div>

          <div class="col-12 col-md-2 d-flex justify-content-end">
            <button
              type="button"
              class="btn btn-success btn-sm w-100"
              @click="abrirModalNueva"
            >
              Nueva consulta
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Estado de carga -->
    <div
      v-if="cargando"
      class="text-center text-muted py-5"
      style="font-size: 13px"
    >
      Cargando historia clínica...
    </div>

    <!-- Sin datos -->
    <div
      v-else-if="consultasFiltradas.length === 0"
      class="text-center text-muted py-5"
      style="font-size: 13px"
    >
      No se encontraron consultas clínicas para los filtros seleccionados.
    </div>

    <!-- Tabla de consultas -->
    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th style="width: 120px">Fecha</th>
              <th>Paciente</th>
              <th>Dueño</th>
              <th>Tipo</th>
              <th>Diagnóstico</th>
              <th>Veterinario</th>
              <th style="width: 120px"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="c in consultasFiltradas"
              :key="c.id"
            >
              <td class="small">
                {{ formatFecha(c.fecha) }}
              </td>
              <td class="small fw-semibold">
                {{ c.mascota_nombre }}
              </td>
              <td class="small">
                {{ obtenerDuenoNombre(c.mascota) }}
              </td>
              <td>
                <span class="badge bg-secondary" style="font-size: 11px">
                  {{ c.tipo_display }}
                </span>
              </td>
              <td class="small">
                {{ c.diagnostico || c.motivo_consulta || 'Sin diagnóstico' }}
              </td>
              <td class="small">
                {{ c.veterinario_nombre || 'Sin asignar' }}
              </td>
              <td>
                <div class="d-flex gap-1 justify-content-end">
                  <button
                    type="button"
                    class="btn btn-sm btn-outline-secondary"
                    @click="abrirModalEditar(c)"
                  >
                    Editar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal crear/editar consulta -->
    <div
      id="modalConsulta"
      class="modal fade"
      tabindex="-1"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ modoEdicion ? 'Editar consulta' : 'Nueva consulta' }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12 col-md-6">
                <label class="form-label small fw-semibold">Paciente</label>
                <select
                  v-model.number="form.mascota"
                  class="form-select form-select-sm"
                >
                  <option :value="0">Seleccioná un paciente</option>
                  <option
                    v-for="m in mascotas"
                    :key="m.id"
                    :value="m.id"
                  >
                    {{ m.nombre }} · {{ m.especie_nombre }} ({{ m.usuario_nombre }})
                  </option>
                </select>
              </div>

              <div class="col-12 col-md-6">
                <label class="form-label small fw-semibold">Veterinario</label>
                <select
                  v-model.number="form.veterinario"
                  class="form-select form-select-sm"
                >
                  <option :value="0">Sin especificar</option>
                  <option
                    v-for="v in veterinarios"
                    :key="v.id"
                    :value="v.id"
                  >
                    {{ nombreCompletoVet(v) }}
                  </option>
                </select>
              </div>

              <div class="col-12 col-md-4">
                <label class="form-label small fw-semibold">Fecha</label>
                <input
                  v-model="form.fecha"
                  type="date"
                  class="form-control form-control-sm"
                />
              </div>

              <div class="col-12 col-md-4">
                <label class="form-label small fw-semibold">Tipo de consulta</label>
                <select
                  v-model="form.tipo"
                  class="form-select form-select-sm"
                >
                  <option value="control">Control</option>
                  <option value="vacunacion">Vacunación</option>
                  <option value="cirugia">Cirugía</option>
                  <option value="urgencia">Urgencia</option>
                  <option value="postoperatorio">Postoperatorio</option>
                  <option value="desparasitacion">Desparasitación</option>
                  <option value="otro">Otro</option>
                </select>
              </div>

              <div class="col-12 col-md-4">
                <label class="form-label small fw-semibold">Peso actual (kg)</label>
                <input
                  v-model.number="form.peso_actual"
                  type="number"
                  step="0.1"
                  class="form-control form-control-sm"
                />
              </div>

              <div class="col-12">
                <label class="form-label small fw-semibold">Motivo de consulta</label>
                <textarea
                  v-model="form.motivo_consulta"
                  rows="2"
                  class="form-control"
                ></textarea>
              </div>

              <div class="col-12">
                <label class="form-label small fw-semibold">Diagnóstico</label>
                <textarea
                  v-model="form.diagnostico"
                  rows="2"
                  class="form-control"
                ></textarea>
              </div>

              <div class="col-12">
                <label class="form-label small fw-semibold">Tratamiento / indicaciones</label>
                <textarea
                  v-model="form.tratamiento"
                  rows="2"
                  class="form-control"
                ></textarea>
              </div>

              <div class="col-12">
                <label class="form-label small fw-semibold">Observaciones</label>
                <textarea
                  v-model="form.observaciones"
                  rows="2"
                  class="form-control"
                ></textarea>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-secondary"
              data-bs-dismiss="modal"
            >
              Cancelar
            </button>
            <button
              type="button"
              class="btn btn-success"
              :disabled="guardando"
              @click="guardar"
            >
              <span
                v-if="guardando"
                class="spinner-border spinner-border-sm me-2"
              ></span>
              Guardar consulta
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Modal } from 'bootstrap'
import Swal from 'sweetalert2'

import { useConsultaStore } from '@/stores/consultaStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import { useVeterinarioStore } from '@/stores/veterinarioStore'

import type { Mascota } from '@/interfaces/mascotaInterface'
import type { VeterinarioPerfil } from '@/interfaces/veterinarioPerfilInterface'

// OJO: ahora usamos el tipo que refleja la API real
type ConsultaApi = {
  id: number
  mascota: number
  mascota_nombre: string
  veterinario: number | null
  veterinario_nombre: string | null
  turno: number | null
  fecha: string
  tipo: string
  tipo_display: string
  motivo_consulta: string | null
  diagnostico: string | null
  tratamiento: string | null
  observaciones: string | null
  peso_actual: string | null
  temperatura: string | null
  frecuencia_cardiaca: number | null
  frecuencia_respiratoria: number | null
  proxima_visita: string | null
  recetas: unknown[]
  created_at: string
  updated_at: string
  activo: boolean
}

import type { ConsultaClinicaForm } from '@/interfaces/consultaClinicaInterface'

const route = useRoute()
const consultaStore = useConsultaStore()
const mascotaStore = useMascotaStore()
const veterinarioStore = useVeterinarioStore()

const busqueda = ref('')
const filtros = ref<{
  fechaDesde: string
  fechaHasta: string
}>({
  fechaDesde: new Date(
    new Date().getFullYear(),
    new Date().getMonth(),
    1,
  )
    .toISOString()
    .slice(0, 10),
  fechaHasta: new Date().toISOString().slice(0, 10),
})

const guardando = ref(false)
const modoEdicion = ref(false)
const consultaEditando = ref<ConsultaApi | null>(null)

const form = ref<ConsultaClinicaForm>({
  mascota: 0,
  veterinario: undefined,
  turno: undefined,
  fecha: new Date().toISOString().slice(0, 10),
  tipo: 'control',
  motivo_consulta: '',
  diagnostico: '',
  tratamiento: '',
  observaciones: '',
  peso_actual: undefined,
  temperatura: undefined,
  frecuencia_cardiaca: undefined,
  frecuencia_respiratoria: undefined,
  proxima_visita: undefined,
})

onMounted(async () => {
  await Promise.all([
    consultaStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
    veterinarioStore.obtenerTodos(),
  ])

  const mascotaParam = route.query.mascota
  if (mascotaParam) {
    const id = Number(mascotaParam)
    if (!Number.isNaN(id)) {
      form.value.mascota = id
    }
  }
})

const cargando = computed(
  () =>
    consultaStore.cargando ||
    mascotaStore.cargando ||
    veterinarioStore.cargando,
)

// Aquí asumimos que consultaStore.consultas es el array crudo de la API
const consultas = computed<ConsultaApi[]>(() => consultaStore.consultas as unknown as ConsultaApi[])
const mascotas = computed<Mascota[]>(() => mascotaStore.mascotas)
const veterinarios = computed<VeterinarioPerfil[]>(
  () => veterinarioStore.veterinarios,
)

const consultasFiltradas = computed<ConsultaApi[]>(() => {
  const term = busqueda.value.trim().toLowerCase()
  const desde = filtros.value.fechaDesde
  const hasta = filtros.value.fechaHasta

  return consultas.value
    .filter((c) => {
      if (!c.fecha) return false
      const fechaStr = c.fecha.slice(0, 10)
      const cumpleFecha =
        (!desde || fechaStr >= desde) &&
        (!hasta || fechaStr <= hasta)

      const texto = (
        (c.mascota_nombre ?? '') +
        ' ' +
        (obtenerDuenoNombre(c.mascota) ?? '') +
        ' ' +
        (c.veterinario_nombre ?? '') +
        ' ' +
        (c.diagnostico ?? '') +
        ' ' +
        (c.motivo_consulta ?? '')
      ).toLowerCase()

      const cumpleBusqueda = term ? texto.includes(term) : true

      return cumpleFecha && cumpleBusqueda
    })
    .sort((a, b) => b.fecha.localeCompare(a.fecha))
})

function obtenerDuenoNombre(mascotaId: number): string {
  const m = mascotas.value.find((x) => x.id === mascotaId)
  return m?.usuario_nombre ?? ''
}

function nombreCompletoVet(v: VeterinarioPerfil): string {
  const first = v.usuario.first_name ?? ''
  const last = v.usuario.last_name ?? ''
  return `${first} ${last}`.trim() || 'Veterinario'
}

function formatFecha(iso: string | null | undefined): string {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function getModal(): Modal {
  return Modal.getOrCreateInstance(
    document.getElementById('modalConsulta') as HTMLElement,
  )
}

function abrirModalNueva() {
  modoEdicion.value = false
  consultaEditando.value = null
  form.value = {
    mascota: form.value.mascota || 0,
    veterinario: undefined,
    turno: undefined,
    fecha: new Date().toISOString().slice(0, 10),
    tipo: 'control',
    motivo_consulta: '',
    diagnostico: '',
    tratamiento: '',
    observaciones: '',
    peso_actual: undefined,
    temperatura: undefined,
    frecuencia_cardiaca: undefined,
    frecuencia_respiratoria: undefined,
    proxima_visita: undefined,
  }
  getModal().show()
}

function abrirModalEditar(c: ConsultaApi) {
  modoEdicion.value = true
  consultaEditando.value = c
  form.value = {
    mascota: c.mascota,
    veterinario: c.veterinario ?? undefined,
    turno: c.turno ?? undefined,
    fecha: c.fecha
      ? c.fecha.slice(0, 10)
      : new Date().toISOString().slice(0, 10),
    tipo: c.tipo as ConsultaClinicaForm['tipo'],
    motivo_consulta: c.motivo_consulta ?? '',
    diagnostico: c.diagnostico ?? '',
    tratamiento: c.tratamiento ?? '',
    observaciones: c.observaciones ?? '',
    peso_actual: c.peso_actual
      ? Number(c.peso_actual as unknown as string)
      : undefined,
    temperatura: c.temperatura
      ? Number(c.temperatura as unknown as string)
      : undefined,
    frecuencia_cardiaca: c.frecuencia_cardiaca ?? undefined,
    frecuencia_respiratoria: c.frecuencia_respiratoria ?? undefined,
    proxima_visita: c.proxima_visita ?? undefined,
  }
  getModal().show()
}

async function guardar() {
  if (!form.value.mascota || !form.value.fecha || !form.value.tipo) {
    await Swal.fire(
      'Campos requeridos',
      'Completá al menos paciente, fecha y tipo de consulta.',
      'warning',
    )
    return
  }

  const payload: ConsultaClinicaForm = {
    ...form.value,
    veterinario: form.value.veterinario || undefined,
  }

  try {
    guardando.value = true

    if (modoEdicion.value && consultaEditando.value) {
      await consultaStore.actualizar(consultaEditando.value.id, payload)
      await Swal.fire('Consulta actualizado', '', 'success')
    } else {
      await consultaStore.crear(payload)
      await Swal.fire('Consulta registrada', '', 'success')
    }

    await consultaStore.obtenerTodos()
    getModal().hide()
  } catch (e) {
    await Swal.fire(
      'Error',
      'No se pudo guardar la consulta clínica.',
      'error',
    )
    throw e
  } finally {
    guardando.value = false
  }
}
</script>