from flask_restx import Namespace, Resource, fields
from flask import Flask, jsonify,request, make_response
from models import User
#Import werkzeug to create password authentication
from werkzeug.security import generate_password_hash, check_password_hash 
#configure our application to work with jwt extended in order to create acess and refresh token
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token,jwt_required, get_jwt_identity


#Create a namspace which is similar to a blue print which helps us to have our logic in one module which we can use to register for our application
auth_namespace = Namespace('auth',description="A namesapce for our Authentication")


#Our models serilizers
#Creating our serializer instance (model serializer to matial, serialze or export our model in terms of json)
signup_model = auth_namespace.model(
    "Signup",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    }
)


login_model = auth_namespace.model(
    'Login',
    {
        "username": fields.String(),
        "password": fields.String()
    }
)



#create our flask route
@auth_namespace.route('/signup')
class SignUpResource(Resource):
    @auth_namespace.expect(signup_model)
    def post(self):
        data = request.get_json()

        #logic to determine if the user is registered already
        username = data.get('username')

        db_user = User.query.filter_by(username = username).first()

        if db_user is not None:
            return {"Message":f"User with {username} already exists"}
        #Creating our user object
        new_user = User(
            username = data.get("username"),
            email = data.get("email"),
            password = generate_password_hash(data.get("password"))
        )

        new_user.save()
        return {"Message":"User Created Successfully"},201
    


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        
        db_user = User.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password, password):
            #Give the user a refresh token and access taken
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)

        return jsonify({
            "access_token": access_token,"refresh_token": refresh_token
        })

#A refresh token to create a new, expired access token
@auth_namespace.route('/refresh')
class RefreshResources(Resource):
    @jwt_required(refresh=True)
    def post(self):
        #Access current logged in user, using get_jwt_identity (which will be imported)
        current_user = get_jwt_identity()

        new_access_token = create_access_token(identity=current_user)

        return make_response(jsonify({
            "new_access_token": new_access_token
        }), 200)

        