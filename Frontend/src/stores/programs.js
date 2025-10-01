import { defineStore } from 'pinia'
import axios from 'axios'

export const useProgramsStore = defineStore('programs', {
  state: () => ({
    programs: [],
    loading: false
  }),
  actions: {
    async fetchPrograms() {
      if (this.programs.length > 0) return
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:5000/programs')
        this.programs = res.data
      } finally {
        this.loading = false
      } 
    },
    async refreshPrograms() {
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:5000/programs')
        this.programs = res.data
      } finally {
        this.loading = false
      }
    },
    async deleteProgram(programCode) {
      this.loading = true
      try {
        const res = await axios.delete(`http://127.0.0.1:5000/programs/${programCode}`)

        if (res.status === 200) {
          this.programs = this.programs.filter(p => p.program_code !== programCode)
          return { success: true, message: res.data.message }
        } else {
          throw new Error('Failed to delete program')
        }
      } catch (error) {
        console.error('Error deleting program:', error)

        if (error.response) {
          const status = error.response.status
          const errorData = error.response.data

          if (status === 404) {
            throw new Error('Program not found')
          } else if (status === 500) {
            throw new Error('Server Error: Failed to delete program')
          } else {
            throw new Error(`Error (${status}): ${errorData.error || errorData.message || 'Unknown error'}`)
          }
        } else if (error.request) {
          throw new Error('Network Error: Unable to connect to server. Please check your connection.')
        } else {
          throw new Error('Error deleting program. Please try again.')
        }
      } finally {
        this.loading = false
      }
    }
  }
})
