<script setup>
import { ref } from 'vue' 
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import UserIcon from '@/components/icons/user.svg'
import VeridiaLogo from '@/components/icons/VeridiaLogo.png'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue' 

const authStore = useAuthStore()
const router = useRouter()

const showLogoutModal = ref(false)
const isLoggingOut = ref(false)

const promptLogout = () => {
    const activeElement = document.activeElement
    if (activeElement) {
        activeElement.blur()
    }
    showLogoutModal.value = true
}

const confirmLogout = async () => {
    isLoggingOut.value = true
    try {
        authStore.logout()
        router.push('/login')
    } catch (error) {
        console.error("Logout error:", error)
    } finally {
        isLoggingOut.value = false
        showLogoutModal.value = false 
    }
}
</script>

<template>
  <div class="navbar bg-[#0F766E] text-white shadow-lg z-50 relative">
    
    <div class="navbar-start">
      <div class="dropdown">
        <div tabindex="0" role="button" class="btn btn-ghost lg:hidden text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> 
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /> 
          </svg>
        </div>
        <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow-lg bg-white text-[#0F766E] rounded-box w-52">
          <li><RouterLink to="/students" active-class="bg-[#CCFBF1] font-bold">Students</RouterLink></li>
          <li><RouterLink to="/programs" active-class="bg-[#CCFBF1] font-bold">Programs</RouterLink></li>
          <li><RouterLink to="/colleges" active-class="bg-[#CCFBF1] font-bold">Colleges</RouterLink></li>
        </ul>
      </div>

      <RouterLink to="/" class="btn btn-ghost flex items-center gap-3 px-2 hover:bg-white/10">
        <img :src="VeridiaLogo" alt="Logo" class="w-8 h-8 object-contain brightness-0 invert" />
        
        <div class="flex flex-col items-start leading-tight">
          <span class="text-[10px] font-bold uppercase tracking-widest text-teal-200 opacity-80">
            Veridia
          </span>
          <span class="text-xl font-bold tracking-tight text-white">
            Dashboard
          </span>
        </div>
      </RouterLink>
    </div>

    <div class="navbar-center hidden lg:flex">
      <ul class="menu menu-horizontal px-1 gap-2">
        
        <li>
          <RouterLink 
            to="/students" 
            class="font-pages text-lg px-5 py-2 rounded-lg transition-colors duration-200 hover:bg-white/10" 
            active-class="bg-[#CCFBF1] text-[#0F766E] font-bold shadow-sm"
          >
            Students
          </RouterLink>
        </li>
        <li>
          <RouterLink 
            to="/programs" 
            class="font-pages text-lg px-5 py-2 rounded-lg transition-colors duration-200 hover:bg-white/10" 
            active-class="bg-[#CCFBF1] text-[#0F766E] font-bold shadow-sm"
          >
            Programs
          </RouterLink>
        </li>
        <li>
          <RouterLink 
            to="/colleges" 
            class="font-pages text-lg px-5 py-2 rounded-lg transition-colors duration-200 hover:bg-white/10" 
            active-class="bg-[#CCFBF1] text-[#0F766E] font-bold shadow-sm"
          >
            Colleges
          </RouterLink>
        </li>
      </ul>
    </div>

    <div class="navbar-end">
      <div class="dropdown dropdown-end">
        <label tabindex="0" class="btn btn-ghost btn-circle avatar hover:bg-white/10 transition-colors">
          <div class="w-10 rounded-full bg-[#1D4A47] ring-2 ring-[#CCFBF1] ring-offset-2 ring-offset-[#0F766E] flex items-center justify-center shadow-md">
             <img :src="UserIcon" alt="User" class="w-5 h-5 brightness-0 invert"> 
          </div>
        </label>
        
        <ul tabindex="0" class="menu dropdown-content bg-white text-gray-700 shadow-xl rounded-box w-52 mt-2 p-2 border border-gray-100">
          <li>
            <button @click="promptLogout" class="justify-between hover:bg-red-50 hover:text-red-600">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
    
  </div>
  <ConfirmModal 
    :isOpen="showLogoutModal"
    title="Confirm Logout"
    message="Are you sure you want to log out of Veridia? You will need to log back in to access the dashboard."
    confirm-label="Yes, Logout"
    :isLoading="isLoggingOut"
    @close="showLogoutModal = false"
    @confirm="confirmLogout"
  />
</template>