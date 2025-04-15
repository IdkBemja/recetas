from flask import Flask, render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.recipes import Recipe

@app.route('/recipes/new')
def recipes_new():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    return render_template('new.html')


@app.route('/recipes/create', methods=['POST'])
def recipes_create():
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/recipes/show/<int:id>')
def recipes_show(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    diccionario = {"id": id}
    recipe = Recipe.get_by_id(diccionario)
    return render_template('recipe.html', recipe=recipe)

@app.route('/recipes/edit/<int:id>')
def recipes_edit(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    diccionario = {"id": id}
    recipe = Recipe.get_by_id(diccionario)
    return render_template('recipe.html', recipe=recipe)

@app.route('/recipes/delete/<int:id>')
def recipes_delete(id):
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    diccionario = {"id": id}
    Recipe.borrar(diccionario)
    return redirect('/dashboard')