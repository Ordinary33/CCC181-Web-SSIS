<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useProgramsStore } from '@/stores/programs'
import { useStudentsStore } from '@/stores/students'
import { useModalStore } from '@/stores/modals'
import { useToastStore } from '@/stores/toasts'
import Searchbar from '@/components/Searchbar.vue'
import ProgramModal from '../components/Modals/ProgramModal.vue'
import Pagination from '../components/Pagination.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const store = useProgramsStore()
const studentsStore = useStudentsStore()
const modal = useModalStore()
const toastStore = useToastStore()

// --- Modal & Delete Logic ---
const showDeleteModal = ref(false)
const itemToDelete = ref(null)
const isDeleting = ref(false)

const promptDelete = (program) => {
  itemToDelete.value = program
  showDeleteModal.value = true
}

const handleConfirmDelete = async () => {
  if (!itemToDelete.value) return
  
  isDeleting.value = true
  try {
    await store.deleteProgram(itemToDelete.value.program_code)
    toastStore.showToast('Program deleted successfully!', 'success')
    
    await loadData() // Refresh list
    await studentsStore.refreshStudents() // Optional, if students depend on programs
    
    showDeleteModal.value = false
    itemToDelete.value = null
  } catch (error) {
    console.error('Error deleting program:', error)
    toastStore.showToast(error.message || 'Failed to delete program', 'error')
  } finally {
    isDeleting.value = false
  }
}

// --- Server-Side Pagination State ---
const query = ref('')
const filterBy = ref('All')
const sortBy = ref('Program Code')
const sortDesc = ref(false)
const page = ref(1)
const perPage = 10

const fetchParams = computed(() => ({
  page: page.value,
  limit: perPage,
  query: query.value,
  filterBy: filterBy.value,
  sortBy: sortBy.value,
  sortDesc: sortDesc.value
}))

const loadData = async () => {
  await store.fetchPrograms(fetchParams.value)
}

const totalPages = computed(() => store.pagination.total_pages)


watch([query, filterBy, sortBy, sortDesc], () => {
  if (page.value !== 1) {
    page.value = 1
  } else {
    loadData()
  }
})

watch(page, () => {
  loadData()
})

onMounted(() => {
  loadData()
})

const editProgram = (program) => {
  modal.setCurrentProgram(program)
  modal.setEditMode(true)
  modal.open('programForm')
}
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

  <div class="overflow-x-auto rounded-box bg-transparent">
    <div v-if="store.loading" class="flex justify-center items-center h-64">
      <span class="loading loading-spinner loading-lg text-info"></span>
    </div>

    <div class="mt-10 max-w-6xl mx-auto overflow-hidden rounded-xl shadow-md border border-gray-200 bg-white">
      <table class="table w-full">
        
        <thead class="bg-[#F0FDFA] text-gray-700 font-bold uppercase text-xs tracking-wider">
          <tr>
            <th class="py-4 pl-6">Program Code</th>
            <th>Description</th>
            <th>College</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        
        <tbody class="divide-y divide-gray-100">
          <tr v-for="p in store.programs" :key="p.program_code" class="hover:bg-gray-50 transition-colors">
            
            <td class="pl-6 font-mono font-bold text-gray-700">
              {{ p.program_code }}
            </td>
            
            <td class="font-medium text-gray-600 text-sm">
              {{ p.program_name }}
            </td>
            
            <td>
              <span v-if="p.college_code" class="badge badge-accent badge-xs font-semibold text-black text-xs">
                {{ p.college_code }}
              </span>
              <span v-else class="badge badge-accent badge-xs font-semibold text-black text-xs italic">None</span>
            </td>
            
            <td class="text-center">
              <div class="flex justify-center gap-1">
                
                <div class="tooltip" data-tip="Edit">
                  <button class="btn btn-square btn-ghost btn-xs text-accent" @click="editProgram(p)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
                    </svg>
                  </button>
                </div>

                <div class="tooltip" data-tip="Delete">
                  <button class="btn btn-square btn-ghost btn-xs text-error" @click="promptDelete(p)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                  </button>
                </div>

              </div>
            </td>

          </tr>
        </tbody>
      </table>
    </div>

    <Pagination
      :page="page"
      :total-pages="totalPages"
      @update:page="page = $event"
    />
  </div>

  <ProgramModal />

  <ConfirmModal 
    :isOpen="showDeleteModal"
    title="Delete Program?"
    :message="`Are you sure you want to delete ${itemToDelete?.program_name} (${itemToDelete?.program_code})? This cannot be undone.`"
    :isLoading="isDeleting"
    @close="showDeleteModal = false"
    @confirm="handleConfirmDelete"
  />
</template>