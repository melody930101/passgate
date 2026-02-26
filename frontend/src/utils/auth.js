const TOKEN_KEY = 'passgate_token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
}

/**
 * 校验 Token 是否过期（7 天有效期，根据 JWT payload 或本地存储的过期时间）
 * 简单实现：JWT 通常带 exp，这里先用 7 天粗略判断
 */
export function isTokenExpired(token) {
  if (!token) return true
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp ? payload.exp * 1000 < Date.now() : false
  } catch {
    return true
  }
}
