import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useProgramsStore = defineStore('programs', {
  state: () => ({
    programs: [],
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

    async fetchPrograms(params = {}) {
      this.loading = true
      try {
        const config = { 
          params: params,
          headers: this.getAuthHeader() 
        }
        
        const res = await axios.get('/api/programs/', config)
        
        this.programs = res.data.data
        this.pagination = res.data.pagination
        
      } catch (error) {
        console.error('Fetch programs error:', error)
      } finally {
        this.loading = false
      }
    },

    async refreshPrograms(params = {}) {
      await this.fetchPrograms(params)
    },

    async createProgram(programData) {
      this.loading = true
      try {
        const res = await axios.post('/api/programs/', programData, { headers: this.getAuthHeader() })
        return { success: true, message: res.data.message }
      } catch (error) {
        console.error('Create program error:', error)
        throw new Error(error.response?.data?.error || 'Failed to create program')
      } finally {
        this.loading = false
      }
    },

    async updateProgram(programCode, updatedData) {
      this.loading = true
      try {
        const res = await axios.put(`/api/programs/${programCode}`, updatedData, { headers: this.getAuthHeader() })
        
        const index = this.programs.findIndex(p => p.program_code === programCode)
        if (index !== -1) this.programs[index] = res.data.program
        
        return { success: true, message: res.data.message }
      } catch (error) {
        console.error('Update program error:', error)
        throw new Error(error.response?.data?.error || 'Failed to update program')
      } finally {
        this.loading = false
      }
    },

    async deleteProgram(programCode) {
      this.loading = true
      try {
        const res = await axios.delete(`/api/programs/${programCode}`, { headers: this.getAuthHeader() })
        
        this.programs = this.programs.filter(p => p.program_code !== programCode)
        
        return { success: true, message: res.data.message }
      } catch (error) {
        console.error('Delete program error:', error)
        throw new Error(error.response?.data?.error || 'Failed to delete program')
      } finally {
        this.loading = false
      }
    }
  }
})