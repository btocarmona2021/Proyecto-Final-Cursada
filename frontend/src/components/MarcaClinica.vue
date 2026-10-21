<template>
  <span class="d-inline-flex align-items-center gap-2" style="max-width: 100%; min-width: 0">
    <img
      v-if="clinica?.logo && !falloImagen"
      :src="urlImagen(clinica.logo)"
      :alt="`Logo de ${nombre}`"
      :style="{ width: `${tamano}px`, height: `${tamano}px`, objectFit: 'contain', flexShrink: 0 }"
      @error="falloImagen = true"
    />
    <span v-else class="badge bg-success" aria-hidden="true">V</span>
    <span v-if="mostrarNombre" class="text-truncate">{{ nombre }}</span>
  </span>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useVeterinariaStore } from '@/stores/veterinariaStore'
import { urlImagen } from '@/utils/imagenes'
withDefaults(defineProps<{ mostrarNombre?: boolean; tamano?: number }>(), {
  mostrarNombre: true,
  tamano: 32,
})
const store = useVeterinariaStore()
const clinica = computed(() => store.veterinarias[0])
const nombre = computed(
  () =>
    clinica.value?.nombre_fantasia?.trim() || clinica.value?.razon_social?.trim() || 'VetSystem',
)
const falloImagen = ref(false)
watch(
  () => clinica.value?.logo,
  () => {
    falloImagen.value = false
  },
)
watch(
  nombre,
  (valor) => {
    document.title = valor
  },
  { immediate: true },
)
onMounted(async () => {
  try {
    await store.obtenerTodos()
  } catch {
    /* El ingreso sigue disponible si falla la información pública. */
  }
})
</script>
