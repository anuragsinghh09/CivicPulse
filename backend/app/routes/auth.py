from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/public/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        password = request.form.get('password') or ''

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            if user.role == 'Admin':
                flash('Administrators must use the dedicated admin login.', 'warning')
                return redirect(url_for('admin.login'))

            login_user(user)
            return redirect(url_for('citizen.dashboard'))

        flash('Invalid email or password.', 'danger')
        return render_template('auth/login.html', active_role='public', current_page='login')

    return render_template('auth/login.html', active_role='public', current_page='login')


@auth_bp.route('/public/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = (request.form.get('full_name') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        email = (request.form.get('email') or '').strip()
        password = request.form.get('password') or ''

        if not full_name or not phone or not email or not password:
            flash('All registration fields are required.', 'warning')
            return render_template('auth/register.html', active_role='public', current_page='register')

        if len(password) < 8:
            flash('Password must contain at least 8 characters.', 'warning')
            return render_template('auth/register.html', active_role='public', current_page='register')

        if User.query.filter_by(email=email).first():
            flash('This email address is already registered.', 'warning')
            return render_template('auth/register.html', active_role='public', current_page='register')

        user = User(
            full_name=full_name,
            phone=phone,
            email=email,
            password_hash=generate_password_hash(password),
            role='Citizen',
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', active_role='public', current_page='register')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.home'))
