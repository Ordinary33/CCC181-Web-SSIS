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
        const res = await axios.get('/api/students', this.getAuthConfig())
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
        const res = await axios.get('/api/students', this.getAuthConfig())
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
        const res = await axios.post('/api/students', studentData, this.getAuthConfig())
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
        const res = await axios.put(`/api/students/${studentId}`, updatedData, this.getAuthConfig())
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
        const res = await axios.delete(`/api/students/${studentId}`, this.getAuthConfig())
        this.students = this.students.filter(s => s.student_id !== studentId)
        return res
      } catch (e) {
        console.error('Delete student error:', e.response || e)
        throw e
      } finally {
        this.loading = false
      }
    },

    async updateStudentImage(studentId, file) {
      this.loading = true
      try {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if (!allowedTypes.includes(file.type)) throw new Error('Please upload a valid image (JPEG, PNG, WebP)')

        const maxSize = 5 * 1024 * 1024
        if (file.size > maxSize) throw new Error('File size must be less than 5MB')

        const fileExt = file.name.split('.').pop()
        const fileName = `students/${studentId}-${Date.now()}.${fileExt}`

        const { error: uploadError } = await supabase.storage
          .from('student-avatars')
          .upload(fileName, file, { cacheControl: '3600', upsert: true, contentType: file.type })

        if (uploadError) throw new Error(uploadError.message)

        const { data: urlData } = supabase.storage
          .from('student-avatars')
          .getPublicUrl(fileName)

        if (!urlData?.publicUrl) throw new Error('Failed to get image URL')

        const res = await axios.patch(`/api/students/${studentId}/image`, { image_url: urlData.publicUrl }, this.getAuthConfig())

        const index = this.students.findIndex(s => s.student_id === studentId)
        if (index !== -1) this.students[index].image_url = res.data.student.image_url

        return res.data.student.image_url
      } catch (e) {
        console.error('Update student image error:', e.response || e)
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
