import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

const BASE_URL = 'http://127.0.0.1:5000/students/'

export const useStudentsStore = defineStore('students', {
  state: () => ({
    students: [],
    loading: false
  }),
  getters: {
    auth() {
      return useAuthStore()
    }
  },
  actions: {
    getAuthHeader() {
      return this.auth.token ? { Authorization: `Bearer ${this.auth.token}` } : {}
    },

    async fetchStudents() {
      if (this.students.length > 0) return
      this.loading = true
      try {
        const res = await axios.get(BASE_URL, { headers: this.getAuthHeader() })
        this.students = res.data
      } catch (error) {
        console.error('Fetch students error:', parseError(error))
      } finally {
        this.loading = false
      }
    },

    async refreshStudents() {
      this.loading = true
      try {
        const res = await axios.get(BASE_URL, { headers: this.getAuthHeader() })
        this.students = res.data
      } catch (error) {
        console.error('Refresh students error:', parseError(error))
      } finally {
        this.loading = false
      }
    },

    async createStudent(studentData) {
      this.loading = true
      try {
        const res = await axios.post(BASE_URL, studentData, { headers: this.getAuthHeader() })
        this.students.push(res.data.student)
        return { status: res.status, message: res.data.message }
      } catch (error) {
        console.error('Create student error:', parseError(error))
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateStudent(studentId, updatedData) {
      this.loading = true
      try {
        const res = await axios.put(`${BASE_URL}${studentId}`, updatedData, { headers: this.getAuthHeader() })
        const index = this.students.findIndex(s => s.student_id === studentId)
        if (index !== -1) this.students[index] = res.data.student
        return { status: res.status, message: res.data.message }
      } catch (error) {
        console.error('Update student error:', parseError(error))
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteStudent(studentId) {
      this.loading = true
      try {
        const res = await axios.delete(`${BASE_URL}${studentId}`, { headers: this.getAuthHeader() })
        this.students = this.students.filter(s => s.student_id !== studentId)
        return { status: res.status, message: res.data.message }
      } catch (error) {
        console.error('Delete student error:', parseError(error))
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})

function parseError(error) {
  if (error.response) {
    const data = error.response.data
    if (typeof data === 'object') return data.error || data.message || 'Unknown error'
    return data
  } else if (error.request) {
    return 'Network Error: Unable to connect to server.'
  } else {
    return error.message
  }
}
