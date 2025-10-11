<script setup>
import { useModalStore } from '@/stores/modals'
import StudentIcon from '@/components/icons/student.svg'
import ProgramIcon from '@/components/icons/program.svg'
import CollegeIcon from '@/components/icons/college.svg'

const modal = useModalStore()

function openStudentModal() {
  console.log('Opening student modal...')
  modal.open('studentForm')
  console.log('Modal opened, activeModal:', modal.activeModal)
}
function openProgramModal() {
  console.log('Opening program modal...')
  modal.open('programForm')
  console.log('Modal opened, activeModal:', modal.activeModal)
}
</script>
<template>
<div class="fab">
  
  <div tabindex="0" role="button" class="btn btn-lg btn-circle btn-success">+</div>
  <div>Add Student <button class="btn btn-lg btn-circle" @click="openStudentModal"><img :src="StudentIcon" alt="Student"></button></div>
  <div>Add Program <button class="btn btn-lg btn-circle" @click="openProgramModal"><img :src="ProgramIcon" alt="Program"></button></div>
  <div>Add College <button class="btn btn-lg btn-circle" @click="modal.open('collegeForm')"><img :src="CollegeIcon" alt="College"></button></div>
</div>
</template>