from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

class Org(Base):
    __tablename__ = "org"
    org_ID = Column(Integer, primary_key=True, index=True)
    org_name = Column(String, unique=True, nullable=False)
    purpose = Column(String)
    org_type = Column(String)
    
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
    photo = Column(String)
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False)

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
    photo = Column(String)
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False)

class Care_team(Base):
    __tablename__ = "care_team"
    careteam_id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    department = Column(String)
    photo = Column(String)
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False)

class admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    photo = Column(String)
    user_id = Column(Integer, ForeignKey("user_details.user_id"), nullable=False)

class Immunization(Base):
    __tablename__ = "immunization"
    immunization_id = Column(Integer, primary_key=True, index=True)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    funding_source = Column(String)
    performer_function = Column(String)
    program_eligibility = Column(String)
    reason_code = Column(String)
    report_origin = Column(String)
    route = Column(String)
    site = Column(String)
    status = Column(String)
    status_reason = Column(String)
    subpotent_reason = Column(String)
    target_disease = Column(String)
    vaccine_code = Column(String)

class Observation(Base):
    __tablename__ = "observation"
    observation_id  = Column(Integer, primary_key=True, index=True)
    practitioner_id = Column(Integer, ForeignKey("practitioner.practitioner_id"), nullable=False)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    applies_to = Column(String)
    body_site = Column(String)
    category = Column(String)
    component_interpretation = Column(String)
    component_code = Column(String)
    data_absent_reason = Column(String)
    method = Column(String)
    status = Column(String)
    observation_type = Column(String)

class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(Integer, primary_key=True, index=True)
    appointment_type = Column(String)
    practitioner_id = Column(Integer, ForeignKey("practitioner.practitioner_id"), nullable=False)
    patient_id  = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    cancelation_reason = Column(String)
    participant_required = Column(String)
    participant_type = Column(String)
    reason_code = Column(String)
    service_category = Column(String)
    service_type = Column(String)
    specialty = Column(String)
    status = Column(String)