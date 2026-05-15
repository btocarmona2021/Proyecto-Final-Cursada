<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Dueños / Clientes</h4>
      <p class="text-muted small mb-0">Registro de tutores y sus mascotas</p>
    </div>

    <div class="d-flex flex-wrap gap-2 mb-4 align-items-center">
      <button class="btn btn-success" @click="abrirModalNuevo">+ Nuevo dueño</button>
      <input type="text" class="form-control form-control-sm ms-auto" style="max-width:260px"
        placeholder="Buscar dueño..." v-model="busqueda" />
    </div>

    <div v-if="cargandoVista" class="text-center text-muted py-5">
      Cargando dueños...
    </div>

    <div v-else-if="duenosFiltrados.length === 0" class="text-center text-muted py-5">
      No se encontraron dueños
    </div>

    <div v-else>
      <div v-for="dueno in duenosFiltrados" :key="dueno.id" class="card border-0 shadow-sm mb-3">
        <div class="card-body d-flex justify-content-between align-items-start gap-3 flex-wrap">
          <div class="d-flex gap-3 align-items-start">
            <div class="rounded-circle d-flex align-items-center justify-content-center fw-bold"
              style="width:48px;height:48px;background:#d1e7dd;color:#146c43;">
              {{ iniciales(dueno.first_name, dueno.last_name) }}
            </div>

            <div>
              <h6 class="fw-bold mb-1">
                {{ dueno.first_name }} {{ dueno.last_name }}
              </h6>

              <div class="text-muted small mb-1">
                {{ obtenerTelefono(dueno.id) || 'Sin teléfono' }} · {{ dueno.email || 'Sin email' }}
              </div>

              <div class="text-muted small mb-2">
                {{ obtenerDireccion(dueno.id) || 'Sin dirección cargada' }}
              </div>

              <div class="d-flex flex-wrap gap-1">
                <span v-if="mascotasDeUsuario(dueno.id).length === 0" class="badge text-bg-light">
                  Sin mascotas
                </span>

                <span v-for="m in mascotasDeUsuario(dueno.id)" :key="m.id"
                  class="badge bg-success-subtle text-success-emphasis">
                  {{ m.nombre }}
                </span>
              </div>
            </div>
          </div>

          <div class="d-flex flex-column align-items-start align-items-md-end gap-2">
            <div class="text-muted small">
              {{ mascotasDeUsuario(dueno.id).length }} mascota(s)
            </div>

            <div class="d-flex gap-2">
              <RouterLink :to="`/admin/duenos/${dueno.id}`" class="btn btn-sm btn-outline-secondary">
                Ver detalle
              </RouterLink>
              <button class="btn btn-sm btn-outline-primary" @click="abrirModalEditar(dueno)">
                Editar
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="confirmarEliminar(dueno)">
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL CREAR / EDITAR -->
    <div class="modal fade" id="modalDueno" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modoEdicion ? 'Editar dueño' : 'Nuevo dueño' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Nombre</label>
                <input type="text" class="form-control" v-model="form.first_name" :disabled="modoEdicion" />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Apellido</label>
                <input type="text" class="form-control" v-model="form.last_name" :disabled="modoEdicion" />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Username</label>
              <input type="text" class="form-control" v-model="form.username" :disabled="modoEdicion" />
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Email</label>
              <input type="email" class="form-control" v-model="form.email" :disabled="modoEdicion" />
            </div>

            <div class="mb-3" v-if="!modoEdicion">
              <label class="form-label fw-semibold">Contraseña</label>
              <input type="password" class="form-control" v-model="form.password" />
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Teléfono</label>
              <input type="text" class="form-control" v-model="form.telefono" />
            </div>

            <div class="mb-3">
              <label class="form-label fw-semibold">Dirección</label>
              <input type="text" class="form-control" v-model="form.direccion" />
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
import { useUsuarioStore } from '@/stores/usuarioStore'
import { usePerfilClienteStore } from '@/stores/perfilClienteStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import type { UsuarioAuth } from '@/interfaces/usuarioInterface'
import type { RegistroClienteForm } from '@/interfaces/perfilUsuarioInterface'

const usuarioStore = useUsuarioStore()
const perfilClienteStore = usePerfilClienteStore()
const mascotaStore = useMascotaStore()

const busqueda = ref('')
const modoEdicion = ref(false)
const guardando = ref(false)
const duenoEditando = ref<UsuarioAuth | null>(null)

const formularioVacio = (): RegistroClienteForm => ({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  telefono: '',
  direccion: '',
})

const form = ref<RegistroClienteForm>(formularioVacio())

onMounted(async () => {
  await Promise.all([
    usuarioStore.obtenerTodos(),
    perfilClienteStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
  ])
})

const cargandoVista = computed(() =>
  usuarioStore.cargando || perfilClienteStore.cargando || mascotaStore.cargando
)

const soloClientes = computed(() =>
  usuarioStore.usuarios.filter((u: UsuarioAuth) => u.grupo === 'clientes')
)

const duenosFiltrados = computed(() =>
  soloClientes.value.filter((u: UsuarioAuth) => {
    const texto = `${u.first_name} ${u.last_name} ${u.email} ${u.username}`.toLowerCase()
    return texto.includes(busqueda.value.toLowerCase())
  })
)

function getPerfilPorUsuario(userId: number) {
  return perfilClienteStore.perfiles.find((p) => p.usuario.id === userId) || null
}

function obtenerTelefono(userId: number) {
  return getPerfilPorUsuario(userId)?.telefono ?? ''
}

function obtenerDireccion(userId: number) {
  return getPerfilPorUsuario(userId)?.direccion ?? ''
}

function mascotasDeUsuario(userId: number) {
  return mascotaStore.mascotas.filter((m) => m.usuario === userId)
}

function iniciales(nombre: string, apellido: string) {
  return `${nombre?.[0] ?? ''}${apellido?.[0] ?? ''}`.toUpperCase()
}

function obtenerModal() {
  return Modal.getOrCreateInstance(document.getElementById('modalDueno')!)
}

function abrirModalNuevo() {
  modoEdicion.value = false
  duenoEditando.value = null
  form.value = formularioVacio()
  obtenerModal().show()
}

function abrirModalEditar(u: UsuarioAuth) {
  modoEdicion.value = true
  duenoEditando.value = u
  form.value = {
    username: u.username,
    password: '',
    first_name: u.first_name,
    last_name: u.last_name,
    email: u.email,
    telefono: obtenerTelefono(u.id),
    direccion: obtenerDireccion(u.id),
  }
  obtenerModal().show()
}

async function guardar() {
  if (!form.value.first_name || !form.value.last_name || !form.value.email || !form.value.username) {
    Swal.fire('Campos requeridos', 'Completá nombre, apellido, username y email.', 'warning')
    return
  }

  if (!modoEdicion.value && !form.value.password) {
    Swal.fire('Campos requeridos', 'La contraseña es obligatoria para crear el dueño.', 'warning')
    return
  }

  guardando.value = true

  try {
    if (modoEdicion.value && duenoEditando.value) {
      const perfil = perfilClienteStore.perfiles.find(
        (p) => p.usuario.id === duenoEditando.value!.id
      )

      if (perfil) {
        await perfilClienteStore.actualizar(perfil.id, {
          telefono: form.value.telefono,
          direccion: form.value.direccion,
        })
      }

      await Promise.all([
        usuarioStore.obtenerTodos(),
        perfilClienteStore.obtenerTodos(),
      ])

      Swal.fire({
        icon: 'success',
        title: 'Dueño actualizado',
        timer: 1500,
        showConfirmButton: false,
      })
    } else {
      await perfilClienteStore.crear(form.value)

      await Promise.all([
        usuarioStore.obtenerTodos(),
        perfilClienteStore.obtenerTodos(),
      ])

      Swal.fire({
        icon: 'success',
        title: 'Dueño creado',
        timer: 1500,
        showConfirmButton: false,
      })
    }

    obtenerModal().hide()
  } catch {
    Swal.fire('Error', 'No se pudo guardar el dueño.', 'error')
  } finally {
    guardando.value = false
  }
}

async function confirmarEliminar(u: UsuarioAuth) {
  const result = await Swal.fire({
    title: '¿Eliminar dueño?',
    text: `${u.first_name} ${u.last_name}`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonText: 'Cancelar',
    confirmButtonText: 'Sí, eliminar',
  })

  if (result.isConfirmed) {
    await usuarioStore.eliminar(u.id)
    await Promise.all([
      usuarioStore.obtenerTodos(),
      perfilClienteStore.obtenerTodos(),
    ])
    Swal.fire({
      icon: 'success',
      title: 'Dueño eliminado',
      timer: 1500,
      showConfirmButton: false,
    })
  }
}
</script>