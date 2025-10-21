from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha atual', validators=[DataRequired()])
    new_password = PasswordField('Nova senha', validators=[DataRequired(), Length(min=6)])
    new_password2 = PasswordField('Repita a nova senha', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Alterar senha')

class BookForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autores = StringField('Autores', validators=[Optional()])
    isbn = StringField('ISBN', validators=[Optional()])
    ano = StringField('Ano', validators=[Optional()])
    editora = StringField('Editora', validators=[Optional()])
    categoria = StringField('Categoria', validators=[Optional()])
    quantidade = IntegerField('Quantidade', default=1)
    localizacao = StringField('Localização', validators=[Optional()])
    sinopse = TextAreaField('Sinopse', validators=[Optional()])

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[Optional()])
    matricula = StringField('Matrícula', validators=[DataRequired()])
    role = SelectField('Perfil', choices=[('usuario','Usuário'),('bibliotecario','Bibliotecário'),('admin','Administrador')])
