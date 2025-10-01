import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalStore = defineStore('modal', () => {
  const activeModal = ref(null)
  const isEditMode = ref(false)

  const currentStudent = ref(null)
  const currentProgram = ref(null)
  const currentCollege = ref(null)

  function open(modalName) {
    activeModal.value = modalName
  }

  function close() {
    activeModal.value = null
    isEditMode.value = false
    currentStudent.value = null
    currentProgram.value = null
    currentCollege.value = null
  }

  function setEditMode(editMode) {
    isEditMode.value = editMode
  }

  function setCurrentStudent(student) {
    currentStudent.value = student
  }
  
  function setCurrentProgram(program) {
    currentProgram.value = program
  }

  function setCurrentCollege(college) {
    currentCollege.value = college
  }

  return { activeModal, isEditMode, currentStudent, currentProgram, currentCollege, open, close, setEditMode, setCurrentStudent, setCurrentProgram, setCurrentCollege }
})
