<script setup lang="ts">
import { computed } from 'vue'
import type { HorarioVeterinario } from '@/interfaces/horarioVeterinarioInterface'

interface Props {
  horarios: HorarioVeterinario[]
}

const props = defineProps<Props>()

defineEmits<{
  agregar: []
  editar: [horario: HorarioVeterinario]
  eliminar: [id: number]
}>()

const NOMBRES_DIAS: Record<number, string> = {
  1: 'Lunes',
  2: 'Martes',
  3: 'Miércoles',
  4: 'Jueves',
  5: 'Viernes',
  6: 'Sábado',
  7: 'Domingo'
}

const diasAgrupados = computed(() => {
  const grupos: Record<number, { numero: number; nombre: string; horarios: HorarioVeterinario[] }> = {}

  props.horarios.forEach(h => {
    if (!grupos[h.dia_semana]) {
      grupos[h.dia_semana] = {
        numero: h.dia_semana,
        nombre: NOMBRES_DIAS[h.dia_semana] || 'Desconocido',
        horarios: []
      }
    }
    grupos[h.dia_semana]!.horarios.push(h)
  })

  return Object.values(grupos).sort((a, b) => a.numero - b.numero)
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="fw-bold mb-0">Horarios disponibles</h6>
      <button class="btn btn-sm btn-success" @click="$emit('agregar')">
        + Agregar horario
      </button>
    </div>

    <div v-if="horarios.length === 0" class="text-muted text-center py-3">
      No hay horarios cargados
    </div>

    <div v-else class="calendar-week">
      <div v-for="dia in diasAgrupados" :key="dia.numero" class="mb-3">
        <div class="d-flex align-items-center mb-2">
          <span class="badge bg-primary me-2">{{ dia.nombre }}</span>
          <div class="flex-grow-1" style="height:1px;background:#dee2e6;"></div>
        </div>
        <div class="row g-2">
          <div v-for="horario in dia.horarios" :key="horario.id" class="col-md-6">
            <div class="card border-start border-primary border-3">
              <div class="card-body py-2 px-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <i class="bi bi-clock me-1"></i>
                    <strong>{{ horario.hora_inicio.slice(0, 5) }}</strong> -
                    <strong>{{ horario.hora_fin.slice(0, 5) }}</strong>
                  </div>
                  <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-outline-primary" @click="$emit('editar', horario)">
                      Editar
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="$emit('eliminar', horario.id)">
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.calendar-week {
  max-width: 100%;
}
</style>