// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // ── Auth ──────────────────────────────────────
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guest: true },
  },

  // ── Portal Admin/Vet ──────────────────────────
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, roles: ['administradores', 'veterinarios'] },
    children: [
      { path: '', redirect: { name: 'Dashboard' } },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/admin/DashboardView.vue'),
      },
      { path: 'agenda', name: 'Agenda', component: () => import('@/views/admin/AgendaView.vue') },
      {
        path: 'pacientes',
        name: 'Pacientes',
        component: () => import('@/views/admin/PacientesView.vue'),
      },
      {
        path: 'pacientes/:id',
        name: 'PacienteDetalle',
        component: () => import('@/views/admin/PacienteDetalleView.vue'),
      },
      {
        path: 'historia',
        name: 'Historia',
        component: () => import('@/views/admin/HistoriaView.vue'),
      },
      { path: 'duenos', name: 'Duenos', component: () => import('@/views/admin/DuenosView.vue') },
      {
        path: 'duenos/:id',
        name: 'DuenoDetalle',
        component: () => import('@/views/admin/DuenoDetalleView.vue'),
      },
      {
        path: 'internaciones',
        name: 'Internaciones',
        component: () => import('@/views/admin/InternacionesView.vue'),
      },
      {
        path: 'veterinarios',
        name: 'Veterinarios',
        component: () => import('@/views/admin/VeterinariosView.vue'),
      },
      { path: 'razas', name: 'Razas', component: () => import('@/views/admin/RazasView.vue') },
      {
        path: 'reportes',
        name: 'Reportes',
        component: () => import('@/views/admin/ReportesView.vue'),
      },
    ],
  },

  // ── Portal Cliente ────────────────────────────
  {
    path: '/cliente',
    component: () => import('@/layouts/ClienteLayout.vue'),
    meta: { requiresAuth: true, roles: ['clientes'] },
    children: [
      { path: '', redirect: { name: 'ClienteInicio' } },
      {
        path: 'inicio',
        name: 'ClienteInicio',
        component: () => import('@/views/cliente/InicioView.vue'),
      },
      {
        path: 'mascotas',
        name: 'ClienteMascotas',
        component: () => import('@/views/cliente/MascotasView.vue'),
      },
      {
        path: 'mascotas/:id',
        name: 'ClienteMascotaDetalle',
        component: () => import('@/views/cliente/MascotaDetalleView.vue'),
      },
      {
        path: 'turnos',
        name: 'ClienteTurnos',
        component: () => import('@/views/cliente/TurnosView.vue'),
      },
      {
        path: 'reservar',
        name: 'ClienteReservar',
        component: () => import('@/views/cliente/ReservarView.vue'),
      },
      {
        path: 'internacion/:id',
        name: 'ClienteInternacion',
        component: () => import('@/views/cliente/InternacionView.vue'),
      },
    ],
  },

  // ── Fallback ──────────────────────────────────
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.guest && auth.estaAutenticado) {
    return next(auth.redirectByGrupo())
  }

  if (to.meta.requiresAuth && !auth.estaAutenticado) {
    return next('/login')
  }

  if (to.meta.roles && !to.meta.roles.includes(auth.grupo)) {
    return next(auth.redirectByGrupo())
  }

  next()
})

export default router
