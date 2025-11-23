<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import AddFAB from './components/AddFAB.vue'
import ToastContainer from './components/ToastContainer.vue'
import StudentModal from './components/Modals/StudentModal.vue'
import ProgramModal from './components/Modals/ProgramModal.vue'
import CollegeModal from './components/Modals/CollegeModal.vue'
import AuthModal from './components/Modals/AuthModal.vue'
import { useAuthStore } from '@/stores/auth'
import Footer from './components/Footer.vue'
import axios from 'axios'

const auth = useAuthStore()

if (auth.token) {
  axios.get('/api/auth/protected')
    .catch(() => auth.logout())
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-[#F8FAFC] to-[#C4F4E8] relative flex flex-col">
    
    <header>
      <ToastContainer />
      <Navbar />
      <AddFAB v-if="auth.isLoggedIn" />
    </header>

    <main class="flex-grow px-4 pb-8">
      <RouterView v-if="auth.isLoggedIn" />
    </main>

    <StudentModal v-if="auth.isLoggedIn" />
    <ProgramModal v-if="auth.isLoggedIn" />
    <CollegeModal v-if="auth.isLoggedIn" />

    <AuthModal v-if="!auth.isLoggedIn" />

    <Footer />
    
  </div>
</template>

<style scoped>
</style>