<template>
  <div class="toast toast-top toast-center mt-20 z-[2000]">
    <TransitionGroup 
        name="toast" 
        tag="div" 
        class="flex flex-col gap-2 items-center"
    >
      <div
        v-for="t in toastStore.toasts"
        :key="t.id"
        class="alert shadow-xl rounded-lg border-l-4 w-80 min-h-12 transition-all duration-300 ease-in-out"
        :class="t.type === 'success' ? 'toast-success' : 'toast-error'"
      >
        <svg v-if="t.type === 'success'" xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>

        <span>{{ t.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToastStore } from '@/stores/toasts'
 
const toastStore = useToastStore()
</script>

<style scoped>
.toast-success {
    /* Background: Lightest shade of your teal theme */
    background-color: #F0FDFA; /* Teal-50 */
    /* Border and Text: Primary Deep Teal color */
    border-color: #14B8A6; /* Teal-500 for border */
    color: #0F766E; /* Deep Teal for text */
}
.toast-error {
    /* Background: Soft Red */
    background-color: #FEF2F2; /* Red-50 */
    /* Border and Text: Standard Error Red */
    border-color: #F87171; /* Red-400 */
    color: #B91C1C; /* Dark Red for text */
}
/* Optional: Animation for toasts entering/leaving */
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
    opacity: 0;
    transform: translateY(-20px);
}
</style>