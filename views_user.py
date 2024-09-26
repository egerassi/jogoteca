from jogoteca import app, db
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioLogin, FormularioCriarConta
from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash

@app.route('/criarconta')
def criarconta():
    form = FormularioCriarConta()
    return render_template('criarconta.html', form=form)

@app.route('/novaconta', methods=['POST', ])
def novaconta():
    form = FormularioCriarConta(request.form)

    email = form.email.data
    usuario = form.usuario.data
    senha = form.senha.data
    email_existe = Usuarios.query.filter_by(email=email).first()
    usuario_existe = Usuarios.query.filter_by(usuario=usuario).first()

    if email_existe:
        flash('Email já cadastrado')
        return redirect(url_for('criarconta'))
    elif usuario_existe:
        flash('Nome de usuário já cadastrado')
        return redirect(url_for('criarconta'))
    else:
        conta = Usuarios(email=email, usuario=usuario, senha=generate_password_hash(senha).decode('utf-8'))
        db.session.add(conta)
        db.session.commit()
        flash('Conta criada com sucesso!')
        return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima is None:
        proxima = url_for('index')
    form = FormularioLogin()
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioLogin(request.form)

    usuario = Usuarios.query.filter_by(usuario=form.usuario.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)

    if usuario and senha:
        session['usuario_logado'] = usuario.usuario
        flash(f'{session['usuario_logado']} Logado com sucesso!')

        proxima_pagina = request.form.get('proxima')
        return redirect(proxima_pagina)
    else:
        flash('Login incorreto.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = False
    flash('Logout efetuado com sucesso.')
    return redirect(url_for('index'))