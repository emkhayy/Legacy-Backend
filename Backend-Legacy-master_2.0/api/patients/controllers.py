from pydoc import doc
from flask import request
from flask_restx import Resource, Namespace
from api.extensions import db
from api.patients.models import Patients, Vital_Records, Diagnosis_Records, Appointment
from werkzeug.exceptions import BadRequest, abort
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.constants.http_status_code import *

patient_ns = Namespace("patients", description="Patient-related Authentications")

from api.patients.schema import PatientLoad, PatientDump, Patient_Vital_Load, Patient_Vital_Dump, PatientsDump, Patient_Diagnosis_Dump, Patient_Diagnosis_Load, Patient_appointment, searchLoad



@patient_ns.route('/')
class PatientsResource(Resource):
    # @doc(summary="Register new patient")
    @patient_ns.expect(PatientLoad)
    @patient_ns.marshal_with(PatientDump)
    # @jwt_required()
    def post(self):
        """Create new patient"""
        data = request.get_json()
        email = data.get('email')
        date_obj = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()
        
        db_patient = Patients.query.filter_by(email=email).first()
        if db_patient:
            abort(HTTP_409_CONFLICT, f"Patient with email '{email}' already exist")
        new_patient = Patients(
            surname=data.get('surname'),
            other_names=data.get('other_names'),
            email=data.get('email'),
            gender=data.get('gender'),
            date_of_birth=date_obj,
            address=data.get('address'),
            contact1=data.get('contact1'),
            contact2=data.get('contact2'),
        )
        
        db.session.add(new_patient)
        db.session.commit()
        
        return new_patient
        
    # @doc(summay="Get all patients")
    @patient_ns.marshal_list_with(PatientsDump)
    # @jwt_required()
    def get(self):
        """Get all patients"""
        
        patients = Patients.query.all()
        return patients
    

    

@patient_ns.route('/<int:id>')
class PatientResource(Resource):
    @patient_ns.marshal_with(PatientDump)
    # @jwt_required()
    # @doc(summay="Get a patient with id")
    def get(self, id):
        """Get patient's by id"""
        
        patient = Patients.query.get_or_404(id)
         
        if patient:
             return patient 
         
          
        abort(HTTP_404_NOT_FOUND, "Patient not found")
    
    # @doc(summay="Delete a patients with")    
    def delete(self, id):
        """Delete patient by id"""
        patient = Patients.query.get(id)
         
        if patient:
        # Delete the patient instance
            db.session.delete(patient)
            db.session.commit()

            return {"message": "Patient deleted successfully"}, HTTP_200_OK
        abort(HTTP_404_NOT_FOUND, "Patient not found")
    
    @patient_ns.expect(PatientLoad)
    @patient_ns.marshal_with(PatientDump)    
    def put(self, id):
        """Update patient's info by id """
        
        patient = Patients.query.get_or_404(id)
        
        if patient:
            data = request.get_json()
            for attr, value in data.items():
                if attr== "date_of_birth":
                    value = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()
                setattr(patient, attr, value)
                
            db.session.commit()
            
            return patient
        abort(404, "Patient not found")
        
        
@patient_ns.route('/vital/<int:id>')
class VitalResource(Resource):
    @patient_ns.marshal_list_with(Patient_Vital_Dump)
    def get(self, id):
        """Get all vitals of patient's by id"""
        patient_to_record = Patients.query.filter_by(patient_id =id).first()
        if patient_to_record:
            vitals = Vital_Records.query.filter_by(patient_id=id).all()
        
            if vitals:
                return vitals
            abort(404, "No Vitals available")
        abort(404, f"No such patient with the id {id} is available")
        
    @patient_ns.expect(Patient_Vital_Load)
    @patient_ns.marshal_with(Patient_Vital_Dump) 
    # @jwt_required()  
    def post(self, id):
        """Record patient's vital by id"""
        patient_to_record = Patients.query.filter_by(patient_id =id).first()
        
        if patient_to_record:
            data = request.get_json()
            
            new_vitals = Vital_Records(
                patient_id=id,
                temperature=data.get('temperature'),
                height=data.get('height'),
                bloodpressure_mm=data.get('bloodpressure_mm'),
                bloodpressure_Hg=data.get('bloodpressure_Hg'),
                weight=data.get('weight'),
                keeper_id = 1#get_jwt_identity()  
            )

            db.session.add(new_vitals)
            db.session.commit()
        #new code added please check the conditions(Victor)
            patient_to_record.to_be_attended = True

            person = Appointment(
            person_id = id,
            surname =  patient_to_record.surname,
            other_names =  patient_to_record.other_names,
            gender = patient_to_record.gender
            )

            db.session.add(person)
            db.session.commit()


            return new_vitals 
        abort(HTTP_404_NOT_FOUND, f"No such patient with the id {id} is available")
        
    
@patient_ns.route('/appoint')
class AppointmentResource(Resource):
    @patient_ns.marshal_with(Patient_appointment) 
    # @jwt_required()  
    def get(self):
        """Book an appointment"""
        appointment = Appointment.query.all()
        return appointment
    
        
        
 
 
@patient_ns.route('/diagnosis/<int:id>')
class DiagnosisResource(Resource):
    @patient_ns.marshal_list_with(Patient_Diagnosis_Dump)
    def get(self, id):
        """Record patient's diagnosis by id"""
        patient_to_record = Patients.query.filter_by(patient_id =id).first()
        if patient_to_record:
            diagnosis = Diagnosis_Records.query.filter_by(patient_id=id).all()
        
            if diagnosis:
                return diagnosis
            abort(404, "No Diagnosis available")
        abort(404, f"No such patient with the id {id} is available")
        
    @patient_ns.expect(Patient_Diagnosis_Load)
    @patient_ns.marshal_with(Patient_Diagnosis_Dump)    
    # @jwt_required()
    def post(self, id):
        """Record patient's diagnosis by id"""
        patient_to_record = Patients.query.filter_by(patient_id =id).first()
        patient_to_delete = Appointment.query.filter_by(person_id=id).first()
        
        if patient_to_record:
            data = request.get_json()
            
            new_diagnosis = Diagnosis_Records(
                symptoms=data.get("symptoms"),
                diagnosis=data.get("diagnosis"),
                prescription=data.get("prescription"),
                keeper_id=14,#get_jwt_identity(),
                patient_id=id   
            )
            
            if patient_to_delete:
                db.session.delete(patient_to_delete)
            
            db.session.add(new_diagnosis)
            db.session.commit()
            
            return new_diagnosis, HTTP_200_OK 
        abort(404, f"No such patient with the id {id} is available")
        
        
@patient_ns.route('/search')
class SearchResource(Resource):
    @patient_ns.expect(searchLoad)
    @patient_ns.marshal_list_with(PatientDump)
    def post(self):
        data = request.get_json()
        subtr = data.get('data')
        column = data.get('column_name')
        stri = f"%{subtr}%"
        if column == "surname":
            res = Patients.query.filter(Patients.surname.ilike(stri)).all()
        elif column == "other_names":
            res = Patients.query.filter(Patients.other_names.ilike(stri)).all()
        elif column == 'email':
            res = Patients.query.filter(Patients.email.like(stri)).all()
        elif column == 'address':
            res = Patients.query.filter(Patients.address.like(stri)).all()
        else:
            return abort(HTTP_400_BAD_REQUEST, "No such column")
            
        return res, HTTP_200_OK
        
        