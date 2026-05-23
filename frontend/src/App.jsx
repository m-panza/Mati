import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import SitiosPage from './pages/SitiosPage'
import SectoresPage from './pages/SectoresPage'
import IslasPage from './pages/IslasPage'
import TachosPage from './pages/TachosPage'
import NodosPage from './pages/NodosPage'
import CorrientesPage from './pages/CorrientesPage'
import VehiculosPage from './pages/VehiculosPage'
import ReceptoresPage from './pages/ReceptoresPage'
import PersonasPage from './pages/PersonasPage'
import QRPage from './pages/QRPage'
import AuditoriaPage from './pages/AuditoriaPage'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}><span className="spinner" /></div>
  if (!user) return <Navigate to="/login" replace />
  return children
}

function AppRoutes() {
  const { user } = useAuth()

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage />} />
      <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
        <Route index element={<DashboardPage />} />
        <Route path="sitios" element={<SitiosPage />} />
        <Route path="sectores" element={<SectoresPage />} />
        <Route path="corrientes" element={<CorrientesPage />} />
        <Route path="islas" element={<IslasPage />} />
        <Route path="tachos" element={<TachosPage />} />
        <Route path="nodos" element={<NodosPage />} />
        <Route path="vehiculos" element={<VehiculosPage />} />
        <Route path="receptores" element={<ReceptoresPage />} />
        <Route path="personas" element={<PersonasPage />} />
        <Route path="qr" element={<QRPage />} />
        <Route path="auditoria" element={<AuditoriaPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}
