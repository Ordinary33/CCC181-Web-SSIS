import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalStore = defineStore('modal', () => {
  const activeModal = ref(null)
  const isEditMode = ref(false)
  const currentStudent = ref(null)

  function open(modalName) {
    activeModal.value = modalName
  }

  function close() {
    activeModal.value = null
    isEditMode.value = false
    currentStudent.value = null
  }

  function setEditMode(editMode) {
    console.log('Setting edit mode to:', editMode)
    isEditMode.value = editMode
    console.log('Edit mode is now:', isEditMode.value)
  }

  function setCurrentStudent(student) {
    console.log('Setting current student to:', student)
    currentStudent.value = student
    console.log('Current student is now:', currentStudent.value)
  }

  return { activeModal, isEditMode, currentStudent, open, close, setEditMode, setCurrentStudent }
})
