import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useProgramsStore = defineStore('programs', {
  state: () => ({
    programs: [],
    loading: false
  }),

  getters: {
    auth: () => useAuthStore()
  },

  actions: {
    getAuthHeader() {
      return this.auth.token ? { Authorization: `Bearer ${this.auth.token}` } : {}
    },

    async fetchPrograms() {
      if (this.programs.length > 0) return
      this.loading = true
      try {
        const res = await axios.get('/api/programs/', { headers: this.getAuthHeader() })
        this.programs = res.data
      } catch (error) {
        console.error('Fetch programs error:', error)
      } finally {
        this.loading = false
      }
    },

    async refreshPrograms() {
      this.loading = true
      try {
        const res = await axios.get('/api/programs/', { headers: this.getAuthHeader() })
        this.programs = res.data
      } catch (error) {
        console.error('Refresh programs error:', error)
      } finally {
        this.loading = false
      }
    },

    async createProgram(programData) {
      this.loading = true
      try {
        const res = await axios.post('/api/programs/', programData, { headers: this.getAuthHeader() })
        this.programs.push(res.data.program)
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
