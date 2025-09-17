<template>
    <Searchbar v-model:query="query" v-model:filter="filterBy"
               :filters="['All','ID','First Name','Last Name','Year','Gender','Program']" />
  
    <div class="mt-10"></div>
  
    <div class="overflow-x-auto rounded-box bg-transparent">
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in filteredStudents" :key="s.student_id">
            <td>{{ s.student_id }}</td>
            <td>{{ s.first_name }}</td>
            <td>{{ s.last_name }}</td>
            <td>{{ s.year_level }}</td>
            <td>{{ s.gender }}</td>
            <td>{{ s.program_code }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStudentsStore } from '@/stores/students'
import Searchbar from './Searchbar.vue'
  
  const store = useStudentsStore()
  const query = ref('')
  const filterBy = ref('All')
  
  onMounted(() => {
    store.fetchStudents()
  })
  
  const filteredStudents = computed(() => {
    return store.students.filter(s => {
      if (!query.value) return true
      const q = query.value.toLowerCase()
  
      switch (filterBy.value) {
        case 'ID': return s.student_id.includes(q)
        case 'First Name': return s.first_name.toLowerCase().includes(q)
        case 'Last Name': return s.last_name.toLowerCase().includes(q)
        case 'Year': return s.year_level.toString().includes(q)
        case 'Gender': return s.gender.toLowerCase() === q
        case 'Program': return s.program_code.toLowerCase().includes(q)
        case 'All':
        default:
          return (
            s.student_id.includes(q) ||
            s.first_name.toLowerCase().includes(q) ||
            s.last_name.toLowerCase().includes(q) ||
            s.year_level.toString().includes(q) ||
            s.gender.toLowerCase() === q ||
            s.program_code.toLowerCase().includes(q)
          )
      }
    })
  })
  </script>
  