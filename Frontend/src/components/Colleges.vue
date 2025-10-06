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
          <th v-for="col in columns" :key="col">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="c in filteredData" :key="c.college_code">
          <td>{{ c.college_code }}</td>
          <td>{{ c.college_name }}</td>
          <td><button class="btn btn-accent" @click="editCollege(c)">Edit</button></td>
          <td><button class="btn btn-error" @click="deleteCollege(c)">Delete</button></td>
        </tr>
      </tbody>
    </table>
  </div>

  <CollegeModal />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCollegesStore } from '@/stores/colleges'
import { useProgramsStore } from '@/stores/programs'
import { useModalStore } from '@/stores/modals'
import Searchbar from './Searchbar.vue'
import CollegeModal from './Modals/CollegeModal.vue'

const store = useCollegesStore()
const programStore = useProgramsStore()
const modal = useModalStore()

onMounted(() => store.fetchColleges())
onMounted(() => programStore.fetchPrograms())

const query = ref('')
const filterBy = ref('All')
const sortBy = ref('College Code')
const sortDesc = ref(false)

const columns = ['College Code','College Name']
const keyMap = {
  'College Code': 'college_code',
  'College Name': 'college_name'
}

const filteredData = computed(() => {
  let result = store.colleges.filter(c => {
    if (!query.value) return true
    const q = query.value.toLowerCase()
    if (filterBy.value === 'All') {
      return Object.entries(keyMap).some(([col, k]) =>
        (c[k]+'').toLowerCase().includes(q)
      )
    }
    return (c[keyMap[filterBy.value]]+'').toLowerCase().includes(q)
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
        await programStore.refreshPrograms()
      }
    } catch (error) {
      console.error('Error deleting college:', error)
      alert(`Error: ${error.message}`)
    }
  }
}
</script>
