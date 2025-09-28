<script setup>
import { useModalStore } from '@/stores/modals'
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
  <div>Add Student <button class="btn btn-lg btn-circle" @click="openStudentModal">S</button></div>
  <div>Add Program <button class="btn btn-lg btn-circle" @click="openProgramModal">P</button></div>
  <div>Add College <button class="btn btn-lg btn-circle" @click="modal.open('collegeForm')">C</button></div>
</div>
</template>