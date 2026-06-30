import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, Badge, Btn, Alert, Spinner } from '../components/ui'
import api from '../api/client'
import type { Employee, Payslip } from '../type'

export default function PayslipPage() {
  const { user } = useAuth()
  const [employees,   setEmployees]   = useState<Employee[]>([])
  const [selectedId,  setSelectedId]  = useState(0)
  const [month,       setMonth]       = useState('2025-04')
  const [payslip,     setPayslip]     = useState<Payslip|null>(null)
  const [loading,     setLoading]     = useState(false)
  const [error,       setError]       = useState('')

  useEffect(() => {
    if (user?.role === 'admin') {
      api.get('/employees/?status=active').then(r => {
        setEmployees(r.data)
        setSelectedId(r.data[0]?.id ?? 0)
      })
    } else {
      setSelectedId(user!.employee_id)
    }
  }, [user])

  useEffect(() => {
    if (!selectedId) return
    setLoading(true); setError(''); setPayslip(null)
    api.get(`/payslips/${selectedId}`, { params:{ month } })
      .then(r => setPayslip(r.data))
      .catch(e => setError(e.response?.data?.detail || 'No payslip for this period'))
      .finally(() => setLoading(false))
  }, [selectedId, month])

  const Row = ({ label, value, color, bold }: { label:string; value:string; color?:string; bold?:boolean }) => (
    <div style={{
      display:'flex', justifyContent:'space-between', padding:'6px 0',
      fontSize:13, fontWeight: bold ? 500 : 400,
      borderTop: bold ? '0.5px solid #E5E4DE' : undefined,
      marginTop: bold ? 8 : 0,
    }}>
      <span style={{ color: color ?? '#5F5E5A' }}>{label}</span>
      <span style={{ color: color ?? 'var(--text)' }}>{value}</span>
    </div>
  )

  const fmt = (n: number) => `KES ${n.toLocaleString()}`

  return (
    <div style={{ padding:22, display:'flex', gap:18, alignItems:'flex-start' }}>
      {/* Payslip document */}
      <div style={{ background:'#fff', border:'0.5px solid #E5E4DE', borderRadius:12, padding:26, width:420, flexShrink:0 }}>
        {loading && <Spinner />}
        {error   && <Alert msg={error} />}
        {payslip && (
          <>
            <div style={{ borderBottom:'0.5px solid #E5E4DE', paddingBottom:16, marginBottom:4 }}>
              <div style={{ fontSize:15, fontWeight:600 }}>HR Payroll System Ltd.</div>
              <div style={{ fontSize:12, color:'#5F5E5A', marginTop:2 }}>Payslip for {payslip.pay_period}</div>
              <div style={{ marginTop:13, padding:'10px 13px', background:'#F7F7F5', borderRadius:6 }}>
                <div style={{ fontSize:13, fontWeight:500 }}>{payslip.employee_name}</div>
                <div style={{ fontSize:11, color:'#5F5E5A', marginTop:2 }}>{payslip.job_title} — {payslip.department}</div>
                <div style={{ fontSize:11, color:'#888780' }}>{payslip.email}</div>
                <div style={{ fontSize:11, color:'#888780' }}>Ref: {payslip.reference}</div>
              </div>
            </div>

            <div style={{ fontSize:10, fontWeight:500, color:'#888780', textTransform:'uppercase', letterSpacing:'.05em', margin:'14px 0 8px' }}>Earnings</div>
            <Row label="Basic salary"        value={fmt(payslip.basic_salary)} />
            <Row label="House allowance"     value={fmt(payslip.house_allowance)} />
            <Row label="Transport allowance" value={fmt(payslip.transport_allowance)} />
            <Row label="Gross pay"           value={fmt(payslip.gross_pay)} bold />

            <div style={{ fontSize:10, fontWeight:500, color:'#888780', textTransform:'uppercase', letterSpacing:'.05em', margin:'14px 0 8px' }}>Deductions</div>
            <Row label="PAYE (tax)" value={`- ${fmt(payslip.paye)}`} color="#791F1F" />
            <Row label="NHIF"       value={`- ${fmt(payslip.nhif)}`} color="#791F1F" />
            <Row label="NSSF"       value={`- ${fmt(payslip.nssf)}`} color="#791F1F" />
            <Row label="Total deductions" value={`- ${fmt(payslip.total_deductions)}`} bold color="#791F1F" />

            <div style={{ marginTop:12, padding:'12px 0 0', borderTop:'0.5px solid #E5E4DE', display:'flex', justifyContent:'space-between', fontSize:15, fontWeight:600 }}>
              <span>Net pay</span>
              <span style={{ color:'#27500A' }}>{fmt(payslip.net_pay)}</span>
            </div>

            <div style={{ marginTop:18, display:'flex', gap:8 }}>
              <Btn variant="primary" size="sm">Download PDF</Btn>
              <Btn size="sm">Email payslip</Btn>
            </div>
          </>
        )}
      </div>

      {/* Right column — controls + reference */}
      <div style={{ flex:1, display:'flex', flexDirection:'column', gap:14 }}>
        <Card>
          <div style={{ fontSize:12, fontWeight:500, marginBottom:10, color:'#5F5E5A' }}>Payslip settings</div>
          {user?.role === 'admin' && (
            <div style={{ marginBottom:12 }}>
              <label style={{ display:'block', fontSize:12, fontWeight:500, color:'#5F5E5A', marginBottom:5 }}>Employee</label>
              <select value={selectedId} onChange={e => setSelectedId(Number(e.target.value))}
                style={{ width:'100%', padding:'7px 10px', fontSize:13, border:'0.5px solid #D3D1C7', borderRadius:6, background:'#F7F7F5', color:'var(--text)', outline:'none' }}>
                {employees.map(e => <option key={e.id} value={e.id}>{e.name}</option>)}
              </select>
            </div>
          )}
          <label style={{ display:'block', fontSize:12, fontWeight:500, color:'#5F5E5A', marginBottom:5 }}>Pay period</label>
          <input type="month" value={month} onChange={e => setMonth(e.target.value)}
            style={{ width:'100%', padding:'7px 10px', fontSize:13, border:'0.5px solid #D3D1C7', borderRadius:6, background:'#F7F7F5', color:'var(--text)', outline:'none' }} />
        </Card>

        {payslip && (
          <Card>
            <div style={{ fontSize:12, fontWeight:500, marginBottom:12 }}>Payslip reference</div>
            {[
              ['Reference No.', payslip.reference],
              ['Pay period',    payslip.pay_period],
              ['Payment',       payslip.payment_method],
            ].map(([l, v]) => (
              <div key={l} style={{ display:'flex', justifyContent:'space-between', padding:'5px 0', fontSize:12, borderBottom:'0.5px solid #EFEEEA' }}>
                <span style={{ color:'#5F5E5A' }}>{l}</span><span>{v}</span>
              </div>
            ))}
            <div style={{ display:'flex', justifyContent:'space-between', padding:'5px 0', fontSize:12 }}>
              <span style={{ color:'#5F5E5A' }}>Status</span>
              <Badge v={payslip.status as any} />
            </div>
          </Card>
        )}
      </div>
    </div>
  )
}