<script setup>
import { onMounted, reactive, watch, ref, computed, onBeforeUnmount } from 'vue'
import { useModalStore } from '@/stores/modals'
import { useProgramsStore } from '@/stores/programs'
import { useStudentsStore } from '@/stores/students'
import { useToastStore } from '@/stores/toasts'

const modal = useModalStore()
const programsStore = useProgramsStore()
const studentsStore = useStudentsStore()
const toastStore = useToastStore()

const selectedFile = ref(null)
const fileInputRef = ref(null)
const previewUrl = ref('')

const formData = reactive({
  student_id: '',
  first_name: '',
  last_name: '',
  year_level: '',
  gender: '',
  program_code: '',
  image_url: ''
})

const errors = reactive({
  student_id: '',
  first_name: '',
  last_name: '',
  year_level: '',
  gender: '',
  program_code: ''
})

const saving = ref(false)
const buttonLabel = computed(() => (saving.value ? (modal.isEditMode ? 'Updating...' : 'Saving...') : (modal.isEditMode ? 'Update' : 'Save')))

watch(
  () => modal.isEditMode,
  (isEdit) => {
    if (isEdit && modal.currentStudent) {
      Object.assign(formData, modal.currentStudent)
      revokePreviewUrl()
      previewUrl.value = modal.currentStudent.image_url || ''
      selectedFile.value = null
    } else if (!isEdit) {
      resetForm()
    }
  }
)

watch(
  () => modal.currentStudent,
  (student) => {
    if (student && modal.isEditMode) {
      Object.assign(formData, student)
      revokePreviewUrl()
      previewUrl.value = student.image_url || ''
      selectedFile.value = null
    }
  }
)

onMounted(() => {
  programsStore.fetchPrograms()
})

const revokePreviewUrl = () => {
  if (previewUrl.value && previewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(previewUrl.value)
  }
}

onBeforeUnmount(() => {
  revokePreviewUrl()
})

const handleFileChange = (event) => {
  const file = event.target.files[0] || null
  selectedFile.value = file

  revokePreviewUrl()
  previewUrl.value = file ? URL.createObjectURL(file) : (formData.image_url || '')
  if (fileInputRef.value) fileInputRef.value.value = ''
  if (event?.target) event.target.value = ''
}

const triggerFilePicker = () => {
  fileInputRef.value?.click()
}

const displayedImage = computed(() => previewUrl.value || formData.image_url || '')

const placeholderInitials = computed(() => {
  const first = (formData.first_name || '').trim().charAt(0)
  const last = (formData.last_name || '').trim().charAt(0)
  const initials = `${first}${last}`.toUpperCase()
  return initials || '+'
})

const handleAvatarKeydown = (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault()
    triggerFilePicker()
  }
}

const validateForm = () => {
  Object.keys(errors).forEach(key => (errors[key] = ''))
  let isValid = true

  if (!formData.student_id || !formData.student_id.toString().trim()) {
    errors.student_id = 'Student ID is required'
    isValid = false
  } else if (!/^\d{4}-\d{4}$/.test(formData.student_id)) {
    errors.student_id = 'Student ID must be in format NNNN-YYYY'
    isValid = false
  }

  if (!formData.first_name || !formData.first_name.toString().trim()) {
    errors.first_name = 'First Name is required'
    isValid = false
  } else if (!/^[a-zA-Z\s]+$/.test(formData.first_name)) {
    errors.first_name = 'First Name can only contain letters and spaces'
    isValid = false
  }

  if (!formData.last_name || !formData.last_name.toString().trim()) {
    errors.last_name = 'Last Name is required'
    isValid = false
  } else if (!/^[a-zA-Z\s]+$/.test(formData.last_name)) {
    errors.last_name = 'Last Name can only contain letters and spaces'
    isValid = false
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

const handleSubmit = async () => {
  if (!validateForm()) return
  saving.value = true

  try {
    const studentData = {
      student_id: formData.student_id,
      first_name: formData.first_name.trim(),
      last_name: formData.last_name.trim(),
      year_level: parseInt(formData.year_level),
      gender: formData.gender,
      program_code: formData.program_code
    }

    const wasEditing = modal.isEditMode

    let res
    if (wasEditing) {
      res = await studentsStore.updateStudent(formData.student_id, studentData)
      if (selectedFile.value) {
        const imageUrl = await studentsStore.updateStudentImage(formData.student_id, selectedFile.value)
        if (imageUrl) {
          revokePreviewUrl()
          formData.image_url = imageUrl
          previewUrl.value = imageUrl
          selectedFile.value = null
          if (fileInputRef.value) fileInputRef.value.value = ''
        }
      }
    } else {
      res = await studentsStore.createStudent(studentData)
      if (selectedFile.value) {
        const imageUrl = await studentsStore.updateStudentImage(formData.student_id, selectedFile.value)
        if (imageUrl) {
          revokePreviewUrl()
          formData.image_url = imageUrl
          previewUrl.value = imageUrl
          selectedFile.value = null
          if (fileInputRef.value) fileInputRef.value.value = ''
        }
      }
    }

    await studentsStore.refreshStudents()
    resetForm()
    modal.close()
    toastStore.showToast(wasEditing ? 'Student updated successfully!' : 'Student added successfully!', 'success')
    selectedFile.value = null

  } catch (error) {
    console.error('Error saving student:', error)
    toastStore.showToast(error.message || 'Error saving student', 'error')
  } finally {
    saving.value = false
  }
}

const formatStudentId = (event) => {
  let value = (event.target.value || '').toString().replace(/\D/g, '')
  if (value.length > 4) value = value.substring(0, 4) + '-' + value.substring(4, 8)
  formData.student_id = value
}

const resetForm = () => {
  Object.keys(formData).forEach(key => (formData[key] = ''))
  Object.keys(errors).forEach(key => (errors[key] = ''))
  selectedFile.value = null
  revokePreviewUrl()
  previewUrl.value = ''
  if (fileInputRef.value) fileInputRef.value.value = ''
}
</script>

<template>
  <div>
    <div v-if="modal.activeModal === 'studentForm'" class="modal-overlay">
      <div class="modal-content">
        <h1 class="modal-title">{{ modal.isEditMode ? 'Edit Student' : 'Add Student' }}</h1>
        <form @submit.prevent="handleSubmit">

          <div class="form-group avatar-group">
            <input
              ref="fileInputRef"
              type="file"
              accept="image/*"
              class="file-input-hidden"
              @change="handleFileChange"
            />
            <div
              class="avatar-wrapper"
              role="button"
              tabindex="0"
              @click="triggerFilePicker"
              @keydown="handleAvatarKeydown"
            >
              <img
                v-if="displayedImage"
                :src="displayedImage"
                alt="Student avatar preview"
              />
              <div v-else class="avatar-placeholder">
                <span class="avatar-initials">{{ placeholderInitials }}</span>
                <span class="avatar-hint">Upload photo</span>
              </div>
              <div class="avatar-overlay">Change photo</div>
            </div>
          </div>

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
            <input type="text" v-model="formData.first_name" :class="{ 'error': errors.first_name }" />
            <span v-if="errors.first_name" class="error-message">{{ errors.first_name }}</span>
          </div>

          <div class="form-group">
            <label>Last Name:</label>
            <input type="text" v-model="formData.last_name" :class="{ 'error': errors.last_name }" />
            <span v-if="errors.last_name" class="error-message">{{ errors.last_name }}</span>
          </div>

          <div class="form-group">
            <label>Year Level:</label>
            <select v-model="formData.year_level" :class="{ 'error': errors.year_level }">
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
            <select v-model="formData.gender" :class="{ 'error': errors.gender }">
              <option value="">Select gender...</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
            <span v-if="errors.gender" class="error-message">{{ errors.gender }}</span>
          </div>

          <div class="form-group">
            <label>Program:</label>
            <select v-model="formData.program_code" :class="{ 'error': errors.program_code }">
              <option value="">Select a program...</option>
              <option v-for="program in programsStore.programs" :key="program.program_code" :value="program.program_code">
                {{ program.program_code }} - {{ program.program_name }}
              </option>
            </select>
            <span v-if="errors.program_code" class="error-message">{{ errors.program_code }}</span>
          </div>

          <div class="button-group">
            <button type="button" @click="modal.close(); resetForm()" class="btn btn-cancel">Cancel</button>
            <button type="submit" class="btn btn-save" :disabled="saving">{{ buttonLabel }}</button>
          </div>
        </form>
      </div>
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
  background: rgba(0,0,0,0.5);
  z-index: 999;
}
.modal-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  z-index: 1000;
  min-width: 400px;
  max-width: 500px;
}
.modal-title { margin-top:0; text-align:center; font-weight:bold; font-size:24px; color:#333; border-bottom:2px solid #eee; padding-bottom:10px;}
.form-group { margin-bottom:15px;}
.form-group:last-of-type { margin-bottom:20px;}
label { display:block; margin-bottom:5px; font-weight:bold;}
input, select { width:100%; padding:8px; border:1px solid #ddd; border-radius:4px;}
input.error, select.error { border-color:#dc3545; box-shadow:0 0 0 0.2rem rgba(220,53,69,0.25);}
.error-message { color:#dc3545; font-size:12px; margin-top:4px; display:block;}
.button-group { display:flex; gap:10px; justify-content:flex-end;}
.btn { padding:10px 20px; border:none; border-radius:4px; cursor:pointer;}
.btn-cancel { background:#6c757d; color:white;}
.btn-save { background:#28a745; color:white;}
.avatar-group { display:flex; margin-top:20px; justify-content:center; margin-bottom:20px; }
.file-input-hidden { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); border:0;}
.avatar-wrapper { position:relative; width:120px; height:120px; border-radius:50%; background:#f2f2f2; border:2px dashed #ccc; display:flex; align-items:center; justify-content:center; cursor:pointer; transition:transform 0.2s ease, border-color 0.2s ease;}
.avatar-wrapper:hover, .avatar-wrapper:focus { border-color:#28a745; transform:scale(1.02); outline:none; box-shadow:0 0 0 3px rgba(40,167,69,0.35);}
.avatar-wrapper img { width:100%; height:100%; object-fit:cover; border-radius:50%;}
.avatar-placeholder { width:100%; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; color:#495057; background:#f8f9fa; border-radius:50%; border:1px solid rgba(0,0,0,0.08);}
.avatar-initials { font-size:28px; font-weight:700; letter-spacing:0.05em;}
.avatar-hint { font-size:11px; font-weight:500; text-transform:uppercase; letter-spacing:0.08em; color:#868e96;}
.avatar-overlay { position:absolute; inset:0; background:rgba(0,0,0,0.45); color:#fff; display:flex; align-items:center; justify-content:center; font-size:13px; text-transform:uppercase; letter-spacing:0.05em; opacity:0; transition:opacity 0.2s ease; border-radius:50%;}
.avatar-wrapper:hover .avatar-overlay, .avatar-wrapper:focus .avatar-overlay { opacity:1;}
</style>
