import { useState } from 'react'
import { Users } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import api from '../api/client'
import { Btn, Alert } from '../components/ui'

export default function LoginPage() {
  const { login } = useAuth()
  const [role, setRole]     = useState<'admin'|'employee'>('admin')
  const [username, setU]    = useState('enock_admin')
  const [password, setP]    = useState('secret123')
  const [error, setError]   = useState('')
  const [loading, setLoading] = useState(false)

  const switchRole = (r: 'admin'|'employee') => {
    setRole(r)
    setU(r === 'admin' ? 'enock_admin' : 'alice_emp')
    setP('emp123')
    if (r === 'admin') setP('secret123')
    setError('')
  }

  const handleLogin = async () => {
    if (!username || !password) { setError('Please enter username and password'); return }
    setLoading(true); setError('')
    try {
      const form = new URLSearchParams({ username, password })
      const { data } = await api.post('/auth/login', form, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      login(data)
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight:'100vh', display:'flex', alignItems:'center',
      justifyContent:'center', background:'#F1EFE8',
    }}>
      <div style={{
        background:'#fff', border:'0.5px solid #E5E4DE', borderRadius:12,
        padding:36, width:360, boxShadow:'0 4px 24px rgba(0,0,0,0.06)',
      }}>
        <div style={{ width:42, height:42, background:'#E6F1FB', borderRadius:8, display:'flex', alignItems:'center', justifyContent:'center', marginBottom:16 }}>
          <Users size={20} color="#185FA5" />
        </div>

        <h1 style={{ fontSize:20, fontWeight:500, marginBottom:4 }}>HR Payroll System</h1>
        <p style={{ fontSize:13, color:'#5F5E5A', marginBottom:22 }}>Sign in to your account</p>

        {/* Role tabs */}
        <div style={{ display:'flex', gap:6, marginBottom:20 }}>
          {(['admin','employee'] as const).map(r => (
            <button key={r} onClick={() => switchRole(r)} style={{
              padding:'5px 14px', fontSize:12, borderRadius:6, cursor:'pointer',
              border:'0.5px solid', textTransform:'capitalize', fontFamily:'inherit',
              borderColor: role===r ? '#85B7EB' : '#E5E4DE',
              background:  role===r ? '#E6F1FB' : 'transparent',
              color:       role===r ? '#185FA5' : '#5F5E5A',
              fontWeight:  role===r ? 500 : 400,
            }}>{r}</button>
          ))}
        </div>

        {error && <Alert msg={error} />}

        {[
          { label:'Username', val:username, set:setU, type:'text' },
          { label:'Password', val:password, set:setP, type:'password' },
        ].map(f => (
          <div key={f.label} style={{ marginBottom:14 }}>
            <label style={{ display:'block', fontSize:12, fontWeight:500, color:'#5F5E5A', marginBottom:5 }}>{f.label}</label>
            <input
              type={f.type} value={f.val}
              onChange={e => f.set(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleLogin()}
              style={{ width:'100%', padding:'9px 11px', fontSize:13, border:'0.5px solid #D3D1C7', borderRadius:6, background:'#fff', color:'var(--text)', outline:'none' }}
            />
          </div>
        ))}

        <Btn onClick={handleLogin} variant="primary" fullWidth disabled={loading}>
          {loading ? 'Signing in…' : 'Sign in'}
        </Btn>

        <p style={{ marginTop:14, fontSize:11, color:'#888780', textAlign:'center' }}>
          Demo credentials pre-filled — click sign in.
        </p>
      </div>
    </div>
  )
}