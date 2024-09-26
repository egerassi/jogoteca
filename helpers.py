import os
from jogoteca import *
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, EmailField

class FormularioJogo(FlaskForm):
    nome = StringField('Nome', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', validators=[validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioLogin(FlaskForm):
    usuario = StringField('Usuario', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    senha = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    entrar = SubmitField('Entrar')

class FormularioCriarConta(FlaskForm):
    email = EmailField('E-mail', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    usuario = StringField('Usuario', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    senha = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    criar  = SubmitField('Criar')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(arquivo)