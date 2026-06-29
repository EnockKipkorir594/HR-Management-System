import { LayoutDashboard, Users, Calendar, DollarSign, FileText, LogOut } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const NAV = [
  { id:'dashboard',  label:'Dashboard',  Icon:LayoutDashboard },
  { id:'employees',  label:'Employees',  Icon:Users },
  { id:'attendance', label:'Attendance', Icon:Calendar },
  { id:'payroll',    label:'Payroll',    Icon:DollarSign, adminOnly:true },
  { id:'payslip',    label:'Payslip',    Icon:FileText },
]

interface Props { active: string; onNav: (p:string) => void }

export default function Sidebar({ active, onNav }: Props) {
  const { user, logout } = useAuth()
  const nav = NAV.filter(n => !n.adminOnly || user?.role === 'admin')

  return (
    <aside style={{
      width:220, minWidth:220, background:'#fff',
      borderRight:'0.5px solid #E5E4DE',
      display:'flex', flexDirection:'column', height:'100vh',
    }}>
      {/* Logo */}
      <div style={{ padding:'18px 16px 14px', borderBottom:'0.5px solid #E5E4DE' }}>
        <div style={{
          width:36, height:36, background:'#E6F1FB', borderRadius:8,
          display:'flex', alignItems:'center', justifyContent:'center', marginBottom:10,
        }}>
          <Users size={18} color="#185FA5" />
        </div>
        <div style={{ fontSize:13, fontWeight:500 }}>HR Payroll System</div>
        <div style={{ fontSize:11, color:'#888780', marginTop:2 }}>
          {user?.role === 'admin' ? 'Administrator' : 'Employee Portal'}
        </div>
      </div>

      {/* Nav */}
      <nav style={{ padding:'12px 0', flex:1 }}>
        <div style={{ fontSize:10, fontWeight:500, color:'#888780', padding:'0 14px 8px', letterSpacing:'.05em', textTransform:'uppercase' }}>
          Menu
        </div>
        {nav.map(({ id, label, Icon }) => {
          const on = active === id
          return (
            <button key={id} onClick={() => onNav(id)} style={{
              width:'100%', display:'flex', alignItems:'center', gap:9,
              padding:'9px 14px', fontSize:13, border:'none', background:'none',
              color: on ? '#185FA5' : '#5F5E5A',
              backgroundColor: on ? '#E6F1FB' : 'transparent',
              borderLeft: `2px solid ${on ? '#185FA5' : 'transparent'}`,
              cursor:'pointer', textAlign:'left',
            }}>
              <Icon size={15} style={{ opacity: on ? 1 : 0.65, flexShrink:0 }} />
              {label}
            </button>
          )
        })}
      </nav>

      {/* Footer */}
      <div style={{ padding:'12px 14px', borderTop:'0.5px solid #E5E4DE' }}>
        <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:10 }}>
          <div style={{
            width:30, height:30, borderRadius:'50%', background:'#E6F1FB',
            display:'flex', alignItems:'center', justifyContent:'center',
            fontSize:11, fontWeight:600, color:'#185FA5', flexShrink:0,
          }}>
            {user?.initials}
          </div>
          <div>
            <div style={{ fontSize:12, fontWeight:500 }}>{user?.name}</div>
            <div style={{ fontSize:11, color:'#888780', textTransform:'capitalize' }}>{user?.role}</div>
          </div>
        </div>
        <button onClick={logout} style={{
          width:'100%', padding:'7px 10px', fontSize:12, display:'flex',
          alignItems:'center', justifyContent:'center', gap:6,
          border:'0.5px solid #E5E4DE', borderRadius:6, background:'transparent', color:'#5F5E5A', cursor:'pointer',
        }}>
          <LogOut size={13} /> Sign out
        </button>
      </div>
    </aside>
  )
}