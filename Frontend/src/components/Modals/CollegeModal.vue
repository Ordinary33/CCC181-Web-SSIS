<script setup>
import { ref, reactive, watch, computed } from 'vue'
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
const buttonLabel = computed(() => saving.value ? (modal.isEditMode ? 'Updating...' : 'Saving...') : (modal.isEditMode ? 'Update' : 'Save'))


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
    

    try {
        const collegeData = {
            college_code: formData.college_code,
            college_name: formData.college_name.trim()
        }

        if (modal.isEditMode) {
            await axios.put(`/api/colleges/${originalCollege.value}`, collegeData)
        } else {
            await axios.post('/api/colleges', collegeData)
        }

        const wasEditMode = modal.isEditMode
        resetForm()
        modal.close()
        toastStore.showToast(wasEditMode ? 'College updated successfully!' : 'College added successfully!', 'success')

        await collegesStore.refreshColleges()
        await programStore.refreshPrograms()
    } catch (error) {
        console.error('Error saving college:', error)
        let message = 'Error saving college. Please try again.';
        if (error.response && error.response.data) {
            message = error.response.data.error || error.response.data.message || message
        } else if (error.message) {
             message = error.message
        }
        toastStore.showToast(message, 'error')
    } finally {
        saving.value = false
    }
}
</script>

<template>

    <div v-if="modal.activeModal === 'collegeForm'" class="fixed inset-0 bg-black/50 z-[999] flex items-center justify-center">

        <div class="relative bg-white rounded-xl shadow-2xl p-6 md:p-8 w-full max-w-md transition-all duration-300">
            

            <h1 class="text-2xl font-extrabold text-[#0F766E] text-center pb-4 mb-6 border-b border-gray-200">
                {{ modal.isEditMode ? 'Edit College Details' : 'Add New College' }}
            </h1>

            <form @submit.prevent="handleSubmit" class="space-y-6">
                

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">College Code:</label>
                    <input 
                        type="text" 
                        v-model="formData.college_code"
                        @input="formatCollegeCode"
                        placeholder="CCS"
                        maxlength="20"
                        :class="[
                            'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150',
                            errors.college_code ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]',
                            modal.isEditMode ? 'bg-gray-100 cursor-not-allowed text-gray-500' : 'bg-white'
                        ]"
                        :readonly="modal.isEditMode"
                    />
                    <span v-if="errors.college_code" class="text-xs text-red-500 mt-1 block">{{ errors.college_code }}</span>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">College Name:</label>
                    <input 
                        type="text" 
                        v-model="formData.college_name"
                        placeholder="College of Computer Studies"
                        :class="[
                            'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150',
                            errors.college_name ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                        ]"
                    />
                    <span v-if="errors.college_name" class="text-xs text-red-500 mt-1 block">{{ errors.college_name }}</span>
                </div>

                <div class="flex justify-end gap-3 pt-4">
                    <button type="button" @click="modal.close(); resetForm()" 
                        class="btn bg-gray-500 text-white hover:bg-gray-600 border-none px-6 text-sm shadow-md"
                    >
                        Cancel
                    </button>
                    <button type="submit" 
                        class="btn bg-[#0F766E] text-white hover:bg-[#0d6e66] border-none px-6 text-sm shadow-md" 
                        :disabled="saving"
                    >
                        <span v-if="saving" class="loading loading-spinner loading-sm"></span>
                        {{ buttonLabel }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>