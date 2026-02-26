import { defineStore } from 'pinia'
import { getToken, setToken, removeToken, isTokenExpired } from '@/utils/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getToken() || '',
    id: null,
    username: '',
    name: '',
    role: '' // 'admin' | 'staff'
  }),

  getters: {
    isAdmin: (state) => state.role === 'admin',
    isLoggedIn: (state) => !!state.token && !isTokenExpired(state.token)
  },

  actions: {
    setUser(payload) {
      this.token = payload.token
      this.id = payload.id
      this.username = payload.username
      this.name = payload.name
      this.role = payload.role
      setToken(payload.token)
    },

    logout() {
      this.token = ''
      this.id = null
      this.username = ''
      this.name = ''
      this.role = ''
      removeToken()
    }
  }
})
