const PHONE_REG = /^1\d{10}$/

export function validatePhone(phone) {
  if (!phone || !String(phone).trim()) return { valid: false, message: '请输入手机号' }
  if (!PHONE_REG.test(String(phone))) return { valid: false, message: '请输入正确的 11 位手机号' }
  return { valid: true }
}

export function validateQuantity(qty) {
  const n = Number(qty)
  if (Number.isNaN(n) || n < 1) return { valid: false, message: '张数至少为 1' }
  if (n > 10) return { valid: false, message: '张数最多为 10' }
  return { valid: true }
}
