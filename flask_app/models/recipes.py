from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        #JOIN
        self.first_name = data['first_name']
    
    #Valida la receta
    @staticmethod
    def validate_recipe(form):
        is_valid = True

        if len(form['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'recipe')
            is_valid = False
        
        if len(form['description']) < 3:
            flash('La descripción debe tener al menos 3 caracteres', 'recipe')
            is_valid = False
        
        if len(form['instructions']) < 3:
            flash('Las instrucciones deben de tener al menos 3 caracteres', 'recipe')
            is_valid = False
        
        if form['date_made'] == "":
            flash('Ingrese una fecha válida', 'recipe')
            is_valid = False
        
        return is_valid

    @classmethod
    def save(cls, form):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s)"
        result = connectToMySQL('esquema_recetas_aa').query_db(query, form)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*, users.first_name FROM recipes JOIN users ON user_id = users.id"
        results = connectToMySQL('esquema_recetas_aa').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT recipes.*, users.first_name FROM recipes JOIN users ON user_id = users.id WHERE recipes.id = %(id)s"
        result = connectToMySQL('esquema_recetas_aa').query_db(query, data)
        recipe = cls(result[0])
        return recipe
    
    @classmethod
    def borrar(cls, form):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas_aa').query_db(query, form)
        return result