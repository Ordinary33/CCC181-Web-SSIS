<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const mode = ref('login')
const error = ref(null)

async function handleSubmit() {
  error.value = null

  if (mode.value === 'register' && password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  try {
    if (mode.value === 'login') {
      await auth.login(username.value, password.value)
    } else {
      await auth.register(username.value, password.value)
    }
  } catch (e) {
    error.value = e.message
  }
}
</script>


<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-[300px] shadow-lg">
      <h2 class="text-lg font-bold mb-4 text-center">
        {{ mode === 'login' ? 'Login' : 'Register' }}
      </h2>

      <input v-model="username" class="input input-bordered w-full mb-2" placeholder="Username" />
      <input v-model="password" type="password" class="input input-bordered w-full mb-2" placeholder="Password" />

      <input
        v-if="mode === 'register'"
        v-model="confirmPassword"
        type="password"
        class="input input-bordered w-full mb-4"
        placeholder="Confirm Password"
      />

      <button @click="handleSubmit" :disabled="auth.loading" class="btn btn-primary w-full mb-2">
        {{ auth.loading ? (mode === 'login' ? 'Logging in...' : 'Registering...') : (mode === 'login' ? 'Login' : 'Register') }}
      </button>

      <p v-if="error" class="text-red-600 text-center mb-2">{{ error }}</p>

      <p class="text-sm text-center">
        <a href="#" @click.prevent="mode = mode === 'login' ? 'register' : 'login'" class="text-blue-600 hover:underline">
          {{ mode === 'login' ? 'No account? Register here.' : 'Already have an account? Login here.' }}
        </a>
      </p>
    </div>
  </div>
</template>

