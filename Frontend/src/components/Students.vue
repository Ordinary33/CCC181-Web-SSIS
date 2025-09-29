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


  onMounted(() => programsStore.fetchPrograms())
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

  const editStudent = (student) => {
    console.log('Edit student clicked:', student)
    // Set the student data first
    modal.setCurrentStudent(student)
    modal.setEditMode(true)
    console.log('Edit mode set to:', modal.isEditMode)
    console.log('Current student set to:', modal.currentStudent)
    // Then open the modal
    modal.open('studentForm')
  }

  const deleteStudent = (student) => {
    if (confirm(`Are you sure you want to delete student ${student.first_name} ${student.last_name}?`)) {
      // TODO: Implement delete functionality
      console.log('Delete student:', student)
    }
  }
  
  </script>
  