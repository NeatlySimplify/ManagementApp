import axios from 'axios'

const api = axios.create({
  baseURL: window.__API_URL__,
  timeout: 10000,
  withCredentials: true
})

export default api
