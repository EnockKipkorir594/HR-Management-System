from flask import (Blueprint, render_template, redirect,
                   url_for, flash, request, make_response)
from flask_login import login_required, current_user
from app.models.employees import Employee
from app.models.payroll import PayrollRecord
from app import db
from datetime import datetime, date
from sqlalchemy import func

payroll_bp = Blueprint('payroll', __name__)


def hr_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_hr():
            flash('HR access required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


@payroll_bp.route('/')
@login_required
def list_payroll():
    period = request.args.get('period', datetime.utcnow().strftime('%Y-%m'))
    page   = request.args.get('page', 1, type=int)

    records = (PayrollRecord.query
               .filter_by(pay_period=period)
               .join(Employee)
               .order_by(Employee.first_name)
               .paginate(page=page, per_page=20, error_out=False))

    # Period summary
    summary = db.session.query(
        func.count(PayrollRecord.id).label('count'),
        func.sum(PayrollRecord.gross_pay).label('total_gross'),
        func.sum(PayrollRecord.total_deductions).label('total_deductions'),
        func.sum(PayrollRecord.net_pay).label('total_net'),
    ).filter_by(pay_period=period).first()

    return render_template('payroll/list.html',
                           records=records, period=period, summary=summary)


@payroll_bp.route('/run', methods=['GET', 'POST'])
@login_required
@hr_required
def run_payroll():
    """Process payroll for all active employees for a given period."""
    if request.method == 'POST':
        period   = request.form.get('pay_period')     # e.g. 2024-01
        pay_date = request.form.get('pay_date')

        if not period or not pay_date:
            flash('Pay period and pay date are required.', 'danger')
            return redirect(url_for('payroll.run_payroll'))

        pay_date = datetime.strptime(pay_date, '%Y-%m-%d').date()

        # Check if payroll already processed for this period
        existing = PayrollRecord.query.filter_by(pay_period=period).first()
        if existing:
            flash(f'Payroll for {period} has already been processed.', 'warning')
            return redirect(url_for('payroll.list_payroll', period=period))

        employees = Employee.query.filter_by(is_active=True).all()
        if not employees:
            flash('No active employees found.', 'warning')
            return redirect(url_for('payroll.run_payroll'))

        processed = 0
        errors    = 0

        for emp in employees:
            try:
                record = PayrollRecord.generate_for_employee(
                    employee        = emp,
                    pay_period      = period,
                    pay_date        = pay_date,
                    overtime        = 0,
                    bonus           = 0,
                    loan_deduction  = 0,
                    other_deduction = 0,
                )
                db.session.add(record)
                processed += 1
            except Exception as e:
                errors += 1

        db.session.commit()
        flash(f'Payroll processed for {processed} employees '
              f'({errors} errors) — period {period}.', 'success')
        return redirect(url_for('payroll.list_payroll', period=period))

    return render_template('payroll/run.html',
                           today=date.today().strftime('%Y-%m-%d'))


@payroll_bp.route('/<int:record_id>/approve', methods=['POST'])
@login_required
@hr_required
def approve(record_id):
    record = PayrollRecord.query.get_or_404(record_id)
    record.status       = 'approved'
    record.processed_at = datetime.utcnow()
    db.session.commit()
    flash('Payroll record approved.', 'success')
    return redirect(url_for('payroll.list_payroll',
                            period=record.pay_period))


@payroll_bp.route('/<int:record_id>/payslip')
@login_required
def payslip(record_id):
    record = PayrollRecord.query.get_or_404(record_id)
    emp    = Employee.query.get_or_404(record.employee_id)

    # Employees can only view their own payslip
    if current_user.role == 'employee':
        if emp.email != current_user.email:
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard.index'))

    return render_template('payroll/payslip.html', record=record, emp=emp)