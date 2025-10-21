from . import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime
import enum

class RoleEnum(enum.Enum):
    ADMIN = "admin"
    BIBLIOTECARIO = "bibliotecario"
    USUARIO = "usuario"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(30))
    matricula = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.USUARIO)
    active = db.Column(db.Boolean, default=True)
    blocked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role in (RoleEnum.ADMIN, RoleEnum.BIBLIOTECARIO)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autores = db.Column(db.String(255))
    isbn = db.Column(db.String(20), unique=True)
    ano = db.Column(db.String(10))
    editora = db.Column(db.String(120))
    categoria = db.Column(db.String(120))
    quantidade = db.Column(db.Integer, default=1)
    localizacao = db.Column(db.String(120))
    sinopse = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoanStatus(enum.Enum):
    ATIVO = "ativo"
    DEVOLVIDO = "devolvido"
    SOLICITADO = "solicitado"   # novo: solicitação pendente feita por usuário
    REJEITADO = "rejeitado"     # novo: solicitação rejeitada

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime, default=datetime.utcnow)
    data_devolucao_prevista = db.Column(db.DateTime)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    renovacoes = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum(LoanStatus), default=LoanStatus.ATIVO)
    multa = db.Column(db.Float, default=0.0)

    book = db.relationship('Book', backref='loans')
    user = db.relationship('User', backref='loans')

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    action = db.Column(db.String(255))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    actor = db.relationship('User')
