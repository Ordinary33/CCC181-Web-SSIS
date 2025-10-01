<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import axios from 'axios'
import { useModalStore } from '@/stores/modals'
import { useStudentsStore } from '@/stores/students'
import { useProgramsStore } from '@/stores/programs'
import { useCollegesStore } from '@/stores/colleges'

const modal = useModalStore()
const programsStore = useProgramsStore()
const collegesStore = useCollegesStore()
const studentStore = useStudentsStore()
const originalProgram = ref('')

const formData = reactive({
  program_code: '',
  program_name: '',
  college_code: ''
})

watch(() => modal.isEditMode, (isEdit) => {
  if (isEdit && modal.currentProgram) {
    formData.program_code = modal.currentProgram.program_code
    formData.program_name = modal.currentProgram.program_name
    formData.college_code = modal.currentProgram.college_code

    originalProgram.value = modal.currentProgram.program_code
  } else if (!isEdit) {
    resetForm()
    originalProgram.value = ''
  }
})

watch(() => modal.currentProgram, (program) => {
  if (program && modal.isEditMode) {
    formData.program_code = program.program_code
    formData.program_name = program.program_name
    formData.college_code = program.college_code
  }
})

const errors = reactive({
  program_code: '',
  program_name: '',
  college_code: ''
})

onMounted(() => {
  collegesStore.fetchColleges()
})

const validateForm = () => {
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  let isValid = true

  if (!formData.program_code.trim()) {
    errors.program_code = 'Program Code is required'
    isValid = false
  } else {
    const programCodeRegex = /^[A-Za-z]{2,}$/
    if (!programCodeRegex.test(formData.program_code)) {
      errors.program_code = 'Program Code must be in format BS (e.g., BS)'
      isValid = false
    }
  }

  if (!formData.program_name.trim()) {
    errors.program_name = 'Program Name is required'
    isValid = false
  } else {
    const nameRegex = /^[a-zA-Z\s]+$/
    if (!nameRegex.test(formData.program_name)) {
      errors.program_name = 'Program Name can only contain letters and spaces'
      isValid = false
    }
  }
  if (!formData.college_code.trim()) {
    errors.college_code = 'College Code is required'
    isValid = false
  }
  return isValid
}

const formatProgramCode = (event) => {
  let value = event.target.value.toUpperCase()
  value = value.replace(/[^A-Z]/g, '')
  formData.program_code = value
}

const resetForm = () => {
  formData.program_code = ''
  formData.program_name = ''
  formData.college_code = ''
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })
}

const handleSubmit = async (e) => {
  e.preventDefault()
  
  if (validateForm()) {
    try {
      const saveButton = e.target.querySelector('.btn-save')
      const originalText = saveButton.textContent
      saveButton.textContent = 'Saving...'
      saveButton.disabled = true
      
      const programData = {
        program_code: formData.program_code,
        program_name: formData.program_name.trim(),
        college_code: formData.college_code
      }
      
      let response
      
      if (modal.isEditMode) {
        response = await axios.put(`http://127.0.0.1:5000/programs/${originalProgram.value}`, programData)
      } else {
        response = await axios.post('http://127.0.0.1:5000/programs', programData)
      }
      
      if (response.status === 201 || response.status === 200) {
        const wasEditMode = modal.isEditMode
        console.log('Program saved successfully:', response.data)
        
        resetForm()
        modal.close()
        
        await programsStore.refreshPrograms()
        await studentStore.refreshStudents()
        
        const successMessage = wasEditMode ? 'Program updated successfully!' : 'Program added successfully!'
        alert(successMessage)
        
      } else {
        throw new Error('Failed to save program')
      }
      
    } catch (error) {
      console.error('Error saving program:', error)
      
      if (error.response) {
        const status = error.response.status
        const errorData = error.response.data
        
        if (status === 409) {
          alert(`Error: ${errorData.error}`)
        } else if (status === 400) {
          alert(`Error: ${errorData.error}`)
        } else if (status === 500) {
          alert(`Server Error: ${errorData.error || 'Failed to save program'}`)
        } else {
          alert(`Error (${status}): ${errorData.error || errorData.message || 'Unknown error'}`)
        }
      } else if (error.request) {
        alert('Network Error: Unable to connect to server. Please check your connection.')
      } else {
        alert('Error saving program. Please try again.')
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
</script>
<template>
    <div v-if="modal.activeModal === 'programForm'" class="modal-overlay">
      <div class="modal-content">
        <h1 class="modal-title">{{ modal.isEditMode ? 'Edit Program' : 'Add Program' }}</h1>
        <form @submit="handleSubmit">
          <div class="form-group">
            <label>Program Code:</label>
            <input 
              type="text" 
              v-model="formData.program_code"
              @input="formatProgramCode"
              placeholder="BSCS"
              maxlength="20"
              :class="{ 'error': errors.program_code }"
              :style="modal.isEditMode ? 'background-color: #f5f5f5;' : ''"
            />  
            <span v-if="errors.program_code" class="error-message">{{ errors.program_code }}</span>
          </div>
          <div class="form-group">
            <label>Program Name:</label>
            <input 
              type="text" 
              v-model="formData.program_name"
              placeholder="Bachelor of Science"
              :class="{ 'error': errors.program_name }"
            />
            <span v-if="errors.program_name" class="error-message">{{ errors.program_name }}</span>
          </div>
          <div class="form-group">
            <label>College:</label>
            <select 
              v-model="formData.college_code"
              :class="{ 'error': errors.college_code }"
            >
              <option value="">Select a college...</option>
              <option v-for="college in collegesStore.colleges" :key="college.college_code" :value="college.college_code">
                {{ college.college_code }} - {{ college.college_name }}
              </option>
            </select>
            <span v-if="errors.college_code" class="error-message">{{ errors.college_code }}</span>
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

.btn-save:disabled {
  background: #6c757d;
  cursor: not-allowed;
  opacity: 0.6;
}
</style>