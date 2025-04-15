from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#Importación de BCrypt -> Encriptar la contraseña
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')    
    
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    form = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pass_encrypt
    }

    id = User.save(form)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')

    form = {"id": session['user_id']}
    user = User.get_by_id(form)

    recipes = Recipe.get_all()

    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('E-mail no registrado', 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')