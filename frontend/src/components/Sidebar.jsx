import React, { useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const NAV_ITEMS = [
  { path: '/', label: 'Dashboard', icon: '⊞', exact: true },
  { type: 'section', label: 'Maestros' },
  { path: '/sitios', label: 'Sitios', icon: '📍' },
  { path: '/sectores', label: 'Sectores', icon: '▦' },
  { path: '/corrientes', label: 'Corrientes', icon: '♻' },
  { path: '/islas', label: 'Islas', icon: '🗂' },
  { path: '/tachos', label: 'Tachos', icon: '🗑' },
  { path: '/nodos', label: 'Nodos', icon: '◈' },
  { path: '/vehiculos', label: 'Vehículos', icon: '🚛' },
  { path: '/receptores', label: 'Receptores', icon: '🤝' },
  { path: '/personas', label: 'Personas', icon: '👤' },
  { type: 'section', label: 'Herramientas' },
  { path: '/qr', label: 'QR', icon: '▦' },
  { path: '/auditoria', label: 'Auditoría', icon: '📋' },
]

const styles = {
  sidebar: {
    width: '220px',
    minWidth: '220px',
    background: 'var(--bg-2)',
    borderRight: '1px solid var(--border)',
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    overflowY: 'auto',
    position: 'sticky',
    top: 0,
  },
  logo: {
    padding: '20px 16px 16px',
    borderBottom: '1px solid var(--border)',
    marginBottom: '8px',
  },
  logoText: {
    fontSize: '16px',
    fontWeight: '800',
    color: 'var(--text)',
    letterSpacing: '0.05em',
  },
  logoSub: {
    fontSize: '10px',
    color: 'var(--text-2)',
    marginTop: '2px',
  },
  nav: {
    flex: 1,
    padding: '4px 8px',
  },
  section: {
    fontSize: '10px',
    fontWeight: '700',
    color: 'var(--text-2)',
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
    padding: '10px 8px 4px',
  },
  user: {
    padding: '12px 16px',
    borderTop: '1px solid var(--border)',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  userInfo: {
    flex: 1,
    overflow: 'hidden',
  },
  userName: {
    fontSize: '13px',
    fontWeight: '600',
    color: 'var(--text)',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  userRol: {
    fontSize: '11px',
    color: 'var(--text-2)',
  },
  logoutBtn: {
    background: 'none',
    border: 'none',
    color: 'var(--text-2)',
    fontSize: '16px',
    cursor: 'pointer',
    padding: '4px',
  },
}

const navLinkStyle = ({ isActive }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  padding: '7px 10px',
  borderRadius: '6px',
  color: isActive ? 'var(--text)' : 'var(--text-2)',
  background: isActive ? 'var(--bg-3)' : 'transparent',
  fontWeight: isActive ? '600' : '400',
  fontSize: '13px',
  textDecoration: 'none',
  transition: 'background 0.1s, color 0.1s',
  marginBottom: '1px',
})

export default function Sidebar() {
  const { user, logout } = useAuth()
  const location = useLocation()

  return (
    <aside style={styles.sidebar}>
      <div style={styles.logo}>
        <div style={styles.logoText}>SIGRAV</div>
        <div style={styles.logoSub}>Gestión de Residuos</div>
      </div>

      <nav style={styles.nav}>
        {NAV_ITEMS.map((item, i) => {
          if (item.type === 'section') {
            return <div key={i} style={styles.section}>{item.label}</div>
          }
          // Admin-only items
          if (item.adminOnly && user?.rol !== 'admin') return null

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.exact}
              style={navLinkStyle}
            >
              <span style={{ fontSize: '14px', width: '18px', textAlign: 'center' }}>{item.icon}</span>
              {item.label}
            </NavLink>
          )
        })}
        {user?.rol === 'admin' && (
          <NavLink to="/usuarios" style={navLinkStyle}>
            <span style={{ fontSize: '14px', width: '18px', textAlign: 'center' }}>👑</span>
            Usuarios
          </NavLink>
        )}
      </nav>

      <div style={styles.user}>
        <div style={{ width: '30px', height: '30px', borderRadius: '50%', background: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: '700', color: '#fff', flexShrink: 0 }}>
          {user?.nombre?.[0]?.toUpperCase() || 'U'}
        </div>
        <div style={styles.userInfo}>
          <div style={styles.userName}>{user?.nombre} {user?.apellido}</div>
          <div style={styles.userRol}>{user?.rol}</div>
        </div>
        <button style={styles.logoutBtn} onClick={logout} title="Cerrar sesión">✕</button>
      </div>
    </aside>
  )
}
