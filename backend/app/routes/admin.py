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
    if request.method == 'POST':
        from ..services.complaint_service import update_complaint_status

        status = request.form.get('status') or request.form.get('decision')
        priority = request.form.get('priority')
        department_id = request.form.get('department')
        assigned_to = request.form.get('assignedTo') or request.form.get('assigned_to')
        note = request.form.get('note') or ''

        if status:
            complaint = update_complaint_status(complaint, status, current_user.user_id, note)
        if priority:
            complaint.priority = priority
        if department_id and assigned_to:
            dept = Department.query.get(department_id)
            if dept is None:
                flash('Department not found.', 'warning')
                return render_template('admin/complaint_detail.html', active_role='admin', current_page='admin_complaints', complaint=complaint)
            assignment = Assignment(
                complaint_id=complaint.complaint_id,
                department_id=dept.department_id,
                assigned_to=assigned_to,
                assigned_by=current_user.user_id,
            )
            db.session.add(assignment)
            complaint.status = 'Assigned'
            complaint.updated_at = db.func.current_timestamp()
            db.session.add(StatusHistory(
                complaint_id=complaint.complaint_id,
                previous_status=complaint.status,
                new_status='Assigned',
                changed_by=current_user.user_id,
                note='Department assignment updated.',
            ))
        db.session.commit()
        flash('Complaint updated successfully.', 'success')
        return redirect(url_for('admin.complaint_detail', complaint_id=complaint.complaint_id))

    return render_template('admin/complaint_detail.html', active_role='admin', current_page='admin_complaints', complaint=complaint)


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
