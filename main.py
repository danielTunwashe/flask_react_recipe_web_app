#import flask
from flask import Flask, request, jsonify
#importing our flask framework to help us build the flask API
from flask_restx import Api
#Import our configuration files from the config.py (for now we are using development config)
#import a context processor to help us access our db
from models import Recipe, User
from exts import db
#Instanciate flask migrate to work with our application
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipes import recipe_namespace
from auth import auth_namespace
#Import flask - cors to allow cross origin access (ie for port 5000 to work with port 3000)
from flask_cors import CORS

#Creating an application factory to keep all the logic of creating our application
def create_app(config):
    #create flask instance
    app=Flask(__name__,static_url_path='/',static_folder='./client/build')
    #Setting our application to work with the devConfig
    app.config.from_object(config)
    #Register our flask cors with in our application factory(configuring our api to work with an application on a different port)
    CORS(app)

    #To register our Flask app with SQLAlchemy instance
    db.init_app(app)

    #Instanciate our flask migrate to our application
    migrate = Migrate(app,db)

    #configure our app to work with jwt manager
    JWTManager(app)

    #create an instance of the API
    api=Api(app,doc='/docs')

    api.add_namespace(recipe_namespace)
    api.add_namespace(auth_namespace)

        
    #Adding a context process to help us create our database within our application
    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "Recipe":Recipe,
            "User":User
        }
    
    @app.route('/')
    def index():
        return app.send_static_file('index.html')


    @app.errorhandler(404)
    def not_found(err):
        return app.send_static_file('index.html')

    #Run our flask app
    return app