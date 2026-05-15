<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Vacunas</h4>
      <p class="text-muted small mb-0">Registro completo de vacunación de todas las mascotas</p>
    </div>

    <div class="d-flex flex-wrap gap-2 mb-3 align-items-center">
      <button class="btn btn-success" @click="abrirModalNueva">+ Nueva vacuna</button>
      <input 
        type="text" 
        class="form-control form-control-sm" 
        style="max-width:220px"
        placeholder="Buscar vacuna..." 
        v-model="busqueda" 
      />
      <select class="form-select form-select-sm" style="width:200px" v-model="filtroMascota">
        <option value="">Todas las mascotas</option>
        <option v-for="m in mascotaStore.mascotas" :key="m.id" :value="m.id">
          {{ m.nombre }} ({{ m.usuario_nombre }})
        </option>
      </select>
      <select class="form-select form-select-sm ms-auto" style="width:180px" v-model="filtroEstado">
        <option value="">Todos los estados</option>
        <option value="vigente">Al día</option>
        <option value="proxima">Próxima (30 días)</option>
        <option value="vencida">Vencida</option>
      </select>
    </div>

    <div v-if="cargando" class="text-center text-muted py-5">
      Cargando vacunas...
    </div>

    <div v-else-if="vacunasFiltradas.length === 0" class="text-center text-muted py-5">
      No se encontraron vacunas
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Vacuna</th>
              <th>Mascota</th>
              <th>Dueño</th>
              <th>Fecha aplicación</th>
              <th>Próxima dosis</th>
              <th>Estado</th>
              <th style="width:180px"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="v in vacunasFiltradas" :key="v.id">
              <td class="fw-semibold">{{ v.nombre }}</td>
              <td>{{ obtenerMascotaNombre(v.mascota) }}</td>
              <td class="small text-muted">{{ obtenerDuenoNombre(v.mascota) }}</td>
              <td class="small">{{ formatearFecha(v.fecha_aplicacion) }}</td>
              <td class="small">{{ v.fecha_proxima ? formatearFecha(v.fecha_proxima) : '—' }}</td>
              <td>
                <span class="badge" :class="estadoVacuna(v.fecha_proxima)">
                  {{ etiquetaVacuna(v.fecha_proxima) }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-1">
                  <button class="btn btn-sm btn-outline-secondary" @click="verDetalle(v)">
                    Ver
                  </button>
                  <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditar(v)">
                    Editar
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminar(v)">
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
    <div class="modal fade" id="modalVacuna" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicion ? 'Editar vacuna' : 'Nueva vacuna' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Mascota</label>
              <select class="form-select" v-model="form.mascota">
                <option :value="0">Seleccioná una mascota</option>
                <option v-for="m in mascotaStore.mascotas" :key="m.id" :value="m.id">
                  {{ m.nombre }} - {{ m.usuario_nombre }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Nombre de la vacuna</label>
              <input type="text" class="form-control" v-model="form.nombre" />
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Fecha aplicación</label>
                <input type="date" class="form-control" v-model="form.fecha_aplicacion" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Próxima dosis</label>
                <input type="date" class="form-control" v-model="form.fecha_proxima" />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Observaciones</label>
              <textarea class="form-control" rows="3" v-model="form.observaciones"></textarea>
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

    <!-- MODAL DETALLE -->
    <div class="modal fade" id="modalDetalle" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content" v-if="vacunaDetalle">
          <div class="modal-header">
            <h5 class="modal-title">{{ vacunaDetalle.nombre }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <strong>Mascota:</strong> {{ obtenerMascotaNombre(vacunaDetalle.mascota) }}
            </div>
            <div class="mb-3">
              <strong>Dueño:</strong> {{ obtenerDuenoNombre(vacunaDetalle.mascota) }}
            </div>
            <div class="mb-3">
              <strong>Fecha de aplicación:</strong> {{ formatearFecha(vacunaDetalle.fecha_aplicacion) }}
            </div>
            <div class="mb-3">
              <strong>Próxima dosis:</strong> 
              {{ vacunaDetalle.fecha_proxima ? formatearFecha(vacunaDetalle.fecha_proxima) : 'No programada' }}
            </div>
            <div class="mb-3">
              <strong>Estado:</strong>
              <span class="badge ms-2" :class="estadoVacuna(vacunaDetalle.fecha_proxima)">
                {{ etiquetaVacuna(vacunaDetalle.fecha_proxima) }}
              </span>
            </div>
            <div v-if="vacunaDetalle.observaciones" class="mb-3">
              <strong>Observaciones:</strong>
              <p class="text-muted mb-0 mt-1">{{ vacunaDetalle.observaciones }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cerrar</button>
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
import { useVacunaStore } from '@/stores/vacunaStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import type { Vacuna } from '@/interfaces/vacunaInterface'

const vacunaStore = useVacunaStore()
const mascotaStore = useMascotaStore()

const busqueda = ref('')
const filtroMascota = ref<number | ''>('')
const filtroEstado = ref<string>('')
const guardando = ref(false)
const modoEdicion = ref(false)
const vacunaEditando = ref<Vacuna | null>(null)
const vacunaDetalle = ref<Vacuna | null>(null)

const formularioVacio = () => ({
  mascota: 0,
  nombre: '',
  fecha_aplicacion: new Date().toISOString().slice(0, 10),
  fecha_proxima: '',
  observaciones: '',
})

const form = ref(formularioVacio())

onMounted(async () => {
  await Promise.all([
    vacunaStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
  ])
})

const cargando = computed(() => vacunaStore.cargando || mascotaStore.cargando)

const vacunasFiltradas = computed(() => {
  return vacunaStore.vacunas.filter((v) => {
    const coincideNombre = v.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const coincideMascota = filtroMascota.value ? v.mascota === filtroMascota.value : true
    
    let coincideEstado = true
    if (filtroEstado.value) {
      const estado = getEstadoVacuna(v.fecha_proxima)
      coincideEstado = estado === filtroEstado.value
    }

    return coincideNombre && coincideMascota && coincideEstado
  })
})

function getEstadoVacuna(fechaProxima: string | null): string {
  if (!fechaProxima) return 'vigente'
  const dias = Math.ceil((new Date(fechaProxima).getTime() - new Date().setHours(0, 0, 0, 0)) / 86400000)
  if (dias < 0) return 'vencida'
  if (dias <= 30) return 'proxima'
  return 'vigente'
}

function estadoVacuna(fechaProxima: string | null) {
  if (!fechaProxima) return 'bg-secondary'
  const dias = Math.ceil((new Date(fechaProxima).getTime() - new Date().setHours(0, 0, 0, 0)) / 86400000)
  if (dias < 0) return 'bg-danger'
  if (dias <= 30) return 'bg-warning text-dark'
  return 'bg-success'
}

function etiquetaVacuna(fechaProxima: string | null) {
  if (!fechaProxima) return 'Sin próxima'
  const dias = Math.ceil((new Date(fechaProxima).getTime() - new Date().setHours(0, 0, 0, 0)) / 86400000)
  if (dias < 0) return 'Vencida'
  if (dias <= 30) return `Próxima (${dias}d)`
  return 'Al día'
}

function formatearFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function obtenerMascotaNombre(mascotaId: number) {
  return mascotaStore.mascotas.find((m) => m.id === mascotaId)?.nombre ?? '—'
}

function obtenerDuenoNombre(mascotaId: number) {
  return mascotaStore.mascotas.find((m) => m.id === mascotaId)?.usuario_nombre ?? '—'
}

function obtenerModal() {
  return Modal.getOrCreateInstance(document.getElementById('modalVacuna')!)
}

function obtenerModalDetalle() {
  return Modal.getOrCreateInstance(document.getElementById('modalDetalle')!)
}

function abrirModalNueva() {
  modoEdicion.value = false
  vacunaEditando.value = null
  form.value = formularioVacio()
  obtenerModal().show()
}

function abrirModalEditar(v: Vacuna) {
  modoEdicion.value = true
  vacunaEditando.value = v
  form.value = {
    mascota: v.mascota,
    nombre: v.nombre,
    fecha_aplicacion: v.fecha_aplicacion,
    fecha_proxima: v.fecha_proxima ?? '',
    observaciones: v.observaciones ?? '',
  }
  obtenerModal().show()
}

function verDetalle(v: Vacuna) {
  vacunaDetalle.value = v
  obtenerModalDetalle().show()
}

async function guardar() {
  if (!form.value.mascota || !form.value.nombre || !form.value.fecha_aplicacion) {
    Swal.fire('Campos requeridos', 'Mascota, nombre y fecha de aplicación son obligatorios.', 'warning')
    return
  }

  guardando.value = true
  try {
    if (modoEdicion.value && vacunaEditando.value) {
      await vacunaStore.actualizar(vacunaEditando.value.id, form.value)
      Swal.fire({ icon: 'success', title: 'Vacuna actualizada', timer: 1500, showConfirmButton: false })
    } else {
      await vacunaStore.crear(form.value)
      Swal.fire({ icon: 'success', title: 'Vacuna registrada', timer: 1500, showConfirmButton: false })
    }
    await vacunaStore.obtenerTodos()
    obtenerModal().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar la vacuna.', 'error')
  } finally {
    guardando.value = false
  }
}

async function confirmarEliminar(v: Vacuna) {
  const result = await Swal.fire({
    title: '¿Eliminar vacuna?',
    text: `${v.nombre} - ${obtenerMascotaNombre(v.mascota)}`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })

  if (result.isConfirmed) {
    await vacunaStore.eliminar(v.id)
    await vacunaStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Vacuna eliminada', timer: 1500, showConfirmButton: false })
  }
}
</script>