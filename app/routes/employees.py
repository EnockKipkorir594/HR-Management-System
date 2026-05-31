from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.employees import Employee, LeaveRecord
from app import db
from datetime import datetime, date

employees_bp = Blueprint('employees', __name__)


def hr_required(f):
    """Decorator — HR managers and admins only."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_hr():
            flash('HR access required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


@employees_bp.route('/')
@login_required
def list_employees():
    search = request.args.get('search', '').strip()
    dept   = request.args.get('dept', '')
    page   = request.args.get('page', 1, type=int)

    query = Employee.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            db.or_(
                Employee.first_name.ilike(f'%{search}%'),
                Employee.last_name.ilike(f'%{search}%'),
                Employee.employee_number.ilike(f'%{search}%'),
                Employee.email.ilike(f'%{search}%'),
            )
        )
    if dept:
        query = query.filter_by(department=dept)

    employees = query.order_by(Employee.first_name).paginate(
        page=page, per_page=15, error_out=False
    )

    departments = db.session.query(Employee.department).distinct().all()
    departments = [d[0] for d in departments]

    return render_template('employees/list.html',
        employees=employees, departments=departments,
        search=search, selected_dept=dept
    )


@employees_bp.route('/add', methods=['GET', 'POST'])
@login_required
@hr_required
def add_employee():
    if request.method == 'POST':
        try:
            # Auto-generate employee number
            last = Employee.query.order_by(Employee.id.desc()).first()
            new_id = (last.id + 1) if last else 1
            emp_number = f'EMP{new_id:04d}'

            emp = Employee(
                employee_number = emp_number,
                first_name      = request.form['first_name'].strip(),
                last_name       = request.form['last_name'].strip(),
                email           = request.form['email'].strip(),
                phone           = request.form.get('phone', '').strip(),
                national_id     = request.form.get('national_id', '').strip(),
                gender          = request.form.get('gender'),
                department      = request.form['department'].strip(),
                job_title       = request.form['job_title'].strip(),
                employment_type = request.form.get('employment_type', 'full_time'),
                date_hired      = datetime.strptime(
                                    request.form['date_hired'], '%Y-%m-%d').date(),
                basic_salary    = float(request.form.get('basic_salary', 0)),
                house_allowance = float(request.form.get('house_allowance', 0)),
                transport_allow = float(request.form.get('transport_allow', 0)),
            )
            db.session.add(emp)
            db.session.commit()
            flash(f'Employee {emp.full_name} added successfully '
                  f'({emp_number}).', 'success')
            return redirect(url_for('employees.list_employees'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error adding employee: {str(e)}', 'danger')

    return render_template('employees/add.html')


@employees_bp.route('/<int:emp_id>')
@login_required
def detail(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    payroll_history = (emp.payroll_records
                       .order_by(db.text('pay_period DESC'))
                       .limit(12).all())
    leave_history = (emp.leave_records
                     .order_by(db.text('start_date DESC'))
                     .limit(10).all())
    return render_template('employees/detail.html',
                           emp=emp,
                           payroll_history=payroll_history,
                           leave_history=leave_history)


@employees_bp.route('/<int:emp_id>/edit', methods=['GET', 'POST'])
@login_required
@hr_required
def edit_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)

    if request.method == 'POST':
        try:
            emp.first_name      = request.form['first_name'].strip()
            emp.last_name       = request.form['last_name'].strip()
            emp.email           = request.form['email'].strip()
            emp.phone           = request.form.get('phone', '').strip()
            emp.department      = request.form['department'].strip()
            emp.job_title       = request.form['job_title'].strip()
            emp.basic_salary    = float(request.form.get('basic_salary', 0))
            emp.house_allowance = float(request.form.get('house_allowance', 0))
            emp.transport_allow = float(request.form.get('transport_allow', 0))
            emp.updated_at      = datetime.utcnow()

            db.session.commit()
            flash('Employee record updated.', 'success')
            return redirect(url_for('employees.detail', emp_id=emp.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Update failed: {str(e)}', 'danger')

    return render_template('employees/add.html', emp=emp, editing=True)


@employees_bp.route('/<int:emp_id>/deactivate', methods=['POST'])
@login_required
@hr_required
def deactivate(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    emp.is_active       = False
    emp.date_terminated = date.today()
    db.session.commit()
    flash(f'{emp.full_name} has been deactivated.', 'warning')
    return redirect(url_for('employees.list_employees'))


@employees_bp.route('/<int:emp_id>/leave', methods=['POST'])
@login_required
@hr_required
def add_leave(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    try:
        start = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end   = datetime.strptime(request.form['end_date'],   '%Y-%m-%d').date()
        days  = (end - start).days + 1

        leave = LeaveRecord(
            employee_id = emp.id,
            leave_type  = request.form['leave_type'],
            start_date  = start,
            end_date    = end,
            days_taken  = days,
            status      = request.form.get('status', 'pending'),
            notes       = request.form.get('notes', ''),
        )
        db.session.add(leave)
        db.session.commit()
        flash(f'Leave record added for {emp.full_name}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('employees.detail', emp_id=emp_id))