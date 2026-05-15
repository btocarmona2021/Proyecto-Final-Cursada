<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Especies y Razas</h4>
      <p class="text-muted small mb-0">Gestión de especies animales y sus razas</p>
    </div>

    <!-- Tabs -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <button 
          class="nav-link" 
          :class="{ active: tabActiva === 'especies' }" 
          @click="tabActiva = 'especies'"
        >
          Especies
        </button>
      </li>
      <li class="nav-item">
        <button 
          class="nav-link" 
          :class="{ active: tabActiva === 'razas' }" 
          @click="tabActiva = 'razas'"
        >
          Razas
        </button>
      </li>
    </ul>

    <!-- TAB ESPECIES -->
    <div v-if="tabActiva === 'especies'">
      <div class="d-flex gap-2 mb-3">
        <button class="btn btn-success" @click="abrirModalNuevaEspecie">+ Nueva especie</button>
        <input 
          type="text" 
          class="form-control form-control-sm ms-auto" 
          style="max-width:260px"
          placeholder="Buscar especie..." 
          v-model="busquedaEspecie" 
        />
      </div>

      <div v-if="especieStore.cargando" class="text-center text-muted py-5">
        Cargando especies...
      </div>

      <div v-else-if="especiesFiltradas.length === 0" class="text-center text-muted py-5">
        No se encontraron especies
      </div>

      <div v-else class="card border-0 shadow-sm">
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th style="width:80px"></th>
                <th>Nombre</th>
                <th style="width:120px">Razas</th>
                <th style="width:180px"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="e in especiesFiltradas" :key="e.id">
                <td class="text-center" style="font-size:2rem">{{ e.emoji }}</td>
                <td class="fw-semibold">{{ e.nombre }}</td>
                <td class="text-muted small">{{ contarRazas(e.id) }} raza(s)</td>
                <td>
                  <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditarEspecie(e)">
                      Editar
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminarEspecie(e)">
                      Eliminar
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB RAZAS -->
    <div v-if="tabActiva === 'razas'">
      <div class="d-flex gap-2 mb-3">
        <button class="btn btn-success" @click="abrirModalNuevaRaza">+ Nueva raza</button>
        <input 
          type="text" 
          class="form-control form-control-sm ms-auto" 
          style="max-width:260px"
          placeholder="Buscar raza..." 
          v-model="busquedaRaza" 
        />
        <select class="form-select form-select-sm" style="width:180px" v-model="filtroEspecie">
          <option value="">Todas las especies</option>
          <option v-for="e in especieStore.especies" :key="e.id" :value="e.id">
            {{ e.emoji }} {{ e.nombre }}
          </option>
        </select>
      </div>

      <div v-if="razaStore.cargando" class="text-center text-muted py-5">
        Cargando razas...
      </div>

      <div v-else-if="razasFiltradas.length === 0" class="text-center text-muted py-5">
        No se encontraron razas
      </div>

      <div v-else class="card border-0 shadow-sm">
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Nombre</th>
                <th>Especie</th>
                <th style="width:180px"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in razasFiltradas" :key="r.id">
                <td class="fw-semibold">{{ r.nombre }}</td>
                <td>
                  <span class="me-2">{{ r.especie?.emoji }}</span>
                  {{ r.especie?.nombre }}
                </td>
                <td>
                  <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditarRaza(r)">
                      Editar
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminarRaza(r)">
                      Eliminar
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- MODAL ESPECIE -->
    <div class="modal fade" id="modalEspecie" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicionEspecie ? 'Editar especie' : 'Nueva especie' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Nombre</label>
              <input type="text" class="form-control" v-model="formEspecie.nombre" />
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Emoji</label>
              <input type="text" class="form-control" v-model="formEspecie.emoji" placeholder="🐶" />
              <small class="text-muted">Un solo emoji</small>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-success" @click="guardarEspecie" :disabled="guardando">
              {{ guardando ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL RAZA -->
    <div class="modal fade" id="modalRaza" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicionRaza ? 'Editar raza' : 'Nueva raza' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Especie</label>
              <select class="form-select" v-model="formRaza.especieId">
                <option :value="0">Seleccioná una especie</option>
                <option v-for="e in especieStore.especies" :key="e.id" :value="e.id">
                  {{ e.emoji }} {{ e.nombre }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Nombre de la raza</label>
              <input type="text" class="form-control" v-model="formRaza.nombre" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-success" @click="guardarRaza" :disabled="guardando">
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
import { useEspecieStore } from '@/stores/especieStore'
import { useRazaStore } from '@/stores/razaStore'
import type { Especie } from '@/interfaces/especieInterface'
import type { Raza } from '@/interfaces/razaInterface'

const especieStore = useEspecieStore()
const razaStore = useRazaStore()

const tabActiva = ref<'especies' | 'razas'>('especies')
const busquedaEspecie = ref('')
const busquedaRaza = ref('')
const filtroEspecie = ref<number | ''>('')
const guardando = ref(false)

const modoEdicionEspecie = ref(false)
const especieEditando = ref<Especie | null>(null)
const formEspecie = ref({ nombre: '', emoji: '' })

const modoEdicionRaza = ref(false)
const razaEditando = ref<Raza | null>(null)
const formRaza = ref({ nombre: '', especieId: 0 })

onMounted(async () => {
  await Promise.all([
    especieStore.obtenerTodos(),
    razaStore.obtenerTodos(),
  ])
})

const especiesFiltradas = computed(() =>
  especieStore.especies.filter((e) =>
    e.nombre.toLowerCase().includes(busquedaEspecie.value.toLowerCase())
  )
)

const razasFiltradas = computed(() =>
  razaStore.razas.filter((r) => {
    const coincideNombre = r.nombre.toLowerCase().includes(busquedaRaza.value.toLowerCase())
    const coincideEspecie = filtroEspecie.value ? r.especie?.id === filtroEspecie.value : true
    return coincideNombre && coincideEspecie
  })
)

function contarRazas(especieId: number) {
  return razaStore.razas.filter((r) => r.especie?.id === especieId).length
}

function getModalEspecie() {
  return Modal.getOrCreateInstance(document.getElementById('modalEspecie')!)
}

function getModalRaza() {
  return Modal.getOrCreateInstance(document.getElementById('modalRaza')!)
}

function abrirModalNuevaEspecie() {
  modoEdicionEspecie.value = false
  especieEditando.value = null
  formEspecie.value = { nombre: '', emoji: '' }
  getModalEspecie().show()
}

function abrirModalEditarEspecie(e: Especie) {
  modoEdicionEspecie.value = true
  especieEditando.value = e
  formEspecie.value = { nombre: e.nombre, emoji: e.emoji ?? '' }
  getModalEspecie().show()
}

function abrirModalNuevaRaza() {
  modoEdicionRaza.value = false
  razaEditando.value = null
  formRaza.value = { nombre: '', especieId: 0 }
  getModalRaza().show()
}

function abrirModalEditarRaza(r: Raza) {
  modoEdicionRaza.value = true
  razaEditando.value = r
  formRaza.value = { nombre: r.nombre, especieId: r.especie?.id ?? 0 }
  getModalRaza().show()
}

async function guardarEspecie() {
  if (!formEspecie.value.nombre) {
    Swal.fire('Campo requerido', 'El nombre es obligatorio.', 'warning')
    return
  }

  guardando.value = true
  try {
    if (modoEdicionEspecie.value && especieEditando.value) {
      await especieStore.actualizar(especieEditando.value.id, formEspecie.value)
      Swal.fire({ icon: 'success', title: 'Especie actualizada', timer: 1500, showConfirmButton: false })
    } else {
      await especieStore.crear(formEspecie.value)
      Swal.fire({ icon: 'success', title: 'Especie creada', timer: 1500, showConfirmButton: false })
    }
    await especieStore.obtenerTodos()
    getModalEspecie().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar la especie.', 'error')
  } finally {
    guardando.value = false
  }
}

async function guardarRaza() {
  if (!formRaza.value.nombre || !formRaza.value.especieId) {
    Swal.fire('Campos requeridos', 'Nombre y especie son obligatorios.', 'warning')
    return
  }

  guardando.value = true
  try {
    const payload = {
      nombre: formRaza.value.nombre,
      especie_id: formRaza.value.especieId
    }

    if (modoEdicionRaza.value && razaEditando.value) {
      await razaStore.actualizar(razaEditando.value.id, payload)
      Swal.fire({ icon: 'success', title: 'Raza actualizada', timer: 1500, showConfirmButton: false })
    } else {
      await razaStore.crear(payload)
      Swal.fire({ icon: 'success', title: 'Raza creada', timer: 1500, showConfirmButton: false })
    }
    await razaStore.obtenerTodos()
    getModalRaza().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar la raza.', 'error')
  } finally {
    guardando.value = false
  }
}

async function confirmarEliminarEspecie(e: Especie) {
  const cantRazas = contarRazas(e.id)
  
  if (cantRazas > 0) {
    Swal.fire({
      icon: 'warning',
      title: 'No se puede eliminar',
      text: `Esta especie tiene ${cantRazas} raza(s) asociada(s). Eliminá primero las razas.`,
    })
    return
  }

  const result = await Swal.fire({
    title: '¿Eliminar especie?',
    text: e.nombre,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })

  if (result.isConfirmed) {
    await especieStore.eliminar(e.id)
    await especieStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Especie eliminada', timer: 1500, showConfirmButton: false })
  }
}

async function confirmarEliminarRaza(r: Raza) {
  const result = await Swal.fire({
    title: '¿Eliminar raza?',
    text: r.nombre,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })

  if (result.isConfirmed) {
    await razaStore.eliminar(r.id)
    await razaStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Raza eliminada', timer: 1500, showConfirmButton: false })
  }
}
</script>