<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Servicios</h4>
      <p class="text-muted small mb-0">Tipos de consulta y precios</p>
    </div>

    <div class="d-flex gap-2 mb-3">
      <button class="btn btn-success" @click="abrirModalNuevo">+ Nuevo servicio</button>
      <input 
        type="text" 
        class="form-control form-control-sm ms-auto" 
        style="max-width:260px"
        placeholder="Buscar servicio..." 
        v-model="busqueda" 
      />
    </div>

    <div v-if="servicioStore.cargando" class="text-center text-muted py-5">
      Cargando servicios...
    </div>

    <div v-else-if="serviciosFiltrados.length === 0" class="text-center text-muted py-5">
      No se encontraron servicios
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Precio</th>
              <th>Duración</th>
              <th>Estado</th>
              <th style="width:180px"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in serviciosFiltrados" :key="s.id">
              <td class="fw-semibold">{{ s.nombre }}</td>
              <td class="text-muted small">{{ s.descripcion || '—' }}</td>
              <td class="fw-bold text-success">${{ s.precio }}</td>
              <td class="small">{{ s.duracion_estimada }} min</td>
              <td>
                <span class="badge" :class="s.activo ? 'bg-success' : 'bg-secondary'">
                  {{ s.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-1">
                  <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditar(s)">
                    Editar
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminar(s)">
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL -->
    <div class="modal fade" id="modalServicio" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicion ? 'Editar servicio' : 'Nuevo servicio' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Nombre</label>
              <input type="text" class="form-control" v-model="form.nombre" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Descripción</label>
              <textarea class="form-control" rows="2" v-model="form.descripcion"></textarea>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Precio ($)</label>
                <input type="number" class="form-control" v-model.number="form.precio" step="0.01" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Duración (min)</label>
                <input type="number" class="form-control" v-model.number="form.duracionEstimada" />
              </div>
            </div>
            <div class="form-check">
              <input id="activo" class="form-check-input" type="checkbox" v-model="form.activo" />
              <label for="activo" class="form-check-label">Servicio activo</label>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import Swal from 'sweetalert2'
import { useServicioStore } from '@/stores/servicioStore'
import type { Servicio } from '@/interfaces/servicioInterface'

const servicioStore = useServicioStore()

const busqueda = ref('')
const guardando = ref(false)
const modoEdicion = ref(false)
const servicioEditando = ref<Servicio | null>(null)

const formVacio = () => ({
  nombre: '',
  descripcion: '',
  precio: 0,
  duracionEstimada: 30,
  activo: true,
})

const form = ref(formVacio())

onMounted(async () => {
  await servicioStore.obtenerTodos()
})

const serviciosFiltrados = computed(() =>
  servicioStore.servicios.filter((s) =>
    s.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
  )
)

function getModal() {
  return Modal.getOrCreateInstance(document.getElementById('modalServicio')!)
}

function abrirModalNuevo() {
  modoEdicion.value = false
  servicioEditando.value = null
  form.value = formVacio()
  getModal().show()
}

function abrirModalEditar(s: Servicio) {
  modoEdicion.value = true
  servicioEditando.value = s
  form.value = {
    nombre: s.nombre,
    descripcion: s.descripcion || '',
    precio: Number(s.precio),
    duracionEstimada: s.duracion_estimada,
    activo: s.activo,
  }
  getModal().show()
}

async function guardar() {
  if (!form.value.nombre || form.value.precio <= 0) {
    Swal.fire('Campos requeridos', 'Completá nombre y precio válido.', 'warning')
    return
  }

  guardando.value = true
  try {
    const payload = {
      nombre: form.value.nombre,
      descripcion: form.value.descripcion,
      precio: form.value.precio,
      duracion_estimada: form.value.duracionEstimada,
      activo: form.value.activo,
    }

    if (modoEdicion.value && servicioEditando.value) {
      await servicioStore.actualizar(servicioEditando.value.id, payload)
      Swal.fire({ icon: 'success', title: 'Servicio actualizado', timer: 1500, showConfirmButton: false })
    } else {
      await servicioStore.crear(payload)
      Swal.fire({ icon: 'success', title: 'Servicio creado', timer: 1500, showConfirmButton: false })
    }
    await servicioStore.obtenerTodos()
    getModal().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar el servicio.', 'error')
  } finally {
    guardando.value = false
  }
}

async function confirmarEliminar(s: Servicio) {
  const result = await Swal.fire({
    title: '¿Eliminar servicio?',
    text: s.nombre,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })

  if (result.isConfirmed) {
    await servicioStore.eliminar(s.id)
    await servicioStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Servicio eliminado', timer: 1500, showConfirmButton: false })
  }
}
</script>