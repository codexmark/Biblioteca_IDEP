from flask import flash
from flask_login import current_user

def require_bibliotecario():
    if not current_user.is_authenticated or current_user.role.name not in ("BIBLIOTECARIO", "ADMIN"):
        flash("Permissão negada", "danger")
        return False
    return True