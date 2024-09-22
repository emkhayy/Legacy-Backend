from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail


	

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()
mail = Mail()
