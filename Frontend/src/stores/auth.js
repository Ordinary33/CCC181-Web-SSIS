import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    loading: false
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    async login(username, password) {
      this.loading = true
      try {
        const res = await axios.post('/api/auth/login', { username, password })
        if (res.status >= 200 && res.status < 300) {
          this.token = res.data.access_token
          localStorage.setItem('token', this.token)
        }
        return res
      } catch (e) {
        console.error('Login error:', e.response || e)
        throw new Error(e.response?.data?.error || 'Login failed')
      } finally {
        this.loading = false
      }
    },

    async register(username, password) {
      this.loading = true
      try {
        const res = await axios.post('/api/auth/register', { username, password })
        if (res.status >= 200 && res.status < 300) {
          await this.login(username, password)
        }
        return res
      } catch (e) {
        console.error('Register error:', e.response || e)
        throw new Error(e.response?.data?.error || 'Registration failed')
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
