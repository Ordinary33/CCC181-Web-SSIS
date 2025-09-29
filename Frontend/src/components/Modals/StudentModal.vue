<script setup>
import { onMounted, ref, reactive, watch } from 'vue'
import axios from 'axios'
import { useModalStore } from '@/stores/modals'
import { useProgramsStore } from '@/stores/programs'
import { useStudentsStore } from '@/stores/students'

const modal = useModalStore()
const programsStore = useProgramsStore()
const studentsStore = useStudentsStore()

const formData = reactive({
  student_id: '',
  first_name: '',
  last_name: '',
  year_level: '',
  gender: '',
  program_code: ''
})

watch(() => modal.isEditMode, (isEdit) => {
  if (isEdit && modal.currentStudent) {
    formData.student_id = modal.currentStudent.student_id
    formData.first_name = modal.currentStudent.first_name
    formData.last_name = modal.currentStudent.last_name
    formData.year_level = modal.currentStudent.year_level
    formData.gender = modal.currentStudent.gender
    formData.program_code = modal.currentStudent.program_code
  } else if (!isEdit) {
    resetForm()
  }
})

watch(() => modal.currentStudent, (student) => {
  if (student && modal.isEditMode) {
    formData.student_id = student.student_id
    formData.first_name = student.first_name
    formData.last_name = student.last_name
    formData.year_level = student.year_level
    formData.gender = student.gender
    formData.program_code = student.program_code
  }
})

const errors = reactive({
  student_id: '',
  first_name: '',
  last_name: '',
  year_level: '',
  gender: '',
  program_code: ''
})

onMounted(() => {
  programsStore.fetchPrograms()
})

const validateForm = () => {
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  let isValid = true

  if (!formData.student_id.trim()) {
    errors.student_id = 'Student ID is required'
    isValid = false
  } else {
    const studentIdRegex = /^\d{4}-\d{4}$/
    if (!studentIdRegex.test(formData.student_id)) {
      errors.student_id = 'Student ID must be in format NNNN-YYYY (e.g., 2024-0001)'
      isValid = false
    }
  }

  if (!formData.first_name.trim()) {
    errors.first_name = 'First Name is required'
    isValid = false
  } else {
    const nameRegex = /^[a-zA-Z\s]+$/
    if (!nameRegex.test(formData.first_name)) {
      errors.first_name = 'First Name can only contain letters and spaces'
      isValid = false
    }
  }
  if (!formData.last_name.trim()) {
    errors.last_name = 'Last Name is required'
    isValid = false
  } else {
    const nameRegex = /^[a-zA-Z\s]+$/
    if (!nameRegex.test(formData.last_name)) {
      errors.last_name = 'Last Name can only contain letters and spaces'
      isValid = false
    }
  }

  if (!formData.year_level) {
    errors.year_level = 'Year Level is required'
    isValid = false
  }

  if (!formData.gender) {
    errors.gender = 'Gender is required'
    isValid = false
  }

  if (!formData.program_code) {
    errors.program_code = 'Program is required'
    isValid = false
  }

  return isValid
}

const handleSubmit = async (e) => {
  e.preventDefault()
  
  if (validateForm()) {
    try {
      const saveButton = e.target.querySelector('.btn-save')
      const originalText = saveButton.textContent
      saveButton.textContent = 'Saving...'
      saveButton.disabled = true
      
      const studentData = {
        student_id: formData.student_id,
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        year_level: parseInt(formData.year_level),
        gender: formData.gender,
        program_code: formData.program_code
      }
      
      let response
      
      if (modal.isEditMode) {
        response = await axios.put(`http://127.0.0.1:5000/students/${formData.student_id}`, studentData)
      } else {
        response = await axios.post('http://127.0.0.1:5000/students', studentData)
      }
      
      if (response.status === 200 || response.status === 201) {
        const wasEditMode = modal.isEditMode
        
        resetForm()
        modal.close()
        
        await studentsStore.refreshStudents()
        
        const successMessage = wasEditMode ? 'Student updated successfully!' : 'Student added successfully!'
        alert(successMessage)
        
      } else {
        throw new Error('Failed to save student')
      }
      
    } catch (error) {
      console.error('Error saving student:', error)
      
      if (error.response) {
        const status = error.response.status
        const errorData = error.response.data
        
        if (status === 409) {
          alert(`Error: ${errorData.error}`)
        } else if (status === 400) {
          alert(`Error: ${errorData.error}`)
        } else if (status === 500) {
          alert(`Server Error: ${errorData.error || 'Failed to save student'}`)
        } else {
          alert(`Error (${status}): ${errorData.error || errorData.message || 'Unknown error'}`)
        }
      } else if (error.request) {
        alert('Network Error: Unable to connect to server. Please check your connection.')
      } else {
        alert('Error saving student. Please try again.')
      }
      
    } finally {
      const saveButton = e.target.querySelector('.btn-save')
      saveButton.textContent = 'Save'
      saveButton.disabled = false
    }
  } else {
    console.log('Form has validation errors')
  }
}

const formatStudentId = (event) => {
  let value = event.target.value.replace(/\D/g, '') 
  if (value.length > 4) {
    value = value.substring(0, 4) + '-' + value.substring(4, 8)
  }
  formData.student_id = value
}

const resetForm = () => {
  Object.keys(formData).forEach(key => {
    formData[key] = ''
  })
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })
}
</script>

<template>
  <div v-if="modal.activeModal === 'studentForm'" class="modal-overlay">
    <div class="modal-content">
      <h1 class="modal-title">{{ modal.isEditMode ? 'Edit Student' : 'Add Student' }}</h1>
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
            :readonly="modal.isEditMode"
            :style="modal.isEditMode ? 'background-color: #f5f5f5; cursor: not-allowed;' : ''"
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
          <button type="submit" class="btn btn-save">{{ modal.isEditMode ? 'Update' : 'Save' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  min-width: 400px;
  max-width: 500px;
}

.modal-title {
  margin-top: 0;
  text-align: center;
  font-weight: bold;
  font-size: 24px;
  color: #333;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group:last-of-type {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

input.error, select.error {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

.error-message {
  color: #dc3545;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-save {
  background: #28a745;
  color: white;
}
</style>
