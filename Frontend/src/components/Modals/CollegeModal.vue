<script setup>
import { ref, reactive, watch } from 'vue'
import { useModalStore } from '@/stores/modals'
import { useCollegesStore } from '@/stores/colleges'
import { useProgramsStore } from '@/stores/programs'
import { useToastStore } from '@/stores/toasts'
import axios from 'axios'

const modal = useModalStore()
const collegesStore = useCollegesStore()
const programStore = useProgramsStore()
const toastStore = useToastStore()

const originalCollege = ref('')

const formData = reactive({
  college_code: '',
  college_name: ''
})

const errors = reactive({
  college_code: '',
  college_name: ''
})

const saving = ref(false)
const buttonLabel = ref('Save')

watch(() => modal.isEditMode, (isEdit) => {
  if (isEdit && modal.currentCollege) {
    formData.college_code = modal.currentCollege.college_code
    formData.college_name = modal.currentCollege.college_name
    originalCollege.value = modal.currentCollege.college_code
  } else {
    resetForm()
    originalCollege.value = ''
  }
})

watch(() => modal.currentCollege, (college) => {
  if (college && modal.isEditMode) {
    formData.college_code = college.college_code
    formData.college_name = college.college_name
  }
})

const validateForm = () => {
  Object.keys(errors).forEach(key => errors[key] = '')
  let isValid = true

  if (!formData.college_code.trim()) {
    errors.college_code = 'College Code is required'
    isValid = false
  } else if (!/^[A-Za-z]{2,}$/.test(formData.college_code)) {
    errors.college_code = 'College Code must be letters only (e.g., CC)'
    isValid = false
  }

  if (!formData.college_name.trim()) {
    errors.college_name = 'College Name is required'
    isValid = false
  } else if (!/^[a-zA-Z\s]+$/.test(formData.college_name)) {
    errors.college_name = 'College Name can only contain letters and spaces'
    isValid = false
  }

  return isValid
}

const formatCollegeCode = (event) => {
  formData.college_code = event.target.value.toUpperCase().replace(/[^A-Z]/g, '')
}

const resetForm = () => {
  Object.keys(formData).forEach(key => formData[key] = '')
  Object.keys(errors).forEach(key => errors[key] = '')
}

const handleSubmit = async () => {
  if (!validateForm()) return
  saving.value = true
  buttonLabel.value = modal.isEditMode ? 'Updating...' : 'Saving...'

  try {
    const collegeData = {
      college_code: formData.college_code,
      college_name: formData.college_name.trim()
    }

    if (modal.isEditMode) {
      await axios.put(`http://127.0.0.1:5000/colleges/${originalCollege.value}`, collegeData)
    } else {
      await axios.post('http://127.0.0.1:5000/colleges', collegeData)
    }

    const wasEditMode = modal.isEditMode
    resetForm()
    modal.close()
    toastStore.showToast(wasEditMode ? 'College updated successfully!' : 'College added successfully!', 'success')

    await collegesStore.refreshColleges()
    await programStore.refreshPrograms()
  } catch (error) {
    console.error('Error saving college:', error)
    if (error.response && error.response.data) {
      toastStore.showToast(error.response.data.error || error.response.data.message || 'Failed to save college', 'error')
    } else if (error.message) {
      toastStore.showToast(error.message, 'error')
    } else {
      toastStore.showToast('Error saving college. Please try again.', 'error')
    }
  } finally {
    saving.value = false
    buttonLabel.value = 'Save'
  }
}
</script>

<template>
  <div v-if="modal.activeModal === 'collegeForm'" class="modal-overlay">
    <div class="modal-content">
      <h1 class="modal-title">{{ modal.isEditMode ? 'Edit College' : 'Add College' }}</h1>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>College Code:</label>
          <input 
            type="text" 
            v-model="formData.college_code"
            @input="formatCollegeCode"
            placeholder="CCS"
            maxlength="20"
            :class="{ 'error': errors.college_code }"
            :style="modal.isEditMode ? 'background-color: #f5f5f5;' : ''"
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
          <button type="submit" class="btn btn-save" :disabled="saving">{{ buttonLabel }}</button>
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
.form-group { margin-bottom: 15px; }
.form-group:last-of-type { margin-bottom: 20px; }
label { display: block; margin-bottom: 5px; font-weight: bold; }
input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
input.error, select.error { border-color: #dc3545; box-shadow:0 0 0 0.2rem rgba(220,53,69,0.25); }
.error-message { color:#dc3545; font-size:12px; margin-top:4px; display:block; }
.button-group { display:flex; gap:10px; justify-content:flex-end; }
.btn { padding:10px 20px; border:none; border-radius:4px; cursor:pointer; }
.btn-cancel { background:#6c757d; color:white; }
.btn-save { background:#28a745; color:white; }
.btn-save:disabled { background:#6c757d; cursor:not-allowed; opacity:0.6; }
</style>
