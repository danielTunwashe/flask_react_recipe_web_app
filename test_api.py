import unittest
from main import create_app
from config import TestConfig
from exts import db
from main import create_app

#First import our testcase which inherits from unit tests
class APITestCase(unittest.TestCase):
    #Create our tear down and setup functions
    #set up function helps us to declear the different variables we are going to using for our test case
    def setUp(self):
        self.app = create_app(TestConfig)
        #Access our test client whiich is an interface that flask provides for us to test our application 
        #which helps us to make the diffetent request to the different route associated with our application
        self.client = self.app.test_client(self)
        #Craete our database by importing db or the sqlalchemy instance and initialize it with the cuurrent app we are working with
        with self.app.app_context():
            db.create_all()

    #Testing the signup route
    def test_signup(self):
        signup_response = self.client.post('/auth/signup',
            json={"username": "testuser", 
                  "password": "testpassword",
                  "email": "testemail@test.com"
                 }
        )

        #access our response and test out status code
        status_code = signup_response.status_code
        #assert if respCode = 201
        self.assertEqual(status_code,201)

    #Testing the login route
    def test_login(self):
        signup_response = self.client.post('/auth/signup',
            json={"username": "testuser", 
                  "password": "testpassword",
                  "email": "testemail@test.com"
                 }
        )
        login_response = self.client.post('/auth/login',
            json={"username": "testuser", 
                  "password": "testpassword"
                 }
        )
        status_code=login_response.status_code
        self.assertEqual(status_code,200)
    

    #Test for getting all recipes
    def test_get_all_recipes(self):
        '''TEST FOR GETTING ALL RECIPES'''
        response = self.client.get('/recipe/recipes')

        # print(response.json)
        signup_response = self.client.post('/auth/signup',
            json={"username": "testuser", 
                  "password": "testpassword",
                  "email": "testemail@test.com"
                 }
        )
        login_response = self.client.post('/auth/login',
            json={"username": "testuser", 
                  "password": "testpassword"
                 }
        )

        access_token = login_response.json['access_token']

        

        get_all_recipe_response = self.client.get('/recipe/recipes',
            headers={
                 "Authorization": f"Bearer {access_token}" 
            }
        )

        status_code = get_all_recipe_response.status_code
        self.assertEqual(status_code,200)

    #Test to Get a single recipe
    def test_get_one_recipe(self):
        id = 1
        response = self.client.get(f'/recipe/recipes/{id}')
        status_code = response.status_code
        self.assertEqual(status_code,404)

    #Test for creating a recipe
    def test_create_recipe(self):
        signup_response = self.client.post('/auth/signup',
            json={"username": "testuser", 
                  "password": "testpassword",
                  "email": "testemail@test.com"
                 }
        )
        login_response = self.client.post('/auth/login',
            json={"username": "testuser", 
                  "password": "testpassword"
                 }
        )

        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post('/recipe/recipes',
        json={"title": "Test recipe",
              "description": "Test description"
             },
             headers={
                 "Authorization": f"Bearer {access_token}" 
            }
        )
        status_code = create_recipe_response.status_code
        self.assertEqual(status_code,201)
        print(create_recipe_response.json)

    #Test for updating a recipe
    def test_update_recipe(self):

        signup_response = self.client.post('/auth/signup',
            json={"username": "testuser", 
                  "password": "testpassword",
                  "email": "testemail@test.com"
                 }
        )
        login_response = self.client.post('/auth/login',
            json={"username": "testuser", 
                  "password": "testpassword"
                 }
        )

        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post('/recipe/recipes',
        json={"title": "Test recipe",
              "description": "Test description"
             },
             headers={
                 "Authorization": f"Bearer {access_token}" 
            }
        )        
        id = 1
        update_recipe_response = self.client.put(f'recipe/recipe/{id}',
        json={"title": "Test recipe 1",
              "description": "Test description 1" 
             },
             headers={
                 "Authorization": f"Bearer {access_token}" 
            }
        )

        status_code = update_recipe_response.status_code
        self.assertEqual(status_code,200)

    #Test for deleting a recipe
    def test_delete_recipe(self):
        signup_response = self.client.post('/auth/signup',
            json={"username": "testuser", 
                  "password": "testpassword",
                  "email": "testemail@test.com"
                 }
        )
        login_response = self.client.post('/auth/login',
            json={"username": "testuser", 
                  "password": "testpassword"
                 }
        )

        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post('/recipe/recipes',
        json={"title": "Test recipe",
              "description": "Test description"
             },
             headers={
                 "Authorization": f"Bearer {access_token}" 
            }
        )        
        id = 1
        delete_recipe_response = self.client.delete(f'/recipe/recipe/{id}',
        headers={
            "Authorization": f"Bearer {access_token}" 
            }
        )

        status_code = delete_recipe_response.status_code
        self.assertEqual(status_code,200)

    


    #The Tear down function help us to destroy whatever things we have created in the setup function
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# We create our test runner helps us to discover whatever test we have written and run them
if __name__ == '__main__':
    unittest.main()