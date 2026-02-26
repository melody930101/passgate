import request from './index'

export function login(data) {
  return request.post('auth/login', data)
}

export function changePassword(data) {
  return request.post('auth/change-password', data)
}
