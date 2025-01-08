from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from bloom.models.user import User
from bloom import db
from bloom.forms import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('portfolio.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title="Register", form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("portfolio.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password", "error")
            return redirect(url_for("auth.login"))

        login_user(user)
        # next_page = request.args.get('next')
        # print(f"Request: {request.args}")
        # print(f"Next page: {next_page}")
        # if next_page:
        #     return redirect(next_page)
        flash("Logged in successfully", "success")
        return redirect(url_for("portfolio.home"))
    return render_template('auth/login.html', title="Login", form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))