<template>
  <Searchbar
    v-model:query="query"
    v-model:filter="filterBy"
    v-model:sortBy="sortBy"
    v-model:sortDesc="sortDesc"
    :filters="['All','College Code','College Name']"
    :sortOptions="['College Code','College Name']"
  />

  <div class="mt-10 overflow-x-auto rounded-box bg-transparent">
    <div v-if="store.loading" class="flex justify-center items-center h-64">
      <span class="loading loading-spinner loading-lg text-info"></span>
    </div>

    <table v-else class="table max-w-4xl mx-auto bg-[#E5EFC1]">
      <thead>
        <tr>
          <th>College Code</th>
          <th>College Name</th>
          <th class="text-center">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in paginatedColleges" :key="c.college_code">
          <td>{{ c.college_code }}</td>
          <td>{{ c.college_name }}</td>
          <td class="text-center">
            <div class="flex justify-center gap-2">
              <button class="btn btn-accent btn-sm" @click="editCollege(c)">Edit</button>
              <button class="btn btn-error btn-sm" @click="deleteCollege(c)">Delete</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>


    <div class="flex justify-center items-center gap-4 mt-3">
      <button class="btn btn-success" :disabled="page === 1" @click="page--">Prev</button>
      <span>Page {{ page }} of {{ totalPages }}</span>
      <button class="btn btn-success" :disabled="page === totalPages" @click="page++">Next</button>
    </div>
  </div>

  <CollegeModal />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCollegesStore } from '@/stores/colleges'
import { useModalStore } from '@/stores/modals'
import Searchbar from './Searchbar.vue'
import CollegeModal from './Modals/CollegeModal.vue'

const store = useCollegesStore()
const modal = useModalStore()

const query = ref('')
const filterBy = ref('All')
const sortBy = ref('College Code')
const sortDesc = ref(false)
const page = ref(1)
const perPage = 11

onMounted(() => store.fetchColleges())

const editCollege = (college) => {
  modal.setCurrentCollege(college)
  modal.setEditMode(true)
  modal.open('collegeForm')
}

const deleteCollege = async (college) => {
  if (confirm(`Are you sure you want to delete college ${college.college_code}?`)) {
    try {
      const result = await store.deleteCollege(college.college_code)
      if (result.success) {
        alert(result.message)
        await store.refreshColleges()
      }
    } catch (error) {
      console.error('Error deleting college:', error)
      alert(`Error: ${error.message}`)
    }
  }
}

const filteredColleges = computed(() => {
  let result = store.colleges.filter(c => {
    if (!query.value) return true
    const q = query.value.toLowerCase()
    switch (filterBy.value) {
      case 'College Code': return c.college_code.toLowerCase().includes(q)
      case 'College Name': return c.college_name.toLowerCase().includes(q)
      default:
        return (
          c.college_code.toLowerCase().includes(q) ||
          c.college_name.toLowerCase().includes(q)
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

const totalPages = computed(() => Math.ceil(filteredColleges.value.length / perPage))
const paginatedColleges = computed(() => {
  const start = (page.value - 1) * perPage
  return filteredColleges.value.slice(start, start + perPage)
})
</script>
