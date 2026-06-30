export type Role = 'admin' | 'employee'

export interface AuthUser {
  access_token: string
  user_id: number
  name: string
  initials: string
  role: Role
  employee_id: number
}

export interface Employee {
  id: number
  name: string
  department: string
  job_title: string
  basic_salary: number
  allowances: number
  status: 'active' | 'inactive'
  role: Role
  email: string
}

export interface AttendanceRecord {
  employee_id: number
  month: string
  day: number
  status: 'present' | 'absent' | 'leave' | 'off'
}

export interface PayrollRecord {
  id: number
  employee_id: number
  employee_name: string
  month: string
  basic_salary: number
  allowances: number
  gross_pay: number
  paye: number
  nhif: number
  nssf: number
  net_pay: number
  status: 'processed' | 'pending'
}

export interface Payslip {
  reference: string
  pay_period: string
  employee_id: number
  employee_name: string
  job_title: string
  department: string
  email: string
  basic_salary: number
  house_allowance: number
  transport_allowance: number
  gross_pay: number
  paye: number
  nhif: number
  nssf: number
  total_deductions: number
  net_pay: number
  payment_method: string
  status: string
}