from exts import db

#Create our model
'''
class Recipe:
    id: int primary key
    title: str
    description: str (text)
'''

class Recipe(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(), nullable=False)
    description=db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<Recipe {self.title} >"
    
    
    #methods to help in creating the CRUD operations
    #To save
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    #To delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    #To Update
    def update(self,title,description):
        self.title = title
        self.description = description

        db.session.commit()

# User Model

'''
Class User:
    id: Integer
    username:string
    email:string
    password:string
'''

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(25), nullable=False, unique=True)
    email=db.Column(db.String(80), nullable=False)
    password=db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<User {self.username} >"
    #methods to help in creating the CRUD operations
    #To save
    def save(self):
        db.session.add(self)
        db.session.commit()