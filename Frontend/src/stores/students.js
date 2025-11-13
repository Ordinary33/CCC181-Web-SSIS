import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { supabase } from '@/plugins/supabase.js'

import axios from 'axios'

export const useStudentsStore = defineStore('students', {
  state: () => ({
    students: [],
    loading: false
  }),

  getters: {
    auth: () => useAuthStore()
  },

  actions: {
    async fetchStudents() {
      if (this.students.length > 0) return
      this.loading = true
      try {
        const res = await axios.get('/students', this.getAuthConfig())
        this.students = res.data
      } catch (e) {
        console.error('Fetch students error:', e.response || e)
      } finally {
        this.loading = false
      }
    },

    async refreshStudents() {
      this.loading = true
      try {
        const res = await axios.get('/students', this.getAuthConfig())
        this.students = res.data
      } catch (e) {
        console.error('Refresh students error:', e.response || e)
      } finally {
        this.loading = false
      }
    },

    async createStudent(studentData) {
      this.loading = true
      try {
        const res = await axios.post('/students', studentData, this.getAuthConfig())
        this.students.push(res.data.student)
        return res
      } catch (e) {
        console.error('Create student error:', e.response || e)
        throw e
      } finally {
        this.loading = false
      }
    },

    async updateStudent(studentId, updatedData) {
      this.loading = true
      try {
        const res = await axios.put(`/students/${studentId}`, updatedData, this.getAuthConfig())
        const index = this.students.findIndex(s => s.student_id === studentId)
        if (index !== -1) this.students[index] = res.data.student
        return res
      } catch (e) {
        console.error('Update student error:', e.response || e)
        throw e
      } finally {
        this.loading = false
      }
    },

    async deleteStudent(studentId) {
      this.loading = true
      try {
        const res = await axios.delete(`/students/${studentId}`, this.getAuthConfig())
        this.students = this.students.filter(s => s.student_id !== studentId)
        return res
      } catch (e) {
        console.error('Delete student error:', e.response || e)
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
