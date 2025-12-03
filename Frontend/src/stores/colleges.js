import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useCollegesStore = defineStore('colleges', {
  state: () => ({
    colleges: [],
    loading: false,
    pagination: {
      total_records: 0,
      total_pages: 1,
      current_page: 1,
      limit: 10
    }
  }),

  getters: {
    auth: () => useAuthStore()
  },

  actions: {
    async fetchColleges(params = {}) {
      this.loading = true
      try {
        const config = {
          params: params,
          ...this.getAuthConfig()
        }
        
        const res = await axios.get('/api/colleges', config)
        
        this.colleges = res.data.data
        this.pagination = res.data.pagination
      } catch (e) {
        console.error('Fetch colleges error:', e.response || e)
      } finally {
        this.loading = false
      }
    },

    async refreshColleges(params = {}) {
      await this.fetchColleges(params)
    },

    async createCollege(collegeData) {
      this.loading = true
      try {
        const res = await axios.post('/api/colleges', collegeData, this.getAuthConfig())
        return { success: true, message: res.data.message }
      } catch (e) {
        console.error('Create college error:', e.response || e)
        throw new Error(e.response?.data?.error || 'Failed to create college')
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
        
        return { success: true, message: res.data.message }
      } catch (e) {
        console.error('Update college error:', e.response || e)
        throw new Error(e.response?.data?.error || 'Failed to update college')
      } finally {
        this.loading = false
      }
    },

    async deleteCollege(collegeCode) {
      this.loading = true
      try {
        const res = await axios.delete(`/api/colleges/${collegeCode}`, this.getAuthConfig())
        
        this.colleges = this.colleges.filter(c => c.college_code !== collegeCode)
        
        return { success: true, message: res.data.message }
      } catch (e) {
        console.error('Delete college error:', e.response || e)
        throw new Error(e.response?.data?.error || 'Failed to delete college')
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