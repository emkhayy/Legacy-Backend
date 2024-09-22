import os
from dotenv import load_dotenv





load_dotenv()

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    
    
class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    DEBUG = True
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
<<<<<<< HEAD
    JWT_SECRET_KEY = os.getenv["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv["JWT_ACCESS_TOKEN_EXPIRES"]
    JWT_REFRESH_TOKEN_EXPIRES = os.getenv["JWT_REFRESH_TOKEN_EXPIRES"]


=======
   
>>>>>>> 7c7519f5f489352feb386dec09433dd46003e44b
    
class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    DEBUG = os.getenv("DEBUG")
    SQLALCHEMY_ECHO = os.getenv("ECHO")
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    MAIL_DEBUG = False


class TestConfig(BaseConfig):
    pass

