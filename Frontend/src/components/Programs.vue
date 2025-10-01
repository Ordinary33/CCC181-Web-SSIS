<template>
    <Searchbar
      v-model:query="query"
      v-model:filter="filterBy"
      v-model:sortBy="sortBy"
      v-model:sortDesc="sortDesc"
      :filters="['All','Program Code','Program Name','College Code']"
      :sortOptions="['Program Code','Program Name','College Code']"
    />
  
    <div class="mt-10 overflow-x-auto rounded-box bg-transparent">
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
          <td>{{ p.college_code || 'None'}}</td>
          <td><button class="btn btn-accent" @click="editProgram(p)">Edit</button></td>
          <td><button class="btn btn-error" @click="deleteProgram(p)">Delete</button></td>
        </tr>
      </tbody>
    </table>
    </div>
    <ProgramModal />
  </template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStudentsStore } from '@/stores/students'
import { useProgramsStore } from '@/stores/programs'
import { useModalStore } from '@/stores/modals'
import Searchbar from './Searchbar.vue'
import ProgramModal from './Modals/ProgramModal.vue'


const studentStore = useStudentsStore()
const modal = useModalStore()
const store = useProgramsStore()
const query = ref('')
const filterBy = ref('All')
const sortBy = ref('Program Code')
const sortDesc = ref(false)

onMounted(() => store.fetchPrograms())

const editProgram = (program) => {
  modal.setCurrentProgram(program)
  modal.setEditMode(true)
  modal.open('programForm')
}

const deleteProgram = async (program) => {
  if (confirm(`Are you sure you want to delete program ${program.program_code}?`)) {
    try {
      const result = await store.deleteProgram(program.program_code)
      
      if (result.success) {
        alert(result.message)
        await studentStore.refreshStudents()
      }
    } catch (error) {
      console.error('Error deleting program:', error)
      alert(`Error: ${error.message}`)
    }
  }
}

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


