<template>
  <div>
    <p v-if="cargando" role="status">Cargando receta…</p>
    <div v-else-if="errorCarga" class="alert alert-danger" role="alert">
      {{ errorCarga }}
      <button type="button" class="btn btn-sm btn-outline-danger ms-2" @click="cargar">
        Reintentar
      </button>
    </div>
    <template v-else>
      <div v-if="error" class="alert alert-danger" role="alert">{{ error }}</div>
      <p v-if="mensaje" class="alert alert-success" role="status">{{ mensaje }}</p>
      <p v-if="items.length === 0" class="text-muted">
        Esta consulta todavía no tiene medicamentos recetados.
      </p>
      <div v-for="item in items" :key="item.id" class="mb-3">
        <RecetaDetalle :items="[item]" />
        <div class="d-flex gap-2">
          <button
            type="button"
            class="btn btn-sm btn-outline-primary"
            :disabled="guardando"
            @click="editar(item)"
          >
            Editar medicamento
          </button>
          <button
            type="button"
            class="btn btn-sm btn-outline-danger"
            :disabled="guardando"
            @click="eliminar(item)"
          >
            Eliminar medicamento
          </button>
        </div>
      </div>
      <form @submit.prevent="guardar" class="border-top pt-3 mt-3">
        <h6>{{ editando === null ? 'Agregar medicamento' : 'Editar medicamento' }}</h6>
        <fieldset :disabled="guardando">
          <div class="row g-3">
            <div class="col-sm-6">
              <label for="receta-medicamento" class="form-label">Medicamento *</label>
              <input
                id="receta-medicamento"
                v-model="form.medicamento"
                class="form-control"
                maxlength="150"
                required
              />
            </div>
            <div class="col-sm-6">
              <label for="receta-dosis" class="form-label">Dosis *</label>
              <input
                id="receta-dosis"
                v-model="form.dosis"
                class="form-control"
                maxlength="150"
                required
              />
            </div>
            <div class="col-sm-8">
              <label for="receta-frecuencia" class="form-label">Frecuencia</label>
              <input
                id="receta-frecuencia"
                v-model="form.frecuencia"
                class="form-control"
                maxlength="150"
              />
            </div>
            <div class="col-sm-4">
              <label for="receta-dias" class="form-label">Días</label>
              <input
                id="receta-dias"
                v-model.number="form.dias"
                type="number"
                min="1"
                step="1"
                class="form-control"
              />
            </div>
            <div class="col-12">
              <label for="receta-indicaciones" class="form-label">Indicaciones</label>
              <textarea
                id="receta-indicaciones"
                v-model="form.indicaciones"
                class="form-control"
                rows="3"
              ></textarea>
            </div>
          </div>
          <div class="d-flex gap-2 mt-3">
            <button type="submit" class="btn btn-success">
              {{
                guardando
                  ? 'Guardando…'
                  : editando === null
                    ? 'Agregar medicamento'
                    : 'Guardar medicamento'
              }}
            </button>
            <button
              v-if="editando !== null"
              type="button"
              class="btn btn-outline-secondary"
              @click="restablecer"
            >
              Cancelar edición
            </button>
          </div>
        </fieldset>
      </form>
    </template>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Swal from 'sweetalert2'
import RecetaDetalle from '@/components/RecetaDetalle.vue'
import { useRecetaStore } from '@/stores/recetaStore'
import type { RecetaItem } from '@/interfaces/recetaItemInterface'
const props = defineProps<{ consulta: number }>()
const emit = defineEmits<{ actualizado: [] }>()
const store = useRecetaStore()
const cargando = ref(true)
const guardando = ref(false)
const errorCarga = ref('')
const error = ref('')
const mensaje = ref('')
const editando = ref<number | null>(null)
const vacio = () => ({
  medicamento: '',
  dosis: '',
  frecuencia: '',
  dias: '' as number | '',
  indicaciones: '',
})
const form = ref(vacio())
const items = computed(() => store.recetas.filter((item) => item.consulta === props.consulta))
function restablecer() {
  editando.value = null
  form.value = vacio()
}
async function cargar() {
  cargando.value = true
  errorCarga.value = ''
  try {
    await store.obtenerTodos()
  } catch {
    errorCarga.value = 'No se pudo cargar la receta. Reintentá antes de modificarla.'
  } finally {
    cargando.value = false
  }
}
function editar(item: RecetaItem) {
  editando.value = item.id
  form.value = {
    medicamento: item.medicamento,
    dosis: item.dosis,
    frecuencia: item.frecuencia ?? '',
    dias: item.dias ?? '',
    indicaciones: item.indicaciones ?? '',
  }
  error.value = ''
  mensaje.value = ''
}
function explicarError(e: unknown) {
  const datos = (e as { response?: { data?: Record<string, unknown> } })?.response?.data
  return String(
    datos?.medicamento ||
      datos?.dosis ||
      datos?.frecuencia ||
      datos?.dias ||
      datos?.indicaciones ||
      datos?.consulta ||
      datos?.detail ||
      datos?.non_field_errors ||
      'No se pudo guardar el cambio. Revisá la conexión e intentá nuevamente.',
  )
}
async function guardar() {
  if (guardando.value || cargando.value || errorCarga.value) return
  error.value = ''
  mensaje.value = ''
  const dias = form.value.dias === '' ? null : Number(form.value.dias)
  if (
    !form.value.medicamento.trim() ||
    !form.value.dosis.trim() ||
    (dias !== null && (!Number.isInteger(dias) || dias < 1))
  ) {
    error.value =
      'Completá medicamento y dosis. Los días deben ser un número entero mayor que cero.'
    return
  }
  guardando.value = true
  const datos = {
    ...form.value,
    consulta: props.consulta,
    medicamento: form.value.medicamento.trim(),
    dosis: form.value.dosis.trim(),
    dias,
  }
  try {
    if (editando.value === null) await store.crear(datos)
    else await store.actualizar(editando.value, datos)
    restablecer()
    mensaje.value = 'Medicamento guardado.'
    emit('actualizado')
  } catch (e) {
    error.value = explicarError(e)
  } finally {
    guardando.value = false
  }
}
async function eliminar(item: RecetaItem) {
  if (guardando.value) return
  const resultado = await Swal.fire({
    title: '¿Eliminar medicamento?',
    text: item.medicamento,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Eliminar',
    cancelButtonText: 'Cancelar',
  })
  if (!resultado.isConfirmed || guardando.value) return
  error.value = ''
  mensaje.value = ''
  guardando.value = true
  try {
    await store.eliminar(item.id)
    if (editando.value === item.id) restablecer()
    mensaje.value = 'Medicamento eliminado.'
    emit('actualizado')
  } catch (e) {
    error.value = explicarError(e)
  } finally {
    guardando.value = false
  }
}
onMounted(cargar)
</script>
