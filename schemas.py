from typing import List, Optional
from pydantic import BaseModel

class OrgBase(BaseModel):
    org_name: str
    purpose: str
    org_type: str
class OrgCreate(OrgBase):
    pass
class Org(OrgBase):
    org_ID: int
    class Config:
        orm_mode = True

class BedBase(BaseModel):
    alloted_to: str
    org_name: str
class BedCreate(BedBase):
    pass
class Bed(BedBase):
    id: int
    is_occupied: bool

# User

class Userbase(BaseModel):
    username : str
    secret : str
    phone : str
    email : str
    entity_type : str
    aadhar : str
    org_id : int
    fullname : str
    address : str
    dob : str
    blood_group : str
    gender : str

class userCreate(Userbase):
    password : str
class User(Userbase):
    user_id : int
    class Config:
        orm_mode = True

# Practitioner

class PractitionerBase(BaseModel):
    status : str
    department : str
    photo : str
    user_id : int
class Practitioner(PractitionerBase):
    practitioner_id : int
    class Config:
        orm_mode = True

# Patient

class PatientBase(BaseModel):
    martial_status : str
    communication_language : str
    contact_relationship : str
    contact_name : str
    contact_number : str
    bloodgroup : str
    status : str
    photo : str
    user_id : int
class Patient(PatientBase):
    patient_id = int 
    class Config:
        orm_mode = True

# Care Team

class CareTeamBase(BaseModel):
    status : str 
    department : str
    photo : str
    user_id : str
class CareTeam(CareTeamBase):
    careteam_id : int
    class Config:
        orm_mode = True

# Admin

class AdminBase(BaseModel):
    status : str
    photo : str
    user_id : str
class Admin(AdminBase):
    admin_id : int
    class Config:
        orm_mode = True

class AppointmentBase(BaseModel):
    appointment_type : str
    practitioner_id : int
    patient_id  : int
    cancelation_reason : str
    participant_required : str
    participant_type : str
    reason_code : str
    service_category : str
    service_type : str
    specialty : str
    status : str
class Appointment(AppointmentBase):
    appointment_id : int
    class Config:
        orm_mode = True

class ImmunizationBase(BaseModel):
    patient_id  : int
    funding_source : str
    performer_function : str
    program_eligibility : str
    reason_code : str
    report_origin : str
    route : str
    site : str
    status : str
    status_reason : str
    subpotent_reason : str
    target_disease : str
    vaccine_code : str
class Immunization(ImmunizationBase):
    immunization_id : int
    class Config:
        orm_mode = True

class ObservationBase(BaseModel):
    practitioner_id : int
    patient_id  : int
    applies_to : str
    body_site : str
    category : str
    component_interpretation : str
    component_code : str
    data_absent_reason : str
    method : str
    status : str
    observation_type : str
class Observation(ObservationBase):
    observation_id  : int
    class Config:
        orm_mode = True

class ProcedureBase(BaseModel):
    category : str
    code : str
    complication : str
    focal_device_action : str
    follow_up : str
    outcome : str
    performer_function : str
    reason_code : str
    status : str
    status_reason : str
    used_code : str
    practitioner_id : int
    patient_id  : int
class Procedure(ProcedureBase):
    procedure_id : int
    class Config:
        orm_mode = True


class AllergyBase(BaseModel):
    patient_id : int
    category : str
    clinical_status : str
    criticality : str
    purpose : str
    reaction_exposure_route : str
    reaction_manifestation : str
    reaction_substance : str
    verification_status : str
    code : str
class Allergy(AllergyBase):
    allergy_id  : int
    class Config:
        orm_mode = True



class ReportBase(BaseModel):
    practitioner_id : int
    patient_id  : int
    code : str
    conclusion_code: str
    category : str
    status : str
class Report(ReportBase):
    report_id : int
    class Config:
        orm_mode = True


class MedicationBase(BaseModel):
    code : str
    form : str
    status : str
    patient_id : int
    
class Medication(MedicationBase):
    medication_id : int
    class Config:
        orm_mode = True

class StatementBase(BaseModel):
    category : str
    medications : str
    reason_code : str
    status : str
    status_reasons : str
    patient_id  : int
class Statement(StatementBase):
    statement_id : int
    class Config:
        orm_mode = True

    
class BMIBase(BaseModel):
    patient_id  : int
    date : str
    height : str
    weight : str
    blood_pressure : str
class BMI(BMIBase):
    bmi_id : int
    class Config:
        orm_mode = True


class ProblemBase(BaseModel):
    patient_id  : int
    body_site : str
    category : str
    clinical_status : str
    code : str
    evidence_code : str
    reaction_severity : str
    severity : str
    stage_summary : str
    stage_type : str
    verification_status : str
class Problem(ProblemBase):
    problem_id : int
    class Config:
        orm_mode = True


class FamilyHistoryBase(BaseModel):
    patient_id  : str
    condition_code : str
    condition_outcome : str
    data_absent_reason : str
    reason_code : str
    relationship : str
    sex : str
    status : str
class FamilyHistory(FamilyHistoryBase):
    familyhistory_id : int
    class Config:
        orm_mode = True



class InvoiceBase(BaseModel):
    patient_id  : int
    description : str
    unit_cost : str
    quantity : str
class Invoice(InvoiceBase):
    invoice_id : str
    class Config:
        orm_mode = True

class LogsBase(BaseModel):
    description : str
    patient_id  : str
    performer_id  : str
class Logs(LogsBase):
    log_id : int
    class Config:
        orm_mode = True