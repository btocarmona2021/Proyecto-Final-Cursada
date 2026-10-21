<template>
  <div class="mb-3">
    <label :for="id" class="form-label fw-semibold">{{ etiqueta }}</label>
    <div v-if="vista" class="mb-2">
      <img
        :src="vista"
        alt="Vista previa de la imagen"
        style="width: 100px; height: 100px; object-fit: contain; border-radius: 12px"
      />
    </div>
    <input
      :id="id"
      ref="entrada"
      type="file"
      class="form-control"
      accept="image/jpeg,image/png,image/webp"
      @change="seleccionar"
    />
    <p class="form-text mb-1">
      JPG, PNG o WebP. Máximo 5 MB. Se guarda al confirmar el formulario.
    </p>
    <button
      v-if="modelValue"
      type="button"
      class="btn btn-sm btn-outline-secondary"
      @click="deshacer"
    >
      Deshacer selección
    </button>
    <p v-if="error" class="text-danger small" role="alert">{{ error }}</p>
  </div>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { urlImagen } from '@/utils/imagenes'
const props = defineProps<{
  modelValue?: File | null
  actual?: string | null
  etiqueta: string
  id: string
}>()
const emit = defineEmits<{ 'update:modelValue': [valor: File | null] }>()
const entrada = ref<HTMLInputElement | null>(null)
const temporal = ref('')
const error = ref('')
const vista = computed(() => temporal.value || urlImagen(props.actual))
watch(
  () => props.modelValue,
  (archivo) => {
    if (temporal.value) URL.revokeObjectURL(temporal.value)
    temporal.value = archivo ? URL.createObjectURL(archivo) : ''
    if (!archivo && entrada.value) entrada.value.value = ''
    error.value = ''
  },
  { immediate: true },
)
function seleccionar(evento: Event) {
  const campo = evento.target as HTMLInputElement
  const archivo = campo.files?.[0]
  if (!archivo) return
  if (
    !['image/jpeg', 'image/png', 'image/webp'].includes(archivo.type) ||
    archivo.size > 5 * 1024 * 1024
  ) {
    error.value = 'Elegí una imagen JPG, PNG o WebP de hasta 5 MB.'
    campo.value = ''
    return
  }
  error.value = ''
  emit('update:modelValue', archivo)
}
function deshacer() {
  emit('update:modelValue', null)
}
onBeforeUnmount(() => {
  if (temporal.value) URL.revokeObjectURL(temporal.value)
})
</script>
