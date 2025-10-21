from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import User, AuditLog, RoleEnum
from .forms import UserForm
from . import db
from flask_login import login_required, current_user

bp = Blueprint('admin', __name__)

def require_admin():
    return current_user.is_authenticated and current_user.role.name == "ADMIN"

@bp.route('/users')
@login_required
def users_list():
    if not require_admin():
        flash("Permissão negada", "danger")
        return redirect(url_for('auth.index'))
    users = User.query.all()
    return render_template('users/user_list.html', users=users)

@bp.route('/users/create', methods=['GET','POST'])
@login_required
def create_user():
    if not require_admin():
        flash("Permissão negada", "danger")
        return redirect(url_for('auth.index'))
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("E-mail já cadastrado", "warning")
            return redirect(url_for('admin.users_list'))
        u = User(nome=form.nome.data, email=form.email.data, telefone=form.telefone.data, matricula=form.matricula.data)
        if form.role.data == 'admin':
            u.role = RoleEnum.ADMIN
        elif form.role.data == 'bibliotecario':
            u.role = RoleEnum.BIBLIOTECARIO
        else:
            u.role = RoleEnum.USUARIO
        u.set_password("senha123")
        db.session.add(u)
        db.session.commit()
        db.session.add(AuditLog(actor_id=current_user.id, action="create_user", details=f"user_id={u.id}"))
        db.session.commit()
        flash("Usuário criado com sucesso", "success")
        return redirect(url_for('admin.users_list'))
    return render_template('users/user_form.html', form=form)

@bp.route('/users/block/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    if not require_admin():
        flash("Permissão negada", "danger")
        return redirect(url_for('admin.users_list'))
    u = User.query.get_or_404(user_id)
    u.blocked = True
    db.session.add(AuditLog(actor_id=current_user.id, action="block_user", details=f"user_id={u.id}"))
    db.session.commit()
    flash("Usuário bloqueado", "success")
    return redirect(url_for('admin.users_list'))

@bp.route('/users/unblock/<int:user_id>', methods=['POST'])
@login_required
def unblock_user(user_id):
    if not require_admin():
        flash("Permissão negada", "danger")
        return redirect(url_for('admin.users_list'))
    u = User.query.get_or_404(user_id)
    u.blocked = False
    db.session.add(AuditLog(actor_id=current_user.id, action="unblock_user", details=f"user_id={u.id}"))
    db.session.commit()
    flash("Usuário desbloqueado", "success")
    return redirect(url_for('admin.users_list'))

@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not require_admin():
        return redirect(url_for('admin.users_list'))
    
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('admin.users_list'))
    
    return render_template('users/user_form.html', form=form, user=user)

@bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if not require_admin():
        return redirect(url_for('admin.users_list'))
    
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin.users_list'))
