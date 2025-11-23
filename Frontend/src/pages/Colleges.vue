<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useProgramsStore } from '@/stores/programs'
import { useCollegesStore } from '@/stores/colleges'
import { useModalStore } from '@/stores/modals'
import { useToastStore } from '@/stores/toasts'
import Searchbar from '../components/Searchbar.vue'
import CollegeModal from '../components/Modals/CollegeModal.vue'
import Pagination from '../components/Pagination.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const store = useCollegesStore()
const programsStore = useProgramsStore()
const modal = useModalStore()
const toastStore = useToastStore()

const showDeleteModal = ref(false)
const itemToDelete = ref(null)
const isDeleting = ref(false)

const promptDelete = (college) => {
  itemToDelete.value = college
  showDeleteModal.value = true
}

const handleConfirmDelete = async () => {
  if (!itemToDelete.value) return
  
  isDeleting.value = true
  try {
    const result = await store.deleteCollege(itemToDelete.value.college_code)
    
    toastStore.showToast(result.message || 'College deleted successfully', 'success')
    
    await store.refreshColleges()
    await programsStore.refreshPrograms()
    
    showDeleteModal.value = false
    itemToDelete.value = null
  } catch (error) {
    console.error('Error deleting college:', error)
    toastStore.showToast(error.message || 'Failed to delete college', 'error')
  } finally {
    isDeleting.value = false
  }
}

const query = ref('')
const filterBy = ref('All')
const sortBy = ref('College Code')
const sortDesc = ref(false)
const page = ref(1)
const perPage = 10

onMounted(() => store.fetchColleges())

watch([query, filterBy, sortBy, sortDesc], () => page.value = 1)

const editCollege = (college) => {
  modal.setCurrentCollege(college)
  modal.setEditMode(true)
  modal.open('collegeForm')
}

const deleteCollege = async (college) => {
  if (!confirm(`Are you sure you want to delete college ${college.college_code}?`)) return
  try {
    const result = await store.deleteCollege(college.college_code)
    toastStore.showToast(result.message, 'success')
    await store.refreshColleges()
    await programsStore.refreshPrograms()
  } catch (error) {
    console.error('Error deleting college:', error)
    toastStore.showToast(error.message || 'Failed to delete college', 'error')
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

const totalPages = computed(() => {
  const pages = Math.ceil(filteredColleges.value.length / perPage)
  return pages > 0 ? pages : 1
})

watch(filteredColleges, () => {
  if (filteredColleges.value.length === 0) page.value = 1
  else if (page.value > totalPages.value) page.value = totalPages.value
})

const paginatedColleges = computed(() => {
  const start = (page.value - 1) * perPage
  return filteredColleges.value.slice(start, start + perPage)
})
</script>

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
              <button class="btn btn-error btn-sm" @click="promptDelete(c)">Delete</button>
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

  <CollegeModal />

  <ConfirmModal 
    :isOpen="showDeleteModal"
    title="Delete College?"
    :message="`Are you sure you want to delete ${itemToDelete?.college_name} (${itemToDelete?.college_code})? This will also delete all associated programs.`"
    :isLoading="isDeleting"
    @close="showDeleteModal = false"
    @confirm="handleConfirmDelete"
  />
</template>


