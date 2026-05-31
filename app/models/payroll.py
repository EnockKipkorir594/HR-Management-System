from app import db
from datetime import datetime
from decimal import Decimal


# ─── Kenyan Statutory Rates (2024) ───────────────────────────────────────────

def compute_shif(gross):
    """SHIF deduction based on gross salary bands (Kenya 2024)."""
    gross = float(gross)
    if gross < 6000:       return 300
    elif gross < 12000:    return 330
    elif gross < 30000:    return 825
    elif gross < 50000:    return 1375
    elif gross < 70000:    return 1925
    elif gross < 100000:   return 2750
    elif gross < 300000:    return 1700
    else: return 27500


def compute_nssf(gross):
    """NSSF Tier I + Tier II deduction (Kenya 2024 — new rates)."""
    gross = float(gross)
    tier1_limit = 7000
    tier2_limit = 36000
    rate = 0.06   # 6% employee contribution
    tier1 = min(gross, tier1_limit) * rate
    tier2 = min(max(gross - tier1_limit, 0), tier2_limit - tier1_limit) * rate
    return round(tier1 + tier2, 2)


def compute_paye(taxable_income):
    """
    PAYE computation using Kenya Revenue Authority (KRA) tax bands 2024.
    Monthly personal relief = KES 2,400
    """
    taxable = float(taxable_income)
    tax = 0.0

    # KRA Monthly Tax Bands
    bands = [
        (24000,  0.10),
        (8333,   0.25),
        (467667, 0.30),
        (float('inf'), 0.35),
    ]

    remaining = taxable
    for band_limit, rate in bands:
        if remaining <= 0:
            break
        taxable_in_band = min(remaining, band_limit)
        tax += taxable_in_band * rate
        remaining -= taxable_in_band

    # Personal Relief
    personal_relief = 2400
    paye = max(tax - personal_relief, 0)
    return round(paye, 2)


# ─── Payroll Record Model ─────────────────────────────────────────────────────

class PayrollRecord(db.Model):
    __tablename__ = 'payroll_records'

    id              = db.Column(db.Integer, primary_key=True)
    employee_id     = db.Column(db.Integer,
                                db.ForeignKey('employees.id'), nullable=False)
    pay_period      = db.Column(db.String(20), nullable=False)  # e.g. 2024-01
    pay_date        = db.Column(db.Date, nullable=False)

    # Earnings
    basic_salary    = db.Column(db.Numeric(12, 2), default=0)
    house_allowance = db.Column(db.Numeric(12, 2), default=0)
    transport_allow = db.Column(db.Numeric(12, 2), default=0)
    overtime_pay    = db.Column(db.Numeric(12, 2), default=0)
    bonus           = db.Column(db.Numeric(12, 2), default=0)
    gross_pay       = db.Column(db.Numeric(12, 2), default=0)

    # Statutory Deductions
    paye            = db.Column(db.Numeric(12, 2), default=0)
    nhif            = db.Column(db.Numeric(12, 2), default=0)
    nssf            = db.Column(db.Numeric(12, 2), default=0)

    # Other Deductions
    loan_deduction  = db.Column(db.Numeric(12, 2), default=0)
    other_deduction = db.Column(db.Numeric(12, 2), default=0)
    total_deductions = db.Column(db.Numeric(12, 2), default=0)

    # Net Pay
    net_pay         = db.Column(db.Numeric(12, 2), default=0)

    status          = db.Column(db.String(20), default='draft')
    # statuses: draft | approved | paid
    notes           = db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at    = db.Column(db.DateTime)

    @classmethod
    def generate_for_employee(cls, employee, pay_period, pay_date,
                               overtime=0, bonus=0,
                               loan_deduction=0, other_deduction=0):
        """
        Auto-compute a full payroll record for one employee.
        Applies Kenyan statutory deductions automatically.
        """
        # ── Earnings
        basic    = float(employee.basic_salary or 0)
        house    = float(employee.house_allowance or 0)
        transport = float(employee.transport_allow or 0)
        overtime = float(overtime)
        bonus    = float(bonus)
        gross    = basic + house + transport + overtime + bonus

        # ── Statutory deductions (only if eligible)
        nhif = compute_shif(gross) if employee.nhif_eligible else 0
        nssf = compute_nssf(gross) if employee.nssf_eligible else 0

        # Taxable income = gross minus NSSF (NSSF is pre-tax relief)
        taxable_income = max(gross - nssf, 0)
        paye = compute_paye(taxable_income)

        # ── Total deductions and net pay
        total_deductions = nhif + nssf + paye + float(loan_deduction) + \
                           float(other_deduction)
        net_pay = gross - total_deductions

        record = cls(
            employee_id      = employee.id,
            pay_period       = pay_period,
            pay_date         = pay_date,
            basic_salary     = round(basic, 2),
            house_allowance  = round(house, 2),
            transport_allow  = round(transport, 2),
            overtime_pay     = round(overtime, 2),
            bonus            = round(bonus, 2),
            gross_pay        = round(gross, 2),
            paye             = round(paye, 2),
            nhif             = round(nhif, 2),
            nssf             = round(nssf, 2),
            loan_deduction   = round(float(loan_deduction), 2),
            other_deduction  = round(float(other_deduction), 2),
            total_deductions = round(total_deductions, 2),
            net_pay          = round(net_pay, 2),
        )
        return record

    def __repr__(self):
        return (f'<Payroll emp={self.employee_id} '
                f'period={self.pay_period} net={self.net_pay}>')