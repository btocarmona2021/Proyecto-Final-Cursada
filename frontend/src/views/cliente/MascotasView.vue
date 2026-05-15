<!-- src/views/cliente/MascotasView.vue -->
<template>
  <div class="container-fluid">
    <!-- Encabezado -->
    <div class="mb-3 d-flex justify-content-between align-items-center">
      <div>
        <h4 class="fw-bold mb-1">Mis mascotas</h4>
        <p class="text-muted mb-0" style="font-size: 13px">
          Listado de tus mascotas registradas en la clínica
        </p>
      </div>
      <RouterLink
        :to="{ name: 'ClienteReservar' }"
        class="btn btn-sm btn-success d-none d-sm-inline-flex align-items-center"
      >
        <span class="me-1">🗓️</span>
        Reservar turno
      </RouterLink>
    </div>

    <!-- Buscador -->
    <div class="mb-3">
      <input
        v-model="busqueda"
        type="text"
        class="form-control form-control-sm"
        placeholder="Buscar por nombre, especie o raza..."
      />
    </div>

    <!-- Estado de carga -->
    <div
      v-if="cargando"
      class="text-center text-muted py-4"
      style="font-size: 13px"
    >
      Cargando mascotas...
    </div>

    <!-- Sin mascotas -->
    <div
      v-else-if="mascotasFiltradas.length === 0"
      class="alert alert-secondary"
      style="font-size: 13px"
    >
      Todavía no tenés mascotas registradas. Contactá a la clínica para dar de alta
      a tu mascota o hazlo en tu próxima visita.
    </div>

    <!-- Lista de mascotas -->
    <div v-else class="row g-2">
      <div
        v-for="m in mascotasFiltradas"
        :key="m.id"
        class="col-12"
      >
        <div
          class="card border-0 shadow-sm mb-1"
          role="button"
          @click="irDetalle(m.id)"
        >
          <div class="card-body d-flex align-items-center gap-3">
            <div
              class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
              style="width: 52px; height: 52px; background: #e7f5ff"
            >
              <span style="font-size: 1.7rem">
                {{ avatarEmoji(m.especie_nombre) }}
              </span>
            </div>
            <div class="flex-grow-1">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <div class="fw-bold" style="font-size: 15px">
                    {{ m.nombre }}
                  </div>
                  <div class="text-muted" style="font-size: 12px">
                    {{ m.especie_nombre }} · {{ m.raza_nombre }}
                  </div>
                  <div
                    v-if="m.peso_actual"
                    class="text-muted"
                    style="font-size: 12px"
                  >
                    Peso: {{ m.peso_actual }} kg
                  </div>
                </div>
                <span
                  class="badge"
                  :class="m.sexo === 'M' ? 'bg-primary' : 'bg-danger'"
                  style="font-size: 11px"
                >
                  {{ m.sexo_display }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMascotaStore } from '@/stores/mascotaStore'
import type { Mascota } from '@/interfaces/mascotaInterface'

const router = useRouter()
const mascotaStore = useMascotaStore()

const busqueda = ref('')
const cargando = ref(false)

onMounted(async () => {
  cargando.value = true
  try {
    await mascotaStore.obtenerTodos()
  } finally {
    cargando.value = false
  }
})

const mascotas = computed<Mascota[]>(() => mascotaStore.mascotas)

const mascotasFiltradas = computed<Mascota[]>(() => {
  const term = busqueda.value.trim().toLowerCase()
  if (!term) return mascotas.value
  return mascotas.value.filter((m) => {
    return (
      m.nombre.toLowerCase().includes(term) ||
      (m.especie_nombre ?? '').toLowerCase().includes(term) ||
      (m.raza_nombre ?? '').toLowerCase().includes(term)
    )
  })
})

function irDetalle(id: number) {
  router.push({ name: 'ClienteMascotaDetalle', params: { id } })
}

function avatarEmoji(especieNombre: string | null | undefined) {
  const lower = especieNombre?.toLowerCase() ?? ''
  if (lower.includes('perro')) return '🐶'
  if (lower.includes('gato')) return '🐱'
  if (lower.includes('ave') || lower.includes('pájaro')) return '🦜'
  if (lower.includes('conejo')) return '🐰'
  return '🐾'
}
</script>