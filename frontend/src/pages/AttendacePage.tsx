import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, CardHeader, Spinner } from '../components/ui'
import api from '../api/client'
import type { Employee, AttendanceRecord } from '../type'

const STATUS_STYLE: Record<string, { bg:string; border:string; color:string; label:string }> = {
  present: { bg:'#EAF3DE', border:'#97C459', color:'#27500A', label:'Present' },
  absent:  { bg:'#FCEBEB', border:'#F09595', color:'#791F1F', label:'Absent'  },
  leave:   { bg:'#FAEEDA', border:'#EF9F27', color:'#854F0B', label:'Leave'   },
  off:     { bg:'#F7F7F5', border:'#E5E4DE', color:'#888780', label:'Off'     },
}

const DAYS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

export default function AttendancePage() {
  const { user } = useAuth()
  const [employees, setEmployees]   = useState<Employee[]>([])
  const [selectedId, setSelectedId] = useState<number>(0)
  const [month,     setMonth]       = useState('2025-04')
  const [records,   setRecords]     = useState<AttendanceRecord[]>([])
  const [loading,   setLoading]     = useState(false)

  useEffect(() => {
    if (user?.role === 'admin') {
      api.get('/employees/?status=active').then(r => {
        setEmployees(r.data)
        if (r.data.length && !selectedId) setSelectedId(r.data[0].id)
      })
    } else {
      setSelectedId(user!.employee_id)
    }
  }, [user])

  useEffect(() => {
    if (!selectedId) return
    setLoading(true)
    api.get('/attendance/', { params:{ employee_id:selectedId, month } })
      .then(r => setRecords(r.data))
      .finally(() => setLoading(false))
  }, [selectedId, month])

  const map = Object.fromEntries(records.map(r => [r.day, r.status]))
  const summary = records.reduce((acc, r) => {
    acc[r.status] = (acc[r.status] || 0) + 1; return acc
  }, {} as Record<string,number>)

  // Compute day-of-week offset for the selected month (0=Mon)
  const [yr, mo] = month.split('-').map(Number)
  const firstDay = new Date(yr, mo-1, 1).getDay() // 0=Sun
  const offset   = firstDay === 0 ? 6 : firstDay - 1 // shift to Mon-start
  const daysInMonth = new Date(yr, mo, 0).getDate()

  return (
    <div style={{ padding:22 }}>
      <Card>
        <CardHeader title={`Attendance — ${month}`}>
          <div style={{ display:'flex', gap:10, alignItems:'center' }}>
            {Object.entries(STATUS_STYLE).filter(([k]) => k !== 'off').map(([k, s]) => (
              <span key={k} style={{ display:'flex', alignItems:'center', gap:4, fontSize:11, color:'#5F5E5A' }}>
                <span style={{ width:10, height:10, background:s.bg, border:`0.5px solid ${s.border}`, borderRadius:2, display:'inline-block' }} />
                {s.label}
              </span>
            ))}
          </div>
        </CardHeader>

        <div style={{ display:'flex', gap:10, marginBottom:18 }}>
          {user?.role === 'admin' && (
            <select value={selectedId} onChange={e => setSelectedId(Number(e.target.value))}
              style={{ padding:'6px 10px', fontSize:12, border:'0.5px solid #D3D1C7', borderRadius:6, background:'#F7F7F5', color:'var(--text)', outline:'none' }}>
              {employees.map(e => <option key={e.id} value={e.id}>{e.name} — {e.department}</option>)}
            </select>
          )}
          <input type="month" value={month} onChange={e => setMonth(e.target.value)}
            style={{ padding:'6px 10px', fontSize:12, border:'0.5px solid #D3D1C7', borderRadius:6, background:'#F7F7F5', color:'var(--text)', outline:'none' }} />
        </div>

        {loading ? <Spinner /> : (
          <>
            {/* Day-of-week headers */}
            <div style={{ display:'grid', gridTemplateColumns:'repeat(7,1fr)', gap:5, marginBottom:5 }}>
              {DAYS.map(d => <div key={d} style={{ textAlign:'center', fontSize:11, fontWeight:500, color:'#888780', padding:'5px 0' }}>{d}</div>)}
            </div>
            {/* Calendar grid */}
            <div style={{ display:'grid', gridTemplateColumns:'repeat(7,1fr)', gap:5 }}>
              {/* Empty cells for offset */}
              {Array.from({ length: offset }, (_, i) => <div key={`e${i}`} />)}
              {Array.from({ length: daysInMonth }, (_, i) => {
                const day    = i + 1
                const status = map[day] ?? 'off'
                const s      = STATUS_STYLE[status]
                return (
                  <div key={day} style={{ padding:'7px 4px', textAlign:'center', borderRadius:6, border:`0.5px solid ${s.border}`, background:s.bg, color:s.color }}>
                    <div style={{ fontWeight:600, fontSize:13 }}>{day}</div>
                    <div style={{ fontSize:10, marginTop:2 }}>{s.label}</div>
                  </div>
                )
              })}
            </div>

            {/* Summary */}
            <div style={{ marginTop:16, display:'flex', gap:20, fontSize:12, color:'#5F5E5A', paddingTop:14, borderTop:'0.5px solid #E5E4DE' }}>
              <span>Present: <strong style={{ color:'#27500A' }}>{summary.present ?? 0}</strong></span>
              <span>Absent: <strong style={{ color:'#791F1F' }}>{summary.absent ?? 0}</strong></span>
              <span>On leave: <strong style={{ color:'#854F0B' }}>{summary.leave ?? 0}</strong></span>
              <span>Days off: <strong>{summary.off ?? 0}</strong></span>
            </div>
          </>
        )}
      </Card>
    </div>
  )
}