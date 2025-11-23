<script setup>
import { ref, computed } from 'vue' 
import { useAuthStore } from '@/stores/auth'
import UserIcon from '@/components/icons/user.svg' 

const auth = useAuthStore()
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const mode = ref('login')
const error = ref(null)

const passwordVisible = ref(false)

const passwordInputType = computed(() => passwordVisible.value ? 'text' : 'password')

const togglePasswordVisibility = () => {
    passwordVisible.value = !passwordVisible.value
}

const submitButtonLabel = computed(() => {
    if (auth.loading) {
        return mode.value === 'login' ? 'Logging in...' : 'Registering...'
    }
    return mode.value === 'login' ? 'Secure Login' : 'Create Account'
})

async function handleSubmit() {
    error.value = null

    if (!username.value || !password.value) {
        error.value = 'Please fill in all required fields.'
        return
    }

    if (mode.value === 'register') {
        if (password.value !== confirmPassword.value) {
            error.value = 'Passwords do not match.'
            return
        }
        if (password.value.length < 6) {
             error.value = 'Password must be at least 6 characters long.'
            return
        }
    }

    try {
        if (mode.value === 'login') {
            await auth.login(username.value, password.value)
        } else {
            await auth.register(username.value, password.value)
        }
    } catch (e) {
        error.value = e.message || `Failed to ${mode.value}`
    }
}
</script>

<template>
  <div class="fixed inset-0 bg-black/70 flex items-center justify-center z-[100]">
    
    <div 
      class="bg-white rounded-xl p-8 max-w-sm w-full md:w-[400px] shadow-2xl transition-all duration-300"
      @keyup.enter="handleSubmit"
    >
      
      <div class="flex flex-col items-center mb-8">
        <div class="text-4xl font-extrabold tracking-tight text-[#0F766E] mb-1">
            Veridia
        </div>
        <h1 class="text-xl font-extrabold text-gray-700">{{ mode === 'login' ? 'Sign In' : 'Register' }}</h1>
        <p class="text-sm text-gray-500 mt-1">Access the Student Information System</p>
      </div>

      <form @submit.prevent="handleSubmit">
        
        <label class="input input-bordered flex items-center gap-3 w-full mb-4 rounded-lg focus-within:border-[#0F766E] focus-within:ring-1 focus-within:ring-[#0F766E]">
          <img :src="UserIcon" alt="User" class="w-4 h-4 opacity-60 text-gray-400" />
          <input 
            v-model="username" 
            type="text" 
            class="grow placeholder-gray-400 text-sm focus:outline-none" 
            placeholder="Username" 
            required
          />
        </label>
        
        <label class="input input-bordered flex items-center gap-3 w-full mb-4 rounded-lg focus-within:border-[#0F766E] focus-within:ring-1 focus-within:ring-[#0F766E]">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 opacity-60 text-gray-400">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          <input 
            v-model="password" 
            :type="passwordInputType"
            class="grow placeholder-gray-400 text-sm focus:outline-none" 
            placeholder="Password" 
            required
          />
          <button type="button" @click.prevent="togglePasswordVisibility" tabindex="-1" class="btn btn-ghost btn-xs btn-circle text-gray-500 hover:text-[#0F766E]">
            <svg v-if="passwordVisible" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                <path d="M9.88 9.88c.8.8 1.48 1.83 1.89 2.89"></path><path d="M12 2C6.5 2 2 12 2 12s3 7 10 7 10-7 10-7c-.24-.6-.57-1.15-1-1.65"></path><path d="M16.48 16.48A5 5 0 0 0 12 10.92"></path><line x1="2" y1="2" x2="22" y2="22"></line>
            </svg>
          </button>
        </label>

        <label 
          v-if="mode === 'register'" 
          class="input input-bordered flex items-center gap-3 w-full mb-6 rounded-lg focus-within:border-[#0F766E] focus-within:ring-1 focus-within:ring-[#0F766E]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 opacity-60 text-gray-400">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          <input
            v-model="confirmPassword"
            :type="passwordInputType"
            class="grow placeholder-gray-400 text-sm focus:outline-none"
            placeholder="Confirm Password"
            required
          />
          <button type="button" @click.prevent="togglePasswordVisibility" tabindex="-1" class="btn btn-ghost btn-xs btn-circle text-gray-500 hover:text-[#0F766E]">
            <svg v-if="passwordVisible" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
                <path d="M9.88 9.88c.8.8 1.48 1.83 1.89 2.89"></path><path d="M12 2C6.5 2 2 12 2 12s3 7 10 7 10-7 10-7c-.24-.6-.57-1.15-1-1.65"></path><path d="M16.48 16.48A5 5 0 0 0 12 10.92"></path><line x1="2" y1="2" x2="22" y2="22"></line>
            </svg>
          </button>
        </label>

        <p v-if="error" class="text-red-600 bg-red-50 border border-red-200 p-3 rounded-lg text-sm text-center mb-4 transition-opacity">
            {{ error }}
        </p>

        <button 
          type="submit"
          :disabled="auth.loading" 
          class="btn w-full mb-4 border-none text-white font-semibold shadow-md transition-all duration-200"
          :class="{'bg-[#0F766E] hover:bg-[#0d6e66]': !auth.loading, 'bg-gray-400 cursor-not-allowed': auth.loading}"
        >
          <span v-if="auth.loading" class="loading loading-spinner loading-sm"></span>
          {{ submitButtonLabel }}
        </button>

      </form>
      
      <p class="text-sm text-center text-gray-500">
        {{ mode === 'login' ? 'No account?' : 'Already have an account?' }}
        <a 
          href="#" 
          @click.prevent="mode = mode === 'login' ? 'register' : 'login'; error = null" 
          class="text-[#0F766E] font-medium hover:underline transition-colors"
        >
          {{ mode === 'login' ? 'Register here.' : 'Login here.' }}
        </a>
      </p>
    </div>
  </div>
</template>