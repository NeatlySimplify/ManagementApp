import { defineStore } from 'pinia'
import { api } from '@/util/api'

class User {
  constructor(email, name) {
    this.email = email
    this.name = name
    this.entityTitle = ''
    this.engagementTitle = ''
  }
}

const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
  }),
  actions: {
    async login(email, password) {
      try {
        const response = await api.post('/api/login', { email, password })
        this.user = new User(response.data.user.email, response.data.user.name)
      } catch (error) {
        console.error(error)
      }
    },
    async logout() {
      try {
        await api.post('/api/logout')
        this.user = null
      } catch (error) {
        console.error(error)
      }
    },
    async updateEngagementTitle(title) {
      try {
        await api.put('/api/user/engagement', { title })
        this.user.engagementTitle = title
      } catch (error) {
        console.error(error)
      }
    },
    async updateEntityTitle(title) {
      try {
        await api.put('/api/user/entity', { title })
        this.user.entityTitle = title
      } catch (error) {
        console.error(error)
      }
    },
  },
})

export default useUserStore
