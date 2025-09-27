import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalStore = defineStore('modal', () => {
  const activeModal = ref(null) 

  function open(modalName) {
    activeModal.value = modalName
  }

  function close() {
    activeModal.value = null
  }

  return { activeModal, open, close }
})
