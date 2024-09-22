from api import create_app
from api.config import DevConfig, ProdConfig


app = create_app(DevConfig)


if __name__ == '__main__':
    
    app.run()
    
