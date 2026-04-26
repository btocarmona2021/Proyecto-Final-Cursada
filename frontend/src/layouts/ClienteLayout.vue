<template>
  <div class="app">

    <!-- TOPBAR -->
    <header class="topbar">
      <div class="logo">
        <div class="logo-icon">V</div>
        VetSystem
      </div>

      <div class="ml-auto">
        <button class="tbtn" @click="toggleNotificaciones">
          🔔 <span v-if="notifCount > 0" class="nbadge">{{ notifCount }}</span>
        </button>
        <button class="tbtn" @click="toggleTheme">🌙</button>
        <span class="saludo">Hola, <strong>{{ nombreUsuario }}</strong></span>
        <div class="avatar">{{ iniciales }}</div>
        <button class="tbtn" @click="cerrarSesion">Salir</button>
      </div>
    </header>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- PANEL DE NOTIFICACIONES -->
    <div class="notif-overlay" v-if="mostrarNotif" @click.self="toggleNotificaciones">
      <div class="notif-panel">
        <div class="notif-header">
          <span style="font-weight: 800">Notificaciones</span>
          <button class="tbtn" @click="toggleNotificaciones">Cerrar</button>
        </div>
        <div class="notif-list">
          <slot name="notificaciones">
            <div class="notif-item notif-error">
              <div class="notif-title">Nuevo reporte de internación</div>
              <div class="notif-body">Luna tuvo una buena evolución hoy.</div>
              <div class="notif-time">Hace 15 minutos</div>
            </div>
            <div class="notif-item notif-warn">
              <div class="notif-title">Vacuna por vencer</div>
              <div class="notif-body">La antirrábica de Max vence en 3 días.</div>
              <div class="notif-time">Hoy</div>
            </div>
          </slot>
        </div>
      </div>
    </div>

    <!-- BOTTOM NAV -->
    <nav class="bottom-nav">
      <router-link class="bnav-item" to="/cliente/inicio" active-class="active">
        <span class="bnav-icon">🏠</span>
        Inicio
      </router-link>
      <router-link class="bnav-item" to="/cliente/mascotas" active-class="active">
        <span class="bnav-icon">🐾</span>
        Mascotas
      </router-link>
      <router-link class="bnav-item" to="/cliente/turnos" active-class="active">
        <span class="bnav-icon">📅</span>
        Turnos
      </router-link>
      <router-link class="bnav-item" to="/cliente/internacion" active-class="active">
        <span class="bnav-icon">🏥</span>
        Internación
      </router-link>
    </nav>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const mostrarNotif = ref(false)
const notifCount = ref(2)

const nombreUsuario = computed(() => authStore.grupo ?? 'Usuario')
const iniciales = computed(() => {
  return authStore.grupo?.slice(0, 2).toUpperCase() ?? 'US'
})

const toggleNotificaciones = () => {
  mostrarNotif.value = !mostrarNotif.value
}

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
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* TOPBAR */
.topbar {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 0 20px;
  height: 56px;
  display: flex;
  align-items: center;
  gap: 14px;
  position: sticky;
  top: 0;
  z-index: 50;
}

.logo {
  font-weight: 800;
  font-size: 1.1rem;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
}

.ml-auto {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.saludo {
  font-size: 13px;
  font-weight: 600;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary-highlight);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-primary);
}

.tbtn {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 7px;
  padding: 5px 10px;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: 13px;
  position: relative;
}
.tbtn:hover {
  background: var(--color-surface-2);
}

.nbadge {
  background: var(--color-primary);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 99px;
  margin-left: 2px;
}

/* MAIN */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  max-width: 720px;
  margin: 0 auto;
  width: 100%;
  padding-bottom: 80px; /* espacio para el bottom nav */
}

/* NOTIFICACIONES */
.notif-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
}

.notif-panel {
  position: fixed;
  top: 64px;
  right: 20px;
  width: 360px;
  max-width: calc(100vw - 24px);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  z-index: 120;
}

.notif-header {
  padding: 16px 18px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.notif-list {
  max-height: 420px;
  overflow-y: auto;
  padding: 10px;
}

.notif-item {
  padding: 12px;
  border-radius: 12px;
  margin-bottom: 10px;
  border: 1px solid var(--color-border);
}
.notif-error {
  background: var(--color-error-highlight);
  border-color: var(--color-error);
}
.notif-warn {
  background: var(--color-warning-highlight);
  border-color: var(--color-warning);
}
.notif-title {
  font-size: 12px;
  font-weight: 800;
}
.notif-body {
  font-size: 13px;
  margin-top: 4px;
}
.notif-time {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 6px;
}

/* BOTTOM NAV */
.bottom-nav {
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  display: flex;
  position: sticky;
  bottom: 0;
  z-index: 50;
}

.bnav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 4px 8px;
  cursor: pointer;
  color: var(--color-text-faint);
  font-size: 10px;
  font-weight: 600;
  gap: 3px;
  border-top: 2px solid transparent;
  transition: 0.15s;
  text-decoration: none;
}
.bnav-item.active {
  color: var(--color-primary);
  border-top-color: var(--color-primary);
}

.bnav-icon {
  font-size: 1.3rem;
}
</style>
