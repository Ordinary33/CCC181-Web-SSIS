<template>
<Searchbar v-model:query="query" v-model:filter="filterBy" 
                :filters="['All','Program Code','Program Name','College Code']" />

<div class="mt-10"></div>

<div class="overflow-x-auto rounded-box bg-transparent">
  <div v-if="store.loading" class="flex justify-center items-center h-64">
    <span class="loading loading-spinner loading-lg text-info"></span>
  </div>

  <table v-else class="table max-w-4xl mx-auto bg-[#E5EFC1]">
    <thead>
      <tr>
        <th>Program Code</th>
        <th>Program Name</th>
        <th>College Code</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="p in filteredPrograms" :key="p.program_code">
        <td>{{ p.program_code }}</td>
        <td>{{ p.program_name }}</td>
        <td>{{ p.college_code }}</td>
      </tr>
    </tbody>
  </table>
</div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProgramsStore } from '@/stores/programs'
import Searchbar from './Searchbar.vue'

const store = useProgramsStore()
const query = ref('')
const filterBy = ref('All')

onMounted(() => {
  store.fetchPrograms()
})

const filteredPrograms = computed(() => {
  return store.programs.filter(p => {
    if (!query.value) return true
    const q = query.value.toLowerCase()

    switch (filterBy.value) {
      case 'Program Code': return p.program_code.toLowerCase().includes(q)
      case 'Program Name': return p.program_name.toLowerCase().includes(q)
      case 'College Code': return p.college_code.toLowerCase().includes(q)
      case 'All':
      default:
        return (
          p.program_code.toLowerCase().includes(q) ||
          p.program_name.toLowerCase().includes(q) ||
          p.college_code.toLowerCase().includes(q)
        )
    }
  })
})
</script>
