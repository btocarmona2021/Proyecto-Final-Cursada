<template>
  <div>
    <p v-if="!items?.length" class="text-muted small mb-0">Sin medicamentos recetados.</p>
    <ul v-else class="list-unstyled mb-0">
      <li v-for="item in items" :key="item.id" class="border rounded p-3 mb-2">
        <strong>{{ item.medicamento }}</strong>
        <div>Dosis: {{ item.dosis }}</div>
        <div v-if="item.frecuencia">Frecuencia: {{ item.frecuencia }}</div>
        <div v-if="item.dias != null">Duración: {{ item.dias }} día(s)</div>
        <p v-if="item.indicaciones" class="mb-0 mt-1" style="white-space: pre-wrap">
          {{ item.indicaciones }}
        </p>
      </li>
    </ul>
  </div>
</template>
<script setup lang="ts">
import type { RecetaItem } from '@/interfaces/recetaItemInterface'
defineProps<{ items?: RecetaItem[] }>()
</script>
