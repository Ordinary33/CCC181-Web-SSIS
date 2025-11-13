<script setup>
import { computed } from 'vue'

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
    <div class="flex flex-col items-center gap-1 mt-3">
        <span class="text-sm font-medium">
            Page {{ props.page }} of {{ props.totalPages }}
        </span>

        <div class="flex justify-center items-center gap-1 flex-wrap mt-1">
            <button class="btn btn-sm btn-success" :disabled="props.page === 1" @click="goToPage(1)"><<</button>
            <button class="btn btn-sm btn-success" :disabled="props.page === 1" @click="goToPage(props.page - 1)"><</button>

            <button
            v-for="p in pageNumbers"
            :key="p + '-page'"
            class="btn btn-sm btn-success text-black border-none font-bold"
            :class="{
                'bg-[#E5EFC1] text-black': p === props.page,
                'bg-success text-white': p !== props.page
            }"
            @click="goToPage(p)"
            >
            {{ p }}
            </button>

            <button class="btn btn-sm btn-success" :disabled="props.page === props.totalPages" @click="goToPage(props.page + 1)">></button>
            <button class="btn btn-sm btn-success" :disabled="props.page === props.totalPages" @click="goToPage(props.totalPages)">>></button>
        </div>
    </div>
</template>
