import request from './index'

export function getActiveMovies() {
  return request.get('movies/active')
}

export function getAllMovies() {
  return request.get('movies')
}

export function createMovie(data) {
  return request.post('movies', data)
}

export function updateMovie(id, data) {
  return request.put(`movies/${id}`, data)
}

export function deactivateMovie(id) {
  return request.post(`movies/${id}/deactivate`)
}
