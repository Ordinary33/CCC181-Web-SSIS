<script setup>
import { ref } from 'vue' // <--- This was missing before!
import { useModalStore } from '@/stores/modals'
import StudentIcon from '@/components/icons/student.svg'
import ProgramIcon from '@/components/icons/program.svg'
import CollegeIcon from '@/components/icons/college.svg'
import AddIcon from '@/components/icons/add.svg'

const modal = useModalStore()
const isOpen = ref(false)

function openStudentModal() {
  console.log('Opening student modal...')
  modal.open('studentForm')
}

function openProgramModal() {
  console.log('Opening program modal...')
  modal.open('programForm')
}

const toggleFab = () => {
  isOpen.value = !isOpen.value
}

const handleAction = (action) => {
  action()
  isOpen.value = false
}
</script>

<template>
  <div class="fixed bottom-8 right-8 z-50 flex flex-col items-end gap-4">

    <TransitionGroup 
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 translate-y-4 scale-75"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-4 scale-75"
    >
      <template v-if="isOpen">
        
        <div key="college" class="flex items-center gap-3 group">
          <span class="bg-gray-800 text-white text-xs py-1.5 px-2.5 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap pointer-events-none">
            Add College
          </span>
          <button 
            class="btn btn-circle shadow-lg border-none bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E]"
            @click="handleAction(() => modal.open('collegeForm'))"
          >
            <img :src="CollegeIcon" alt="College" class="w-6 h-6">
          </button>
        </div>

        <div key="program" class="flex items-center gap-3 group">
          <span class="bg-gray-800 text-white text-xs py-1.5 px-2.5 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap pointer-events-none">
            Add Program
          </span>
          <button 
            class="btn btn-circle shadow-lg border-none bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E]"
            @click="handleAction(() => modal.open('programForm'))"
          >
            <img :src="ProgramIcon" alt="Program" class="w-6 h-6">
          </button>
        </div>

        <div key="student" class="flex items-center gap-3 group">
          <span class="bg-gray-800 text-white text-xs py-1.5 px-2.5 rounded shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap pointer-events-none">
            Add Student
          </span>
          <button 
            class="btn btn-circle shadow-lg border-none bg-[#CCFBF1] hover:bg-[#99F6E4] text-[#0F766E]"
            @click="handleAction(() => modal.open('studentForm'))"
          >
            <img :src="StudentIcon" alt="Student" class="w-6 h-6">
          </button>
        </div>

      </template>
    </TransitionGroup>

    <button 
      class="btn btn-lg btn-circle shadow-xl border-none bg-[#0F766E] hover:bg-[#0d6e66] text-white transition-transform duration-300"
      :class="{ 'rotate-45': isOpen }"
      @click="toggleFab"
    >
      <img :src="AddIcon" alt="Add" class="w-8 h-8 transition-transform duration-300">
    </button>

  </div>
</template>