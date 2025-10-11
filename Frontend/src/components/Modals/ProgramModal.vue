<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useModalStore } from '@/stores/modals'
import { useProgramsStore } from '@/stores/programs'
import { useCollegesStore } from '@/stores/colleges'
import { useStudentsStore } from '@/stores/students'
import { useToastStore } from '@/stores/toasts'

const modal = useModalStore()
const programsStore = useProgramsStore()
const collegesStore = useCollegesStore()
const studentsStore = useStudentsStore()
const toastStore = useToastStore()

const formData = reactive({
  program_code: '',
  program_name: '',
  college_code: ''
})

const errors = reactive({
  program_code: '',
  program_name: '',
  college_code: ''
})

const saving = ref(false)
const buttonLabel = computed(() => saving.value ? (modal.isEditMode ? 'Updating...' : 'Saving...') : (modal.isEditMode ? 'Update' : 'Save'))

const originalProgram = ref('')

watch(() => modal.isEditMode, (isEdit) => {
  if (isEdit && modal.currentProgram) {
    Object.assign(formData, modal.currentProgram)
    originalProgram.value = modal.currentProgram.program_code
  } else {
    resetForm()
    originalProgram.value = ''
  }
})

watch(() => modal.currentProgram, (program) => {
  if (program && modal.isEditMode) Object.assign(formData, program)
})

onMounted(() => {
  collegesStore.fetchColleges()
})

const validateForm = () => {
  Object.keys(errors).forEach(key => errors[key] = '')
  let isValid = true

  if (!formData.program_code.trim()) {
    errors.program_code = 'Program Code is required'
    isValid = false
  } else if (!/^[A-Za-z]{2,}$/.test(formData.program_code)) {
    errors.program_code = 'Program Code must be letters only (e.g., BS)'
    isValid = false
  }

  if (!formData.program_name.trim()) {
    errors.program_name = 'Program Name is required'
    isValid = false
  } else if (!/^[a-zA-Z\s]+$/.test(formData.program_name)) {
    errors.program_name = 'Program Name can only contain letters and spaces'
    isValid = false
  }

  if (!formData.college_code.trim()) {
    errors.college_code = 'College Code is required'
    isValid = false
  }

  return isValid
}

const resetForm = () => {
  Object.keys(formData).forEach(key => formData[key] = '')
  Object.keys(errors).forEach(key => errors[key] = '')
}

const formatProgramCode = (e) => {
  formData.program_code = e.target.value.toUpperCase().replace(/[^A-Z]/g, '')
}

const handleSubmit = async () => {
  if (!validateForm()) return

  saving.value = true

  const programData = {
    program_code: formData.program_code,
    program_name: formData.program_name.trim(),
    college_code: formData.college_code
  }

  try {
    if (modal.isEditMode) {
      await programsStore.updateProgram(originalProgram.value, programData)
    } else {
      await programsStore.createProgram(programData)
    }

    const wasEditMode = modal.isEditMode
    resetForm()
    modal.close()

    toastStore.showToast(
      wasEditMode ? 'Program updated successfully!' : 'Program added successfully!',
      'success'
    )

    await programsStore.refreshPrograms()
    await studentsStore.refreshStudents()
  } catch (error) {
    console.error('Error saving program:', error)
    toastStore.showToast(error.message || 'Failed to save program', 'error')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div v-if="modal.activeModal === 'programForm'" class="modal-overlay">
    <div class="modal-content">
      <h1 class="modal-title">{{ modal.isEditMode ? 'Edit Program' : 'Add Program' }}</h1>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Program Code:</label>
          <input type="text" v-model="formData.program_code" @input="formatProgramCode"
                 placeholder="BSCS" maxlength="20"
                 :class="{ 'error': errors.program_code }"
                 :style="modal.isEditMode ? 'background-color: #f5f5f5;' : ''"/>
          <span v-if="errors.program_code" class="error-message">{{ errors.program_code }}</span>
        </div>

        <div class="form-group">
          <label>Program Name:</label>
          <input type="text" v-model="formData.program_name" placeholder="Bachelor of Science"
                 :class="{ 'error': errors.program_name }"/>
          <span v-if="errors.program_name" class="error-message">{{ errors.program_name }}</span>
        </div>

        <div class="form-group">
          <label>College:</label>
          <select v-model="formData.college_code" :class="{ 'error': errors.college_code }">
            <option value="">Select a college...</option>
            <option v-for="c in collegesStore.colleges" :key="c.college_code" :value="c.college_code">
              {{ c.college_code }} - {{ c.college_name }}
            </option>
          </select>
          <span v-if="errors.college_code" class="error-message">{{ errors.college_code }}</span>
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
.modal-overlay { position: fixed; top:0; left:0; width:100vw; height:100vh; background: rgba(0,0,0,0.5); z-index: 999; }
.modal-content { position: fixed; top:50%; left:50%; transform: translate(-50%,-50%); background:white; padding:30px; border-radius:8px; box-shadow:0 4px 20px rgba(0,0,0,0.3); min-width:400px; max-width:500px; }
.modal-title { text-align:center; font-weight:bold; font-size:24px; border-bottom:2px solid #eee; padding-bottom:10px; }
.form-group { margin-bottom:15px; }
label { display:block; margin-bottom:5px; font-weight:bold; }
input, select { width:100%; padding:8px; border:1px solid #ddd; border-radius:4px; }
input.error, select.error { border-color:#dc3545; box-shadow:0 0 0 0.2rem rgba(220,53,69,0.25); }
.error-message { color:#dc3545; font-size:12px; margin-top:4px; display:block; }
.button-group { display:flex; gap:10px; justify-content:flex-end; }
.btn { padding:10px 20px; border:none; border-radius:4px; cursor:pointer; }
.btn-cancel { background:#6c757d; color:white; }
.btn-save { background:#28a745; color:white; }
.btn-save:disabled { background:#6c757d; cursor:not-allowed; opacity:0.6; }
</style>
