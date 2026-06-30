import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, CardHeader, Badge, Btn, Alert, Spinner, Empty } from '../components/ui'
import api from '../api/client'
import type { PayrollRecord } from '../type'

interface Summary {
  month:string; headcount:number; total_gross:number; total_net:number;
  total_paye:number; total_nhif:number; total_nssf:number; pending:number; processed:number;
}

export default function PayrollPage() {
  const { user } = useAuth()
  const [month,   setMonth]   = useState('2025-04')
  const [records, setRecords] = useState<PayrollRecord[]>([])
  const [summary, setSummary] = useState<Summary|null>(null)
  const [loading, setLoading] = useState(false)
  const [running, setRunning] = useState(false)
  const [msg,     setMsg]     = useState<{text:string;type:'success'|'error'}|null>(null)

  if (user?.role !== 'admin') return (
    <div style={{ padding:22 }}><Alert msg="Admin access required." /></div>
  )

  const load = async () => {
    setLoading(true)
    const [pr, sm] = await Promise.all([
      api.get('/payroll/', { params:{ month } }),
      api.get('/payroll/summary', { params:{ month } }),
    ])
    setRecords(pr.data); setSummary(sm.data)
    setLoading(false)
  }

  useEffect(() => { load() }, [month])

  const handleRun = async () => {
    setRunning(true); setMsg(null)
    try {
      await api.post(`/payroll/run?month=${month}`)
      await load()
      setMsg({ text:'Payroll processed successfully with real PAYE/NHIF/NSSF calculations.', type:'success' })
    } catch {
      setMsg({ text:'Failed to run payroll.', type:'error' })
    } finally {
      setRunning(false)
    }
  }

  const fmt = (n: number) => `KES ${n.toLocaleString()}`

  return (
    <div style={{ padding:22 }}>
      {msg && <Alert msg={msg.text} type={msg.type} />}

      {/* Summary cards */}
      {summary && (
        <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:10, marginBottom:20 }}>
          {[
            { label:'Headcount',   value:String(summary.headcount) },
            { label:'Total gross', value:fmt(summary.total_gross), color:'#185FA5' },
            { label:'Total net',   value:fmt(summary.total_net),   color:'#27500A' },
            { label:'Total PAYE',  value:fmt(summary.total_paye),  color:'#791F1F' },
          ].map(c => (
            <div key={c.label} style={{ background:'#F7F7F5', borderRadius:8, padding:'14px 16px' }}>
              <div style={{ fontSize:11.5, color:'#5F5E5A', marginBottom:6 }}>{c.label}</div>
              <div style={{ fontSize:18, fontWeight:500, color: c.color ?? 'var(--text)' }}>{c.value}</div>
            </div>
          ))}
        </div>
      )}

      <Card>
        <CardHeader title={`Payroll — ${month}`}>
          <div style={{ display:'flex', gap:8, alignItems:'center' }}>
            <input type="month" value={month} onChange={e => setMonth(e.target.value)}
              style={{ padding:'6px 10px', fontSize:12, border:'0.5px solid #D3D1C7', borderRadius:6, background:'#F7F7F5', color:'var(--text)', outline:'none' }} />
            <Btn variant="primary" onClick={handleRun} disabled={running}>
              {running ? 'Processing…' : 'Run payroll'}
            </Btn>
          </div>
        </CardHeader>

        {loading ? <Spinner /> : records.length === 0 ? <Empty msg="No payroll records for this period." /> : (
          <div style={{ overflowX:'auto' }}>
            <table style={{ width:'100%', borderCollapse:'collapse', fontSize:12 }}>
              <thead>
                <tr>{['Employee','Basic salary','Allowances','Gross pay','PAYE','NHIF','NSSF','Net pay','Status'].map(h => (
                  <th key={h} style={{ textAlign:'left', padding:'7px 10px', fontSize:11, fontWeight:500, color:'#888780', borderBottom:'0.5px solid #E5E4DE' }}>{h}</th>
                ))}</tr>
              </thead>
              <tbody>
                {records.map(r => (
                  <tr key={r.id}>
                    <td style={{ padding:'9px 10px', borderBottom:'0.5px solid #EFEEEA', fontWeight:500 }}>{r.employee_name}</td>
                    {[r.basic_salary, r.allowances, r.gross_pay, r.paye, r.nhif, r.nssf].map((v, i) => (
                      <td key={i} style={{ padding:'9px 10px', borderBottom:'0.5px solid #EFEEEA' }}>{v.toLocaleString()}</td>
                    ))}
                    <td style={{ padding:'9px 10px', borderBottom:'0.5px solid #EFEEEA', fontWeight:500, color:'#27500A' }}>
                      {r.net_pay.toLocaleString()}
                    </td>
                    <td style={{ padding:'9px 10px', borderBottom:'0.5px solid #EFEEEA' }}><Badge v={r.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {summary && (
          <div style={{ marginTop:14, paddingTop:12, borderTop:'0.5px solid #E5E4DE', display:'flex', gap:20, fontSize:12, color:'#5F5E5A' }}>
            <span>Pending: <strong style={{ color:'#854F0B' }}>{summary.pending}</strong></span>
            <span>Processed: <strong style={{ color:'#27500A' }}>{summary.processed}</strong></span>
            <span>NHIF total: <strong>KES {summary.total_nhif.toLocaleString()}</strong></span>
            <span>NSSF total: <strong>KES {summary.total_nssf.toLocaleString()}</strong></span>
          </div>
        )}
      </Card>
    </div>
  )
}