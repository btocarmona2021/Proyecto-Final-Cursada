<template>
  <div class="d-flex flex-column vh-100">

    <!-- TOPBAR -->
    <nav
      class="navbar navbar-expand navbar-light bg-white border-bottom px-3"
      style="height: 52px"
    >
      <span class="navbar-brand fw-bold text-success me-3">
        <span class="badge bg-success me-1">V</span> VetSystem
      </span>

      <input
        class="form-control form-control-sm w-auto flex-grow-1 mx-3"
        style="max-width: 340px"
        type="text"
        placeholder="Buscar paciente, dueño o turno..."
      />

      <div class="ms-auto d-flex align-items-center gap-2">
        <button class="btn btn-sm btn-outline-secondary" @click="cerrarSesion">
          Salir
        </button>
        <span class="badge bg-success fs-6">{{ iniciales }}</span>
      </div>
    </nav>


    <!-- BODY: sidebar + contenido -->
    
    <div class="d-flex flex-grow-1 overflow-hidden">
      <!-- SIDEBAR -->
      <nav
        class="bg-white border-end d-flex flex-column py-2"
        style="width: 220px; overflow-y: auto"
      >
        <!-- PRINCIPAL -->
        <p
          class="text-uppercase text-muted px-3 mb-1"
          style="font-size: 10px; font-weight: 700; letter-spacing: 0.1em"
        >
          Principal
        </p>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/dashboard"
          active-class="active-link"
        >
          🏠 Dashboard
        </RouterLink>
        <RouterLink
          class="nav-link px-3 py-2 d-flex align-items-center"
          to="/admin/agenda"
          active-class="active-link"
        >
          📅 Agenda
          <span v-if="turnosHoy > 0" class="badge bg-success ms-auto">
            {{ turnosHoy }}
          </span>
        </RouterLink>

        <!-- CLÍNICA -->
        <p
          class="text-uppercase text-muted px-3 mb-1 mt-2"
          style="font-size: 10px; font-weight: 700; letter-spacing: 0.1em"
        >
          Clínica
        </p>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/pacientes"
          active-class="active-link"
        >
          🐾 Pacientes
        </RouterLink>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/historia"
          active-class="active-link"
        >
          📋 Historia Clínica
        </RouterLink>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/duenos"
          active-class="active-link"
        >
          👤 Dueños
        </RouterLink>
        <RouterLink
          class="nav-link px-3 py-2 d-flex align-items-center"
          to="/admin/internaciones"
          active-class="active-link"
        >
          🏥 Internaciones
          <span v-if="internacionesActivas > 0" class="badge bg-danger ms-auto">
            {{ internacionesActivas }}
          </span>
        </RouterLink>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/vacunas"
          active-class="active-link"
        >
          💉 Vacunas
        </RouterLink>

        <!-- GESTIÓN -->
        <p
          class="text-uppercase text-muted px-3 mb-1 mt-2"
          style="font-size: 10px; font-weight: 700; letter-spacing: 0.1em"
        >
          Gestión
        </p>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/veterinarios"
          active-class="active-link"
        >
          👨‍⚕️ Veterinarios
        </RouterLink>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/razas"
          active-class="active-link"
        >
          🐶 Razas y Especies
        </RouterLink>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/servicios"
          active-class="active-link"
        >
          🧾 Servicios
        </RouterLink>

        <!-- ANALÍTICA -->
        <p
          class="text-uppercase text-muted px-3 mb-1 mt-2"
          style="font-size: 10px; font-weight: 700; letter-spacing: 0.1em"
        >
          Analítica
        </p>
        <RouterLink
          class="nav-link px-3 py-2"
          to="/admin/reportes"
          active-class="active-link"
        >
          📊 Reportes
        </RouterLink>
      </nav>

      <!-- CONTENIDO -->
      <main class="flex-grow-1 overflow-auto p-4 bg-light">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

const turnosHoy = ref(0)
const internacionesActivas = ref(0)

const iniciales = computed(
  () => authStore.grupo?.slice(0, 2).toUpperCase() ?? 'US'
)

const cerrarSesion = () => authStore.logout()
</script>

<style scoped>
.active-link {
  color: #198754 !important;
  font-weight: 600;
  background: #d1e7dd;
  border-left: 3px solid #198754;
}
.nav-link {
  color: #555;
  font-size: 13px;
  border-left: 3px solid transparent;
}
.nav-link:hover {
  background: #f8f9fa;
  color: #000;
}
</style>