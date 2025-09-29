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
    isEditMode.value = editMode
  }

  function setCurrentStudent(student) {
    currentStudent.value = student
  }

  return { activeModal, isEditMode, currentStudent, open, close, setEditMode, setCurrentStudent }
})
