const TOKEN_KEY = 'minitask_token'

export function setToken(token) { localStorage.setItem(TOKEN_KEY, token) }
export function getToken() { return localStorage.getItem(TOKEN_KEY) }
export function logout() { localStorage.removeItem(TOKEN_KEY) }

export async function api(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`/api${path}`, { ...options, headers })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`)
  return data
}
