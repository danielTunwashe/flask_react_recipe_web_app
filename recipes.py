#Create a namesapce
from flask_restx import Namespace, Resource, fields
from flask import Flask, jsonify,request, make_response
from models import Recipe
from flask_jwt_extended import JWTManager, jwt_required

recipe_namespace = Namespace('recipe',description="A namespace for Recipes")

#Creating our serializer instance (model serializer to matial, serialze or export our model in terms of json)
recipe_model=recipe_namespace.model(
    "Recipe",
    {
        "id": fields.Integer(),
        "title": fields.String(),
        "description": fields.String(),
    }
)


@recipe_namespace.route('/hello')
class HelloResource(Resource):
    def get(self):
        return make_response(jsonify( {"Message": "Hello World!!"}),200)

@recipe_namespace.route('/recipes')
class RecipesResource(Resource):
    #To turn our sql object into a json
    @recipe_namespace.marshal_list_with(recipe_model)
    # @jwt_required()
    def get(self):
        '''Get all recipes from our database'''

        recipes = Recipe.query.all()

        return recipes, 200
    

    @recipe_namespace.marshal_with(recipe_model)
    @recipe_namespace.expect(recipe_model)
    @jwt_required()
    def post(self):
        '''Create a new recipe'''
        
        #Access the data coming from our client using request (import) contains the data from the frontenc
        data = request.get_json()

        #Create a new recipe using the data passed from the client
        new_recipe = Recipe(
            title=data.get('title'),
            description=data.get('description')
        )

        new_recipe.save()

        return new_recipe, 201



@recipe_namespace.route('/recipe/<int:id>')
class RecipeResource(Resource):
    @recipe_namespace.marshal_with(recipe_model)
    def get(self, id):
        '''Get a recipe from our database by id'''
    
        #Query the database for a recipe
        recipe = Recipe.query.get_or_404(id)

        return recipe,200
    


    @recipe_namespace.marshal_with(recipe_model)
    @jwt_required()
    def put(self, id):
        '''Update a recipe by id'''
        #Query the database for the specific recipe to update
        recipe_to_update = Recipe.query.get_or_404(id)

        data=request.get_json()

        recipe_to_update.update(data.get('title'), data.get('description'))

        return recipe_to_update, 200


    @recipe_namespace.marshal_with(recipe_model)
    @jwt_required()
    def delete(self, id):
        '''Delete a recipe by id'''
        #Query for the specific recipe
        recipe_to_delete = Recipe.query.get_or_404(id)

        recipe_to_delete.delete()

        return recipe_to_delete,200

