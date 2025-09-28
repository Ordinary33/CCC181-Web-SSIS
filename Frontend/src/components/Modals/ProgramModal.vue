<script setup>
import { ref } from 'vue'
import { useModalStore } from '@/stores/modals'
import { useProgramsStore } from '@/stores/programs'
import { useCollegeStore } from '@/stores/college'
const modal = useModalStore()
const programsStore = useProgramsStore()
const collegeStore = useCollegeStore()
</script>
<template>
    <div v-if="modal.activeModal === 'programForm'" class="modal-overlay">
      <div class="modal-content">
        <h1 class="modal-title">Add Program</h1>
        <form @submit="handleSubmit">
          <div class="form-group">
            <label>Student ID:</label>
            <input 
              type="text" 
              v-model="formData.student_id"
              @input="formatStudentId"
              placeholder="2024-0001"
              maxlength="9"
              :class="{ 'error': errors.student_id }"
            />
            <span v-if="errors.student_id" class="error-message">{{ errors.student_id }}</span>
          </div>
          <div class="form-group">
            <label>First Name:</label>
            <input 
              type="text" 
              v-model="formData.first_name"
              :class="{ 'error': errors.first_name }"
            />
            <span v-if="errors.first_name" class="error-message">{{ errors.first_name }}</span>
          </div>
          <div class="form-group">
            <label>Last Name:</label>
            <input 
              type="text" 
              v-model="formData.last_name"
              :class="{ 'error': errors.last_name }"
            />
            <span v-if="errors.last_name" class="error-message">{{ errors.last_name }}</span>
          </div>
          <div class="form-group">
            <label>Year Level:</label>
            <select 
              v-model="formData.year_level"
              :class="{ 'error': errors.year_level }"
            >
              <option value="">Select year level...</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>
            <span v-if="errors.year_level" class="error-message">{{ errors.year_level }}</span>
          </div>
          <div class="form-group">
            <label>Gender:</label>
            <select 
              v-model="formData.gender"
              :class="{ 'error': errors.gender }"
            >
              <option value="">Select gender...</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
            <span v-if="errors.gender" class="error-message">{{ errors.gender }}</span>
          </div>
           <div class="form-group">
             <label>Program:</label>
             <select 
               v-model="formData.program_code"
               :class="{ 'error': errors.program_code }"
             >
               <option value="">Select a program...</option>
               <option v-for="program in programsStore.programs" :key="program.program_code" :value="program.program_code">
                 {{ program.program_code }} - {{ program.program_name }}
               </option>
             </select>
             <span v-if="errors.program_code" class="error-message">{{ errors.program_code }}</span>
           </div>
          <div class="button-group">
            <button type="button" @click="modal.close(); resetForm()" class="btn btn-cancel">Cancel</button>
            <button type="submit" class="btn btn-save">Save</button>
          </div>
        </form>
      </div>
    </div>
  </template>