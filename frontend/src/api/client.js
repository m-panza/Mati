const BASE_URL = import.meta.env.VITE_API_URL || '/api'

export function getToken() {
  return localStorage.getItem('sigrav_token')
}

export function setToken(token) {
  localStorage.setItem('sigrav_token', token)
}

export function removeToken() {
  localStorage.removeItem('sigrav_token')
}

export async function authFetch(path, options = {}) {
  const token = getToken()
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers })
  if (res.status === 401) {
    removeToken()
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }
  return res
}

async function handleResponse(res) {
  if (!res.ok) {
    let msg = `HTTP ${res.status}`
    try {
      const data = await res.json()
      msg = data.detail || JSON.stringify(data)
    } catch (_) {}
    throw new Error(msg)
  }
  if (res.status === 204) return null
  return res.json()
}

// Generic CRUD factory
function crudApi(prefix) {
  return {
    list: (params = {}) => {
      const qs = new URLSearchParams(
        Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
      ).toString()
      return authFetch(`${prefix}${qs ? '?' + qs : ''}`).then(handleResponse)
    },
    get: (id) => authFetch(`${prefix}/${id}`).then(handleResponse),
    create: (data) =>
      authFetch(prefix, { method: 'POST', body: JSON.stringify(data) }).then(handleResponse),
    update: (id, data) =>
      authFetch(`${prefix}/${id}`, { method: 'PUT', body: JSON.stringify(data) }).then(handleResponse),
    deactivate: (id) =>
      authFetch(`${prefix}/${id}`, { method: 'DELETE' }).then(handleResponse),
  }
}

export const api = {
  auth: {
    login: (email, password) =>
      fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      }).then(handleResponse),
    me: () => authFetch('/auth/me').then(handleResponse),
  },
  users: crudApi('/users'),
  sitios: crudApi('/sitios'),
  sectores: crudApi('/sectores'),
  corrientes: crudApi('/corrientes'),
  clasificaciones: crudApi('/clasificaciones'),
  islas: crudApi('/islas'),
  tachos: crudApi('/tachos'),
  nodos: crudApi('/nodos'),
  vehiculos: crudApi('/vehiculos'),
  receptores: crudApi('/receptores'),
  personas: crudApi('/personas'),
  qr: {
    generar: (entidad_tipo, entidad_id) =>
      authFetch('/qr/generar', {
        method: 'POST',
        body: JSON.stringify({ entidad_tipo, entidad_id }),
      }).then(handleResponse),
    get: (entidad_tipo, entidad_id) =>
      authFetch(`/qr/${entidad_tipo}/${entidad_id}`).then(handleResponse),
    imagenUrl: (codigo_qr) => `${BASE_URL}/qr/imagen/${codigo_qr}`,
  },
  documentos: {
    list: (params = {}) => {
      const qs = new URLSearchParams(
        Object.entries(params).filter(([, v]) => v !== undefined && v !== null)
      ).toString()
      return authFetch(`/documentos${qs ? '?' + qs : ''}`).then(handleResponse)
    },
    upload: (formData) => {
      const token = getToken()
      return fetch(`${BASE_URL}/documentos/upload`, {
        method: 'POST',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      }).then(handleResponse)
    },
    deactivate: (id) =>
      authFetch(`/documentos/${id}`, { method: 'DELETE' }).then(handleResponse),
  },
  auditoria: {
    list: (params = {}) => {
      const qs = new URLSearchParams(
        Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
      ).toString()
      return authFetch(`/auditoria${qs ? '?' + qs : ''}`).then(handleResponse)
    },
  },
  exportar: {
    url: (entity) => `${BASE_URL}/exportar/${entity}`,
  },
}
