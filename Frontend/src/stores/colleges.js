import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useCollegesStore = defineStore('colleges', {
  state: () => ({
    colleges: [],
    loading: false
  }),

  getters: {
    auth: () => useAuthStore()
  },

  actions: {
    async fetchColleges() {
      if (this.colleges.length > 0) return
      this.loading = true
      try {
        const res = await axios.get('/api/colleges', this.getAuthConfig())
        this.colleges = res.data
      } catch (e) {
        console.error('Fetch colleges error:', e.response || e)
      } finally {
        this.loading = false
      }
    },

    async refreshColleges() {
      this.loading = true
      try {
        const res = await axios.get('/api/colleges', this.getAuthConfig())
        this.colleges = res.data
      } catch (e) {
        console.error('Refresh colleges error:', e.response || e)
      } finally {
        this.loading = false
      }
    },

    async createCollege(collegeData) {
      this.loading = true
      try {
        const res = await axios.post('/api/colleges', collegeData, this.getAuthConfig())
        this.colleges.push(res.data.college)
        return res
      } catch (e) {
        console.error('Create college error:', e.response || e)
        throw e
      } finally {
        this.loading = false
      }
    },

    async updateCollege(originalCode, updatedData) {
      this.loading = true
      try {
        const res = await axios.put(`/api/colleges/${originalCode}`, updatedData, this.getAuthConfig())
        const index = this.colleges.findIndex(c => c.college_code === originalCode)
        if (index !== -1) this.colleges[index] = res.data.college
        return res
      } catch (e) {
        console.error('Update college error:', e.response || e)
        throw e
      } finally {
        this.loading = false
      }
    },

    async deleteCollege(collegeCode) {
      this.loading = true
      try {
        const res = await axios.delete(`/api/colleges/${collegeCode}`, this.getAuthConfig())
        this.colleges = this.colleges.filter(c => c.college_code !== collegeCode)
        return res
      } catch (e) {
        console.error('Delete college error:', e.response || e)
        throw e
      } finally {
        this.loading = false
      }
    },

    getAuthConfig() {
      return this.auth.token
        ? { headers: { Authorization: `Bearer ${this.auth.token}` } }
        : {}
    }
  }
})
