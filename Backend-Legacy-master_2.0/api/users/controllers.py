
from os import link
from re import search
from tarfile import LENGTH_LINK
from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace
from api.constants.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE, HTTP_409_CONFLICT
from api.extensions import db, mail
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from flask_restx import Api
from flask_jwt_extended import create_access_token,create_refresh_token
import api.users.models as userModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flask_mail import Message
from  sqlalchemy import select
User = userModel.User
user_ns = Namespace("user", description="User Authentications")
from api.users.schema import UserNewLoad, UserNewDump, UserLoginLoad, UserLoginDump, UserUpdate,UsersDump,SpecUserDump, searchLoad

api = Api()




@user_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        """Get all user"""
        return{'message': 'hello world'}
    
@user_ns.route("/signup")
class SignUP(Resource):
    
    @user_ns.marshal_with(UserNewDump)
    @user_ns.expect(UserNewLoad)
    def post(self):
        """Sign up by fillig the required spaces"""
        
        #get user response
        data = request.get_json()
        email = data.get('email')
        
        #check if already in database
        db_user = User.query.filter_by(email=email).first() 
        if db_user:
            abort(HTTP_409_CONFLICT, {"message": f"User with email {email} already exist"})
            # return make_response(jsonify({"message": f"User with email {email} already exist"}), HTTP_409_CONFLICT)
            #return jsonify({"message": f"User with email {email} already exist"})
        
        
        #create date object
        #date_obj = datetime.strptime(data.get('birth_date'), '%m-%d-%Y').date()
        
        #create a new user
        # new_user = userModel.Nurse(
        #     other_name=data.get('other_name'), 
        #     surname=data.get('surname'), 
        #     email=data.get('email'),
        #     birth_date=date_obj, 
        #     #password = generate_password_hash(data.get('password'), method='sha256'),
        #     gender=data.get("gender"),
        #     contact1=data.get("contact1"),
        #     contact2=data.get("contact2"),
        #     address=data.get("address"),
        #     qualification=data.get("qualification")
        #     )
        
        # db.session.add(new_user)
        # db.session.commit()
        #new_user.send(reciever='admin', title="New Employee", message=new_user)
        if data.get('qualification') == "Nurse":
            new_user = userModel.Nurse(**data)            
            userModel.Nurse.save(new_user)
            db_user = User.query.filter_by(email=email).first()            
            new_user_mail(db_user, db_user.public_id)
            
        elif data.get('qualification') == "Doctor":
            new_user = userModel.Doctor(**data)
            userModel.Doctor.save(new_user)
            db_user = User.query.filter_by(email=email).first()
            new_user_mail(db_user, db_user.public_id)
            
        elif data.get('qualification') == "Admin":
            new_user = userModel.Admin(**data)
            userModel.Admin.save(new_user)        
            db_user = User.query.filter_by(email=email).first()
            new_user_mail(db_user, db_user.public_id)
            
        return  new_user, HTTP_200_OK#jsonify({"message": "done!"})
            
    
@user_ns.route("/login")
class LogIn(Resource):
    
    @user_ns.marshal_with(UserLoginDump)
    @user_ns.expect(UserLoginLoad)
    def post(self):
        """LogIn by username & password"""
        
        #get user respsonse
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        #check if in database
        db_user = User.query.filter_by(username=username).first()
        #print(db_user)
        if db_user:
            #if  db_user.password != passcode:#db_user.check_hashed_password(passcode):
            passcode=db_user.password_hash
            print(passcode)
            if check_password_hash(passcode, password):
                db_user.access_token = create_access_token(identity=db_user.public_id)
                db_user.refresh_token = create_refresh_token(identity=db_user.public_id)
                return db_user
            abort(HTTP_400_BAD_REQUEST, {"message": "Incorrect Username or password"})
        abort(HTTP_400_BAD_REQUEST, {"message": f"Wrong credentials"})
        #return db_user
        
        
    
    
    
    
    
    
@user_ns.route('/users')
class UsersResource(Resource):

    @user_ns.marshal_list_with(UsersDump)
    # @jwt_required()    
    def get(self):
        """Get all users"""

        users = User.query.all()
        return users, HTTP_200_OK
@user_ns.route('/doctors')
class DoctorsResource(Resource):

    @user_ns.marshal_list_with(SpecUserDump)
    # @jwt_required()
    def get(self):
        """Get all Doctors"""

        doctors = User.query.filter_by(qualification="Doctor").all()
        return doctors, HTTP_200_OK

@user_ns.route('/user/<int:public_id>')
class UserResource(Resource):
    
    @user_ns.marshal_with(UserNewDump)
    # @jwt_required()
    def get(self, public_id):
        """Get user by public_id"""
        user = User.query.get_or_404(public_id)
        if user:
            return user
        abort(404, "User not found")

    @user_ns.expect(UserUpdate)
    @jwt_required()
    @user_ns.marshal_with(UserNewDump)
    def put(self, public_id):
        """Update a user by public_id"""
        user_to_update = User.query.get_or_404(public_id)
        data = request.get_json()
        # if user_to_update:
        #     data = request.get_json()
        #     for attr, value in data.items():
        #         if attr== "date_of_birth":
        #             value = datetime.strptime(data.get('date_of_birth'), '%m-%d-%Y').date()
        #         setattr(user_to_update, attr, value)
        
        #      db.session.commit()                

        updated_user = user_to_update.update_user(
                        email=data.get('email'),
                        password_hash=generate_password_hash(data.get('password')),
                        surname=data.get('surname'),
                        other_name=data.get('other_name'),
                        qualification=data.get('qualification'),
                        contact1=data.get('contact1'),
                        contact2=data.get('contact2'), 
                        address=data.get('address')
                        )
        msg = Message('Account Update', recipients=[data.get('email')])
        link = str(api.url_for(LogIn, _external=True))
        msg.body = f"<p><h2>Account Updated Successfully</h2><br>Click on link to go to the Login page. <a href={link}>Click Here</a></p>"
        mail.send(msg)
        update = User.query.get_or_404(public_id)
        return update

    #@user_ns.marshal_with(UserNewDump)
    @jwt_required()
    def delete(self, public_id):
        """Delete a user by public_id"""
        user_to_be_deleted = User.query.get_or_404(public_id)
        if user_to_be_deleted:
            User.delete_user(user_to_be_deleted)
            deleted_user_mail(user_to_be_deleted)
            return jsonify({"message":"User has been deleted successfully"})
        abort(HTTP_404_NOT_FOUND, "No such User found")
    
        
        
# @user_ns.route("/user/notication")     
# class NotficationResource(Resource):
#     @user_ns.expect(UserNewLoad)
#     def get(self, new_emp):
#         pass
    
    

    
# @user_ns.route("/admin/<int:id>")
# class AcceptEmployeeResource(Resource):
#     def get(self, id):
#         new_emp = User.query.get(id)
         
#         if new_emp:
#         # Delete the patient instance
#             new_emp.status = 'accepted'
#             db.session.delete(new_emp)
#             db.session.commit()

#             pending_list = User.query.filter_by(status='Pending').all()
        
#             return pending_list
#         abort(404, "Patient not found")


@user_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        
        return make_response(jsonify({"access_token": new_access_token}), HTTP_200_OK)
            
        
        
        
def new_user_mail(user, user_id):
    email = str(user.email)
    username = user.username
    password = user.password           
    qualification= user.qualification
    msg = Message('SignUp Account', recipients=[email])
    link = f"https://frontend-team-legacy-health-service.vercel.app/{qualification}Login"
    msg.body = f"<p><h2>Account Created Successfully</h2><br>You have successfully registered as a {qualification}.<br>Your Special Identification Number, Username and Password are given below.<br><b>Identification Number:&nbsp;&nbsp; {user_id}</b><br><b>Username:&nbsp;&nbsp;{username}</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Password:&nbsp;&nbsp;{password}</b><br><b>Please ensure that you note it down as you will use for login.</b><br>Click on link to go to the Login page. <a href={link}>Click Here</a></p>"
    mail.send(msg)
    
def  deleted_user_mail(user):
    email = str(user.email)
    msg = Message('Account Deleted', recipients=[email])
    # link = str(api.url_for(NotificationResource, _external=True))
    msg.body = f"<p><h2>Your account has been deleted!.</h2><br> If you have no idea why you are receiving this email, please notify the administrator.<a href={link}>Click Here</a></p>"
    mail.send(msg)

@user_ns.route('/nurses')
class NursesResource(Resource): 
    @user_ns.marshal_list_with(UsersDump)
    # @jwt_required()
    
    def get(self):
        """Get all nurses"""

        nurses = User.query.filter_by(qualification='Nurse'). all()
        return nurses, HTTP_200_OK
    

@user_ns.route('/search')
class SearchResource(Resource):
    @user_ns.marshal_list_with(UsersDump)
    @user_ns.expect(searchLoad)
    def post(self):
        data = request.get_json()
        substr = data.get('data')
        column = data.get('column_name')
        qualification = data.get('qualification')
        stri = f"%{substr}%"
        if qualification == "Nurse" or qualification == "Nurse" or qualification == "Doctor" or qualification == "Admin":
            # res = User.query.filter_by(qualification= qualification).filter(User.username.ilike(stri)).all()
                if column == 'username':
                    res = User.query.filter_by(qualification= qualification).filter(User.username.ilike(stri)).all()
                elif column == 'surname':
                    res = User.query.filter(User.surname.like(stri), qualification= qualification).all()
                elif column == 'other_name':
                    res = User.query.filter(User.other_name.like(stri), qualification= qualification).all()
                elif column == 'email':
                    res = User.query.filter(User.email.like(stri), qualification= qualification).all()
                else:
                    return abort(HTTP_400_BAD_REQUEST, "No such column")
            
        else:
                if column == 'username':
                    res = User.query.filter(User.username.ilike(stri)).all()
                elif column == 'surname':
                    res = User.query.filter(User.surname.like(stri)).all()
                elif column == 'other_name':
                    res = User.query.filter(User.other_name.like(stri)).all()
                elif column == 'email':
                    res = User.query.filter(User.email.like(stri)).all()
                elif column == 'address':
                    res = User.query.filter(User.address.like(stri)).all()
                else:
                    return abort(HTTP_400_BAD_REQUEST, "No such column")

        return res, HTTP_200_OK