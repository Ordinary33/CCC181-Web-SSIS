<script setup>
import { watch } from 'vue'
import { ref, computed, onMounted } from 'vue'
import { useStudentsStore } from '@/stores/students'
import { useProgramsStore } from '@/stores/programs'
import { useModalStore } from '@/stores/modals'
import { useToastStore } from '@/stores/toasts'
import Searchbar from './Searchbar.vue'
import StudentModal from './Modals/StudentModal.vue'

const store = useStudentsStore()
const programsStore = useProgramsStore()
const modal = useModalStore()
const toastStore = useToastStore()

const query = ref('')
const filterBy = ref('All')
const sortBy = ref('ID')
const sortDesc = ref(false)
const page = ref(1)
const perPage = 11

watch([query, filterBy, sortBy, sortDesc], () => {
  page.value = 1
})

onMounted(() => {
  programsStore.fetchPrograms()
  store.fetchStudents()
})

const keyMap = {
  ID: 'student_id',
  'First Name': 'first_name',
  'Last Name': 'last_name',
  Year: 'year_level',
  Gender: 'gender',
  Program: 'program_code'
}

const filteredStudents = computed(() => {
  let result = store.students.filter(s => {
    if (!query.value) return true
    const q = query.value.toLowerCase()

    if (filterBy.value === 'Gender')
      return s.gender.toLowerCase() === q

    if (filterBy.value === 'All')
      return Object.values(keyMap).some(k => (s[k] + '').toLowerCase().includes(q))

    return (s[keyMap[filterBy.value]] + '').toLowerCase().includes(q)
  })

  if (sortBy.value) {
    result.sort((a, b) => {
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

const totalPages = computed(() => {
  const pages = Math.ceil(filteredStudents.value.length / perPage)
  return pages > 0 ? pages : 1
})

watch(filteredStudents, () => {
  if (filteredStudents.value.length === 0) {
    page.value = 1
  } else if (page.value > totalPages.value) {
    page.value = totalPages.value
  }
})

const paginatedStudents = computed(() => {
  const start = (page.value - 1) * perPage
  return filteredStudents.value.slice(start, start + perPage)
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
      toastStore.showToast('Student deleted successfully', 'success')
      await store.fetchStudents()
      
    } catch (error) {
      console.error('Error deleting student:', error)
      toastStore.showToast(`Error: ${error.message}`, 'error')
    }
  }
}
</script>

<template>
  <div>
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
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Year</th>
            <th>Gender</th>
            <th>Program</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in paginatedStudents" :key="s.student_id">
            <td>{{ s.student_id }}</td>
            <td>{{ s.first_name }}</td>
            <td>{{ s.last_name }}</td>
            <td>{{ s.year_level }}</td>
            <td>{{ s.gender }}</td>
            <td>{{ s.program_code || 'None' }}</td>
            <td class="text-center">
              <div class="flex justify-center gap-2">
                <button class="btn btn-accent btn-sm" @click="editStudent(s)">Edit</button>
                <button class="btn btn-error btn-sm" @click="deleteStudent(s)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="flex justify-center items-center gap-4 mt-3">
        <button class="btn btn-success" :disabled="page === 1" @click="page--">Prev</button>
        <span>Page {{ page }} of {{ totalPages }}</span>
        <button class="btn btn-success" :disabled="page >= totalPages || filteredStudents.length === 0" @click="page++">Next</button>
      </div>
    </div>

    <StudentModal />
  </div>
</template>