import { useEffect, useState } from 'react'
import { Search, Trash2, ToggleLeft } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Card, CardHeader, Badge, Btn, Alert, Spinner, Empty } from '../components/ui'
import api from '../api/client'
import type { Employee } from '../type'

export default function EmployeesPage({ onNav }: { onNav:(p:string)=>void }) {
  const { user } = useAuth()
  const [emps, setEmps]     = useState<Employee[]>([])
  const [q, setQ]           = useState('')
  const [loading, setLoading] = useState(true)
  const [msg, setMsg]       = useState<{text:string;type:'error'|'success'}|null>(null)

  const load = async (search='') => {
    setLoading(true)
    const r = await api.get('/employees/', { params: search ? { search } : {} })
    setEmps(r.data)
    setLoading(false)
  }

  useEffect(() => { load() }, [])

  const handleSearch = (v: string) => { setQ(v); load(v) }

  const toggleStatus = async (id: number) => {
    await api.patch(`/employees/${id}/status`)
    load(q)
    setMsg({ text:'Status updated', type:'success' })
    setTimeout(() => setMsg(null), 2500)
  }

  const deleteEmp = async (id: number, name: string) => {
    if (!confirm(`Delete ${name}? This cannot be undone.`)) return
    await api.delete(`/employees/${id}`)
    load(q)
    setMsg({ text:`${name} removed`, type:'success' })
    setTimeout(() => setMsg(null), 2500)
  }

  return (
    <div style={{ padding:22 }}>
      {msg && <Alert msg={msg.text} type={msg.type} />}
      {user?.role === 'employee' && (
        <Alert msg="You have read-only access to the employee directory." type="info" />
      )}
      <Card>
        <CardHeader title="All employees">
          <div style={{ display:'flex', gap:8, alignItems:'center' }}>
            <div style={{ position:'relative' }}>
              <Search size={13} style={{ position:'absolute', left:9, top:'50%', transform:'translateY(-50%)', color:'#888780' }} />
              <input value={q} onChange={e => handleSearch(e.target.value)} placeholder="Search..."
                style={{ paddingLeft:28, paddingRight:10, height:32, fontSize:12, border:'0.5px solid #D3D1C7', borderRadius:6, background:'#F7F7F5', color:'var(--text)', outline:'none', width:185 }} />
            </div>
            {user?.role === 'admin' && <Btn variant="primary" size="sm" onClick={() => onNav('add-employee')}>+ Add employee</Btn>}
          </div>
        </CardHeader>

        {loading ? <Spinner /> : emps.length === 0 ? <Empty msg="No employees found." /> : (
          <div style={{ overflowX:'auto' }}>
            <table style={{ width:'100%', borderCollapse:'collapse', fontSize:12 }}>
              <thead>
                <tr>{['Name','Department','Job title','Basic salary','Status','Role',''].map(h => (
                  <th key={h} style={{ textAlign:'left', padding:'7px 11px', fontSize:11, fontWeight:500, color:'#888780', borderBottom:'0.5px solid #E5E4DE' }}>{h}</th>
                ))}</tr>
              </thead>
              <tbody>
                {emps.map(e => (
                  <tr key={e.id}>
                    <td style={{ padding:'9px 11px', borderBottom:'0.5px solid #EFEEEA', fontWeight:500 }}>{e.name}</td>
                    <td style={{ padding:'9px 11px', borderBottom:'0.5px solid #EFEEEA', color:'#5F5E5A' }}>{e.department}</td>
                    <td style={{ padding:'9px 11px', borderBottom:'0.5px solid #EFEEEA', color:'#5F5E5A' }}>{e.job_title}</td>
                    <td style={{ padding:'9px 11px', borderBottom:'0.5px solid #EFEEEA' }}>KES {e.basic_salary.toLocaleString()}</td>
                    <td style={{ padding:'9px 11px', borderBottom:'0.5px solid #EFEEEA' }}><Badge v={e.status} /></td>
                    <td style={{ padding:'9px 11px', borderBottom:'0.5px solid #EFEEEA' }}><Badge v={e.role} /></td>
                    <td style={{ padding:'9px 11px', borderBottom:'0.5px solid #EFEEEA' }}>
                      {user?.role === 'admin' && (
                        <div style={{ display:'flex', gap:6 }}>
                          <button onClick={() => toggleStatus(e.id)} title="Toggle status"
                            style={{ background:'none', border:'none', cursor:'pointer', color:'#888780', padding:2 }}>
                            <ToggleLeft size={14} />
                          </button>
                          <button onClick={() => deleteEmp(e.id, e.name)} title="Delete"
                            style={{ background:'none', border:'none', cursor:'pointer', color:'#A32D2D', padding:2 }}>
                            <Trash2 size={14} />
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}