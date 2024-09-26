from os import times
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos, Usuarios
from jogoteca import *
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo, FormularioLogin, FormularioCriarConta
import time


@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.nome)
    return render_template('lista.html', titulo = 'Jogos', jogos = lista)
#render_template chamando o html dessa pagina, e atribuindo as viariaveis criadas no html a algo que podemos usar no py

@app.route('/novo_jogo')
def novo():
    if not isinstance(session.get('usuario_logado'), str):
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo = 'Adicionar jogo novo', form=form)

@app.route('/adicionar_jogo', methods=['POST', ])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    #Verifica se o jogo já está no banco de dados.
    jogo_existe = Jogos.query.filter_by(nome=nome).first()

    if jogo_existe:
        flash('Esse jogo já está cadastrado.')
        return redirect(url_for('novo'))
    else:
        jogo = Jogos(nome=nome, categoria=categoria, console=console)
        #Adiciona o jogo na base de dados e comita
        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        arquivo_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        arquivo.save(f'{arquivo_path}/capa{jogo.id}-{timestamp}.jpg')

        flash('Jogo cadastrado com sucesso')
        return redirect(url_for('index'))

@app.route('/editar_jogo/<int:id>')
def editar_jogo(id):
    if not isinstance(session.get('usuario_logado'), str):
        return redirect(url_for('login', proxima=url_for('editar_jogo', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editarjogo.html', titulo = 'Editar jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar_jogo/', methods=['POST'])
def atualizar_jogo():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
        flash('Jogo atualizado com sucesso')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('editar_jogo'))

@app.route('/deletar_jogo/<int:id>')
def deletar_jogo(id):
    if not isinstance(session.get('usuario_logado'), str):
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        Jogos.query.filter_by(id=id).delete()
        db.session.commit()

        flash('Jogo deletado com sucesso')
        return redirect(url_for('index'))

@app.route('/upload_imagem/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)