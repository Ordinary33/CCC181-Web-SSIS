<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useProgramsStore } from '@/stores/programs'
import { useStudentsStore } from '@/stores/students'
import { useModalStore } from '@/stores/modals'
import { useToastStore } from '@/stores/toasts'
import Searchbar from '../components/Searchbar.vue'
import ProgramModal from '../components/Modals/ProgramModal.vue'
import Pagination from '../components/Pagination.vue'

const store = useProgramsStore()
const studentsStore = useStudentsStore()
const modal = useModalStore()
const toastStore = useToastStore()

const query = ref('')
const filterBy = ref('All')
const sortBy = ref('Program Code')
const sortDesc = ref(false)
const page = ref(1)
const perPage = 10

onMounted(() => store.fetchPrograms())

watch([query, filterBy, sortBy, sortDesc], () => {
  page.value = 1
})

const editProgram = (program) => {
  modal.setCurrentProgram(program)
  modal.setEditMode(true)
  modal.open('programForm')
}

const deleteProgram = async (program) => {
  if (!confirm(`Are you sure you want to delete program ${program.program_code}?`)) return
  try {
    await store.deleteProgram(program.program_code)
    toastStore.showToast('Program deleted successfully!', 'success')
    await store.refreshPrograms()
    await studentsStore.refreshStudents()
  } catch (error) {
    console.error('Error deleting program:', error)
    toastStore.showToast(error.message || 'Failed to delete program', 'error')
  }
}

const filteredPrograms = computed(() => {
  let result = store.programs.filter(p => {
    if (!query.value) return true
    const q = query.value.toLowerCase()
    switch (filterBy.value) {
      case 'Program Code': return p.program_code.toLowerCase().includes(q)
      case 'Program Name': return p.program_name.toLowerCase().includes(q)
      case 'College Code': return (p.college_code || '').toLowerCase().includes(q)
      default:
        return (
          p.program_code.toLowerCase().includes(q) ||
          p.program_name.toLowerCase().includes(q) ||
          (p.college_code || '').toLowerCase().includes(q)
        )
    }
  })

  if (sortBy.value && sortBy.value !== 'All') {
    result.sort((a, b) => {
      let aVal = a[sortBy.value.replace(' ', '_').toLowerCase()] || ''
      let bVal = b[sortBy.value.replace(' ', '_').toLowerCase()] || ''
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
  const pages = Math.ceil(filteredPrograms.value.length / perPage)
  return pages > 0 ? pages : 1
})

watch(filteredPrograms, () => {
  if (filteredPrograms.value.length === 0) page.value = 1
  else if (page.value > totalPages.value) page.value = totalPages.value
})

const paginatedPrograms = computed(() => {
  const start = (page.value - 1) * perPage
  return filteredPrograms.value.slice(start, start + perPage)
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
          <th class="text-center">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in paginatedPrograms" :key="p.program_code">
          <td>{{ p.program_code }}</td>
          <td>{{ p.program_name }}</td>
          <td>{{ p.college_code || 'None' }}</td>
          <td class="text-center">
            <div class="flex justify-center gap-2">
              <button class="btn btn-accent btn-sm" @click="editProgram(p)">Edit</button>
              <button class="btn btn-error btn-sm" @click="deleteProgram(p)">Delete</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <Pagination
      :page="page"
      :total-pages="totalPages"
      @update:page="page = $event"
    />
  </div>

  <ProgramModal />
</template>

