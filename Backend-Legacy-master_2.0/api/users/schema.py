from flask_restx import fields
from api.users.controllers import user_ns

UserNewLoad = user_ns.model(
    "SignUp_Request Model",
    {
        "surname": fields.String(),
        "other_name": fields.String(),
        "birth_date": fields.Date(),
        "gender": fields.String(),
        "email": fields.String(),
        "qualification": fields.String(),
        "contact1": fields.String(),
        "contact2": fields.String(),
        "address": fields.String()
   }    
)

UserNewDump = user_ns.model(
    "SignUp_Response Model",
    {
        "public_id": fields.Integer(),
        "other_name": fields.String(),
        "birth_date": fields.Date(),
        "surname": fields.String(),
        "email": fields.String(),
        "username": fields.String(),
        "password": fields.String(),
        "date_created": fields.Date(),
        "gender": fields.String(),
        "qualification": fields.String(),
        "contact1": fields.String(),
        "contact2": fields.String(),
        "address": fields.String()   
   }    
)       

UsersDump = user_ns.model(
    "List Of Users",{
       "public_id": fields.Integer(),
        "username": fields.String(),
        "other_name": fields.String(),
        "surname": fields.String(), 
        "gender": fields.String(),
        "qualification": fields.String(),
    }
)
SpecUserDump = user_ns.model(
    "List Of Specusers",{
       "public_id": fields.Integer(),
        "username": fields.String(),
        "other_name": fields.String(),
        "surname": fields.String(), 
        "gender": fields.String(),
        
    }
)

UserLoginLoad = user_ns.model(
    "Login_Request Model",
    {
        "username": fields.String(),
        "password": fields.String()
        #"qualification": fields.String()
    }
)

UserLoginDump = user_ns.model(
   "Login_Response Model",
    {
        "public_id": fields.Integer(),
        "access_token": fields.String() ,
        "refresh_token": fields.String(),
        "qualification": fields.String() 
    } 
)


UserUpdate = user_ns.model(
    "Update_Request Model",
    {
        "surname": fields.String(),
        "other_name": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
        "qualification": fields.String(),
        "contact1": fields.String(),
        "contact2": fields.String(),
        "address": fields.String()
    }
)
searchLoad = user_ns.model(
        "Search Model",
        {
            'column_name' : fields.String(),
            "data": fields.String(),
            "qualification" : fields.String()
        }
    )
