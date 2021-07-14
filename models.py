from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

class Org(Base):
    __tablename__ = "org"
    org_ID = Column(Integer, primary_key=True, index=True)
    org_name = Column(String, unique=True, nullable=False)
    purpose = Column(String)
    org_type = Column(String)
    max_bed = Column(String)
    
class beds(Base):
    __tablename__ = "beds"
    id = Column(Integer, primary_key=True, index=True)
    alloted_to = Column(String)
    is_occupied = Column(Boolean, default=True)
    org_ID = Column(Integer, ForeignKey("org.org_ID"), nullable=False)

class user_details(Base): 
    __tablename__ = "user_details"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)
    secret = Column(String)
    phone = Column(String)
    email = Column(String)
    entity_type = Column(String)
    aadhar = Column(String, unique=True, nullable=False)
    org_id = Column(Integer, ForeignKey("org.org_ID"), nullable=False)
    fullname = Column(String)
    address = Column(String)
    dob = Column(String)
    blood_group = Column(String)
    gender = Column(String)

class Practitioner(Base):
    __tablename__ = "practitioner"
    practitioner_id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    department = Column(String)
    photo = Column(String, default='https://simplyilm.com/wp-content/uploads/2017/08/temporary-profile-placeholder-1.jpg')
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False, unique=True)

class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(Integer, primary_key=True, index=True)
    martial_status = Column(String)
    communication_language = Column(String)
    contact_relationship = Column(String)
    contact_name = Column(String)
    contact_number = Column(String)
    bloodgroup = Column(String)
    status = Column(String)
    photo = Column(String, default='https://simplyilm.com/wp-content/uploads/2017/08/temporary-profile-placeholder-1.jpg')
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False, unique=True)

class Care_team(Base):
    __tablename__ = "care_team"
    careteam_id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    department = Column(String)
    photo = Column(String, default='https://simplyilm.com/wp-content/uploads/2017/08/temporary-profile-placeholder-1.jpg')
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False, unique=True)

class admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    photo = Column(String, default='https://simplyilm.com/wp-content/uploads/2017/08/temporary-profile-placeholder-1.jpg')
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False, unique=True)

class Immunization(Base):
    __tablename__ = "immunization"
    immunization_id = Column(Integer, primary_key=True, index=True)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    funding_source = Column(String)
    reason_code = Column(String)
    report_origin = Column(String)
    route = Column(String)
    site = Column(String)
    target_disease = Column(String)
    vaccine_code = Column(String)

class Observation(Base):
    __tablename__ = "observation"
    observation_id  = Column(Integer, primary_key=True, index=True)
    practitioner_id = Column(Integer, ForeignKey("practitioner.practitioner_id"), nullable=False)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    body_site = Column(String)
    category = Column(String)
    component_interpretation = Column(String)
    method = Column(String)
    status = Column(String)
    observation_type = Column(String)

class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(Integer, primary_key=True, index=True)
    appointment_type = Column(String)
    practitioner_id = Column(Integer, ForeignKey("practitioner.practitioner_id"), nullable=False)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    participant_type = Column(String)
    reason_code = Column(String)
    specialty = Column(String)
    status = Column(String)
    date = Column(String)
    time = Column(String)

class Procedure(Base):
    __tablename__ = "procedure"
    procedure_id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    code = Column(String)
    complication = Column(String)
    follow_up = Column(String)
    outcome = Column(String)
    reason_code = Column(String)
    status = Column(String)
    status_reason = Column(String)
    used_code = Column(String)
    practitioner_id = Column(Integer, ForeignKey("practitioner.practitioner_id"), nullable=False)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    
class Allergy(Base):
    __tablename__ = "allergy"
    allergy_id  = Column(Integer, primary_key=True, index=True)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    category = Column(String)
    clinical_status = Column(String)
    criticality = Column(String)
    reaction_exposure_route = Column(String)
    reaction_manifestation = Column(String)
    reaction_substance = Column(String)
    
class Report(Base):
    __tablename__ = "report"
    report_id = Column(Integer, primary_key=True, index=True)
    practitioner_id = Column(Integer, ForeignKey("practitioner.practitioner_id"), nullable=False)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    code = Column(String)
    conclusion_code = Column(String)
    category = Column(String)
    status = Column(String)

class Medication(Base):
    __tablename__ = "medication"
    medication_id = Column(Integer, primary_key=True, index=True)
    medicine_name = Column(String)
    form = Column(String)
    status = Column(String)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    
class Statement(Base):
    __tablename__ = "statement"
    statement_id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    medications = Column(String)
    reason_code = Column(String)
    status = Column(String)
    status_reasons = Column(String)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    
class BMI(Base):
    __tablename__ = "bmi"
    bmi_id = Column(Integer, primary_key=True, index=True)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    date =  Column(String)
    height =  Column(String)
    weight =  Column(String)
    blood_pressure = Column(String)
    cholestrol = Column(String)

class Problem(Base):
    __tablename__  = "problem"
    problem_id = Column(Integer, primary_key=True, index=True)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    body_site = Column(String)
    category = Column(String)
    clinical_status = Column(String)
    code = Column(String)
    evidence_code = Column(String)
    reaction_severity = Column(String)
    severity = Column(String)
    

class Family_history(Base):
    __tablename__ = "family_history"
    familyhistory_id = Column(Integer, primary_key=True, index=True)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    condition_code = Column(String)
    condition_outcome = Column(String)
    data_absent_reason = Column(String)
    reason_code = Column(String)
    relationship = Column(String)
    sex = Column(String)
    status = Column(String)
    
class invoice(Base):
    __tablename__ = "invoice"
    invoice_id = Column(Integer, primary_key=True, index=True)
    org_id = Column(String)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    invoice_details = Column(String)
    total_amount = Column(String)
    date = Column(String)
    time = Column(String)
    
# class Schedule(Base):
#     pass
class logs(Base):
    __tablename__ = "logs"
    log_id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    patient_id  = Column(Integer, ForeignKey("user_details.user_id"), nullable=False)
    performer_id  = Column(Integer, ForeignKey("user_details.user_id"), nullable=False)