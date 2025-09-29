import { defineStore } from 'pinia'
import axios from 'axios'

export const useStudentsStore = defineStore('students', {
  state: () => ({
    students: [],
    loading: false
  }),
  actions: {
    async fetchStudents() {
      if (this.students.length > 0) return
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:5000/students')
        this.students = res.data
      } finally {
        this.loading = false
      }
    },
    async refreshStudents() {
      this.loading = true
      try {
        const res = await axios.get('http://127.0.0.1:5000/students')
        this.students = res.data
      } finally {
        this.loading = false
      }
    },
    async deleteStudent(studentId) {
      this.loading = true
      try {
        const res = await axios.delete(`http://127.0.0.1:5000/students/${studentId}`)

        if (res.status === 200) {
          this.students = this.students.filter(s => s.student_id !== studentId)
          return { success: true, message: res.data.message }
        } else {
          throw new Error('Failed to delete student')
        }
      } catch (error) {
        console.error('Error deleting student:', error)

        if (error.response) {
          const status = error.response.status
          const errorData = error.response.data

          if (status === 404) {
            throw new Error('Student not found')
          } else if (status === 500) {
            throw new Error('Server Error: Failed to delete student')
          } else {
            throw new Error(`Error (${status}): ${errorData.error || errorData.message || 'Unknown error'}`)
          }
        } else if (error.request) {
          throw new Error('Network Error: Unable to connect to server. Please check your connection.')
        } else {
          throw new Error('Error deleting student. Please try again.')
        }
      } finally {
        this.loading = false
      }
    }
  }
})
