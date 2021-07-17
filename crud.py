from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import models, schemas


# Organization functions
def get_org(db: Session, org_id: int):
    return db.query(models.Org).filter(models.Org.org_ID == org_id).first()

def get_orgs(db: Session, skip: int = 1, limit: int = 100):
    return db.query(models.Org).offset(skip).limit(limit).all()

def create_org(db: Session, org: schemas.OrgCreate):
    db_org = models.Org(org_name=org.org_name, purpose=org.purpose, org_type=org.org_type, max_bed=org.max_bed)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def get_careteams_of_org(db: Session, org_id: int):
    return db.query(models.user_details,models.Care_team).join(models.Care_team, full = True).filter(models.user_details.org_id == org_id).filter(models.user_details.entity_type == "C").all()

def get_patients_of_org(db: Session, org_id: int):
    return db.query(models.user_details,models.Patient).join(models.Patient, full = True).filter(models.user_details.org_id == org_id).filter(models.user_details.entity_type == "Practitioner").all()

def get_practitioners_of_org(db: Session, org_id: int):
    return db.query(models.user_details,models.Practitioner).join(models.Practitioner, full = True).filter(models.user_details.org_id == org_id).filter(models.user_details.entity_type == "Patient").all()


# Beds functions
def get_beds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.beds).offset(skip).limit(limit).all()

def get_beds_of_patient(db: Session, patient_id: int):
    return db.query(models.beds).filter(models.beds.alloted_to == patient_id).all()
def get_bed_by_id(db: Session, bed_id: int):
    return db.query(models.beds).filter(models.beds.id == bed_id).all()




def create_bed(db: Session, bed: schemas.BedCreate):
    db_bed = models.beds(alloted_to=bed.alloted_to, org_ID=bed.org_ID)
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed
import json
# User Details functions 
def create_user(db: Session, user: schemas.userCreate):
    temp = user.dict()
    db_obj = models.user_details(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_user(db: Session, user_id: int):
    return db.query(models.user_details).filter(models.user_details.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user_details).offset(skip).limit(limit).all()

# Practitioner

def create_practitioner(db: Session, practitioner: schemas.PractitionerBase):
    temp = practitioner.dict()
    db_obj = models.Practitioner(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_practitioner(db: Session, practitioner_id: int):
    return db.query(models.practitioner).filter(models.practitioner.practitioner_id == practitioner_id).first()

def get_practitioners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.practitioner).offset(skip).limit(limit).all()

# Patient
def create_patient(db: Session, Patient: schemas.PatientBase):
    temp = Patient.dict()
    db_obj = models.Patient(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

# Care-Team

def create_careteam(db: Session, careteam: schemas.CareTeamBase):
    temp = careteam.dict()
    db_obj = models.Care_team(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_careteam(db: Session, careteam_id: int):
    return db.query(models.Care_team,models.user_details).join(models.user_details,full=True).filter(models.Care_team.careteam_id == careteam_id).first()
    

def get_careteams(db: Session, org_id:int , skip: int = 0, limit: int = 100):
    return db.query(models.Care_team).offset(skip).limit(limit).all()



# Admin
def create_admin(db: Session, admin: schemas.AdminBase):
    temp = admin.dict()
    db_obj = models.admin(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_admin(db: Session, admin_id: int):
    return db.query(models.admin).filter(models.admin.admin_id == admin_id).first()

def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.admin).offset(skip).limit(limit).all()

# Appointment
def create_appointment(db: Session, appointment: schemas.AppointmentBase):
    temp = appointment.dict()
    db_obj = models.Appointment(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_appointment_of_patient(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()

def get_appointment_of_practitioner(db: Session, practitioner_id: int):
    return db.query(models.Appointment).filter(models.Appointment.practitioner_id == practitioner_id).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.appointment_id == appointment_id).first()

def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()

# Immunization
def create_immunization(db: Session, Immunization: schemas.ImmunizationBase):
    temp = Immunization.dict()
    db_obj = models.Immunization(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_immunization(db: Session, immunization_id: int):
    return db.query(models.Immunization).filter(models.Immunization.immunization_id == immunization_id).first()

def get_immunization_of_patient(db: Session, patient_id: int):
    return db.query(models.Immunization).filter(models.Immunization.patient_id == patient_id).all()



def get_immunizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Immunization).offset(skip).limit(limit).all()

# Observation 
def create_observation(db: Session, Observation: schemas.ObservationBase):
    temp = Observation.dict()
    db_obj = models.Observation(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_observation(db: Session, observation_id: int):
    return db.query(models.Observation).filter(models.Observation.observation_id == observation_id).first()

def get_observation_of_patient(db: Session, patient_id: int):
    return db.query(models.Observation).filter(models.Observation.patient_id == patient_id).all()


def get_observations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Observation).offset(skip).limit(limit).all()

# Procedure

def create_procedure(db: Session, Procedure: schemas.ProcedureBase):
    temp = Procedure.dict()
    db_obj = models.Procedure(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_procedure(db: Session, procedure_id: int):
    return db.query(models.Procedure).filter(models.Procedure.procedure_id == procedure_id).first()

def get_procedure_of_patient(db: Session, patient_id: int):
    return db.query(models.Procedure).filter(models.Procedure.patient_id == patient_id).all()


def get_procedures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Procedure).offset(skip).limit(limit).all()

# Allergy 
def create_allergy(db: Session, Allergy: schemas.AllergyBase):
    temp = Allergy.dict()
    db_obj = models.Allergy(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_allergy(db: Session, allergy_id: int):
    return db.query(models.Allergy).filter(models.Allergy.allergy_id == allergy_id).first()

def get_allergy_of_patient(db: Session, patient_id: int):
    return db.query(models.Allergy).filter(models.Allergy.patient_id == patient_id).all()

def get_allergies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Allergy).offset(skip).limit(limit).all()

# Report
def create_report(db: Session, Report: schemas.ReportBase):
    temp = Report.dict()
    db_obj = models.Report(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_report(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.report_id == report_id).first()

def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Report).offset(skip).limit(limit).all()

# Medication
def create_medication(db: Session, Medication: schemas.MedicationBase):
    temp = Medication.dict()
    db_obj = models.Medication(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_medication(db: Session, medication_id: int):
    return db.query(models.Medication).filter(models.Medication.medication_id == medication_id).first()

def get_medication_of_patient(db: Session, patient_id: int):
    return db.query(models.Medication).filter(models.Medication.patient_id == patient_id).all()

def get_medications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Medication).offset(skip).limit(limit).all()

# Statement
def create_statement(db: Session, Statement: schemas.StatementBase):
    temp = Statement.dict()
    db_obj = models.Statement(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_statement(db: Session, statement_id: int):
    return db.query(models.Statement).filter(models.Statement.statement_id == statement_id).first()

def get_statement_of_patient(db: Session, patient_id: int):
    return db.query(models.Statement).filter(models.Statement.patient_id == patient_id).all()

def get_statements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Statement).offset(skip).limit(limit).all()

# BMI
def create_bmi(db: Session, BMI: schemas.BMIBase):
    temp = BMI.dict()
    db_obj = models.BMI(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_bmi(db: Session, bmi_id: int):
    return db.query(models.BMI).filter(models.BMI.bmi_id == bmi_id).first()
def get_bmi_of_patient(db: Session, patient_id: int):
    return db.query(models.BMI).filter(models.BMI.patient_id == patient_id).all()

def get_bmis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BMI).offset(skip).limit(limit).all()

# Problem
def create_problem(db: Session, Problem: schemas.ProblemBase):
    temp = Problem.dict()
    db_obj = models.Problem(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_problem(db: Session, problem_id: int):
    return db.query(models.Problem).filter(models.Problem.problem_id == problem_id).first()
def get_problem_of_patient(db: Session, patient_id: int):
    return db.query(models.Problem).filter(models.Problem.patient_id == patient_id).all()

def get_problems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Problem).offset(skip).limit(limit).all()

# Family_history
def create_family_history(db: Session, Family_history: schemas.FamilyHistoryBase):
    temp = Family_history.dict()
    db_obj = models.Family_history(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_family_history(db: Session, familyhistory_id: int):
    return db.query(models.Family_history).filter(models.Family_history.familyhistory_id == familyhistory_id ).first()
    
def get_family_history_of_patient(db: Session, patient_id: int):
    return db.query(models.Family_history).filter(models.Family_history.patient_id == patient_id ).all()

def get_family_histories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Family_history).offset(skip).limit(limit).all()

# Invoice
def create_earning(db: Session, earning: schemas.HospitalEarningBase):
    temp = earning.dict()
    db_obj = models.hospital_earning(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_earning(db: Session, earning_id: int):
    return db.query(models.hospital_earning).filter(models.hospital_earning.earning_id == earning_id).first()
    
def get_earnings_of_org(db: Session, org_id: int):
    return db.query(models.hospital_earning).filter(models.hospital_earning.org_id == org_id).all()

# def get_invoices(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.invoice).offset(skip).limit(limit).all()

# Logs
def create_log(db: Session, logs: schemas.LogsBase):
    temp = logs.dict()
    db_obj = models.logs(**temp)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
def get_log(db: Session, log_id: int):
    return db.query(models.logs).filter(models.logs.log_id == log_id).first()
    
def get_log_of_patient(db: Session, patient_id: int):
    return db.query(models.logs).filter(models.logs.patient_id == patient_id).all()

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.logs).offset(skip).limit(limit).all()


# Analytics

def group_careteam_by_department_of_org(db: Session, org_id:int , skip: int = 0, limit: int = 100):
    return db.query(models.Care_team.department,func.count(models.Care_team.department)).join(models.user_details, full = True).filter(models.user_details.org_id == org_id).filter(models.user_details.entity_type == "CareTeam").group_by(models.Care_team.department).all()

def group_practitioner_by_department_of_org(db: Session, org_id:int , skip: int = 0, limit: int = 100):
    return db.query(models.Practitioner.department,func.count(models.Practitioner.department)).join(models.user_details, full = True).filter(models.user_details.org_id == org_id).filter(models.user_details.entity_type == "Practitioner").group_by(models.Practitioner.department).all()

def group_patients_by_gender_of_org(db: Session, org_id:int , skip: int = 0, limit: int = 100):
    return db.query(models.user_details.gender,func.count(models.user_details.gender)).filter(models.user_details.org_id == org_id).filter(models.user_details.entity_type == "Patient").group_by(models.user_details.gender).all()

def group_entities_of_org(db: Session, org_id:int , skip: int = 0, limit: int = 100):
    return db.query(models.user_details.entity_type,func.count(models.user_details.entity_type)).filter(models.user_details.org_id == org_id).group_by(models.user_details.entity_type).all()


def get_beds_of_org(db: Session, org_id: int):
    return db.query(models.beds.is_occupied, func.count(models.beds.is_occupied)).filter(models.beds.org_ID == org_id).filter(models.beds.is_occupied == "True").group_by(models.beds.is_occupied).all()

def get_earning_of_org(db: Session, org_id: str):
    return db.query(models.hospital_earning).filter(models.hospital_earning.org_id == org_id).all()
