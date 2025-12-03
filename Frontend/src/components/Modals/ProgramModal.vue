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
    // UPDATED: Fetch ALL colleges for the dropdown
    collegesStore.fetchAllColleges()
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
    <div v-if="modal.activeModal === 'programForm'" class="fixed inset-0 bg-black/50 z-[999] flex items-center justify-center">
        <div class="relative bg-white rounded-xl shadow-2xl p-6 md:p-8 w-full max-w-md transition-all duration-300">
            
            <h1 class="text-2xl font-extrabold text-[#0F766E] text-center pb-4 mb-6 border-b border-gray-200">
                {{ modal.isEditMode ? 'Edit Program Details' : 'Add New Program' }}
            </h1>

            <form @submit.prevent="handleSubmit" class="space-y-6">
                
                <div class="form-group">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Program Code:</label>
                    <input type="text" v-model="formData.program_code" @input="formatProgramCode"
                        placeholder="BSCS" maxlength="20"
                        :class="[
                            'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150',
                            errors.program_code ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                        ]"
                    />
                    <span v-if="errors.program_code" class="text-xs text-red-500 mt-1 block">{{ errors.program_code }}</span>
                </div>

                <div class="form-group">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Program Name:</label>
                    <input type="text" v-model="formData.program_name" placeholder="Bachelor of Science in..."
                        :class="[
                            'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150',
                            errors.program_name ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                        ]"
                    />
                    <span v-if="errors.program_name" class="text-xs text-red-500 mt-1 block">{{ errors.program_name }}</span>
                </div>

                <div class="form-group">
                    <label class="block text-sm font-medium text-gray-700 mb-1">College:</label>
                    <select v-model="formData.college_code"
                        :class="[
                            'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150 appearance-none bg-white',
                            errors.college_code ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                        ]"
                    >
                        <option value="">Select a college...</option>
                        <option v-for="c in collegesStore.allColleges" :key="c.college_code" :value="c.college_code">
                            {{ c.college_code }} - {{ c.college_name }}
                        </option>
                    </select>
                    <span v-if="errors.college_code" class="text-xs text-red-500 mt-1 block">{{ errors.college_code }}</span>
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

<style scoped>
</style>