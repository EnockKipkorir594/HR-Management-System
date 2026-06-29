import { ReactNode, CSSProperties } from 'react'

// ── Badge ────────────────────────────────────────────────────────────────────
type BadgeV = 'active'|'inactive'|'admin'|'employee'|'present'|'absent'|'leave'|'off'|'processed'|'pending'
const BS: Record<BadgeV, CSSProperties> = {
  active:    { background:'#EAF3DE', color:'#27500A', border:'0.5px solid #97C459' },
  inactive:  { background:'#F1EFE8', color:'#5F5E5A', border:'0.5px solid #E5E4DE' },
  admin:     { background:'#E6F1FB', color:'#0C447C', border:'0.5px solid #85B7EB' },
  employee:  { background:'#EEEDFE', color:'#534AB7', border:'0.5px solid #AFA9EC' },
  present:   { background:'#EAF3DE', color:'#27500A', border:'0.5px solid #97C459' },
  absent:    { background:'#FCEBEB', color:'#791F1F', border:'0.5px solid #F09595' },
  leave:     { background:'#FAEEDA', color:'#854F0B', border:'0.5px solid #EF9F27' },
  off:       { background:'#F1EFE8', color:'#888780', border:'0.5px solid #E5E4DE' },
  processed: { background:'#EAF3DE', color:'#27500A', border:'0.5px solid #97C459' },
  pending:   { background:'#FAEEDA', color:'#854F0B', border:'0.5px solid #EF9F27' },
}

export function Badge({ v, label }: { v: BadgeV; label?: string }) {
  return (
    <span style={{ ...BS[v], display:'inline-block', padding:'2px 9px', borderRadius:99, fontSize:11, fontWeight:500 }}>
      {label ?? v.charAt(0).toUpperCase() + v.slice(1)}
    </span>
  )
}

// ── Button ────────────────────────────────────────────────────────────────────
interface BtnProps {
  children: ReactNode
  onClick?: () => void
  variant?: 'primary'|'secondary'|'danger'|'success'
  disabled?: boolean
  size?: 'sm'|'md'
  type?: 'button'|'submit'
  fullWidth?: boolean
}
export function Btn({ children, onClick, variant='secondary', disabled, size='md', type='button', fullWidth }: BtnProps) {
  const base: CSSProperties = {
    display:'inline-flex', alignItems:'center', justifyContent:'center', gap:6,
    borderRadius:'var(--r)', fontWeight:500, cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.6 : 1, border:'none', transition:'opacity .1s',
    width: fullWidth ? '100%' : undefined,
    padding: size === 'sm' ? '5px 12px' : '8px 16px',
    fontSize: size === 'sm' ? 12 : 13,
  }
  const variants: Record<string, CSSProperties> = {
    primary:   { background:'#185FA5', color:'#fff' },
    secondary: { background:'transparent', color:'#5F5E5A', border:'0.5px solid #D3D1C7' },
    danger:    { background:'#FCEBEB', color:'#791F1F', border:'0.5px solid #F09595' },
    success:   { background:'#EAF3DE', color:'#27500A', border:'0.5px solid #97C459' },
  }
  return (
    <button type={type} onClick={onClick} disabled={disabled} style={{ ...base, ...variants[variant] }}>
      {children}
    </button>
  )
}

// ── Card ─────────────────────────────────────────────────────────────────────
export function Card({ children, style }: { children: ReactNode; style?: CSSProperties }) {
  return (
    <div style={{
      background: '#fff', border: '0.5px solid #E5E4DE',
      borderRadius: 10, padding: '18px 20px', ...style,
    }}>
      {children}
    </div>
  )
}

export function CardHeader({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:16 }}>
      <span style={{ fontSize:14, fontWeight:500 }}>{title}</span>
      {children}
    </div>
  )
}

// ── Spinner ───────────────────────────────────────────────────────────────────
export function Spinner() {
  return (
    <div style={{ display:'flex', alignItems:'center', justifyContent:'center', padding:40 }}>
      <div style={{
        width:28, height:28, borderRadius:'50%',
        border:'2.5px solid #E5E4DE', borderTopColor:'#185FA5',
        animation:'spin 0.7s linear infinite',
      }} />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  )
}

// ── Input ─────────────────────────────────────────────────────────────────────
interface InputProps {
  label: string
  value: string | number
  onChange: (v: string) => void
  type?: string
  placeholder?: string
  required?: boolean
  error?: string
}
export function Input({ label, value, onChange, type='text', placeholder, required, error }: InputProps) {
  return (
    <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
      <label style={{ fontSize:12, fontWeight:500, color:'#5F5E5A' }}>
        {label}{required && <span style={{ color:'#A32D2D' }}> *</span>}
      </label>
      <input
        type={type} value={value} onChange={e => onChange(e.target.value)}
        placeholder={placeholder} required={required}
        style={{
          padding:'8px 10px', fontSize:13, border:`0.5px solid ${error ? '#F09595' : '#D3D1C7'}`,
          borderRadius:'var(--r)', background:'#fff', color:'var(--text)', outline:'none',
        }}
      />
      {error && <span style={{ fontSize:11, color:'#A32D2D' }}>{error}</span>}
    </div>
  )
}

export function Select({ label, value, onChange, options, required }: {
  label: string; value: string; onChange: (v: string) => void
  options: { value: string; label: string }[]; required?: boolean
}) {
  return (
    <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
      <label style={{ fontSize:12, fontWeight:500, color:'#5F5E5A' }}>
        {label}{required && <span style={{ color:'#A32D2D' }}> *</span>}
      </label>
      <select value={value} onChange={e => onChange(e.target.value)} style={{
        padding:'8px 10px', fontSize:13, border:'0.5px solid #D3D1C7',
        borderRadius:'var(--r)', background:'#fff', color:'var(--text)', outline:'none',
      }}>
        {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </div>
  )
}

// ── Alert ─────────────────────────────────────────────────────────────────────
export function Alert({ msg, type='error' }: { msg: string; type?: 'error'|'info'|'success' }) {
  const s: Record<string, CSSProperties> = {
    error:   { background:'#FCEBEB', color:'#791F1F', border:'0.5px solid #F09595' },
    info:    { background:'#E6F1FB', color:'#0C447C', border:'0.5px solid #85B7EB' },
    success: { background:'#EAF3DE', color:'#27500A', border:'0.5px solid #97C459' },
  }
  return <div style={{ ...s[type], padding:'9px 13px', borderRadius:'var(--r)', fontSize:12, marginBottom:14 }}>{msg}</div>
}

// ── Empty state ───────────────────────────────────────────────────────────────
export function Empty({ msg }: { msg: string }) {
  return <div style={{ padding:'32px 0', textAlign:'center', color:'#888780', fontSize:13 }}>{msg}</div>
}