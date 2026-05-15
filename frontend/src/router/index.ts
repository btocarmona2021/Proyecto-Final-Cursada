// src/router/index.ts
import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { invitado: true },
  },

  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiereAuth: true, roles: ['administradores', 'veterinarios'] },
    children: [
      { path: '', redirect: { name: 'Dashboard' } },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/admin/DashboardView.vue'),
      },
      {
        path: 'agenda',
        name: 'Agenda',
        component: () => import('@/views/admin/AgendaView.vue'),
      },
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
      {
        path: 'duenos',
        name: 'Duenos',
        component: () => import('@/views/admin/DuenosView.vue'),
      },
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
        path: 'vacunas',
        name: 'Vacunas',
        component: () => import('@/views/admin/VacunasView.vue'),
      },
      {
        path: 'veterinarios',
        name: 'Veterinarios',
        component: () => import('@/views/admin/VeterinariosView.vue'),
      },
      {
        path: 'razas',
        name: 'Razas',
        component: () => import('@/views/admin/RazasView.vue'),
      },
      {
        path: 'servicios',
        name: 'Servicios',
        component: () => import('@/views/admin/ServiciosView.vue'),
      },
      {
        path: 'reportes',
        name: 'Reportes',
        component: () => import('@/views/admin/ReportesView.vue'),
      },
    ],
  },

  {
    path: '/cliente',
    component: () => import('@/layouts/ClienteLayout.vue'),
    meta: { requiereAuth: true, roles: ['clientes'] },
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

  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

function destinoPorRol(to: RouteLocationNormalized, auth: ReturnType<typeof useAuthStore>) {
  if (to.name === 'Login' && auth.estaAutenticado) {
    const rol = auth.grupo

    if (rol === 'clientes') {
      return { name: 'ClienteInicio' }
    }

    if (rol === 'administradores' || rol === 'veterinarios') {
      return { name: 'Dashboard' }
    }

    return { path: '/login' }
  }

  return true
}

router.beforeEach((to) => {
  const auth = useAuthStore()

  const redireccionRol = destinoPorRol(to, auth)
  if (redireccionRol !== true) {
    return redireccionRol
  }

  if (to.meta.requiereAuth && !auth.estaAutenticado) {
    if (to.path !== '/login') {
      return '/login'
    }
  }

  return true
})

export default router