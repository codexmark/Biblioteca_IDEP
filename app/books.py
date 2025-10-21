from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from .models import Book, AuditLog, Loan
from .forms import BookForm
from . import db
from flask_login import login_required, current_user
from app.utils import require_bibliotecario

bp = Blueprint('books', __name__)

@bp.route('/')
@login_required
def list_books():
    q = request.args.get('q','')
    page = request.args.get('page', 1, type=int)
    query = Book.query.filter(Book.ativo==True)
    if q:
        query = query.filter(
            (Book.titulo.ilike(f"%{q}%")) |
            (Book.autores.ilike(f"%{q}%")) |
            (Book.categoria.ilike(f"%{q}%"))
        )
    pag = query.paginate(page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    return render_template('books/book_list.html', pag=pag, q=q)

@bp.route('/create', methods=['GET','POST'])
@login_required
def create_book():
    if not require_bibliotecario():
        return redirect(url_for('books.list_books'))
    form = BookForm()
    if form.validate_on_submit():
        if form.isbn.data:
            exists = Book.query.filter_by(isbn=form.isbn.data).first()
            if exists:
                flash("ISBN já cadastrado. Edite o livro existente.", "warning")
                return redirect(url_for('books.list_books'))
        book = Book(
            titulo=form.titulo.data,
            autores=form.autores.data,
            isbn=form.isbn.data,
            ano=form.ano.data,
            editora=form.editora.data,
            categoria=form.categoria.data,
            quantidade=form.quantidade.data or 1,
            localizacao=form.localizacao.data,
            sinopse=form.sinopse.data
        )
        db.session.add(book)
        db.session.commit()
        db.session.add(AuditLog(actor_id=current_user.id, action="create_book", details=f"book_id={book.id}"))
        db.session.commit()
        flash("Livro cadastrado com sucesso", "success")
        return redirect(url_for('books.list_books'))
    return render_template('books/book_form.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    if not require_bibliotecario():
        return redirect(url_for('books.list_books'))
    
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Livro atualizado com sucesso!', 'success')
        return redirect(url_for('books.list_books'))
    
    return render_template('books/book_form.html', form=form, book=book)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_book(id):
    if not require_bibliotecario():
        return redirect(url_for('books.list_books'))
    
    book = Book.query.get_or_404(id)
    
    # Verificar se há empréstimos ativos associados ao livro
    if Loan.query.filter_by(book_id=book.id).count() > 0:
        flash('Não é possível excluir o livro, pois há empréstimos ativos associados.', 'danger')
        return redirect(url_for('books.list_books'))
    
    db.session.delete(book)
    db.session.commit()
    flash('Livro excluído com sucesso!', 'success')
    return redirect(url_for('books.list_books'))
