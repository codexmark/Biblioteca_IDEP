from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file
from .models import Book, Loan, User, AuditLog, LoanStatus 
from . import db
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.utils import require_bibliotecario

bp = Blueprint('loans', __name__)

@bp.route('/')
@login_required
def list_loans():
    page = request.args.get('page',1,type=int)
    q = Loan.query.order_by(Loan.data_emprestimo.desc())
    pag = q.paginate(page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    return render_template('loans/loan_list.html', pag=pag)

@bp.route('/create', methods=['GET','POST'])
@login_required
def create_loan():
    if current_user.role.name not in ("BIBLIOTECARIO", "ADMIN"):
        flash("Permissão negada", "danger")
        return redirect(url_for('loans.list_loans'))
    if request.method == "POST":
        book_id = int(request.form.get('book_id'))
        user_id = int(request.form.get('user_id'))
        book = Book.query.get(book_id)
        user = User.query.get(user_id)
        if not book or book.quantidade <= 0:
            flash("Livro indisponível", "danger")
            return redirect(url_for('books.list_books'))
        if user.blocked:
            flash("Usuário bloqueado", "danger")
            return redirect(url_for('loans.list_loans'))
        book.quantidade -= 1
        loan = Loan(
            book_id=book.id,
            user_id=user.id,
            data_devolucao_prevista = datetime.utcnow() + timedelta(days=14)
        )
        db.session.add(loan)
        db.session.add(AuditLog(actor_id=current_user.id, action="create_loan", details=f"loan_id={loan.id}"))
        db.session.commit()
        flash("Empréstimo registrado", "success")
        return redirect(url_for('loans.list_loans'))
    books = Book.query.filter(Book.quantidade>0).all()
    users = User.query.all()
    return render_template('loans/loan_form.html', books=books, users=users)

@bp.route('/return/<int:loan_id>', methods=['POST'])
@login_required
def return_loan(loan_id):
    if current_user.role.name not in ("BIBLIOTECARIO", "ADMIN"):
        flash("Permissão negada", "danger")
        return redirect(url_for('loans.list_loans'))
    loan = Loan.query.get_or_404(loan_id)
    if loan.status == LoanStatus.DEVOLVIDO:
        flash("Empréstimo já devolvido", "warning")
        return redirect(url_for('loans.list_loans'))
    loan.data_devolucao = datetime.utcnow()
    atraso = (loan.data_devolucao - loan.data_devolucao_prevista).days
    if atraso > 0:
        loan.multa = atraso * 1.0
    loan.status = LoanStatus.DEVOLVIDO
    loan.book.quantidade += 1
    db.session.add(AuditLog(actor_id=current_user.id, action="return_loan", details=f"loan_id={loan.id}, multa={loan.multa}"))
    db.session.commit()
    flash("Devolução registrada", "success")
    return redirect(url_for('loans.list_loans'))

@bp.route('/renew/<int:loan_id>', methods=['POST'])
@login_required
def renew_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if current_user.id != loan.user_id and current_user.role.name not in ("BIBLIOTECARIO", "ADMIN"):
        flash("Permissão negada", "danger")
        return redirect(url_for('loans.list_loans'))
    # Removida verificação de Reservation (RF10 desfeita)
    if loan.renovacoes >= 2:
        flash("Limite de renovações atingido", "danger")
        return redirect(url_for('loans.list_loans'))
    loan.renovacoes += 1
    loan.data_devolucao_prevista += timedelta(days=7)
    db.session.add(AuditLog(actor_id=current_user.id, action="renew_loan", details=f"loan_id={loan.id}, renovacoes={loan.renovacoes}"))
    db.session.commit()
    flash("Empréstimo renovado", "success")
    return redirect(url_for('loans.list_loans'))

@bp.route('/report/excel')
@login_required
def report_excel():
    loans = Loan.query.all()
    rows = []
    for L in loans:
        rows.append({
            "id": L.id,
            "livro": L.book.titulo if L.book else "",
            "usuario": L.user.nome if L.user else "",
            "data_emprestimo": L.data_emprestimo,
            "data_devol_prev": L.data_devolucao_prevista,
            "status": L.status.value
        })
    import pandas as pd, io
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='emprestimos')
    buf.seek(0)
    return send_file(buf, download_name="emprestimos.xlsx", as_attachment=True)

@bp.route('/report/pdf')
@login_required
def report_pdf():
    loans = Loan.query.all()
    import io
    buf = io.BytesIO()
    p = canvas.Canvas(buf, pagesize=letter)
    y = 750
    p.setFont("Helvetica", 12)
    p.drawString(30, y+20, "Relatório de Empréstimos")
    for L in loans:
        line = f"#{L.id} - {L.book.titulo if L.book else ''} - {L.user.nome if L.user else ''} - {L.status.value}"
        p.drawString(30, y, line)
        y -= 20
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buf.seek(0)
    return send_file(buf, download_name="emprestimos.pdf", as_attachment=True)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_loan(id):
    if not require_bibliotecario():
        return redirect(url_for('loans.list_loans'))
    
    loan = Loan.query.get_or_404(id)
    form = LoanForm(obj=loan)
    
    if form.validate_on_submit():
        form.populate_obj(loan)
        db.session.commit()
        flash('Empréstimo atualizado com sucesso!', 'success')
        return redirect(url_for('loans.list_loans'))
    
    return render_template('loans/loan_form.html', form=form, loan=loan)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_loan(id):
    if not require_bibliotecario():
        return redirect(url_for('loans.list_loans'))
    
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    flash('Empréstimo excluído com sucesso!', 'success')
    return redirect(url_for('loans.list_loans'))

@bp.route('/request/<int:book_id>', methods=['GET','POST'])
@login_required
def request_loan(book_id):
    # usuários normais solicitam; bibliotecários usam fluxo direto
    if current_user.role.name in ("BIBLIOTECARIO", "ADMIN"):
        flash("Use o fluxo de registro de empréstimo.", "info")
        return redirect(url_for('loans.list_loans'))

    book = Book.query.get_or_404(book_id)
    if not book:
        flash("Livro não encontrado.", "danger")
        return redirect(url_for('books.list_books'))

    # criar solicitação; não altera quantidade até aprovação
    loan = Loan(
        book_id=book.id,
        user_id=current_user.id,
        data_emprestimo = datetime.utcnow(),
        data_devolucao_prevista = None,
        status = LoanStatus.SOLICITADO
    )
    db.session.add(loan)
    db.session.add(AuditLog(actor_id=current_user.id, action="request_loan", details=f"book_id={book.id}, loan_id={loan.id if loan.id else 'n/a'}"))
    db.session.commit()
    flash("Solicitação de empréstimo enviada. Aguarde aprovação.", "success")
    return redirect(url_for('books.list_books'))


@bp.route('/approve/<int:loan_id>', methods=['POST'])
@login_required
def approve_request(loan_id):
    if not require_bibliotecario():
        flash("Permissão negada", "danger")
        return redirect(url_for('loans.list_loans'))

    loan = Loan.query.get_or_404(loan_id)
    if loan.status != LoanStatus.SOLICITADO:
        flash("Empréstimo não está em estado de solicitação.", "warning")
        return redirect(url_for('loans.list_loans'))

    book = Book.query.get(loan.book_id)
    if not book or book.quantidade <= 0:
        flash("Não há exemplares disponíveis para aprovação.", "danger")
        return redirect(url_for('loans.list_loans'))

    book.quantidade -= 1
    loan.status = LoanStatus.ATIVO
    loan.data_devolucao_prevista = datetime.utcnow() + timedelta(days=14)
    db.session.add(AuditLog(actor_id=current_user.id, action="approve_request", details=f"loan_id={loan.id}"))
    db.session.commit()
    flash("Solicitação aprovada e empréstimo registrado.", "success")
    return redirect(url_for('loans.list_loans'))


@bp.route('/reject/<int:loan_id>', methods=['POST'])
@login_required
def reject_request(loan_id):
    if not require_bibliotecario():
        flash("Permissão negada", "danger")
        return redirect(url_for('loans.list_loans'))

    loan = Loan.query.get_or_404(loan_id)
    if loan.status != LoanStatus.SOLICITADO:
        flash("Empréstimo não está em estado de solicitação.", "warning")
        return redirect(url_for('loans.list_loans'))

    loan.status = LoanStatus.REJEITADO
    db.session.add(AuditLog(actor_id=current_user.id, action="reject_request", details=f"loan_id={loan.id}"))
    db.session.commit()
    flash("Solicitação rejeitada.", "info")
    return redirect(url_for('loans.list_loans'))

@bp.route('/requests', methods=['GET'])
@login_required
def list_requests():
    # somente bibliotecários/administradores podem ver e agir sobre solicitações
    if not require_bibliotecario():
        flash("Permissão negada", "danger")
        return redirect(url_for('loans.list_loans'))

    pending = Loan.query.filter_by(status=LoanStatus.SOLICITADO).order_by(Loan.data_emprestimo.asc()).all()
    return render_template('loans/request_list.html', requests=pending)
