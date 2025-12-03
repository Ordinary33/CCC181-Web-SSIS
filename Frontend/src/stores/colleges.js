import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useCollegesStore = defineStore('colleges', {
  state: () => ({
    colleges: [], // Paginated list (Table)
    allColleges: [], // NEW: Full list (Dropdowns)
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
    getAuthHeader() {
      return this.auth.token ? { Authorization: `Bearer ${this.auth.token}` } : {}
    },

    async fetchColleges(params = {}) {
      this.loading = true
      try {
        const config = {
          params: params,
          headers: this.getAuthHeader()
        }
        const res = await axios.get('/api/colleges', config)
        
        this.colleges = res.data.data
        this.pagination = res.data.pagination
      } catch (error) {
        console.error('Fetch colleges error:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchAllColleges() {
      try {
        const params = { page: 1, limit: 1000, sort_by: 'college_name' }
        const config = { params: params, headers: this.getAuthHeader() }
        
        const res = await axios.get('/api/colleges', config)
        this.allColleges = res.data.data
      } catch (error) {
        console.error('Fetch all colleges error:', error)
      }
    },

    async refreshColleges(params = {}) {
      await this.fetchColleges(params)
      await this.fetchAllColleges()
    },

    async createCollege(collegeData) {
      this.loading = true
      try {
        const res = await axios.post('/api/colleges', collegeData, { headers: this.getAuthHeader() })
        return { success: true, message: res.data.message }
      } catch (error) {
        console.error('Create college error:', error)
        throw new Error(error.response?.data?.error || 'Failed to create college')
      } finally {
        this.loading = false
      }
    },

    async updateCollege(collegeCode, updatedData) {
      this.loading = true
      try {
        const res = await axios.put(`/api/colleges/${collegeCode}`, updatedData, { headers: this.getAuthHeader() })
        
        const index = this.colleges.findIndex(c => c.college_code === collegeCode)
        if (index !== -1) this.colleges[index] = res.data.college
        
        return { success: true, message: res.data.message }
      } catch (error) {
        console.error('Update college error:', error)
        throw new Error(error.response?.data?.error || 'Failed to update college')
      } finally {
        this.loading = false
      }
    },

    async deleteCollege(collegeCode) {
      this.loading = true
      try {
        const res = await axios.delete(`/api/colleges/${collegeCode}`, { headers: this.getAuthHeader() })
        
        this.colleges = this.colleges.filter(c => c.college_code !== collegeCode)
        
        return { success: true, message: res.data.message }
      } catch (error) {
        console.error('Delete college error:', error)
        throw new Error(error.response?.data?.error || 'Failed to delete college')
      } finally {
        this.loading = false
      }
    }
  }
})