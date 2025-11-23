import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

const inferApiBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }

  if (typeof window !== 'undefined') {
    if (window.location.port === '5173') {
      return 'http://localhost:5000'
    }
    return window.location.origin
  }

  return 'http://localhost:5000'
}

axios.defaults.baseURL = inferApiBaseUrl()

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})


const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
