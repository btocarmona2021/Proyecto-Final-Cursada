<template>
  <div class="app">

    <!-- TOPBAR -->
    <header class="topbar">
      <div class="logo">
        <div class="logo-icon">V</div>
        VetSystem
      </div>

      <!-- Búsqueda global -->
      <div class="search-wrap">
        <input
          class="search-input"
          type="text"
          placeholder="Buscar paciente, dueño o turno..."
        />
      </div>

      <div class="ml-auto">
        <button class="tbtn" @click="toggleTheme">Tema</button>
        <div class="avatar">{{ iniciales }}</div>
        <button class="tbtn" @click="cerrarSesion">Salir</button>
      </div>
    </header>

    <!-- SIDEBAR -->
    <nav class="sidebar">
      <div class="nav-sec">Principal</div>
      <router-link class="nav-item" to="/admin/dashboard" active-class="active">
        <span class="nav-icon">⊞</span> Dashboard
      </router-link>
      <router-link class="nav-item" to="/admin/agenda" active-class="active">
        <span class="nav-icon">📅</span> Agenda
        <span v-if="turnosHoy > 0" class="nbadge">{{ turnosHoy }}</span>
      </router-link>

      <div class="nav-sec">Clínica</div>
      <router-link class="nav-item" to="/admin/pacientes" active-class="active">
        <span class="nav-icon">🐾</span> Pacientes
      </router-link>
      <router-link class="nav-item" to="/admin/historia" active-class="active">
        <span class="nav-icon">📋</span> Historia Clínica
      </router-link>
      <router-link class="nav-item" to="/admin/duenos" active-class="active">
        <span class="nav-icon">👤</span> Dueños
      </router-link>
      <router-link class="nav-item" to="/admin/internaciones" active-class="active">
        <span class="nav-icon">🏥</span> Internaciones
        <span v-if="internacionesActivas > 0" class="nbadge">{{ internacionesActivas }}</span>
      </router-link>

      <div class="nav-sec">Gestión</div>
      <router-link
        v-if="authStore.esAdmin"
        class="nav-item"
        to="/admin/veterinarios"
        active-class="active"
      >
        <span class="nav-icon">👨‍⚕️</span> Veterinarios
      </router-link>
      <router-link
        v-if="authStore.esAdmin"
        class="nav-item"
        to="/admin/razas"
        active-class="active"
      >
        <span class="nav-icon">🐶</span> Razas y Especies
      </router-link>
      <router-link
        v-if="authStore.esAdmin"
        class="nav-item"
        to="/admin/reportes"
        active-class="active"
      >
        <span class="nav-icon">📊</span> Reportes
      </router-link>
    </nav>

    <!-- CONTENIDO -->
    <main class="main">
      <router-view />
    </main>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Badges (luego los conectás a la API)
const turnosHoy = ref(5)
const internacionesActivas = ref(3)

// Iniciales del usuario en el avatar
const iniciales = computed(() => {
  return authStore.grupo?.slice(0, 2).toUpperCase() ?? 'US'
})

const cerrarSesion = () => {
  authStore.logout()
}

const toggleTheme = () => {
  const html = document.documentElement
  html.setAttribute(
    'data-theme',
    html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
  )
}
</script>

<style scoped>
.app {
  display: grid;
  grid-template-columns: 220px 1fr;
  grid-template-rows: 52px 1fr;
  height: 100vh;
  overflow: hidden;
}

/* TOPBAR */
.topbar {
  grid-column: 1 / -1;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 16px;
  z-index: 10;
}

.logo {
  font-weight: 800;
  font-size: 1.15rem;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.logo-icon {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
}

.search-wrap {
  flex: 1;
  max-width: 340px;
}

.search-input {
  width: 100%;
  padding: 7px 12px;
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  color: var(--color-text);
  font-size: 13px;
  outline: none;
}

.ml-auto {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-primary-highlight);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--color-primary);
}

.tbtn {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: 5px 8px;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: 13px;
}
.tbtn:hover {
  background: var(--color-surface-2);
}

/* SIDEBAR */
.sidebar {
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
  padding: 8px 0;
}

.nav-sec {
  padding: 14px 12px 4px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: 13px;
  border-left: 3px solid transparent;
  transition: all 0.15s;
  text-decoration: none;
}
.nav-item:hover {
  background: var(--color-surface-2);
  color: var(--color-text);
}
.nav-item.active {
  background: var(--color-primary-highlight);
  color: var(--color-primary);
  border-left-color: var(--color-primary);
  font-weight: 600;
}

.nav-icon {
  font-size: 15px;
  width: 18px;
  text-align: center;
}

.nbadge {
  margin-left: auto;
  background: var(--color-primary);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 7px;
  border-radius: 99px;
}

/* MAIN */
.main {
  overflow-y: auto;
  padding: 28px;
  background: var(--color-bg);
}
</style>
