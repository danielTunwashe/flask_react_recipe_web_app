#Import our configuration as well as our application factory function
from main import create_app
from config import DevConfig, ProdConfig

if __name__ == '__main__':
    app = create_app(ProdConfig)
    

