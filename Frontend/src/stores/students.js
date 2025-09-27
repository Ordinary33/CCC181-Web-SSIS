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
      const res = await axios.get('http://127.0.0.1:5000/students')
      this.students = res.data
      this.loading = false
    },
    async refreshStudents() {
      this.loading = true
      const res = await axios.get('http://127.0.0.1:5000/students')
      this.students = res.data
      this.loading = false
    }
  }
})
