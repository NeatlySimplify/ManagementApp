import axios from "axios";

const api = axios.create({
  //baseURL: window.__API_URL__, // On Production, reads the api from the index received
  baseURL: "/api", // For testing with JSON-Server
  timeout: 10000,
  withCredentials: true,
});

export default api;
