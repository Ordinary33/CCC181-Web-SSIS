import { defineStore } from 'pinia'
import axios from 'axios'

export const useCollegesStore = defineStore('colleges', {
  state: () => ({
    colleges: [],
    loading: false
  }),
  actions: {
    async fetchColleges() {
      if (this.colleges.length > 0) return
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:5000/colleges/')
        this.colleges = res.data
      } finally {
        this.loading = false
      }
    },
    async refreshColleges() {
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:5000/colleges/')
        this.colleges = res.data
      } finally {
        this.loading = false
      }
    },
    async deleteCollege(collegeCode) {
      this.loading = true
      try {
        const res = await axios.delete(`http://127.0.0.1:5000/colleges/${collegeCode}/`)

        if (res.status === 200) {
          this.colleges = this.colleges.filter(c => c.college_code !== collegeCode)
          return { success: true, message: res.data.message }
        } else {
          throw new Error('Failed to delete college')
        }
      } catch (error) {
        console.error('Error deleting college:', error)

        if (error.response) {
          const status = error.response.status
          const errorData = error.response.data

          if (status === 404) {
            throw new Error('College not found')
          } else if (status === 500) {
            throw new Error('Server Error: Failed to delete college')
          } else {
            throw new Error(`Error (${status}): ${errorData.error || errorData.message || 'Unknown error'}`)
          }
        } else if (error.request) {
          throw new Error('Network Error: Unable to connect to server. Please check your connection.')
        } else {  
          throw new Error('Error deleting college. Please try again.')
        }
      } finally {
        this.loading = false
      }
    }
  }
})
