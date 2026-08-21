from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Category, Complaint, Feedback, Location, StatusHistory, User

citizen_bp = Blueprint('citizen', __name__)


def citizen_required(func):
    from functools import wraps

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'Citizen':
            flash('Citizen access required.', 'danger')
            return redirect(url_for('public.home'))
        return func(*args, **kwargs)

    return wrapper


@citizen_bp.route('/citizen/dashboard')
@citizen_required
def dashboard():
    complaints = Complaint.query.filter_by(citizen_id=current_user.user_id).order_by(Complaint.created_at.desc()).all()
    return render_template('citizen/dashboard.html', active_role='citizen', current_page='citizen_dashboard', complaints=complaints)


@citizen_bp.route('/citizen/complaint-form', methods=['GET', 'POST'])
@citizen_required
def complaint_form():
    categories = Category.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        from ..services.complaint_service import create_complaint

        complaint = create_complaint(current_user.user_id, request.form, request.files)
        if complaint is None:
            flash('Please check the complaint details and upload no more than 3 valid images.', 'warning')
            return render_template('citizen/complaint_form.html', active_role='citizen', current_page='complaint_form', categories=categories)
        flash('Complaint submitted successfully.', 'success')
        return redirect(url_for('citizen.complaints'))

    return render_template('citizen/complaint_form.html', active_role='citizen', current_page='complaint_form', categories=categories)


@citizen_bp.route('/citizen/complaints')
@citizen_required
def complaints():
    complaints = Complaint.query.filter_by(citizen_id=current_user.user_id).order_by(Complaint.created_at.desc()).all()
    return render_template('citizen/complaints.html', active_role='citizen', current_page='complaints', complaints=complaints)


@citizen_bp.route('/citizen/complaint-details')
@citizen_required
def complaint_details_default():
    complaint = Complaint.query.filter_by(citizen_id=current_user.user_id).order_by(Complaint.created_at.desc()).first()
    if not complaint:
        flash('No complaints available.', 'warning')
        return redirect(url_for('citizen.dashboard'))
    return redirect(url_for('citizen.complaint_detail', complaint_id=complaint.complaint_id))


@citizen_bp.route('/citizen/complaint-details/<int:complaint_id>')
@citizen_required
def complaint_detail(complaint_id):
    complaint = Complaint.query.filter_by(complaint_id=complaint_id, citizen_id=current_user.user_id).first_or_404()
    return render_template('citizen/complaint_details.html', active_role='citizen', current_page='complaints', complaint=complaint)


@citizen_bp.route('/citizen/profile', methods=['GET', 'POST'])
@citizen_required
def profile():
    if request.method == 'POST':
        full_name = (request.form.get('full_name') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        email = (request.form.get('email') or '').strip()

        if not full_name or not phone or not email:
            flash('Profile fields are required.', 'warning')
            return render_template('citizen/profile.html', active_role='citizen', current_page='profile', user=current_user)

        if User.query.filter(User.email == email, User.user_id != current_user.user_id).first():
            flash('This email is already in use.', 'warning')
            return render_template('citizen/profile.html', active_role='citizen', current_page='profile', user=current_user)

        current_user.full_name = full_name
        current_user.phone = phone
        current_user.email = email
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('citizen.profile'))

    return render_template('citizen/profile.html', active_role='citizen', current_page='profile', user=current_user)


@citizen_bp.route('/citizen/feedback-form/<int:complaint_id>', methods=['GET', 'POST'])
@citizen_required
def feedback_form(complaint_id):
    complaint = Complaint.query.filter_by(complaint_id=complaint_id, citizen_id=current_user.user_id).first_or_404()
    if complaint.status != 'Resolved':
        flash('Feedback is only available for resolved complaints.', 'warning')
        return redirect(url_for('citizen.complaint_detail', complaint_id=complaint_id))
    if complaint.feedback is not None:
        flash('A feedback record already exists for this complaint.', 'warning')
        return redirect(url_for('citizen.complaint_detail', complaint_id=complaint_id))

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = (request.form.get('comment') or '').strip()
        if not rating or not comment:
            flash('Rating and comment are required.', 'warning')
            return render_template('citizen/feedback_form.html', active_role='citizen', current_page='complaints', complaint=complaint)
        try:
            rating_value = int(rating)
        except ValueError:
            flash('Rating must be a whole number between 1 and 5.', 'warning')
            return render_template('citizen/feedback_form.html', active_role='citizen', current_page='complaints', complaint=complaint)
        if rating_value < 1 or rating_value > 5:
            flash('Rating must be between 1 and 5.', 'warning')
            return render_template('citizen/feedback_form.html', active_role='citizen', current_page='complaints', complaint=complaint)

        feedback = Feedback(complaint_id=complaint.complaint_id, rating=rating_value, comment=comment)
        db.session.add(feedback)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Feedback could not be submitted.', 'danger')
            return render_template('citizen/feedback_form.html', active_role='citizen', current_page='complaints', complaint=complaint)
        flash('Feedback submitted successfully.', 'success')
        return redirect(url_for('citizen.complaint_detail', complaint_id=complaint_id))

    return render_template('citizen/feedback_form.html', active_role='citizen', current_page='complaints', complaint=complaint)
