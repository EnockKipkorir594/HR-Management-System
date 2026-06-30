import { useState } from 'react'
import { useAuth } from './context/AuthContext'
import LoginPage       from './pages/LoginPage'
import DashboardPage   from './pages/DashboardPage'
import EmployeesPage   from './pages/EmployeesPage'
import AttendancePage  from './pages/AttendacePage'
import PayrollPage     from './pages/PayrollPage'
import PayslipPage     from './pages/PayslipPage'
import AddEmployeePage from './pages/AddEmployeePage'
import Sidebar         from './components/Sidebar'

const TITLES: Record<string,string> = {
  dashboard:'Dashboard', employees:'Employees', attendance:'Attendance',
  payroll:'Payroll processing', payslip:'Payslip', 'add-employee':'Add new employee',
}

export default function App() {
  const { user } = useAuth()
  const [page, setPage] = useState('dashboard')

  if (!user) return <LoginPage />

  const today = new Date().toLocaleDateString('en-GB', { weekday:'long', year:'numeric', month:'long', day:'numeric' })

  const renderPage = () => {
    switch (page) {
      case 'dashboard':    return <DashboardPage   onNav={setPage} />
      case 'employees':    return <EmployeesPage   onNav={setPage} />
      case 'attendance':   return <AttendancePage  />
      case 'payroll':      return <PayrollPage      />
      case 'payslip':      return <PayslipPage      />
      case 'add-employee': return <AddEmployeePage onNav={setPage} />
      default:             return <DashboardPage   onNav={setPage} />
    }
  }

  return (
    <div style={{ display:'flex', height:'100vh', background:'#F1EFE8' }}>
      <Sidebar active={page} onNav={setPage} />
      <div style={{ flex:1, display:'flex', flexDirection:'column', overflow:'hidden' }}>
        {/* Topbar */}
        <header style={{
          background:'#fff', borderBottom:'0.5px solid #E5E4DE',
          padding:'11px 22px', display:'flex', alignItems:'center', justifyContent:'space-between', flexShrink:0,
        }}>
          <span style={{ fontSize:15, fontWeight:500 }}>{TITLES[page] ?? page}</span>
          <span style={{ fontSize:12, color:'#888780' }}>{today}</span>
        </header>
        <main style={{ flex:1, overflowY:'auto' }}>{renderPage()}</main>
      </div>
    </div>
  )
}