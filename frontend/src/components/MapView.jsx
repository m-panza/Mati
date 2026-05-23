import React, { useEffect, useRef } from 'react'

/**
 * MapView - Leaflet map component showing sitios, islas, nodos as markers.
 * Props:
 *   sitios  - array of {id, codigo, nombre, latitud, longitud}
 *   islas   - array of {id, codigo, nombre, latitud, longitud}
 *   nodos   - array of {id, codigo, nombre, latitud, longitud}
 *   height  - CSS height string (default '400px')
 */
export default function MapView({ sitios = [], islas = [], nodos = [], height = '400px' }) {
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)

  useEffect(() => {
    if (!mapRef.current) return
    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove()
      mapInstanceRef.current = null
    }

    // Lazy load leaflet
    import('leaflet').then(L => {
      // Fix default icon paths
      delete L.Icon.Default.prototype._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      })

      const map = L.map(mapRef.current).setView([-34.6, -58.4], 10)
      mapInstanceRef.current = map

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(map)

      const bounds = []

      const sitioIcon = L.divIcon({
        className: '',
        html: '<div style="width:14px;height:14px;background:#2563eb;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.5)"></div>',
        iconSize: [14, 14],
        iconAnchor: [7, 7],
      })

      const islaIcon = L.divIcon({
        className: '',
        html: '<div style="width:12px;height:12px;background:#16a34a;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.5)"></div>',
        iconSize: [12, 12],
        iconAnchor: [6, 6],
      })

      const nodoIcon = L.divIcon({
        className: '',
        html: '<div style="width:12px;height:12px;background:#ca8a04;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.5)"></div>',
        iconSize: [12, 12],
        iconAnchor: [6, 6],
      })

      sitios.forEach(s => {
        if (s.latitud && s.longitud) {
          const ll = [parseFloat(s.latitud), parseFloat(s.longitud)]
          L.marker(ll, { icon: sitioIcon })
            .bindPopup(`<b style="color:#000">[Sitio] ${s.codigo}</b><br>${s.nombre}`)
            .addTo(map)
          bounds.push(ll)
        }
      })

      islas.forEach(i => {
        if (i.latitud && i.longitud) {
          const ll = [parseFloat(i.latitud), parseFloat(i.longitud)]
          L.marker(ll, { icon: islaIcon })
            .bindPopup(`<b style="color:#000">[Isla] ${i.codigo}</b><br>${i.nombre}`)
            .addTo(map)
          bounds.push(ll)
        }
      })

      nodos.forEach(n => {
        if (n.latitud && n.longitud) {
          const ll = [parseFloat(n.latitud), parseFloat(n.longitud)]
          L.marker(ll, { icon: nodoIcon })
            .bindPopup(`<b style="color:#000">[Nodo] ${n.codigo}</b><br>${n.nombre}`)
            .addTo(map)
          bounds.push(ll)
        }
      })

      if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [20, 20] })
      }
    })

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [sitios, islas, nodos])

  return (
    <div style={{ position: 'relative' }}>
      <div
        ref={mapRef}
        style={{
          height,
          borderRadius: '8px',
          border: '1px solid var(--border)',
          overflow: 'hidden',
        }}
      />
      <div style={{
        position: 'absolute',
        top: '10px',
        right: '10px',
        background: 'rgba(0,0,0,0.75)',
        border: '1px solid var(--border)',
        borderRadius: '6px',
        padding: '8px 10px',
        fontSize: '11px',
        color: 'var(--text)',
        zIndex: 1000,
        display: 'flex',
        flexDirection: 'column',
        gap: '4px',
      }}>
        <span><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', background: '#2563eb', marginRight: '5px' }}></span>Sitio</span>
        <span><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', background: '#16a34a', marginRight: '5px' }}></span>Isla</span>
        <span><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', background: '#ca8a04', marginRight: '5px' }}></span>Nodo</span>
      </div>
    </div>
  )
}
