<script setup>
import { computed } from 'vue'
import ArrowLeft from '@/components/icons/arrowleft.svg'
import ArrowRight from '@/components/icons/arrowright.svg'
import DoubleArrowLeft from '@/components/icons/doublearrowleft.svg'
import DoubleArrowRight from '@/components/icons/doublearrowright.svg'

const props = defineProps({
  page: { type: Number, required: true },
  totalPages: { type: Number, required: true }
})

const emit = defineEmits(['update:page'])

const pageNumbers = computed(() => {
  const total = props.totalPages
  const current = props.page
  const numbers = []

  let start = Math.max(1, current - 2)
  let end = Math.min(total, current + 2)

  if (current <= 3) end = Math.min(5, total)
  if (current >= total - 2) start = Math.max(total - 4, 1)

  for (let i = start; i <= end; i++) numbers.push(i)
  return numbers
})

const goToPage = (p) => {
  if (p >= 1 && p <= props.totalPages) emit('update:page', p)
}
</script>

<template>
  <div class="flex flex-col items-center gap-3 mt-6">
    <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">
      Page {{ props.page }} of {{ props.totalPages }}
    </span>

    <div class="flex justify-center items-center gap-1 flex-wrap">
      
      <button 
        class="btn btn-sm btn-square border border-[#0F766E] bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E] disabled:bg-gray-100 disabled:border-gray-200 disabled:opacity-50" 
        :disabled="props.page === 1" 
        @click="goToPage(1)"
      >
        <img :src="DoubleArrowLeft" alt="DAL" class="w-4 h-4">
      </button>

      <button 
        class="btn btn-sm btn-square border border-[#0F766E] bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E] disabled:bg-gray-100 disabled:border-gray-200 disabled:opacity-50" 
        :disabled="props.page === 1" 
        @click="goToPage(props.page - 1)"
      >
        <img :src="ArrowLeft" alt="AL" class="w-4 h-4">
      </button>

      <button
        v-for="p in pageNumbers"
        :key="p + '-page'"
        class="btn btn-sm min-w-[32px] shadow-sm transition-all duration-200 border"
        :class="{
          'bg-[#0F766E] text-white border-[#0F766E] hover:bg-[#0d6e66] hover:border-[#0d6e66]': p === props.page, 
          'bg-white text-gray-700 border-gray-300 hover:bg-[#CCFBF1] hover:text-[#0F766E] hover:border-[#0F766E]': p !== props.page
        }"
        @click="goToPage(p)"
      >
        {{ p }}
      </button>

      <button 
        class="btn btn-sm btn-square border border-[#0F766E] bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E] disabled:bg-gray-100 disabled:border-gray-200 disabled:opacity-50" 
        :disabled="props.page === props.totalPages" 
        @click="goToPage(props.page + 1)"
      >
        <img :src="ArrowRight" alt="DAR" class="w-4 h-4">
      </button>

      <button 
        class="btn btn-sm btn-square border border-[#0F766E] bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E] disabled:bg-gray-100 disabled:border-gray-200 disabled:opacity-50" 
        :disabled="props.page === props.totalPages" 
        @click="goToPage(props.totalPages)"
      >
        <img :src="DoubleArrowRight" alt="AR" class="w-4 h-4">
      </button>
      
    </div>
  </div>
</template>
