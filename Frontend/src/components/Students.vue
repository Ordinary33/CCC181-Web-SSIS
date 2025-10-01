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
            <td>{{ s.student_id }}</td>
            <td>{{ s.first_name }}</td>
            <td>{{ s.last_name }}</td>
            <td>{{ s.year_level }}</td>
            <td>{{ s.gender }}</td>
            <td>{{ s.program_code || 'None' }}</td>
            <td><button class="btn btn-accent" @click="editStudent(s)">Edit</button></td>
            <td><button class="btn btn-error" @click="deleteStudent(s)">Delete</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <StudentModal />
  </template>


  <script setup>

  import { useProgramsStore } from '@/stores/programs'
  import { useModalStore } from '@/stores/modals'
  import { ref, computed, onMounted } from 'vue'
  import { useStudentsStore } from '@/stores/students'
  import Searchbar from './Searchbar.vue'
  import StudentModal from './Modals/StudentModal.vue'


  const modal = useModalStore()
  const programsStore = useProgramsStore()
  const store = useStudentsStore()

  onMounted(() => programsStore.fetchPrograms())
  onMounted(() => store.fetchStudents())
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
  
    return result.map(s => ({
    ...s,
    program_code: s.program_code ?? 'None'
    }))
  })


  const editStudent = (student) => {
    modal.setCurrentStudent(student)
    modal.setEditMode(true)
    modal.open('studentForm')
  }

  const deleteStudent = async (student) => {
    if (confirm(`Are you sure you want to delete student ${student.student_id}?`)) {
      try {
        const result = await store.deleteStudent(student.student_id)
        
        if (result.success) {
          alert(result.message)
        }
      } catch (error) {
        console.error('Error deleting student:', error)
        alert(`Error: ${error.message}`)
      }
    }
  }
  
  </script>
  