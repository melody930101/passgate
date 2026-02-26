import request from './index'

export function checkUnusedTickets(params) {
  return request.get('tickets/check-unused', { params })
}

export function createTicket(data) {
  return request.post('tickets', data)
}

export function getTickets(params) {
  return request.get('tickets', { params })
}

export function getTicketDetail(id) {
  return request.get(`tickets/${id}`)
}

export function voidTicket(id) {
  return request.post(`tickets/${id}/void`)
}

export function verifyTicket(data) {
  return request.post('tickets/verify', data)
}

export function getCheckHistory(params) {
  return request.get('tickets/check-history', { params })
}
