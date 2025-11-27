import { defineStore } from 'pinia'
import axios from 'axios'
import { useToastStore } from '@/stores/toasts'
import router from '@/router'
import { nextTick } from 'vue'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        loading: false
    }),
    getters: {
        isLoggedIn: (state) => !!state.token
    },
    actions: {
        async login(username, password, showToast = true) {
            if (this.loading) return;
            this.loading = true
            const toastStore = useToastStore()
            try {
                const res = await axios.post('/api/auth/login', { username, password })
                
                if (res.status >= 200 && res.status < 300) {
                    this.token = res.data.access_token
                    localStorage.setItem('token', this.token)
                    
                    if (showToast) {
                        toastStore.showToast('Login successful! Welcome back.', 'success')
                    }
                    router.push('/')
                }
                return res
            } catch (e) {
                console.error('Login error:', e.response || e)
                const errorMessage = e.response?.data?.error || 'Login failed. Check credentials.'
                toastStore.showToast(errorMessage, 'error')
                throw new Error(errorMessage)
            } finally {
                this.loading = false
            }
        },
        async register(username, password) {
            if (this.loading) return;

            this.loading = true 
            const toastStore = useToastStore()
            
            try {
                const res = await axios.post('/api/auth/register', { username, password })
                
                if (res.status >= 200 && res.status < 300) {
                    this.loading = false
                    await this.login(username, password, false)
                    toastStore.showToast('Registration successful! You are now logged in.', 'success')
                    return res
                }
                
            } catch (e) {
                console.error('Register error:', e.response || e)
                const errorMessage = e.response?.data?.error || 'Registration failed. Try a different username.'
                toastStore.showToast(errorMessage, 'error')
                throw new Error(errorMessage)
            } finally {
                this.loading = false
            }
            return null
        },

        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            router.push('/login')
        }
    }
})