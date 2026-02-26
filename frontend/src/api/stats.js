import request from './index'

export function getTodayStats() {
  return request.get('stats/today')
}
