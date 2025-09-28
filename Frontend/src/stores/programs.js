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
    }
  }
})
