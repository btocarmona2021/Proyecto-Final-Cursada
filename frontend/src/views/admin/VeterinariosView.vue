<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Veterinarios</h4>
      <p class="text-muted small mb-0">Equipo médico y horarios</p>
    </div>

    <div class="d-flex flex-wrap gap-2 mb-4 align-items-center">
      <button v-if="auth.esAdmin" class="btn btn-success" @click="abrirModalNuevo">
        + Agregar veterinario
      </button>
      <input
        v-model="busqueda"
        type="text"
        class="form-control form-control-sm ms-auto"
        style="max-width: 260px"
        placeholder="Buscar veterinario..."
      />
    </div>

    <div v-if="cargandoVista" class="text-center text-muted py-5">Cargando veterinarios...</div>
    <div v-else-if="errorCarga" class="alert alert-danger">{{ errorCarga }}</div>

    <div v-else-if="veterinariosFiltrados.length === 0" class="text-center text-muted py-5">
      No se encontraron veterinarios
    </div>

    <div v-else>
      <div v-for="vet in veterinariosFiltrados" :key="vet.id" class="card border-0 shadow-sm mb-3">
        <div class="card-body d-flex justify-content-between align-items-start gap-3 flex-wrap">
          <div class="d-flex gap-3 align-items-start">
            <div
              class="rounded-circle d-flex align-items-center justify-content-center fw-bold"
              style="width: 52px; height: 52px; background: #d1e7dd; color: #146c43"
            >
              <img
                v-if="vet.foto"
                :src="urlImagen(vet.foto)"
                alt=""
                class="rounded-circle"
                style="width: 100%; height: 100%; object-fit: cover"
              />
              <span v-else>{{ inicialesVet(vet.usuario.first_name, vet.usuario.last_name) }}</span>
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
                <span
                  class="badge"
                  :class="vet.disponible ? 'text-bg-success' : 'text-bg-secondary'"
                >
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
              <button
                v-if="auth.esAdmin"
                class="btn btn-sm btn-outline-primary"
                @click="abrirModalEditar(vet)"
              >
                Editar
              </button>
              <button class="btn btn-sm btn-outline-success" @click="abrirModalHorario(vet)">
                Horario
              </button>
              <button
                v-if="auth.esAdmin"
                class="btn btn-sm btn-outline-danger"
                @click="confirmarEliminar(vet)"
              >
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
            <ImagenSelector
              v-model="form.foto"
              :actual="veterinarioEditando?.foto"
              etiqueta="Foto del veterinario"
              id="imagen-veterinarios"
            />
            <template v-if="!modoEdicion">
              <div class="mb-3">
                <label class="form-label fw-semibold">Usuario</label>
                <input class="form-control" v-model="form.username" autocomplete="off" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Contraseña inicial</label>
                <input
                  type="password"
                  class="form-control"
                  v-model="form.password"
                  autocomplete="new-password"
                />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Nombre</label>
                <input class="form-control" v-model="form.first_name" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Apellido</label>
                <input class="form-control" v-model="form.last_name" />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold">Email</label>
                <input type="email" class="form-control" v-model="form.email" />
              </div>
            </template>

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

            <div class="form-check" v-if="modoEdicion">
              <input
                id="disponible"
                class="form-check-input"
                type="checkbox"
                v-model="form.disponible"
              />
              <label for="disponible" class="form-check-label"> Disponible </label>
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
                    <div class="mb-3">
                      <img
                        v-if="veterinarioDetalle.foto"
                        :src="urlImagen(veterinarioDetalle.foto)"
                        :alt="`Foto de ${nombreCompleto(veterinarioDetalle)}`"
                        class="rounded-circle"
                        style="width:96px;height:96px;object-fit:cover"
                      />
                      <div
                        v-else
                        class="rounded-circle d-flex align-items-center justify-content-center fw-bold"
                        style="width:96px;height:96px;background:#d1e7dd;color:#146c43;font-size:1.8rem"
                        aria-label="Sin foto de perfil"
                      >
                        {{ inicialesVet(veterinarioDetalle.usuario.first_name, veterinarioDetalle.usuario.last_name) }}
                      </div>
                    </div>
                    <h6 class="fw-bold mb-3">Perfil profesional</h6>
                    <div class="mb-2">
                      <strong>Matrícula:</strong> {{ veterinarioDetalle.matricula }}
                    </div>
                    <div class="mb-2">
                      <strong>Especialidad:</strong>
                      {{ veterinarioDetalle.especialidad || 'Sin especialidad' }}
                    </div>
                    <div class="mb-2">
                      <strong>Email:</strong> {{ veterinarioDetalle.usuario.email || 'Sin email' }}
                    </div>
                    <div class="mb-2">
                      <strong>Estado:</strong>
                      {{ veterinarioDetalle.disponible ? 'Disponible' : 'No disponible' }}
                    </div>
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
              <select
                class="form-select"
                v-model="formHorario.veterinario_id"
                :disabled="modoEdicionHorario"
              >
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
import ImagenSelector from '@/components/ImagenSelector.vue'
import { urlImagen } from '@/utils/imagenes'
import { useAuthStore } from '@/stores/authStore'
import { computed, onMounted, ref } from 'vue'
import { Modal } from 'bootstrap'
import Swal from 'sweetalert2'
import { useVeterinarioStore } from '@/stores/veterinarioStore'
import { useHorarioVeterinarioStore } from '@/stores/horarioVeterinarioStore'
import HorariosCalendario from '@/components/HorariosCalendario.vue'
import type {
  VeterinarioPerfil,
  VeterinarioPerfilForm,
} from '@/interfaces/veterinarioPerfilInterface'
import type {
  HorarioVeterinario,
  HorarioVeterinarioForm,
} from '@/interfaces/horarioVeterinarioInterface'

const auth = useAuthStore()
const veterinarioStore = useVeterinarioStore()
const horarioStore = useHorarioVeterinarioStore()

const busqueda = ref('')
const errorCarga = ref('')
const guardando = ref(false)
const guardandoHorario = ref(false)

const modoEdicion = ref(false)
const modoEdicionHorario = ref(false)

const veterinarioEditando = ref<VeterinarioPerfil | null>(null)
const veterinarioDetalle = ref<VeterinarioPerfil | null>(null)
const horarioEditando = ref<HorarioVeterinario | null>(null)

const formularioVacio = (): VeterinarioPerfilForm => ({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  matricula: '',
  especialidad: '',
  biografia: '',
  disponible: true,
  foto: null,
})

const formularioHorarioVacio = (): HorarioVeterinarioForm => ({
  veterinario_id: 0,
  dia_semana: 1,
  hora_inicio: '',
  hora_fin: '',
})

const form = ref<VeterinarioPerfilForm>(formularioVacio())
const formHorario = ref<HorarioVeterinarioForm>(formularioHorarioVacio())

onMounted(async () => {
  try {
    await Promise.all([veterinarioStore.obtenerTodos(), horarioStore.obtenerTodos()])
  } catch {
    errorCarga.value = 'No se pudieron cargar los veterinarios y sus horarios. Intentá nuevamente.'
  }
})

const cargandoVista = computed(() => veterinarioStore.cargando || horarioStore.cargando)

function nombreCompleto(vet: VeterinarioPerfil): string {
  return `${vet.usuario.first_name} ${vet.usuario.last_name}`
}

const veterinariosFiltrados = computed(() =>
  veterinarioStore.veterinarios.filter((v) => {
    const nombre = nombreCompleto(v)
    const texto =
      `${nombre} ${v.especialidad ?? ''} ${v.matricula} ${v.usuario.email ?? ''}`.toLowerCase()
    return texto.includes(busqueda.value.toLowerCase())
  }),
)

function inicialesVet(primer_nombre: string, apellido: string) {
  return `${primer_nombre?.[0] ?? ''}${apellido?.[0] ?? ''}`.toUpperCase()
}

function horariosDeVeterinario(veterinarioId: number) {
  return horarioStore.horarios.filter((h) => h.veterinario_id === veterinarioId)
}

function horariosOrdenados(veterinarioId: number) {
  return [...horariosDeVeterinario(veterinarioId)].sort((a, b) => a.dia_semana - b.dia_semana)
}

function obtenerModalVeterinario() {
  return Modal.getOrCreateInstance(document.getElementById('modalVeterinario')!)
}

function obtenerModalDetalle() {
  return Modal.getOrCreateInstance(document.getElementById('modalDetalleVeterinario')!)
}

function obtenerModalHorario() {
  return Modal.getOrCreateInstance(document.getElementById('modalHorario')!)
}

function abrirModalNuevo() {
  modoEdicion.value = false
  veterinarioEditando.value = null
  form.value = formularioVacio()
  obtenerModalVeterinario().show()
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
  obtenerModalVeterinario().show()
}

function verDetalle(vet: VeterinarioPerfil) {
  veterinarioDetalle.value = vet
  obtenerModalDetalle().show()
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
  obtenerModalHorario().show()
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
  obtenerModalHorario().show()
}

async function guardarVeterinario() {
  if (!form.value.matricula) {
    Swal.fire('Campos requeridos', 'Completá la matrícula.', 'warning')
    return
  }

  if (
    !modoEdicion.value &&
    (!form.value.username ||
      !form.value.password ||
      !form.value.first_name ||
      !form.value.last_name ||
      !form.value.email)
  ) {
    Swal.fire(
      'Campos requeridos',
      'Completá usuario, contraseña, nombre, apellido y email.',
      'warning',
    )
    return
  }

  guardando.value = true
  try {
    if (modoEdicion.value && veterinarioEditando.value) {
      await veterinarioStore.actualizar(veterinarioEditando.value.id, form.value)
      Swal.fire({
        icon: 'success',
        title: 'Veterinario actualizado',
        timer: 1500,
        showConfirmButton: false,
      })
    } else {
      await veterinarioStore.crear(form.value)
      Swal.fire({
        icon: 'success',
        title: 'Veterinario creado',
        timer: 1500,
        showConfirmButton: false,
      })
    }

    await veterinarioStore.obtenerTodos()
    obtenerModalVeterinario().hide()
  } catch (error: unknown) {
    const data = (error as { response?: { data?: Record<string, unknown> } })?.response?.data
    const msg = String(
      data?.foto ||
        data?.username ||
        data?.email ||
        data?.matricula ||
        data?.detail ||
        data?.non_field_errors ||
        'No se pudo guardar el veterinario.',
    )
    Swal.fire('Error', msg, 'error')
  } finally {
    guardando.value = false
  }
}

async function guardarHorario() {
  if (
    !formHorario.value.veterinario_id ||
    !formHorario.value.hora_inicio ||
    !formHorario.value.hora_fin
  ) {
    Swal.fire('Campos requeridos', 'Completá veterinario, hora inicio y hora fin.', 'warning')
    return
  }

  guardandoHorario.value = true
  try {
    if (modoEdicionHorario.value && horarioEditando.value) {
      await horarioStore.actualizar(horarioEditando.value.id, formHorario.value)
      Swal.fire({
        icon: 'success',
        title: 'Horario actualizado',
        timer: 1500,
        showConfirmButton: false,
      })
    } else {
      await horarioStore.crear(formHorario.value)
      Swal.fire({ icon: 'success', title: 'Horario creado', timer: 1500, showConfirmButton: false })
    }

    await horarioStore.obtenerTodos()
    obtenerModalHorario().hide()
  } catch (error: unknown) {
    const data = (error as { response?: { data?: Record<string, unknown> } })?.response?.data
    const msg = String(data?.detail || data?.non_field_errors || 'No se pudo guardar el horario.')
    Swal.fire('Error', msg, 'error')
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
    Swal.fire({
      icon: 'success',
      title: 'Horario eliminado',
      timer: 1500,
      showConfirmButton: false,
    })
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
    Swal.fire({
      icon: 'success',
      title: 'Veterinario eliminado',
      timer: 1500,
      showConfirmButton: false,
    })
  }
}
</script>
