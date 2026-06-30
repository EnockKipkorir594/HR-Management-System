import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Card, Btn, Alert, Input, Select } from '../components/ui'
import api from '../api/client'

interface Props { onNav:(p:string)=>void }

export default function AddEmployeePage({ onNav }: Props) {
  const { user } = useAuth()
  const [form, setForm] = useState({
    name:'', email:'', job_title:'', department:'Engineering',
    basic_salary:'', allowances:'', role:'employee', status:'active',
  })
  const [error,   setError]   = useState('')
  const [success, setSuccess] = useState('')
  const [saving,  setSaving]  = useState(false)

  if (user?.role !== 'admin') return (
    <div style={{ padding:22 }}><Alert msg="Admin access required." /></div>
  )

  const set = (k: string) => (v: string) => setForm(f => ({ ...f, [k]: v }))

  const handleSubmit = async () => {
    if (!form.name || !form.email || !form.job_title || !form.basic_salary) {
      setError('Please fill in all required fields'); return
    }
    setSaving(true); setError('')
    try {
      await api.post('/employees/', {
        ...form,
        basic_salary: parseFloat(form.basic_salary),
        allowances:   parseFloat(form.allowances || '0'),
      })
      setSuccess(`${form.name} added successfully!`)
      setTimeout(() => onNav('employees'), 1500)
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to add employee')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div style={{ padding:22 }}>
      <Card style={{ maxWidth:640 }}>
        <div style={{ fontSize:14, fontWeight:500, marginBottom:20 }}>Add new employee</div>
        {error   && <Alert msg={error} />}
        {success && <Alert msg={success} type="success" />}
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:14, marginBottom:18 }}>
          <Input label="Full name"        value={form.name}         onChange={set('name')}         placeholder="e.g. Jane Mwangi" required />
          <Input label="Email"            value={form.email}        onChange={set('email')}        type="email" placeholder="jane@company.co.ke" required />
          <Input label="Job title"        value={form.job_title}    onChange={set('job_title')}    placeholder="e.g. Software Engineer" required />
          <Select label="Department" value={form.department} onChange={set('department')} options={[
            {value:'Engineering',label:'Engineering'},{value:'HR',label:'HR'},
            {value:'Finance',label:'Finance'},{value:'Operations',label:'Operations'},
          ]} />
          <Input label="Basic salary (KES)" value={form.basic_salary} onChange={set('basic_salary')} type="number" placeholder="e.g. 75000" required />
          <Input label="Allowances (KES)"   value={form.allowances}   onChange={set('allowances')}   type="number" placeholder="e.g. 6000" />
          <Select label="Role" value={form.role} onChange={set('role')} options={[
            {value:'employee',label:'Employee'},{value:'admin',label:'Admin'},
          ]} />
          <Select label="Status" value={form.status} onChange={set('status')} options={[
            {value:'active',label:'Active'},{value:'inactive',label:'Inactive'},
          ]} />
        </div>
        <div style={{ display:'flex', gap:8 }}>
          <Btn variant="primary" onClick={handleSubmit} disabled={saving}>{saving ? 'Saving…' : 'Save employee'}</Btn>
          <Btn onClick={() => onNav('employees')}>Cancel</Btn>
        </div>
      </Card>
    </div>
  )
}