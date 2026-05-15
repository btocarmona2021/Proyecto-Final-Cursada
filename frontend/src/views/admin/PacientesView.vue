<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Pacientes</h4>
      <p class="text-muted small mb-0">Registro de animales atendidos</p>
    </div>

    <div class="d-flex flex-wrap gap-2 mb-4 align-items-center">
      <button class="btn btn-success" @click="abrirModalNuevo">+ Nuevo paciente</button>
      <input type="text" class="form-control form-control-sm ms-auto" style="max-width:260px"
        placeholder="Buscar por nombre..." v-model="busqueda" />
      <select class="form-select form-select-sm" style="width:160px" v-model="filtroEspecie">
        <option value="">Todas las especies</option>
        <option v-for="e in especieStore.especies" :key="e.id" :value="e.nombre">
          {{ e.nombre }}
        </option>
      </select>
    </div>

    <div v-if="mascotaStore.cargando" class="text-center text-muted py-5">Cargando pacientes...</div>
    <div v-else-if="mascotasFiltradas.length === 0" class="text-center text-muted py-5">
      No se encontraron pacientes
    </div>

    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Nombre</th>
              <th>Especie / Raza</th>
              <th>Dueño</th>
              <th>Peso</th>
              <th>Sexo</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in mascotasFiltradas" :key="m.id">
              <td class="fw-semibold">{{ m.nombre }}</td>
              <td>
                {{ m.especie_nombre }}
                <span class="text-muted small">/ {{ m.raza_nombre }}</span>
              </td>
              <td>{{ m.usuario_nombre }}</td>
              <td>{{ m.peso_actual ? m.peso_actual + ' kg' : '—' }}</td>
              <td>
                <span class="badge" :class="m.sexo === 'M' ? 'bg-primary' : 'bg-danger'">
                  {{ m.sexo_display }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-1">
                  <RouterLink :to="`/admin/pacientes/${m.id}`" class="btn btn-sm btn-outline-secondary">
                    Ver ficha
                  </RouterLink>
                  <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditar(m)">Editar</button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminar(m)">Eliminar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL -->
    <div class="modal fade" id="modalMascota" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicion ? 'Editar paciente' : 'Nuevo paciente' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">

            <div class="mb-3">
              <label class="form-label fw-semibold">Nombre</label>
              <input type="text" class="form-control" v-model="form.nombre" />
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Especie</label>
              <select class="form-select" v-model="especieSeleccionada" @change="cambiarEspecie">
                <option :value="0">Seleccioná una especie</option>
                <option v-for="e in especieStore.especies" :key="e.id" :value="e.id">
                  {{ e.nombre }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Raza</label>
              <select class="form-select" v-model="form.raza" :disabled="especieSeleccionada === 0">
                <option :value="0">
                  {{ especieSeleccionada === 0 ? 'Primero seleccioná una especie' : 'Seleccioná una raza' }}
                </option>
                <option v-for="r in razasFiltradas" :key="r.id" :value="r.id">
                  {{ r.nombre }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Dueño</label>
              <select class="form-select" v-model="form.usuario">
                <option :value="0">Seleccioná un dueño</option>
                <option v-for="u in soloClientes" :key="u.id" :value="u.id">
                  {{ u.first_name }} {{ u.last_name }}
                </option>
              </select>
            </div>

            <div class="row">
              <div class="col mb-3">
                <label class="form-label fw-semibold">Fecha nacimiento</label>
                <input type="date" class="form-control" v-model="form.fecha_nacimiento" />
              </div>
              <div class="col mb-3">
                <label class="form-label fw-semibold">Sexo</label>
                <select class="form-select" v-model="form.sexo">
                  <option value="">No especificado</option>
                  <option value="M">Macho</option>
                  <option value="H">Hembra</option>
                </select>
              </div>
            </div>

            <div class="row">
              <div class="col mb-3">
                <label class="form-label fw-semibold">Peso (kg)</label>
                <input type="number" step="0.1" class="form-control" v-model="form.peso_actual" />
              </div>
              <div class="col mb-3">
                <label class="form-label fw-semibold">Color</label>
                <input type="text" class="form-control" v-model="form.color" />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Microchip</label>
              <input type="text" class="form-control" v-model="form.microchip" />
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
import { useMascotaStore } from '@/stores/mascotaStore'
import { useEspecieStore } from '@/stores/especieStore'
import { useRazaStore } from '@/stores/razaStore'
import { useUsuarioStore } from '@/stores/usuarioStore'
import type { Mascota, MascotaForm } from '@/interfaces/mascotaInterface'

const mascotaStore = useMascotaStore()
const especieStore = useEspecieStore()
const razaStore = useRazaStore()
const usuarioStore = useUsuarioStore()

const busqueda = ref('')
const filtroEspecie = ref('')
const modoEdicion = ref(false)
const mascotaEditando = ref<Mascota | null>(null)
const guardando = ref(false)
const especieSeleccionada = ref<number>(0)

const formVacio = (): MascotaForm => ({
  nombre: '',
  raza: 0,
  usuario: 0,
  fecha_nacimiento: '',
  sexo: 'M',
  color: '',
  peso_actual: undefined,
  microchip: '',
  foto: null,
})

const form = ref<MascotaForm>(formVacio())

onMounted(async () => {
  await Promise.all([
    mascotaStore.obtenerTodos(),
    especieStore.obtenerTodos(),
    razaStore.obtenerTodos(),
    usuarioStore.obtenerTodos(),
  ])
})

const soloClientes = computed(() =>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  usuarioStore.usuarios.filter((u :any) => u.grupo === 'clientes')
)

const razasFiltradas = computed(() => {
  if (especieSeleccionada.value === 0) return []
  
  return razaStore.razas.filter((r) => r.especie?.id === especieSeleccionada.value)
})

const mascotasFiltradas = computed(() =>
  mascotaStore.mascotas.filter((m) => {
    const coincideNombre = m.nombre.toLowerCase().includes(busqueda.value.toLowerCase())
    const coincideEspecie = filtroEspecie.value ? m.especie_nombre === filtroEspecie.value : true
    return coincideNombre && coincideEspecie
  })
)

function cambiarEspecie() {
  form.value.raza = 0
}

function getModal() {
  return Modal.getOrCreateInstance(document.getElementById('modalMascota')!)
}

function abrirModalNuevo() {
  modoEdicion.value = false
  mascotaEditando.value = null
  especieSeleccionada.value = 0
  form.value = formVacio()
  getModal().show()
}

function abrirModalEditar(m: Mascota) {
  modoEdicion.value = true
  mascotaEditando.value = m
  
  const razaActual = razaStore.razas.find((r) => r.id === m.raza)
  if (razaActual && razaActual.especie) {
    especieSeleccionada.value = razaActual.especie.id
  }
  
  form.value = {
    nombre: m.nombre,
    raza: m.raza,
    usuario: m.usuario,
    fecha_nacimiento: m.fecha_nacimiento ?? '',
    sexo: m.sexo,
    color: m.color ?? '',
    peso_actual: m.peso_actual ? parseFloat(m.peso_actual) : undefined,
    microchip: m.microchip ?? '',
    foto: null,
  }
  getModal().show()
}

async function guardar() {
  if (!form.value.nombre || !form.value.raza || !form.value.usuario) {
    Swal.fire('Campos requeridos', 'Nombre, raza y dueño son obligatorios.', 'warning')
    return
  }
  guardando.value = true
  try {
    if (modoEdicion.value && mascotaEditando.value) {
      await mascotaStore.actualizar(mascotaEditando.value.id, form.value)
      Swal.fire({ icon: 'success', title: 'Paciente actualizado', timer: 1500, showConfirmButton: false })
    } else {
      await mascotaStore.crear(form.value)
      Swal.fire({ icon: 'success', title: 'Paciente creado', timer: 1500, showConfirmButton: false })
    }
    await mascotaStore.obtenerTodos()
    getModal().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar el paciente.', 'error')
  } finally {
    guardando.value = false
  }
}

async function confirmarEliminar(m: Mascota) {
  const result = await Swal.fire({
    title: '¿Eliminar paciente?',
    text: `${m.nombre} — ${m.especie_nombre}`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })
  if (result.isConfirmed) {
    await mascotaStore.eliminar(m.id)
    await mascotaStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Paciente eliminado', timer: 1500, showConfirmButton: false })
  }
}
</script>