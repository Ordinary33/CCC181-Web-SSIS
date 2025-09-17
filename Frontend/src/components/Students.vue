<template>
    <Searchbar
    v-model:query="query"
    v-model:filter="filterBy"
    v-model:sortBy="sortBy"
    v-model:sortDesc="sortDesc"
    :filters="['All','ID','First Name','Last Name','Year','Gender','Program']"
    :sortOptions="['ID','First Name','Last Name','Year','Gender','Program']"
    />
  
    <div class="mt-10 overflow-x-auto rounded-box bg-transparent">
      <div v-if="store.loading" class="flex justify-center items-center h-64">
        <span class="loading loading-spinner loading-lg text-info"></span>
      </div>
  
      <table v-else class="table max-w-4xl mx-auto bg-[#E5EFC1]">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in filteredData" :key="s.student_id">
            <td v-for="col in columns" :key="col">{{ s[keyMap[col]] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useStudentsStore } from '@/stores/students'
  import Searchbar from './Searchbar.vue'
  
  const store = useStudentsStore()
  const query = ref('')
  const filterBy = ref('All')
  const sortBy = ref('ID')
  const sortDesc = ref(false)
  
  const columns = ['ID','First Name','Last Name','Year','Gender','Program']
  const keyMap = {
    'ID': 'student_id',
    'First Name': 'first_name',
    'Last Name': 'last_name',
    'Year': 'year_level',
    'Gender': 'gender',
    'Program': 'program_code'
  }
  
  onMounted(() => store.fetchStudents())
  
  const filteredData = computed(() => {
    let result = store.students.filter(s => {
      if (!query.value) return true
      const q = query.value.toLowerCase()
      if (filterBy.value === 'Gender') {
        return s[keyMap[filterBy.value]].toLowerCase() === q
        }
      if (filterBy.value === 'All') {
        return Object.entries(keyMap).some(([col, k]) => {
        if (col === 'Gender') return s[k].toLowerCase() === q
        return (s[k]+'').toLowerCase().includes(q)
    })
}
      return (s[keyMap[filterBy.value]]+'').toLowerCase().includes(q)
    })
  
    if (sortBy.value) {
      result.sort((a,b) => {
        let aVal = a[keyMap[sortBy.value]]
        let bVal = b[keyMap[sortBy.value]]
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
  