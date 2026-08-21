from flask import Blueprint, redirect, render_template, url_for

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    return redirect(url_for('public.home'))


@public_bp.route('/public/home')
def home():
    return render_template('public/home.html', active_role='public', current_page='home')


@public_bp.route('/public/about')
def about():
    return render_template('public/about.html', active_role='public', current_page='about')




