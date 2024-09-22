from flask import Flask
from flask_restx import Api
from api.extensions import db, jwt, migrate,mail,cors
from api.users.controllers import user_ns
from api.patients.controllers import patient_ns
from dotenv import load_dotenv
from datetime import datetime
from api.main.routes import hms_ns



load_dotenv()

def create_app(config):           
    app = Flask(__name__) 
    app.config.from_object(config)
    api = Api(app, docs='\docs')
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    
    api.add_namespace(user_ns)
    api.add_namespace(patient_ns)
    api.add_namespace(hms_ns)
    
  
    
    with app.app_context():
        #db.drop_all()
        db.create_all()
  
   
    return app

