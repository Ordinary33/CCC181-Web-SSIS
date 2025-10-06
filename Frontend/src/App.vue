<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import AddFAB from './components/AddFAB.vue'
import StudentModal from './components/Modals/StudentModal.vue'
import ProgramModal from './components/Modals/ProgramModal.vue'
import CollegeModal from './components/Modals/CollegeModal.vue'
import AuthModal from './components/Modals/AuthModal.vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const auth = useAuthStore()

if (auth.token) {
  axios.get('/auth/protected')
    .catch(() => auth.logout()) 
}
</script>

<template>
  <div class="min-h-screen bg-[#A2D5AB] relative">
    <header>
      <Navbar />
      <AddFAB v-if="auth.isLoggedIn" />
    </header>

    <RouterView v-if="auth.isLoggedIn" />

    <StudentModal v-if="auth.isLoggedIn" />
    <ProgramModal v-if="auth.isLoggedIn" />
    <CollegeModal v-if="auth.isLoggedIn" />

    <AuthModal v-if="!auth.isLoggedIn" />
  </div>
</template>

<style scoped>
</style>
