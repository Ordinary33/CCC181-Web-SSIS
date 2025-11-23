<script setup>
defineProps({
  isOpen: Boolean,
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed?'
  },
  confirmLabel: {
    type: String,
    default: 'Yes, Delete'
  },
  isLoading: Boolean
})

const emit = defineEmits(['close', 'confirm'])
</script>

<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content">
      <h2 class="text-xl font-bold text-red-600 mb-4">{{ title }}</h2>
      
      <p class="text-gray-600 mb-6">{{ message }}</p>
      
      <div class="flex justify-end gap-3">
        <button 
          @click="$emit('close')" 
          class="btn bg-gray-500 text-white hover:bg-gray-600 border-none"
          :disabled="isLoading"
        >
          Cancel
        </button>
        
        <button 
          @click="$emit('confirm')" 
          class="btn bg-red-600 text-white hover:bg-red-700 border-none"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Processing...' : confirmLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
</style>