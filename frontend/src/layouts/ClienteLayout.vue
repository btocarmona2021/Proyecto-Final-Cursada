<!-- src/layouts/ClienteLayout.vue -->
<template>
  <div class="cliente-layout d-flex flex-column">
    <!-- TOPBAR -->
    <nav
      class="navbar navbar-light bg-white border-bottom flex-shrink-0 px-3"
      style="min-height: 56px"
    >
      <span style="max-width: 30%" class="navbar-brand fw-bold text-success mb-0">
        <MarcaClinica />
      </span>
      <div class="ms-auto d-flex align-items-center gap-2">
        <button
          class="btn btn-sm btn-outline-secondary position-relative"
          @click="alternarNotificaciones"
        >
          🔔
          <span
            v-if="cantidadNotif > 0"
            class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
            style="font-size: 9px"
          >
            {{ cantidadNotif }}
          </span>
        </button>
        <span class="small fw-semibold d-none d-sm-inline">
          Hola, <strong>{{ nombreUsuario }}</strong>
        </span>
        <FotoSesion :alternativa="iniciales" @nombre-cargado="nombreUsuario = $event" />
        <button class="btn btn-sm btn-outline-danger" @click="cerrarSesion">Salir</button>
      </div>
    </nav>

    <!-- CONTENIDO -->
    <main class="cliente-contenido flex-grow-1 overflow-auto">
      <RouterView />
    </main>

    <!-- PANEL NOTIFICACIONES -->
    <div
      v-if="mostrarNotif"
      class="position-fixed top-0 start-0 w-100 h-100"
      style="z-index: 1050"
      @click.self="alternarNotificaciones"
    >
      <div
        class="position-fixed bg-white border rounded-4 shadow-lg p-0"
        style="top: 64px; right: 16px; width: 360px; max-width: calc(100vw - 32px); z-index: 1060"
      >
        <div class="d-flex justify-content-between align-items-center p-3 border-bottom">
          <span class="fw-bold">Notificaciones</span>
          <button class="btn btn-sm btn-outline-secondary" @click="alternarNotificaciones">
            Cerrar
          </button>
        </div>
        <div class="p-2" style="max-height: 400px; overflow-y: auto">
          <div
            v-for="n in notificacionStore.notificaciones.slice(0, 10)"
            :key="n.id"
            class="alert mb-2 py-2 px-3"
            :class="n.leida ? 'alert-secondary' : alertaTipo(n.tipo)"
          >
            <div class="fw-bold small">
              {{ n.titulo }}
            </div>
            <div class="small">
              {{ n.mensaje }}
            </div>
            <div class="text-muted" style="font-size: 11px">
              {{ formatearFecha(n.created_at) }}
            </div>
          </div>
          <div
            v-if="notificacionStore.notificaciones.length === 0"
            class="text-center text-muted py-3 small"
          >
            Sin notificaciones
          </div>
        </div>
      </div>
    </div>

    <!-- BOTTOM NAV -->
    <nav class="navbar bg-white border-top p-0 flex-shrink-0">
      <div class="d-flex w-100">
        <RouterLink class="bnav-item" :to="{ name: 'ClienteInicio' }" active-class="bnav-active">
          <span>🏠</span> Inicio
        </RouterLink>
        <RouterLink class="bnav-item" :to="{ name: 'ClienteMascotas' }" active-class="bnav-active">
          <span>🐾</span> Mascotas
        </RouterLink>
        <RouterLink class="bnav-item" :to="{ name: 'ClienteTurnos' }" active-class="bnav-active">
          <span>📅</span> Turnos
        </RouterLink>
        <RouterLink
          class="bnav-item"
          :to="{ name: 'ClienteInternacion', params: { id: 1 } }"
          active-class="bnav-active"
        >
          <span>🏥</span> Internación
        </RouterLink>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import MarcaClinica from '@/components/MarcaClinica.vue'
import FotoSesion from '@/components/FotoSesion.vue'
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useNotificacionStore } from '@/stores/notificacionStore'

const authStore = useAuthStore()
const notificacionStore = useNotificacionStore()

const mostrarNotif = ref(false)

const cantidadNotif = computed(() => notificacionStore.noLeidas)
const nombreUsuario = ref('Cliente')
const iniciales = computed(() => 'CL')

onMounted(() => {
  notificacionStore.obtenerTodos()
})

const alternarNotificaciones = () => {
  mostrarNotif.value = !mostrarNotif.value
}

const cerrarSesion = () => {
  authStore.cerrarSesion()
}

function alertaTipo(tipo: string) {
  const map: Record<string, string> = {
    turno: 'alert-primary',
    vacuna: 'alert-warning',
    internacion: 'alert-danger',
    sistema: 'alert-info',
  }
  return map[tipo] ?? 'alert-secondary'
}

function formatearFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString('es-AR', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.cliente-layout {
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
}
.cliente-contenido {
  min-height: 0;
  width: 100%;
  max-width: 1040px;
  margin: 0 auto;
  padding: 12px 16px;
}
.bnav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 4px;
  font-size: 10px;
  font-weight: 600;
  color: #6c757d;
  text-decoration: none;
  border-top: 2px solid transparent;
  gap: 2px;
}
.bnav-item span {
  font-size: 1.3rem;
}
.bnav-active {
  color: #198754 !important;
  border-top-color: #198754;
}
</style>
