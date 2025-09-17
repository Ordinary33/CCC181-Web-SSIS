<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProgramsStore } from '@/stores/programs'
import Searchbar from './Searchbar.vue'

const store = useProgramsStore()
const query = ref('')
const filterBy = ref('All')
const sortBy = ref('Program Code')
const sortDesc = ref(false)

onMounted(() => store.fetchPrograms())

const filteredPrograms = computed(() => {
  let result = store.programs.filter(p => {
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

  if (sortBy.value && sortBy.value !== 'All') {
    result.sort((a, b) => {
      let aVal = a[sortBy.value.replace(' ', '_').toLowerCase()]
      let bVal = b[sortBy.value.replace(' ', '_').toLowerCase()]
      if (typeof aVal === 'string') aVal = aVal.toLowerCase()
      if (typeof bVal === 'string') bVal = bVal.toLowerCase()
      if (aVal < bVal) return sortDesc.value ? 1 : -1
      if (aVal > bVal) return sortDesc.value ? -1 : 1
      return 0
    })
  }

  return result
})
</script>

<template>
  <Searchbar
    v-model:query="query"
    v-model:filter="filterBy"
    v-model:sortBy="sortBy"
    v-model:sortDesc="sortDesc"
    :filters="['All','Program Code','Program Name','College Code']"
    :sortOptions="['Program Code','Program Name','College Code']"
  />

  <div class="mt-10"></div>

  <table class="table max-w-4xl mx-auto bg-[#E5EFC1]">
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
</template>
