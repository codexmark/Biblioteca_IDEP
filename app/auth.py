from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, ChangePasswordForm
from .models import User, AuditLog
from . import db
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            db.session.add(AuditLog(actor_id=user.id if user else None, action="login_failed", details=f"email={form.email.data}"))
            db.session.commit()
            flash("Credenciais inválidas", "danger")
            return redirect(url_for('auth.login'))
        if not user.active or user.blocked:
            flash("Conta inativa ou bloqueada. Contate o administrador.", "danger")
            return redirect(url_for('auth.login'))
        login_user(user)
        db.session.add(AuditLog(actor_id=user.id, action="login_success", details="login efetuado"))
        db.session.commit()
        return redirect(url_for('auth.index'))
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    db.session.add(AuditLog(actor_id=current_user.id, action="logout", details="logout efetuado"))
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Senha atual inválida", "danger")
            return redirect(url_for('auth.change_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        db.session.add(AuditLog(actor_id=current_user.id, action="change_password", details="senha alterada"))
        db.session.commit()
        flash("Senha alterada com sucesso", "success")
        return redirect(url_for('auth.index'))
    return render_template('change_password.html', form=form)
