from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Assignment, Category, Complaint, Department, Feedback, StatusHistory, User

admin_bp = Blueprint('admin', __name__)


def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'Admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('public.home'))
        return func(*args, **kwargs)

    return wrapper


@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('admin-email') or '').strip()
        password = request.form.get('admin-password') or ''

        user = User.query.filter_by(email=email).first()
        if user and user.role == 'Admin' and user.password_hash:
            from werkzeug.security import check_password_hash

            if check_password_hash(user.password_hash, password):
                from flask_login import login_user

                login_user(user)
                return redirect(url_for('admin.dashboard'))

        flash('Invalid admin credentials.', 'danger')
        return render_template('admin/login.html', active_role='public', current_page='login')

    return render_template('admin/login.html', active_role='public', current_page='login')


@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('admin/dashboard.html', active_role='admin', current_page='admin_dashboard', complaints=complaints)


@admin_bp.route('/admin/complaints')
@admin_required
def complaints():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('admin/complaints.html', active_role='admin', current_page='admin_complaints', complaints=complaints)


@admin_bp.route('/admin/complaint-detail')
@admin_required
def complaint_detail_default():
    complaint = Complaint.query.order_by(Complaint.created_at.desc()).first()
    if complaint is None:
        flash('No complaints found.', 'warning')
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.complaint_detail', complaint_id=complaint.complaint_id))


@admin_bp.route('/admin/complaint-detail/<int:complaint_id>', methods=['GET', 'POST'])
@admin_required
def complaint_detail(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    departments = Department.query.filter_by(is_active=True).order_by(Department.name).all()
    if request.method == 'POST':
        from ..services.complaint_service import update_complaint_status

        status = request.form.get('status') or request.form.get('decision')
        priority = request.form.get('priority')
        department_id = request.form.get('department')
        assigned_to = request.form.get('assignedTo') or request.form.get('assigned_to')
        note = request.form.get('note') or ''

        try:
            if priority:
                if priority not in {'Low', 'Medium', 'High', 'Critical'}:
                    raise ValueError('Invalid priority value.')
                complaint.priority = priority

            if status == 'Assigned' or (department_id and assigned_to):
                if complaint.status != 'Verified':
                    raise ValueError('A complaint must be verified before assignment.')
                if not department_id or not assigned_to.strip():
                    raise ValueError('Department and assigned-to are required for assignment.')
                dept = db.session.get(Department, department_id)
                if dept is None or not dept.is_active:
                    raise ValueError('Department not found.')
                db.session.add(Assignment(
                    complaint_id=complaint.complaint_id,
                    department_id=dept.department_id,
                    assigned_to=assigned_to.strip(),
                    assigned_by=current_user.user_id,
                ))
                complaint = update_complaint_status(complaint, 'Assigned', current_user.user_id, note or 'Department assignment recorded.')
            elif status:
                complaint = update_complaint_status(complaint, status, current_user.user_id, note)
            else:
                db.session.commit()
        except ValueError as error:
            db.session.rollback()
            flash(str(error), 'warning')
            return render_template('admin/complaint_detail.html', active_role='admin', current_page='admin_complaints', complaint=complaint, departments=departments)

        flash('Complaint updated successfully.', 'success')
        return redirect(url_for('admin.complaint_detail', complaint_id=complaint.complaint_id))

    return render_template('admin/complaint_detail.html', active_role='admin', current_page='admin_complaints', complaint=complaint, departments=departments)


@admin_bp.route('/admin/categories')
@admin_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', active_role='admin', current_page='categories', categories=categories)


@admin_bp.route('/admin/departments')
@admin_required
def departments():
    departments = Department.query.order_by(Department.name).all()
    return render_template('admin/departments.html', active_role='admin', current_page='departments', departments=departments)


@admin_bp.route('/logout')
def logout():
    from flask_login import logout_user

    logout_user()
    return redirect(url_for('public.home'))
