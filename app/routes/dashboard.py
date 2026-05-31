from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.employees import Employee
from app.models.payroll import PayrollRecord
from app.models.users import User
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    # Summary stats
    total_employees  = Employee.query.filter_by(is_active=True).count()
    total_users      = User.query.filter_by(is_active=True).count()

    current_period   = datetime.utcnow().strftime('%Y-%m')
    payroll_this_month = PayrollRecord.query.filter_by(
        pay_period=current_period
    ).count()

    # Total net pay disbursed this month
    from sqlalchemy import func
    monthly_total = PayrollRecord.query.filter_by(
        pay_period=current_period, status='paid'
    ).with_entities(func.sum(PayrollRecord.net_pay)).scalar() or 0

    # Recent payroll records
    recent_payroll = (PayrollRecord.query
                      .order_by(PayrollRecord.created_at.desc())
                      .limit(5).all())

    # Department breakdown
    from app import db
    dept_stats = (db.session.query(
                      Employee.department,
                      func.count(Employee.id).label('count')
                  )
                  .filter_by(is_active=True)
                  .group_by(Employee.department)
                  .all())

    return render_template('dashboard/index.html',
        total_employees   = total_employees,
        total_users       = total_users,
        payroll_this_month = payroll_this_month,
        monthly_total     = monthly_total,
        recent_payroll    = recent_payroll,
        dept_stats        = dept_stats,
        current_period    = current_period,
    )