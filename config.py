import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "troque-esta-chave-por-uma-secreta"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or         "sqlite:///" + os.path.join(basedir, "instance", "sistema_biblioteca.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 20
