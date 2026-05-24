import React, { useState, useCallback } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const close = useCallback(() => setSidebarOpen(false), [])
  const toggle = useCallback(() => setSidebarOpen(v => !v), [])

  return (
    <div className="app-layout">
      {/* Overlay for mobile */}
      <div
        className={`sidebar-overlay${sidebarOpen ? ' visible' : ''}`}
        onClick={close}
      />

      <Sidebar open={sidebarOpen} onClose={close} />

      <div className="app-main">
        {/* Mobile top bar */}
        <header className="app-topbar">
          <button className="hamburger" onClick={toggle} aria-label="Menú">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <rect y="3"  width="20" height="2" rx="1"/>
              <rect y="9"  width="20" height="2" rx="1"/>
              <rect y="15" width="20" height="2" rx="1"/>
            </svg>
          </button>
          <span className="topbar-logo">SIGRAV</span>
        </header>

        <div className="app-content">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
