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
        const res = await axios.get('http://127.0.0.1:5000/colleges')
        this.colleges = res.data
      } finally {
        this.loading = false
      }
    }
  }
})
