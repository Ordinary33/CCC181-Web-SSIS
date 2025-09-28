<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useModalStore } from '@/stores/modals'
import { useCollegesStore } from '@/stores/colleges'

const modal = useModalStore()
const collegesStore = useCollegesStore()

const formData = reactive({
  college_code: '',
  college_name: ''
})

const errors = reactive({
  college_code: '',
  college_name: ''
})

const validateForm = () => {
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  let isValid = true

  if (!formData.college_code.trim()) {
    errors.college_code = 'College Code is required'
    isValid = false
  } else {
    const collegeCodeRegex = /^[A-Za-z]{2,}$/
    if (!collegeCodeRegex.test(formData.college_code)) {
      errors.college_code = 'College Code must be in format CC (e.g., CC)'
      isValid = false
    }
  }

  if (!formData.college_name.trim()) {
    errors.college_name = 'College Name is required'
    isValid = false
  } else {
    const nameRegex = /^[a-zA-Z\s]+$/
    if (!nameRegex.test(formData.college_name)) {
      errors.college_name = 'College Name can only contain letters and spaces'
      isValid = false
    }
  }
  return isValid
}

const formatCollegeCode = (event) => {
  let value = event.target.value.toUpperCase()
  value = value.replace(/[^A-Z]/g, '')
  formData.college_code = value
}

const resetForm = () => {
  formData.college_code = ''
  formData.college_name = ''
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
      
      const collegeData = {
        college_code: formData.college_code,
        college_name: formData.college_name.trim()
      }
      
      const response = await axios.post('http://127.0.0.1:5000/colleges', collegeData)
      
      if (response.status === 201) {
        console.log('College saved successfully:', response.data)
        
        resetForm()
        modal.close()
        
        await collegesStore.refreshColleges()
        
        alert('College added successfully!')
        
      } else {
        throw new Error('Failed to save college')
      }
      
    } catch (error) {
      console.error('Error saving college:', error)
      
      if (error.response) {
        const status = error.response.status
        const errorData = error.response.data
        
        if (status === 409) {
          alert(`Error: ${errorData.error}`)
        } else if (status === 400) {
          alert(`Error: ${errorData.error}`)
        } else if (status === 500) {
          alert(`Server Error: ${errorData.error || 'Failed to save college'}`)
        } else {
          alert(`Error (${status}): ${errorData.error || errorData.message || 'Unknown error'}`)
        }
      } else if (error.request) {
        alert('Network Error: Unable to connect to server. Please check your connection.')
      } else {
        alert('Error saving college. Please try again.')
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
  <div v-if="modal.activeModal === 'collegeForm'" class="modal-overlay">
    <div class="modal-content">
      <h1 class="modal-title">Add College</h1>
      <form @submit="handleSubmit">
        <div class="form-group">
          <label>College Code:</label>
          <input 
            type="text" 
            v-model="formData.college_code"
            @input="formatCollegeCode"
            placeholder="CCS"
            maxlength="20"
            :class="{ 'error': errors.college_code }"
          />
          <span v-if="errors.college_code" class="error-message">{{ errors.college_code }}</span>
        </div>
        <div class="form-group">
          <label>College Name:</label>
          <input 
            type="text" 
            v-model="formData.college_name"
            placeholder="College of Computer Studies"
            :class="{ 'error': errors.college_name }"
          />
          <span v-if="errors.college_name" class="error-message">{{ errors.college_name }}</span>
        </div>
        <div class="button-group">
          <button type="button" @click="modal.close(); resetForm()" class="btn btn-cancel">Cancel</button>
          <button type="submit" class="btn btn-save">Save</button>
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
