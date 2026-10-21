<template>
  <img
    v-if="foto && !falloImagen"
    :src="urlImagen(foto)"
    alt="Tu foto de perfil"
    class="rounded-circle"
    style="width: 32px; height: 32px; object-fit: cover"
    @error="falloImagen = true"
  />
  <span v-else class="badge bg-success">{{ alternativa }}</span>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import perfilClienteService from '@/services/perfilClienteService'
import perfilVeterinarioService from '@/services/perfilVeterinarioService'
import { urlImagen } from '@/utils/imagenes'
defineProps<{ alternativa: string }>()
const emit = defineEmits<{ nombreCargado: [nombre: string] }>()
const auth = useAuthStore()
const foto = ref<string | null>(null)
const falloImagen = ref(false)
watch(
  () => [auth.tokenAcceso, auth.grupo],
  async (_, __, limpiar) => {
    let vigente = true
    limpiar(() => {
      vigente = false
    })
    foto.value = null
    falloImagen.value = false
    emit('nombreCargado', 'Cliente')
    if (!auth.tokenAcceso || (!auth.esCliente && !auth.esVeterinario)) return
    try {
      // El identificador solo elige el avatar; los permisos los controla el backend.
      const contenido = auth.tokenAcceso.split('.')[1]
      if (!contenido) return
      const id = Number(JSON.parse(atob(contenido.replace(/-/g, '+').replace(/_/g, '/'))).user_id)
      if (!Number.isSafeInteger(id) || id <= 0) return
      const perfiles = auth.esCliente
        ? await perfilClienteService.obtenerTodos()
        : await perfilVeterinarioService.obtenerTodos()
      if (vigente) {
        const perfil = perfiles.find((p) => p.usuario.id === id)
        foto.value = perfil?.foto ?? null
        emit('nombreCargado', perfil?.usuario.first_name || perfil?.usuario.username || 'Cliente')
      }
    } catch {
      /* Si no se puede consultar la foto, se conservan las iniciales. */
    }
  },
  { immediate: true },
)
</script>
