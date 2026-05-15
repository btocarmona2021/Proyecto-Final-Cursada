<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Veterinarios</h4>
      <p class="text-muted small mb-0">Equipo médico y horarios</p>
    </div>

    <div class="d-flex flex-wrap gap-2 mb-4 align-items-center">
      <button class="btn btn-success" @click="abrirModalNuevo">+ Agregar veterinario</button>
      <input v-model="busqueda" type="text" class="form-control form-control-sm ms-auto" style="max-width: 260px"
        placeholder="Buscar veterinario..." />
    </div>

    <div v-if="cargandoVista" class="text-center text-muted py-5">
      Cargando veterinarios...
    </div>

    <div v-else-if="veterinariosFiltrados.length === 0" class="text-center text-muted py-5">
      No se encontraron veterinarios
    </div>

    <div v-else>
      <div v-for="vet in veterinariosFiltrados" :key="vet.id" class="card border-0 shadow-sm mb-3">
        <div class="card-body d-flex justify-content-between align-items-start gap-3 flex-wrap">
          <div class="d-flex gap-3 align-items-start">
            <div class="rounded-circle d-flex align-items-center justify-content-center fw-bold"
              style="width:52px;height:52px;background:#d1e7dd;color:#146c43;">
              {{ inicialesVet(vet.usuario.first_name, vet.usuario.last_name) }}
            </div>

            <div>
              <h6 class="fw-bold mb-1">{{ nombreCompleto(vet) }}</h6>
              <div class="text-success small fw-semibold mb-1">
                {{ vet.especialidad || 'Sin especialidad' }}
              </div>
              <div class="text-muted small mb-1">
                Mat. {{ vet.matricula }} · {{ vet.usuario.email || 'Sin email' }}
              </div>
              <div class="text-muted small">
                {{ vet.biografia || 'Sin biografía cargada' }}
              </div>

              <div class="mt-2">
                <span class="badge" :class="vet.disponible ? 'text-bg-success' : 'text-bg-secondary'">
                  {{ vet.disponible ? 'Disponible hoy' : 'No disponible hoy' }}
                </span>
              </div>
            </div>
          </div>

          <div class="d-flex flex-column align-items-start align-items-md-end gap-2">
            <div class="text-muted small">
              {{ horariosDeVeterinario(vet.id).length }} horario(s)
            </div>

            <div class="d-flex gap-2 flex-wrap justify-content-end">
              <button class="btn btn-sm btn-outline-secondary" @click="verDetalle(vet)">
                Ver perfil
              </button>
              <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditar(vet)">
                Editar
              </button>
              <button class="btn btn-sm btn-outline-success" @click="abrirModalHorario(vet)">
                Horario
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminar(vet)">
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL CREAR / EDITAR VETERINARIO -->
    <div class="modal fade" id="modalVeterinario" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ modoEdicion ? 'Editar veterinario' : 'Nuevo veterinario' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="mb-3" v-if="!modoEdicion">
              <label class="form-label fw-semibold">Usuario</label>
              <select class="form-select" v-model="usuarioSeleccionadoId">
                <option :value="0">Seleccioná un usuario</option>
                <option v-for="u in usuariosVeterinariosDisponibles" :key="u.id" :value="u.id">
                  {{ u.first_name }} {{ u.last_name }} - {{ u.email }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Matrícula</label>
              <input type="text" class="form-control" v-model="form.matricula" />
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Especialidad</label>
              <input type="text" class="form-control" v-model="form.especialidad" />
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Biografía</label>
              <textarea class="form-control" rows="3" v-model="form.biografia"></textarea>
            </div>

            <div class="form-check">
              <input id="disponible" class="form-check-input" type="checkbox" v-model="form.disponible" />
              <label for="disponible" class="form-check-label">
                Disponible
              </label>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-success" @click="guardarVeterinario" :disabled="guardando">
              {{ guardando ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL DETALLE -->
    <div class="modal fade" id="modalDetalleVeterinario" tabindex="-1">
      <div class="modal-dialog modal-xl">
        <div class="modal-content" v-if="veterinarioDetalle">
          <div class="modal-header">
            <h5 class="modal-title">{{ nombreCompleto(veterinarioDetalle) }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="row g-4">
              <div class="col-lg-5">
                <div class="card border-0 bg-light h-100">
                  <div class="card-body">
                    <h6 class="fw-bold mb-3">Perfil profesional</h6>
                    <div class="mb-2"><strong>Matrícula:</strong> {{ veterinarioDetalle.matricula }}</div>
                    <div class="mb-2"><strong>Especialidad:</strong> {{ veterinarioDetalle.especialidad || 'Sin especialidad' }}</div>
                    <div class="mb-2"><strong>Email:</strong> {{ veterinarioDetalle.usuario.email || 'Sin email' }}</div>
                    <div class="mb-2"><strong>Estado:</strong> {{ veterinarioDetalle.disponible ? 'Disponible' : 'No disponible' }}</div>
                    <div class="mt-3">
                      <strong>Biografía:</strong>
                      <div class="text-muted small mt-1">
                        {{ veterinarioDetalle.biografia || 'Sin biografía cargada' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-lg-7">
                <div class="card border-0 bg-light h-100">
                  <div class="card-body">
                    <HorariosCalendario
                      :horarios="horariosOrdenados(veterinarioDetalle.id)"
                      @agregar="abrirModalHorario(veterinarioDetalle)"
                      @editar="editarHorario"
                      @eliminar="eliminarHorario"
                    />
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

    <!-- MODAL HORARIO -->
    <div class="modal fade" id="modalHorario" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ modoEdicionHorario ? 'Editar horario' : 'Nuevo horario' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Veterinario</label>
              <select class="form-select" v-model="formHorario.veterinario_id" :disabled="modoEdicionHorario">
                <option :value="0">Seleccioná un veterinario</option>
                <option v-for="v in veterinarioStore.veterinarios" :key="v.id" :value="v.id">
                  {{ nombreCompleto(v) }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Día</label>
              <select class="form-select" v-model="formHorario.dia_semana">
                <option :value="1">Lunes</option>
                <option :value="2">Martes</option>
                <option :value="3">Miércoles</option>
                <option :value="4">Jueves</option>
                <option :value="5">Viernes</option>
                <option :value="6">Sábado</option>
                <option :value="7">Domingo</option>
              </select>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Hora inicio</label>
                <input type="time" class="form-control" v-model="formHorario.hora_inicio" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Hora fin</label>
                <input type="time" class="form-control" v-model="formHorario.hora_fin" />
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-success" @click="guardarHorario" :disabled="guardandoHorario">
              {{ guardandoHorario ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Modal } from 'bootstrap'
import Swal from 'sweetalert2'
import { useVeterinarioStore } from '@/stores/veterinarioStore'
import { useHorarioVeterinarioStore } from '@/stores/horarioVeterinarioStore'
import { useUsuarioStore } from '@/stores/usuarioStore'
import HorariosCalendario from '@/components/HorariosCalendario.vue'
import type { VeterinarioPerfil, VeterinarioPerfilForm } from '@/interfaces/veterinarioPerfilInterface'
import type { HorarioVeterinario, HorarioVeterinarioForm } from '@/interfaces/horarioVeterinarioInterface'
import type { UsuarioAuth } from '@/interfaces/usuarioInterface'

const veterinarioStore = useVeterinarioStore()
const horarioStore = useHorarioVeterinarioStore()
const usuarioStore = useUsuarioStore()

const busqueda = ref('')
const guardando = ref(false)
const guardandoHorario = ref(false)

const modoEdicion = ref(false)
const modoEdicionHorario = ref(false)

const veterinarioEditando = ref<VeterinarioPerfil | null>(null)
const veterinarioDetalle = ref<VeterinarioPerfil | null>(null)
const horarioEditando = ref<HorarioVeterinario | null>(null)
const usuarioSeleccionadoId = ref<number>(0)

const formVacio = (): VeterinarioPerfilForm => ({
  matricula: '',
  especialidad: '',
  biografia: '',
  disponible: true,
  foto: null,
})

const formHorarioVacio = (): HorarioVeterinarioForm => ({
  veterinario_id: 0,
  dia_semana: 1,
  hora_inicio: '',
  hora_fin: '',
})

const form = ref<VeterinarioPerfilForm>(formVacio())
const formHorario = ref<HorarioVeterinarioForm>(formHorarioVacio())

onMounted(async () => {
  await Promise.all([
    veterinarioStore.obtenerTodos(),
    horarioStore.obtenerTodos(),
    usuarioStore.obtenerTodos(),
  ])
})

const cargandoVista = computed(() =>
  veterinarioStore.cargando || horarioStore.cargando || usuarioStore.cargando
)

function nombreCompleto(vet: VeterinarioPerfil): string {
  return `${vet.usuario.first_name} ${vet.usuario.last_name}`
}

const veterinariosFiltrados = computed(() =>
  veterinarioStore.veterinarios.filter((v) => {
    const nombre = nombreCompleto(v)
    const texto = `${nombre} ${v.especialidad ?? ''} ${v.matricula} ${v.usuario.email ?? ''}`.toLowerCase()
    return texto.includes(busqueda.value.toLowerCase())
  })
)

const usuariosVeterinariosDisponibles = computed(() => {
  const usados = new Set(veterinarioStore.veterinarios.map((v) => v.usuario.id))
  return usuarioStore.usuarios.filter((u: UsuarioAuth) => u.grupo === 'veterinarios' && !usados.has(u.id))
})

function inicialesVet(firstName: string, lastName: string) {
  return `${firstName?.[0] ?? ''}${lastName?.[0] ?? ''}`.toUpperCase()
}

function horariosDeVeterinario(veterinarioId: number) {
  return horarioStore.horarios.filter((h) => h.veterinario_id === veterinarioId)
}

function horariosOrdenados(veterinarioId: number) {
  return [...horariosDeVeterinario(veterinarioId)].sort((a, b) => a.dia_semana - b.dia_semana)
}

function getModalVeterinario() {
  return Modal.getOrCreateInstance(document.getElementById('modalVeterinario')!)
}

function getModalDetalle() {
  return Modal.getOrCreateInstance(document.getElementById('modalDetalleVeterinario')!)
}

function getModalHorario() {
  return Modal.getOrCreateInstance(document.getElementById('modalHorario')!)
}

function abrirModalNuevo() {
  modoEdicion.value = false
  veterinarioEditando.value = null
  usuarioSeleccionadoId.value = 0
  form.value = formVacio()
  getModalVeterinario().show()
}

function abrirModalEditar(vet: VeterinarioPerfil) {
  modoEdicion.value = true
  veterinarioEditando.value = vet
  form.value = {
    matricula: vet.matricula,
    especialidad: vet.especialidad || '',
    biografia: vet.biografia || '',
    disponible: vet.disponible,
    foto: null,
  }
  getModalVeterinario().show()
}

function verDetalle(vet: VeterinarioPerfil) {
  veterinarioDetalle.value = vet
  getModalDetalle().show()
}

function abrirModalHorario(vet: VeterinarioPerfil) {
  modoEdicionHorario.value = false
  horarioEditando.value = null
  formHorario.value = {
    veterinario_id: vet.id,
    dia_semana: 1,
    hora_inicio: '',
    hora_fin: '',
  }
  getModalHorario().show()
}

function editarHorario(horario: HorarioVeterinario) {
  modoEdicionHorario.value = true
  horarioEditando.value = horario
  formHorario.value = {
    veterinario_id: horario.veterinario_id,
    dia_semana: horario.dia_semana,
    hora_inicio: horario.hora_inicio,
    hora_fin: horario.hora_fin,
  }
  getModalHorario().show()
}

async function guardarVeterinario() {
  if (!form.value.matricula) {
    Swal.fire('Campos requeridos', 'Completá la matrícula.', 'warning')
    return
  }

  if (!modoEdicion.value && usuarioSeleccionadoId.value === 0) {
    Swal.fire('Campos requeridos', 'Seleccioná un usuario.', 'warning')
    return
  }

  guardando.value = true
  try {
    if (modoEdicion.value && veterinarioEditando.value) {
      await veterinarioStore.actualizar(veterinarioEditando.value.id, form.value)
      Swal.fire({ icon: 'success', title: 'Veterinario actualizado', timer: 1500, showConfirmButton: false })
    } else {
      const usuario = usuarioStore.usuarios.find((u: UsuarioAuth) => u.id === usuarioSeleccionadoId.value)
      if (!usuario) throw new Error('Usuario no encontrado')

      const payload: VeterinarioPerfilForm = {
        username: usuario.username,
        password: 'temporal123',
        firstName: usuario.first_name,
        lastName: usuario.last_name,
        email: usuario.email,
        ...form.value,
      }

      await veterinarioStore.crear(payload)
      Swal.fire({ icon: 'success', title: 'Veterinario creado', timer: 1500, showConfirmButton: false })
    }

    await veterinarioStore.obtenerTodos()
    getModalVeterinario().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar el veterinario.', 'error')
  } finally {
    guardando.value = false
  }
}

async function guardarHorario() {
  if (!formHorario.value.veterinario_id || !formHorario.value.hora_inicio || !formHorario.value.hora_fin) {
    Swal.fire('Campos requeridos', 'Completá veterinario, hora inicio y hora fin.', 'warning')
    return
  }

  guardandoHorario.value = true
  try {
    if (modoEdicionHorario.value && horarioEditando.value) {
      await horarioStore.actualizar(horarioEditando.value.id, formHorario.value)
      Swal.fire({ icon: 'success', title: 'Horario actualizado', timer: 1500, showConfirmButton: false })
    } else {
      await horarioStore.crear(formHorario.value)
      Swal.fire({ icon: 'success', title: 'Horario creado', timer: 1500, showConfirmButton: false })
    }

    await horarioStore.obtenerTodos()
    getModalHorario().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar el horario.', 'error')
  } finally {
    guardandoHorario.value = false
  }
}

async function eliminarHorario(id: number) {
  const result = await Swal.fire({
    title: '¿Eliminar horario?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar',
  })

  if (result.isConfirmed) {
    await horarioStore.eliminar(id)
    await horarioStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Horario eliminado', timer: 1500, showConfirmButton: false })
  }
}

async function confirmarEliminar(vet: VeterinarioPerfil) {
  const result = await Swal.fire({
    title: '¿Eliminar veterinario?',
    text: nombreCompleto(vet),
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar',
  })

  if (result.isConfirmed) {
    await veterinarioStore.eliminar(vet.id)
    await veterinarioStore.obtenerTodos()
    Swal.fire({ icon: 'success', title: 'Veterinario eliminado', timer: 1500, showConfirmButton: false })
  }
}
</script>