from api.extensions import db
#from secrets import token_hex
from api.patients.models import Patients, Vital_Records, Diagnosis_Records
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = "USER"
    public_id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    other_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    qualification = db.Column(db.String(30), nullable=False)
    contact1 = db.Column(db.String(25), nullable=False)
    contact2 = db.Column(db.String(25), nullable=True, default= None)
    address = db.Column(db.String(50), nullable=False)
    unread_notification = db.Column(db.Integer, nullable=False, default= 0)
    date_created = db.Column(db.DateTime, default= datetime.now())

    __mapper_args__ = {"polymorphic_on": qualification }
        
    
    def __repr__(self) -> str: 
        return f"<User: {self.other_name} {self.surname} {self.email} with username {self.username}"
    
    def serializable(self):
        return {
            "other_name" : self.other_name,
            "surname" :self.surname, 
            "email":self.email,
            "birth_date":self.birth_date, 
            #password : generate_password_hash(data.get('password'), method='sha256'),
            "gender":self.gender,
            "contact1":self.contact1,
            "contact2":self.contact2,
            "address":self.address,
            "qualification":self.qualification
        }          
        
    @property 
    def password(self):
            return f"{(self.surname)[2]}qwe4{(self.other_name)[2]}"
        #raise AttributeError(f"Your employment status is stil pending")
        #raise AttributeError("Password is a write_only field")
    #def check_hashed_password(self, password):
        #_bcrypt.check_password_hash(self.password_hash, password)
        #self.password_hash = generate_password_hash(self.password, )
        #check_password_hash("pbkdf2:sha256:260000$PKDDy2aKZ3WVtheL$39282741ec09a3d142a00005e8e075c7386af47ecc5a199b8d83702238481196", password)
        #check_password_hash(self.password_hash, password)
 
  
    @classmethod
    def add_to_db(cls, user):
        db.session.add(user)
        db.session.commit()
        
        
        
    @classmethod  
    def check_username(cls,user,username):
        var = 1
        while cls.query.filter_by(username=username).first():
            username = f"{(user.other_name)[0]}{user.surname}{var}"
            var+=1
        user.username = username
        
        
    def update_user(self, surname, other_name, email, password_hash, qualification, contact1, contact2, address):
        self.email = email
        self.password_hash = password_hash
        self.surname = surname
        self.other_name = other_name
        self.qualification = qualification
        self.contact1 = contact1
        self.contact2 = contact2
        self.address = address
        db.session.commit()
    
    @classmethod   
    def delete_user(clc, user):
        db.session.delete(user)
        db.session.commit()
        
    # @classmethod
    # def save(cls, user):
    #     user.username = f"{(user.other_name)[0]}{user.surname}" 
    #     passcode = user.password
    #     user.password_hash = generate_password_hash(passcode)
    #     temp = f"{(user.other_name)[0]}{user.surname}" 
    #     cls.check_username(user,temp)
    #     #self.password_hash = generate_password_hash(self.password)
        
    #     db.session.add(user)
    #     db.session.commit()
        

class Admin(User):
    __tablename__ = "ADMIN"
    __mapper_args__ = {"polymorphic_identity": "Admin"}
    public_id = db.Column(db.Integer, db.ForeignKey('USER.public_id',ondelete="CASCADE"))
    admin_id = db.Column(db.Integer, primary_key=True)
    
    
    def __init__(self, other_name, surname, email, birth_date, gender, contact1, contact2, address, qualification):
        self.other_name = other_name
        self.email = email
        self.surname = surname
        date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()        
        self.birth_date = date_obj
        self.gender = gender
        self.contact1 = contact1
        self.contact2 = contact2
        self.address = address
        self.qualification = qualification
    
        
    @classmethod
    def save(cls,user):
        user.username = f"{(user.other_name)[0]}{user.surname}" 
        passcode = user.password
        user.password_hash = generate_password_hash(passcode)
        temp = f"{(user.other_name)[0]}{user.surname}" 
        User.check_username(user,temp)
        db.session.add(user)
        db.session.commit()  

    
    
        
    
class Doctor(User):
    __tablename__ = "DOCTOR"
    __mapper_args__ =  {"polymorphic_identity": "Doctor"}
    public_id = db.Column(db.Integer, db.ForeignKey('USER.public_id',ondelete="CASCADE"))
    doctor_id = db.Column(db.Integer, primary_key=True)
    diagnosis_records = db.relationship(Diagnosis_Records, backref="doctor")
    
    def __init__(self, other_name, surname, email, birth_date, gender, contact1, contact2, address, qualification):
        self.other_name = other_name
        self.email = email
        self.surname = surname
        self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        self.gender = gender
        self.contact1 = contact1
        self.contact2 = contact2
        self.address = address
        self.qualification = qualification
    
    @classmethod
    def save(cls, user):
        user.username = f"{(user.other_name)[0]}{user.surname}" 
        passcode = user.password
        user.password_hash = generate_password_hash(passcode)
        temp = f"{(user.other_name)[0]}{user.surname}" 
        User.check_username(user,temp)
        #self.password_hash = generate_password_hash(self.password)
        
        db.session.add(user)
        db.session.commit()
    
    
class Nurse(User):
    __tablename__ = "NURSE"
    __mapper_args__ =  {"polymorphic_identity": "Nurse"}
    public_id = db.Column(db.Integer, db.ForeignKey('USER.public_id',ondelete="CASCADE"))
    nurse_id = db.Column(db.Integer, primary_key=True)
    vitals = db.relationship("Vital_Records", backref='nurse')
    
    def __init__(self, other_name, surname, email, birth_date, gender, contact1, contact2, address, qualification):
        self.other_name = other_name
        self.email = email
        self.surname = surname
        self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        self.gender = gender
        self.contact1 = contact1
        self.contact2 = contact2
        self.address = address
        self.qualification = qualification
        
        
        
    @classmethod
    def save(cls, user):
        user.username = f"{(user.other_name)[0]}{user.surname}" 
        passcode = user.password
        user.password_hash = generate_password_hash(passcode)
        temp = f"{(user.other_name)[0]}{user.surname}" 
        User.check_username(user,temp)
        #self.password_hash = generate_password_hash(self.password)
        
        db.session.add(user)
        db.session.commit()
    
    
    