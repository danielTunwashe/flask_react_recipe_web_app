#To map our fles on .env to our configuration variables
from decouple import config
#To configure our sqlite database
import  os

#Getting the path of the backend env folder to the database path
BASE_DIR= os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY=config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS',cast=bool)


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'dev.db')
    DEBUG=True
    SQLALCHEMY_ECHO=True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'dev.db')
    SQLALCHEMY_ECHO=config('ECHO')
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS')
    DEBUG=config('DEBUG', cast=bool)


class TestConfig(Config):
    #Helps us specify the database we are going to use for testing purposes
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    #Helps us to avioid recieving sql statements or error generated
    SQLALCHEMY_ECHO=False
    #Helps us to give less error catching
    TESTING=True