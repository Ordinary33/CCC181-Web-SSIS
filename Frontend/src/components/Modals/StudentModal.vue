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

        if (wasEditing) {
            await studentsStore.updateStudent(formData.student_id, studentData)
        } else {
            await studentsStore.createStudent(studentData)
        }

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
        <div v-if="modal.activeModal === 'studentForm'" class="fixed inset-0 bg-black/50 z-[999] flex items-center justify-center">
            <div class="relative bg-white rounded-xl shadow-2xl p-6 md:p-8 w-full max-w-lg transition-all duration-300">

                <h1 class="text-2xl font-extrabold text-[#0F766E] text-center pb-4 mb-4 border-b border-gray-200">
                    {{ modal.isEditMode ? 'Edit Student Record' : 'Add New Student' }}
                </h1>

                <form @submit.prevent="handleSubmit" class="space-y-4">

                    <div class="flex flex-col items-center mb-6">
                        <input
                            ref="fileInputRef"
                            type="file"
                            accept="image/*"
                            class="absolute w-0 h-0 opacity-0"
                            @change="handleFileChange"
                        />
                        <div
                            class="relative w-28 h-28 rounded-full border-2 border-dashed border-[#0F766E] flex items-center justify-center cursor-pointer overflow-hidden transition-all duration-200 hover:scale-[1.02] hover:shadow-lg hover:border-solid focus:outline-none focus:ring-4 focus:ring-[#CCFBF1] focus:ring-offset-2"
                            role="button"
                            tabindex="0"
                            @click="triggerFilePicker"
                            @keydown="handleAvatarKeydown"
                        >
                            <img
                                v-if="displayedImage"
                                :src="displayedImage"
                                alt="Student avatar preview"
                                class="w-full h-full object-cover"
                            />
                            <div v-else class="w-full h-full flex flex-col items-center justify-center bg-gray-50 text-gray-500">
                                <span class="text-3xl font-bold">{{ placeholderInitials }}</span>
                                <span class="text-xs mt-1 text-[#0F766E] font-medium">Upload photo</span>
                            </div>
                            <div class="absolute inset-0 bg-black bg-opacity-40 text-white flex items-center justify-center text-sm font-medium opacity-0 transition-opacity duration-200 hover:opacity-100">
                                Change Photo
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-6">

                        <div class="md:col-span-1">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Student ID:</label>
                            <input
                                type="text"
                                v-model="formData.student_id"
                                @input="formatStudentId"
                                placeholder="2024-0001"
                                maxlength="9"
                                :class="[
                                    'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150',
                                    errors.student_id ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]',
                                    modal.isEditMode ? 'bg-gray-100 cursor-not-allowed text-gray-500' : 'bg-white'
                                ]"
                                :readonly="modal.isEditMode"
                            />
                            <span v-if="errors.student_id" class="text-xs text-red-500 mt-1 block">{{ errors.student_id }}</span>
                        </div>

                        <div class="md:col-span-1">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Year Level:</label>
                            <select
                                v-model="formData.year_level"
                                :class="[
                                    'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150 appearance-none bg-white',
                                    errors.year_level ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                                ]"
                            >
                                <option value="">Select year level...</option>
                                <option value="1">1st Year</option>
                                <option value="2">2nd Year</option>
                                <option value="3">3rd Year</option>
                                <option value="4">4th Year</option>
                            </select>
                            <span v-if="errors.year_level" class="text-xs text-red-500 mt-1 block">{{ errors.year_level }}</span>
                        </div>

                        <div class="md:col-span-1">
                            <label class="block text-sm font-medium text-gray-700 mb-1">First Name:</label>
                            <input
                                type="text"
                                v-model="formData.first_name"
                                placeholder="John"
                                :class="[
                                    'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150',
                                    errors.first_name ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                                ]"
                            />
                            <span v-if="errors.first_name" class="text-xs text-red-500 mt-1 block">{{ errors.first_name }}</span>
                        </div>

                        <div class="md:col-span-1">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Last Name:</label>
                            <input
                                type="text"
                                v-model="formData.last_name"
                                placeholder="Doe"
                                :class="[
                                    'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150',
                                    errors.last_name ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                                ]"
                            />
                            <span v-if="errors.last_name" class="text-xs text-red-500 mt-1 block">{{ errors.last_name }}</span>
                        </div>

                        <div class="md:col-span-1">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Gender:</label>
                            <select
                                v-model="formData.gender"
                                :class="[
                                    'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150 appearance-none bg-white',
                                    errors.gender ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                                ]"
                            >
                                <option value="">Select gender...</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                            <span v-if="errors.gender" class="text-xs text-red-500 mt-1 block">{{ errors.gender }}</span>
                        </div>

                        <!-- 6. Program -->
                        <div class="md:col-span-1">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Program:</label>
                            <select
                                v-model="formData.program_code"
                                :class="[
                                    'w-full px-4 py-2 border rounded-lg text-sm transition-all duration-150 appearance-none bg-white',
                                    errors.program_code ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-[#0F766E] focus:ring-1 focus:ring-[#0F766E]'
                                ]"
                            >
                                <option value="">Select a program...</option>
                                <option v-for="program in programsStore.programs" :key="program.program_code" :value="program.program_code">
                                    {{ program.program_code }} - {{ program.program_name }}
                                </option>
                            </select>
                            <span v-if="errors.program_code" class="text-xs text-red-500 mt-1 block">{{ errors.program_code }}</span>
                        </div>

                    </div>
                    <div class="flex justify-end gap-3 pt-6">
                        <button
                            type="button"
                            @click="modal.close(); resetForm()"
                            class="btn bg-gray-500 text-white hover:bg-gray-600 border-none px-6 text-sm shadow-md"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
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
    </div>
</template>