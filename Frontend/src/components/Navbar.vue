<template>
  <div class="navbar bg-[#39AEA9] text-white shadow-md">
    <div class="navbar-start">
      <div class="dropdown">
        <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> 
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /> 
          </svg>
        </div>
      </div>
      <RouterLink to="/" class="btn btn-ghost text-xl font-ssis" style="font-size: 30px;" >SSIS</RouterLink>
    </div>
    <div class="navbar-center hidden lg:flex">
      <ul class="menu menu-horizontal px-1 space-x-6">
        <li>
          <RouterLink to="/students" class="font-pages" active-class="bg-[#E5EFC1] text-black rounded-lg" style="font-size: 20px;">Students</RouterLink>
        </li>
        <li>
          <RouterLink to="/programs" class="font-pages" active-class="bg-[#E5EFC1] text-black rounded-lg" style="font-size: 20px;">Programs</RouterLink>
        </li>
        <li>
          <RouterLink to="/colleges" class="font-pages" active-class="bg-[#E5EFC1] text-black rounded-lg" style="font-size: 20px;">Colleges</RouterLink>
        </li>
      </ul>
    </div>
    <div class="navbar-end">
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle avatar">
            <div class="w-10 rounded-full bg-white text-[#39AEA9] flex items-center justify-center font-bold"><img :src="UserIcon" alt="User" class="w-6 h-6"></div>
          </label>
          <ul tabindex="0" class="menu dropdown-content bg-white text-black shadow-md rounded-box w-52 mt-2 p-2">
            <li>
              <button @click="logout" class="justify-between">Logout</button>
            </li>
          </ul>
          </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import UserIcon from '@/components/icons/user.svg'

const authStore = useAuthStore()
const router = useRouter()
const dropdownOpen = ref(false)

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const logout = () => {
  if (confirm("Are you sure you want to logout?")) {
    authStore.logout()
    router.push('/login')
    dropdownOpen.value = false
  }
}
</script>
