from flask import Blueprint, render_template
from .models import AuditLog
from flask_login import login_required

bp = Blueprint('reports', __name__)

@bp.route('/audit')
@login_required
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(200).all()
    return render_template('reports/report_preview.html', logs=logs)
