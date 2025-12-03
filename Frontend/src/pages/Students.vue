<script setup>
import { watch, ref, computed, onMounted } from 'vue'
import { useStudentsStore } from '@/stores/students'
import { useProgramsStore } from '@/stores/programs'
import { useModalStore } from '@/stores/modals'
import { useToastStore } from '@/stores/toasts'
import Searchbar from '@/components/Searchbar.vue'
import StudentModal from '../components/Modals/StudentModal.vue'
import Pagination from '../components/Pagination.vue'
import ConfirmModal from '../components/Modals/ConfirmModal.vue'

const store = useStudentsStore()
const programsStore = useProgramsStore()
const modal = useModalStore()
const toastStore = useToastStore()

const showDeleteModal = ref(false)
const itemToDelete = ref(null)
const isDeleting = ref(false)

const promptDelete = (student) => {
  itemToDelete.value = student
  showDeleteModal.value = true
}

const handleConfirmDelete = async () => {
  if (!itemToDelete.value) return
  
  isDeleting.value = true
  try {
    await store.deleteStudent(itemToDelete.value.student_id)
    await loadData() 
    showDeleteModal.value = false
    itemToDelete.value = null
    toastStore.showToast('Student deleted successfully', 'success') 
  } catch (error) {
    toastStore.showToast(error.message, 'error')
  } finally {
    isDeleting.value = false
  }
}

const query = ref('')
const filterBy = ref('All')
const sortBy = ref('ID')
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
  await store.fetchStudents(fetchParams.value)
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
  programsStore.fetchPrograms()
  loadData()
})

const editStudent = (student) => {
  modal.setCurrentStudent(student)
  modal.setEditMode(true)
  modal.open('studentForm')
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

    <div class="overflow-x-auto rounded-box bg-transparent">
      <div v-if="store.loading" class="flex justify-center items-center h-64">
        <span class="loading loading-spinner loading-lg text-info"></span>
      </div>

      <div v-else class="mt-10 max-w-6xl mx-auto overflow-hidden rounded-xl shadow-md border border-gray-200 bg-white">
        <table class="table w-full">
          <thead class="bg-[#F0FDFA] text-gray-700 font-bold uppercase text-xs tracking-wider">
            <tr>
              <th class="w-16"></th> <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Year</th>
              <th>Gender</th>
              <th>Program</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          
          <tbody class="divide-y divide-gray-100">
            <tr v-for="s in store.students" :key="s.student_id" class="hover:bg-gray-50 transition-colors">
              
              <td>
                <div class="avatar">
                  <div class="w-10 h-10 rounded-full ring ring-[#0D9488] ring-offset-2">
                    <template v-if="s.image_url">
                      <img :src="s.image_url" alt="avatar" />
                    </template>
                    <template v-else>
                      <div class="bg-neutral text-neutral-content w-full h-full flex items-center justify-center">
                        <span class="text-xs font-bold">
                          {{ s.first_name.charAt(0) + s.last_name.charAt(0) }}
                        </span>
                      </div>
                    </template>
                  </div>
                </div>
              </td>

              <td class="font-mono text-xs font-semibold text-gray-500">{{ s.student_id }}</td>
              <td class="font-medium text-gray-700">{{ s.first_name }}</td>
              <td class="font-medium text-gray-700">{{ s.last_name }}</td>
              
              <td>
                <span class="badge badge-ghost badge-sm">{{ s.year_level }}</span>
              </td>
              
              <td class="text-gray-500 text-sm">{{ s.gender }}</td>
              
              <td>
                <span v-if="s.program_code" class="badge badge-accent badge-xs font-semibold text-black text-xs">
                  {{ s.program_code }}
                </span>
                <span v-else class="badge badge-accent badge-xs font-semibold text-black text-xs italic">None</span>
              </td>

              <td class="text-center">
                <div class="flex justify-center gap-1">
                  <div class="tooltip" data-tip="Edit">
                    <button class="btn btn-square btn-ghost btn-xs text-accent" @click="editStudent(s)">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
                      </svg>
                    </button>
                  </div>
                  <div class="tooltip" data-tip="Delete">
                    <button class="btn btn-square btn-ghost btn-xs text-error" @click="promptDelete(s)">
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

    <StudentModal />
    <ConfirmModal 
      :isOpen="showDeleteModal"
      title="Delete Student?"
      :message="`Are you sure you want to delete ${itemToDelete?.first_name} ${itemToDelete?.last_name}? This cannot be undone.`"
      :isLoading="isDeleting"
      @close="showDeleteModal = false"
      @confirm="handleConfirmDelete"
    />
  </div>
</template>