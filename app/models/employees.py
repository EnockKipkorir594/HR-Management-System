from app import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employees'

    id              = db.Column(db.Integer, primary_key=True)
    employee_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name      = db.Column(db.String(80), nullable=False)
    last_name       = db.Column(db.String(80), nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    phone           = db.Column(db.String(20))
    national_id     = db.Column(db.String(20), unique=True)
    date_of_birth   = db.Column(db.Date)
    gender          = db.Column(db.String(10))

    # Employment details
    department      = db.Column(db.String(100), nullable=False)
    job_title       = db.Column(db.String(100), nullable=False)
    employment_type = db.Column(db.String(20), default='full_time')
    # types: full_time | part_time | contract | casual
    date_hired      = db.Column(db.Date, nullable=False)
    date_terminated = db.Column(db.Date)
    is_active       = db.Column(db.Boolean, default=True)

    # Salary
    basic_salary    = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    house_allowance = db.Column(db.Numeric(12, 2), default=0)
    transport_allow = db.Column(db.Numeric(12, 2), default=0)

    # Statutory — Kenyan context (NHIF, NSSF, PAYE)
    nhif_eligible   = db.Column(db.Boolean, default=True)
    nssf_eligible   = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow,
                                onupdate=datetime.utcnow)

    # Relationships
    payroll_records = db.relationship('PayrollRecord', backref='employee',
                                      lazy='dynamic')
    leave_records   = db.relationship('LeaveRecord', backref='employee',
                                      lazy='dynamic')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def gross_salary(self):
        return float(self.basic_salary or 0) + \
               float(self.house_allowance or 0) + \
               float(self.transport_allow or 0)

    def __repr__(self):
        return f'<Employee {self.employee_number} — {self.full_name}>'


class LeaveRecord(db.Model):
    __tablename__ = 'leave_records'

    id          = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'),
                            nullable=False)
    leave_type  = db.Column(db.String(30), nullable=False)
    # types: annual | sick | maternity | paternity | unpaid
    start_date  = db.Column(db.Date, nullable=False)
    end_date    = db.Column(db.Date, nullable=False)
    days_taken  = db.Column(db.Integer, nullable=False)
    status      = db.Column(db.String(20), default='pending')
    # statuses: pending | approved | rejected
    notes       = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Leave {self.employee_id} {self.leave_type} {self.status}>'