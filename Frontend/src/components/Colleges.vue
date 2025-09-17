<template>
<Searchbar v-model:query="query" v-model:filter="filterBy" 
                :filters="['All','College Code','College Name']" />
<div class="mt-10"></div>

<div class="overflow-x-auto rounded-box bg-transparent">
  <div v-if="store.loading" class="flex justify-center items-center h-64">
    <span class="loading loading-spinner loading-lg text-info"></span>
  </div>

  <table v-else class="table max-w-4xl mx-auto bg-[#E5EFC1]">
    <thead>
      <tr>
        <th>College Code</th>
        <th>College Name</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="c in filteredColleges" :key="c.college_code">
        <td>{{ c.college_code }}</td>
        <td>{{ c.college_name }}</td>
      </tr>
    </tbody>
  </table>
</div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCollegesStore } from '@/stores/colleges'
import Searchbar from './Searchbar.vue'

const store = useCollegesStore()
const query = ref('')
const filterBy = ref('All')

onMounted(() => {
  store.fetchColleges()
})

const filteredColleges = computed(() => {
  return store.colleges.filter(c => {
    if (!query.value) return true
    const q = query.value.toLowerCase()

    switch (filterBy.value) {
      case 'College Code': return c.college_code.toLowerCase().includes(q)
      case 'College Name': return c.college_name.toLowerCase().includes(q)
      case 'All':
      default:
        return (
            c.college_code.toLowerCase().includes(q) ||
            c.college_name.toLowerCase().includes(q) 
        )
    }
  })
})
</script>
