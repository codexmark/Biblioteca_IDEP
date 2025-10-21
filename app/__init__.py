from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # load instance config overrides if present
    instance_config = os.path.join(app.instance_path, 'config.py')
    if os.path.exists(instance_config):
        app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Blueprints
    from .auth import bp as auth_bp
    from .books import bp as books_bp
    from .loans import bp as loans_bp
    from .admin import bp as admin_bp
    from .reports import bp as reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(loans_bp, url_prefix="/loans")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Auto-create database and seed admin + exemplos if needed
    with app.app_context():
        from . import models
        db.create_all()
        # create admin if not exists
        admin_email = "admin@example.com"
        admin = models.User.query.filter_by(email=admin_email).first()
        if not admin:
            a = models.User(nome="Administrador", email=admin_email, matricula="0000")
            a.role = models.RoleEnum.ADMIN
            a.set_password("admin123")
            db.session.add(a)
            db.session.commit()
            print("Criado usuário admin (admin@example.com / admin123)")
        # seed exemplos se não houver livros
        if models.Book.query.count() == 0:
            from .seed import popular_exemplos
            popular_exemplos()
            print("Dados de exemplo adicionados.")

    return app
