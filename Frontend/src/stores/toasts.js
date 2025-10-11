import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])

  function showToast(message, type = 'success', duration = 3000) {
    const id = Date.now() + Math.random()
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      const idx = toasts.value.findIndex(t => t.id === id)
      if (idx !== -1) toasts.value.splice(idx, 1)
    }, duration)
  }

  return { toasts, showToast }
})
