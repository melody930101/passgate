import axios from 'axios'
import { useUserStore } from '@/store/user'

// 开发代理: baseURL='/api'；直连后端: VITE_API_BASE_URL=http://localhost:8000 则 baseURL=http://localhost:8000/api
const baseURL = (import.meta.env.VITE_API_BASE_URL || '') + '/api'

const request = axios.create({
  baseURL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

request.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})

request.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response?.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default request
