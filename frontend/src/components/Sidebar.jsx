import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const NAV_ITEMS = [
  { path: '/',            label: 'Dashboard',   icon: '⊞', exact: true },
  { type: 'section',     label: 'Maestros' },
  { path: '/sitios',     label: 'Sitios',       icon: '📍' },
  { path: '/sectores',   label: 'Sectores',     icon: '▦'  },
  { path: '/corrientes', label: 'Corrientes',   icon: '♻'  },
  { path: '/islas',      label: 'Islas',        icon: '🗂'  },
  { path: '/tachos',     label: 'Tachos',       icon: '🗑'  },
  { path: '/nodos',      label: 'Nodos',        icon: '◈'  },
  { path: '/vehiculos',  label: 'Vehículos',    icon: '🚛'  },
  { path: '/receptores', label: 'Receptores',   icon: '🤝'  },
  { path: '/personas',   label: 'Personas',     icon: '👤'  },
  { type: 'section',     label: 'Herramientas' },
  { path: '/qr',         label: 'QR',           icon: '▦'  },
  { path: '/auditoria',  label: 'Auditoría',    icon: '📋'  },
]

const linkStyle = ({ isActive }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  padding: '8px 10px',
  borderRadius: '6px',
  color: isActive ? 'var(--text)' : 'var(--text-2)',
  background: isActive ? 'var(--bg-3)' : 'transparent',
  fontWeight: isActive ? '600' : '400',
  fontSize: '13px',
  textDecoration: 'none',
  transition: 'background 0.1s, color 0.1s',
  marginBottom: '1px',
})

export default function Sidebar({ open, onClose }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleNav = () => {
    if (onClose) onClose()
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <aside className={`sidebar${open ? ' open' : ''}`}>
      {/* Logo */}
      <div style={{ padding: '20px 16px 16px', borderBottom: '1px solid var(--border)', marginBottom: '8px' }}>
        <div style={{ fontSize: '16px', fontWeight: '800', color: 'var(--text)', letterSpacing: '0.05em' }}>
          SIGRAV
        </div>
        <div style={{ fontSize: '10px', color: 'var(--text-2)', marginTop: '2px' }}>
          Gestión de Residuos
        </div>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: '4px 8px', overflowY: 'auto' }}>
        {NAV_ITEMS.map((item, i) => {
          if (item.type === 'section') {
            return (
              <div key={i} style={{
                fontSize: '10px', fontWeight: '700', color: 'var(--text-2)',
                textTransform: 'uppercase', letterSpacing: '0.08em',
                padding: '10px 8px 4px',
              }}>
                {item.label}
              </div>
            )
          }
          return (
            <NavLink key={item.path} to={item.path} end={item.exact} style={linkStyle} onClick={handleNav}>
              <span style={{ fontSize: '14px', width: '18px', textAlign: 'center', flexShrink: 0 }}>
                {item.icon}
              </span>
              {item.label}
            </NavLink>
          )
        })}

        {user?.rol === 'admin' && (
          <NavLink to="/usuarios" style={linkStyle} onClick={handleNav}>
            <span style={{ fontSize: '14px', width: '18px', textAlign: 'center', flexShrink: 0 }}>👑</span>
            Usuarios
          </NavLink>
        )}
      </nav>

      {/* User info */}
      <div style={{
        padding: '12px 16px',
        borderTop: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        flexShrink: 0,
      }}>
        <div style={{
          width: '30px', height: '30px', borderRadius: '50%',
          background: 'var(--accent)', display: 'flex', alignItems: 'center',
          justifyContent: 'center', fontSize: '12px', fontWeight: '700',
          color: '#fff', flexShrink: 0,
        }}>
          {user?.nombre?.[0]?.toUpperCase() || 'U'}
        </div>
        <div style={{ flex: 1, overflow: 'hidden' }}>
          <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {user?.nombre} {user?.apellido}
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-2)' }}>{user?.rol}</div>
        </div>
        <button
          onClick={handleLogout}
          title="Cerrar sesión"
          style={{ background: 'none', border: 'none', color: 'var(--text-2)', fontSize: '16px', cursor: 'pointer', padding: '4px', borderRadius: '4px' }}
        >
          ✕
        </button>
      </div>
    </aside>
  )
}
