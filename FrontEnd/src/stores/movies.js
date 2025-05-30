import { api } from '@/util/api'
import { defineStore } from 'pinia'

class Movie {
  constructor(id, title, genre) {
    this.id = id
    this.title = title
    this.genre = genre
  }
}
const useMoviesStore = defineStore('movies', {
  state: () => ({
    movies: [],
  }),
  actions: {
    async fetchMovies() {
      try {
        const response = await api.get('/api/movies')
        const moviesArray = response.data.movies
        for (const { id, title, genre } of moviesArray) {
          this.movies.push(new Movie(id, title, genre))
        }
      } catch (error) {
        console.error(error)
      }
    },
    async addMovie(movie) {
      const response = await api.post('/movies', movie)
      this.movies.push(response.data)
    },
    async updateMovie(movie) {
      const response = await api.put(`/movies/${movie.id}`, movie)
      const index = this.movies.findIndex((m) => m.id === movie.id)
      if (index !== -1) this.movies[index] = response.data
    },
    async deleteMovie(id) {
      await api.delete(`/movies/${id}`)
      this.movies = this.movies.filter((m) => m.id !== id)
    },
    getMoviesMatching(attribute, pattern) {
      const regex = new RegExp(pattern, 'i')
      return this.movies.filter((movie) => regex.test(movie[attribute]))
    },
  },
})

export default useMoviesStore
