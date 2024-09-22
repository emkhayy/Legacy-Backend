from tabnanny import check
from api.extensions import db
#from api.users.models import User
from datetime import datetime


"""patient_id(primary_key)
surname
other_name
email
gender
date_of_birth
address
contact1
contact2
date_registered
"""
class Patients(db.Model):
    __tablename__= "PATIENT"
    patient_id = db.Column(db.Integer, primary_key = True)
    surname = db.Column(db.String(255), nullable = False)
    other_names = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    gender  = db.Column(db.String(255), nullable = False)
    date_of_birth = db.Column(db.DateTime, nullable = False)
    address = db.Column(db.String(255), nullable = False)
    contact1 = db.Column(db.String(255), nullable = False)
    contact2 = db.Column(db.String(255), nullable = True, default ='NULL')
    vitals = db.relationship('Vital_Records', backref="patient")
    to_be_attendend = db.Column(db.Boolean, nullable = False, default = False)
    date_registered = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self,surname,other_names,email,gender,date_of_birth,address,contact1,contact2):
        #self.patient_id = patient_id
        self.surname= surname
        self.other_names =  other_names
        self.email = email
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.address = address
        self.contact1 = contact1
        self.contact2 = contact2

    def serializable(self):
        return{'patient_id' : self.patient_id,
                'surname' : self.surname,
                'other_names' : self.other_names,
                'email' : self.email,
                'gender': self.gender,
                'date_of_birth': self.date_of_birth,
                'address' : self.address,
                'contact1': self.contact1,
                'contact2' : self.contact2,
                'date_registered' : self.date_registered}

"""
temperature
Weight
height
blood pressure
date_created
keeper_id
patient_id(relate: foriegn key)
"""
class Vital_Records(db.Model):
    __tablename__= "VITAL RECORDS"
    record_id= db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey("PATIENT.patient_id",ondelete="CASCADE"))
    temperature = db.Column(db.Numeric)
    weight = db.Column(db.Numeric) 
    height = db.Column(db.Numeric)
   # blood_pressure = db.Column(db.Numeric)
    bloodpressure_mm = db.Column(db.Numeric) #unit in mm
    bloodpressure_Hg = db.Column(db.Numeric) #unit in Hg 
    keeper_id = db.Column(db.Integer, db.ForeignKey("USER.public_id" , ondelete="CASCADE"))
    date_recorded = db.Column(db.DateTime, default= datetime.utcnow())
    
#    keeper_id = db.Column(db.String())

    def __init__(self,patient_id,temperature,weight,height,bloodpressure_mm,bloodpressure_Hg,keeper_id):
        self.patient_id = patient_id
        self.temperature = temperature
        self.weight = weight
        self.height = height
        self.bloodpressure_mm = bloodpressure_mm 
        #self.BloodPressure_mm = BloodPressure_mm
        self.bloodpressure_Hg = bloodpressure_Hg
        self.keeper_id = keeper_id

    # def serializable(self):
    #     return{'patient_id' : self.patient_id,
    #             'temperature' : self.temperature,
    #             'weight' : self.weight,
    #             'height' : self.height,
    #             'Blood_pressure': self.blood_pressure,
    #             'keeper_id':self.keeper_id}

"""
Id
diagnosis
patient_id (relate: foriegn key)
keeper_id
date_recorded
"""
class Diagnosis_Records(db.Model):
    __tablename__= "DIAGNOSIS RECORDS"
    id=db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey(Patients.patient_id,ondelete="CASCADE"))
    symptoms = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    keeper_id = db.Column(db.Integer, db.ForeignKey("USER.public_id",ondelete="CASCADE"))
    date_recorded = db.Column(db.DateTime, default= datetime.utcnow())

    # def __init__(self, patient_id, diagnosis, date_recorded, keeper_id):
    #     self.patient_id = patient_id
    #     self.diagnosis = diagnosis
    #     self.keeper_id = keeper_id
    #     self.date_recorded = date_recorded


    # def serializable(self):
    #     return{'patient_id' : self.patient_id,
    #             'diagnosis' : self.diagnosis,
    #             'keeper_id' : self.keeper_id,
    #             'date_recorded' : self.date_recorded}


#new code added created a table (Victor)
class Appointment(db.Model):
    __tablename__ = "PendingList"
    person_id = db.Column(db.Integer,primary_key=True, nullable = False)
    surname = db.Column(db.String(255), nullable = False)
    other_names = db.Column(db.String(255), nullable = False)
    gender = db.Column(db.String(20), nullable = False)
    