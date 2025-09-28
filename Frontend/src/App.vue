<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import AddFAB from './components/AddFAB.vue'
import StudentModal from './components/Modals/StudentModal.vue'
import ProgramModal from './components/Modals/ProgramModal.vue'

</script>

<template>
<div class="min-h-screen bg-[#A2D5AB]">
  <header>
    <Navbar />
    <AddFAB />
  </header>
 
  <RouterView />
  
  <StudentModal />
  <ProgramModal />
</div>
</template>

<style scoped>
</style>
