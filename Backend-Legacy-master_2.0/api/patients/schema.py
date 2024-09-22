from email.policy import default
from flask_restx import fields
from api.patients.controllers import patient_ns

PatientsDump = patient_ns.model(
    "List of Patients",
    {
        "patient_id":fields.Integer(),
        "surname": fields.String(),
        "other_names": fields.String(),
        "gender": fields.String()
    }
)


PatientLoad = patient_ns.model(
    "Patient_Request_Info",
    {
        "surname": fields.String(),
        "other_names": fields.String(),
        "email": fields.String(),
        "gender": fields.String(),
        "date_of_birth":fields.Date(),
        "address": fields.String(),
        "contact1": fields.String(),
        "contact2": fields.String(default="None"),
        
    }
)

PatientDump = patient_ns.model(
    "Patient_Response_Info",
    {
        "patient_id":fields.Integer(),
        "surname": fields.String(),
        "other_names": fields.String(),
        "email": fields.String(),
        "gender": fields.String(),
        "date_of_birth":fields.Date(),
        "address": fields.String(),
        "contact1": fields.String(),
        "contact2": fields.String(default="None"),
        "date_registered": fields.Date()
    }
)


Patient_Vital_Load = patient_ns.model(
    "Vitals_request_Info",
    {
        "temperature":fields.Float(),
        "height": fields.Float(),
        "bloodpressure_mm": fields.Float(),
        "bloodpressure_Hg": fields.Float(),
        "weight":fields.Float()
    }
)


Patient_Vital_Dump = patient_ns.model(
    "Vitals_Response_Info",
    {
        "record_id":fields.Integer(),
        "patient_id":fields.Integer(),
        "temperature":fields.Float(),
        "height": fields.Float(),
        "bloodpressure_mm": fields.Float(),
        "bloodpressure_Hg": fields.Float(),
        "weight": fields.Float(),
        "keeper_id":fields.Integer(),
        "date_recorded": fields.Date()
    }
)

Patient_Diagnosis_Load = patient_ns.model(
    "Diagnosis_Request_Info",
    {
        "symptoms":fields.String(),
        "diagnosis":fields.String(),
        "prescription":fields.String()
    }
)

Patient_Diagnosis_Dump = patient_ns.model(
    "Diagnosis_Response_Info",
    {
        "id":fields.Integer(),
        "patient_id":fields.Integer(),
        "symptoms":fields.String(),
        "diagnosis":fields.String(),
        "prescription":fields.String(),
        "keeper_id":fields.Integer(),
        "date_recorded": fields.Date()
    }
)

Patient_appointment = patient_ns.model(
    "AWAITING_LIST",
    {
        "person_id":fields.Integer(),
        "surname":fields.String(),
        "other_names":fields.String(),
        "gender":fields.String()
        
    }
)


searchLoad = patient_ns.model(
    "Search Model",
        {
            'column_name' : fields.String(),
            "data": fields.String(),
        }
)