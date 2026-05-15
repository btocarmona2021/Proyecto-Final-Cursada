<template>
  <div>
    <div class="mb-4">
      <h4 class="fw-bold mb-1">Reportes y Estadísticas</h4>
      <p class="text-muted small mb-0">Análisis de datos de la clínica veterinaria</p>
    </div>

    <!-- Filtros -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-3">
            <label class="form-label fw-semibold small">Fecha desde</label>
            <input type="date" class="form-control form-control-sm" v-model="filtros.fechaDesde" />
          </div>
          <div class="col-md-3">
            <label class="form-label fw-semibold small">Fecha hasta</label>
            <input type="date" class="form-control form-control-sm" v-model="filtros.fechaHasta" />
          </div>
          <div class="col-md-3">
            <label class="form-label fw-semibold small">Veterinario</label>
            <select class="form-select form-select-sm" v-model="filtros.veterinario">
              <option value="">Todos</option>
              <option v-for="v in veterinarios" :key="v.id" :value="v.id">
                {{ v.usuario.first_name }} {{ v.usuario.last_name }}
              </option>
            </select>
          </div>
          <div class="col-md-3 d-flex align-items-end">
            <button class="btn btn-success btn-sm w-100" @click="cargarReportes">
              📊 Generar reporte
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- KPIs -->
    <div class="row g-3 mb-4">
      <div class="col-md-3">
        <div class="card border-0 shadow-sm text-center">
          <div class="card-body">
            <div class="text-muted small mb-1">Total turnos</div>
            <div class="fs-3 fw-bold text-primary">{{ stats.totalTurnos }}</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm text-center">
          <div class="card-body">
            <div class="text-muted small mb-1">Pacientes atendidos</div>
            <div class="fs-3 fw-bold text-success">{{ stats.pacientesAtendidos }}</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm text-center">
          <div class="card-body">
            <div class="text-muted small mb-1">Consultas realizadas</div>
            <div class="fs-3 fw-bold text-info">{{ stats.totalConsultas }}</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm text-center">
          <div class="card-body">
            <div class="text-muted small mb-1">Tasa ocupación</div>
            <div class="fs-3 fw-bold text-warning">{{ stats.tasaOcupacion }}%</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Gráficos -->
    <div class="row g-3 mb-4">
      <!-- Turnos por estado -->
      <div class="col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white">
            <span class="fw-semibold">Turnos por estado</span>
          </div>
          <div class="card-body" style="height: 300px">
            <v-chart :option="chartTurnosPorEstado" autoresize style="height: 100%" />
          </div>
        </div>
      </div>

      <!-- Evolución mensual -->
      <div class="col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white">
            <span class="fw-semibold">Evolución de turnos (últimos 6 meses)</span>
          </div>
          <div class="card-body" style="height: 300px">
            <v-chart :option="chartEvolucion" autoresize style="height: 100%" />
          </div>
        </div>
      </div>
    </div>

    <!-- Top servicios -->
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white">
            <span class="fw-semibold">Servicios más solicitados</span>
          </div>
          <div class="card-body" style="height: 300px">
            <v-chart :option="chartServicios" autoresize style="height: 100%" />
          </div>
        </div>
      </div>

      <!-- Razas más atendidas -->
      <div class="col-md-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white">
            <span class="fw-semibold">Top 10 razas más atendidas</span>
          </div>
          <div class="card-body" style="height: 300px">
            <v-chart :option="chartRazas" autoresize style="height: 100%" />
          </div>
        </div>
      </div>
    </div>

    <!-- Tabla resumen -->
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white d-flex justify-content-between align-items-center">
        <span class="fw-semibold">Detalle de turnos</span>
        <button class="btn btn-sm btn-outline-success">
          📥 Exportar Excel
        </button>
      </div>
      <div class="card-body p-0">
        <div v-if="cargando" class="text-center text-muted py-5">
          Cargando datos...
        </div>
        <div v-else-if="turnos.length === 0" class="text-center text-muted py-5">
          No hay datos para el período seleccionado
        </div>
        <table v-else class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Fecha</th>
              <th>Mascota</th>
              <th>Dueño</th>
              <th>Veterinario</th>
              <th>Servicio</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in turnos.slice(0, 20)" :key="t.id">
              <td class="small">{{ formatFecha(t.fecha_hora) }}</td>
              <td class="fw-semibold small">{{ t.mascota_nombre }}</td>
              <td class="small">{{ t.dueno_nombre }}</td>
              <td class="small">{{ t.veterinario_nombre }}</td>
              <td class="small">{{ t.servicio_nombre }}</td>
              <td>
                <span class="badge" :class="badgeEstado(t.estado)">
                  {{ t.estado_display }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTurnoStore } from '@/stores/turnoStore'
import { useVeterinarioStore } from '@/stores/veterinarioStore'
import { useMascotaStore } from '@/stores/mascotaStore'
import type { EstadoTurno } from '@/interfaces/turnoInterface'

const turnoStore = useTurnoStore()
const veterinarioStore = useVeterinarioStore()
const mascotaStore = useMascotaStore()

const cargando = ref(false)

const filtros = ref({
  fechaDesde: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().slice(0, 10),
  fechaHasta: new Date().toISOString().slice(0, 10),
  veterinario: '',
})

const stats = ref({
  totalTurnos: 0,
  pacientesAtendidos: 0,
  totalConsultas: 0,
  tasaOcupacion: 0,
})

onMounted(async () => {
  await Promise.all([
    turnoStore.obtenerTodos(),
    veterinarioStore.obtenerTodos(),
    mascotaStore.obtenerTodos(),
  ])
  cargarReportes()
})

const veterinarios = computed(() => veterinarioStore.veterinarios)

const turnos = computed(() => {
  return turnoStore.turnos.filter(t => {
    const fecha = t.fecha_hora.slice(0, 10)
    const cumpleFecha = fecha >= filtros.value.fechaDesde && fecha <= filtros.value.fechaHasta
    const cumpleVet = !filtros.value.veterinario || t.veterinario_id === Number(filtros.value.veterinario)
    return cumpleFecha && cumpleVet
  })
})

// Gráfico: Turnos por estado (Pie)
const chartTurnosPorEstado = computed(() => {
  const data = {} as Record<string, number>
  
  turnos.value.forEach(t => {
    data[t.estado_display] = (data[t.estado_display] || 0) + 1
  })

  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: 0,
      left: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 18,
            fontWeight: 'bold'
          }
        },
        data: Object.entries(data).map(([name, value]) => ({ name, value }))
      }
    ]
  }
})

// Gráfico: Evolución mensual (Line)
const chartEvolucion = computed(() => {
  const meses: Record<string, number> = {}
  
  turnos.value.forEach(t => {
    const mes = t.fecha_hora.slice(0, 7)
    meses[mes] = (meses[mes] || 0) + 1
  })

  const labels = Object.keys(meses).sort()
  const values = labels.map(m => meses[m])

  return {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: labels,
      boundaryGap: false
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        type: 'line',
        data: values,
        smooth: true,
        areaStyle: {
          color: 'rgba(25, 135, 84, 0.1)'
        },
        itemStyle: {
          color: '#198754'
        },
        lineStyle: {
          width: 3
        }
      }
    ]
  }
})

// Gráfico: Servicios más solicitados (Bar)
const chartServicios = computed(() => {
  const data: Record<string, number> = {}
  
  turnos.value.forEach(t => {
    data[t.servicio_nombre] = (data[t.servicio_nombre] || 0) + 1
  })

  const sorted = Object.entries(data)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: sorted.map(([name]) => name)
    },
    series: [
      {
        type: 'bar',
        data: sorted.map(([, value]) => value),
        itemStyle: {
          color: '#0d6efd',
          borderRadius: [0, 4, 4, 0]
        }
      }
    ]
  }
})

// Gráfico: Top razas (Bar horizontal)
const chartRazas = computed(() => {
  const razaCount: Record<string, number> = {}
  
  turnos.value.forEach(t => {
    const mascota = mascotaStore.mascotas.find(m => m.id === t.mascota_id)
    if (mascota?.raza_nombre) {
      razaCount[mascota.raza_nombre] = (razaCount[mascota.raza_nombre] || 0) + 1
    }
  })

  const sorted = Object.entries(razaCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: sorted.map(([name]) => name),
      axisLabel: {
        fontSize: 11
      }
    },
    series: [
      {
        type: 'bar',
        data: sorted.map(([, value]) => value),
        itemStyle: {
          color: '#198754',
          borderRadius: [0, 4, 4, 0]
        }
      }
    ]
  }
})

function cargarReportes() {
  cargando.value = true
  
  const turnosFiltrados = turnos.value
  stats.value.totalTurnos = turnosFiltrados.length
  
  const mascotasUnicas = new Set(turnosFiltrados.map(t => t.mascota_id))
  stats.value.pacientesAtendidos = mascotasUnicas.size
  
  stats.value.totalConsultas = turnosFiltrados.filter(t => 
    t.estado === 'atendido' || t.estado === 'en_consulta'
  ).length
  
  stats.value.tasaOcupacion = turnosFiltrados.length > 0
    ? Math.round((stats.value.totalConsultas / turnosFiltrados.length) * 100)
    : 0

  setTimeout(() => {
    cargando.value = false
  }, 500)
}

function formatFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString('es-AR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function badgeEstado(estado: EstadoTurno) {
  const map: Record<EstadoTurno, string> = {
    reservado: 'bg-primary',
    confirmado: 'bg-success',
    en_espera: 'bg-warning text-dark',
    en_consulta: 'bg-info text-dark',
    atendido: 'bg-secondary',
    cancelado: 'bg-danger',
  }
  return map[estado] ?? 'bg-secondary'
}
</script>