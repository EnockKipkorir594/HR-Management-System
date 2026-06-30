import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, CardHeader, Badge, Spinner } from '../components/ui'
import api from '../api/client'

interface Stats { total:number; active:number; inactive:number; by_department:Record<string,number> }
interface PaySummary { total_gross:number; total_net:number; headcount:number; pending:number; processed:number }

export default function DashboardPage({ onNav }: { onNav:(p:string)=>void }) {
  const { user } = useAuth()
  const [stats, setStats]     = useState<Stats|null>(null)
  const [paySum, setPaySum]   = useState<PaySummary|null>(null)
  const [recentEmps, setRecentEmps] = useState<any[]>([])

  useEffect(() => {
    api.get('/employees/stats').then(r => setStats(r.data))
    api.get('/employees/?status=active').then(r => setRecentEmps(r.data.slice(0, 4)))
    if (user?.role === 'admin')
      api.get('/payroll/summary?month=2025-04').then(r => setPaySum(r.data))
  }, [user])

  const MetricCard = ({ label, value, sub, color }: { label:string; value:string; sub:string; color?:string }) => (
    <div style={{ background:'#F7F7F5', borderRadius:8, padding:'14px 16px' }}>
      <div style={{ fontSize:11.5, color:'#5F5E5A', marginBottom:6 }}>{label}</div>
      <div style={{ fontSize:24, fontWeight:500, lineHeight:1, color: color ?? 'var(--text)' }}>{value}</div>
      <div style={{ fontSize:11, color:'#888780', marginTop:5 }}>{sub}</div>
    </div>
  )

  return (
    <div style={{ padding:22 }}>
      {/* Welcome */}
      <div style={{
        background:'linear-gradient(120deg,#185FA5 0%,#0C447C 100%)',
        borderRadius:12, padding:'18px 22px', marginBottom:20, color:'#fff',
        display:'flex', alignItems:'center', justifyContent:'space-between',
      }}>
        <div>
          <div style={{ fontSize:15, fontWeight:500 }}>Welcome back, {user?.name.split(' ')[0]} 👋</div>
          <div style={{ fontSize:12, opacity:.8, marginTop:4 }}>
            {user?.role === 'admin' ? "Here's what's happening with your team today." : 'View your attendance, payslip and more.'}
          </div>
        </div>
        <div style={{
          width:44, height:44, borderRadius:'50%', background:'rgba(255,255,255,.15)',
          display:'flex', alignItems:'center', justifyContent:'center', fontSize:15, fontWeight:600,
        }}>{user?.initials}</div>
      </div>

      {/* Metrics */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:10, marginBottom:20 }}>
        <MetricCard label="Total employees" value={stats ? String(stats.total) : '—'} sub={stats ? `${stats.active} active, ${stats.inactive} inactive` : ''} color="#185FA5" />
        {user?.role === 'admin' ? (
          <MetricCard label="Monthly payroll" value={paySum ? `KES ${(paySum.total_net/1000).toFixed(0)}K` : '—'} sub="Net pay — April 2025" />
        ) : (
          <MetricCard label="My department" value="Engineering" sub="Your team" />
        )}
        <MetricCard label="Departments" value={stats ? String(Object.keys(stats.by_department).length) : '—'} sub="Active departments" color="#3B6D11" />
        {user?.role === 'admin' ? (
          <MetricCard label="Payroll status" value={paySum ? `${paySum.processed}/${paySum.headcount}` : '—'} sub="Processed this month" color="#854F0B" />
        ) : (
          <MetricCard label="Pay period" value="April '25" sub="Current period" />
        )}
      </div>

      {/* Bottom row */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:14 }}>
        <Card>
          <CardHeader title="Active employees">
            <button onClick={() => onNav('employees')} style={{ fontSize:12, padding:'5px 11px', border:'0.5px solid #E5E4DE', borderRadius:6, background:'transparent', color:'#5F5E5A', cursor:'pointer' }}>
              View all
            </button>
          </CardHeader>
          {recentEmps.length ? (
            <table style={{ width:'100%', borderCollapse:'collapse', fontSize:12 }}>
              <thead><tr>{['Name','Department','Status'].map(h => <th key={h} style={{ textAlign:'left', padding:'6px 10px', fontSize:11, fontWeight:500, color:'#888780', borderBottom:'0.5px solid #E5E4DE' }}>{h}</th>)}</tr></thead>
              <tbody>
                {recentEmps.map(e => (
                  <tr key={e.id}>
                    <td style={{ padding:'9px 10px', borderBottom:'0.5px solid #EFEEEA', fontWeight:500 }}>{e.name}</td>
                    <td style={{ padding:'9px 10px', borderBottom:'0.5px solid #EFEEEA', color:'#5F5E5A' }}>{e.department}</td>
                    <td style={{ padding:'9px 10px', borderBottom:'0.5px solid #EFEEEA' }}><Badge v={e.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : <Spinner />}
        </Card>

        <Card>
          <div style={{ fontSize:14, fontWeight:500, marginBottom:14 }}>Quick actions</div>
          {[
            { label:'View attendance', page:'attendance', c:{ bg:'#EAF3DE', color:'#27500A', border:'#97C459' } },
            { label:'View my payslip', page:'payslip',   c:{ bg:'#E6F1FB', color:'#185FA5', border:'#85B7EB' } },
            ...(user?.role === 'admin' ? [
              { label:'Run payroll',   page:'payroll',   c:{ bg:'#FAEEDA', color:'#854F0B', border:'#EF9F27' } },
              { label:'Add employee',  page:'add-employee', c:{ bg:'#EEEDFE', color:'#534AB7', border:'#AFA9EC' } },
            ] : []),
          ].map(({ label, page, c }) => (
            <button key={label} onClick={() => onNav(page)} style={{
              width:'100%', textAlign:'left', padding:'11px 14px', marginBottom:8, fontSize:13,
              fontWeight:500, border:`0.5px solid ${c.border}`, borderRadius:6,
              background:c.bg, color:c.color, cursor:'pointer',
            }}>
              {label} →
            </button>
          ))}
        </Card>
      </div>
    </div>
  )
}