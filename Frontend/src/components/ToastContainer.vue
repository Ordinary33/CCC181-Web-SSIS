<template>
    <div class="toast toast-top toast-center mt-20 z-[2000]">
      <div
        v-for="t in toastStore.toasts"
        :key="t.id"
        :class="['alert', 'shadow-lg', t.type === 'success' ? 'alert-success' : 'alert-error']"
      >
        <span>{{ t.message }}</span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useToastStore } from '@/stores/toasts'
  
  const toastStore = useToastStore()
  </script>
  