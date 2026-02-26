/**
 * 手机号脱敏：138****8888
 */
export function maskPhone(phone) {
  if (!phone || typeof phone !== 'string') return ''
  const s = String(phone).trim()
  if (s.length !== 11) return s
  return s.slice(0, 3) + '****' + s.slice(-4)
}
