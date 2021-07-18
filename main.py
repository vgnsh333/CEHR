from typing import List
from fastapi_login import LoginManager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
import crud, models, schemas
from database import SessionLocal, engine
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

SECRET = "your-secret-key"
app = FastAPI()

origins = ['*']
# remove statment
# REMOVE REPORT 
# Procedure -> remove performerFunction ; focalDeviceAction.csv
# ADD API FOR GETTING BMI OF A SINGLE PATIENT

# return db.query(models.Care_team.department,func.count(models.Care_team.department)).join(models.user_details, full = True).filter(models.user_details.org_id == org_id).filter(models.user_details.entity_type == "C").group_by(models.Care_team.department).all()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
manager = LoginManager(SECRET, token_url='/auth/token')

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@manager.user_loader
def load_user(username: str, db ):  # could also be an asynchronous function
    user = db.query(models.user_details).filter(models.user_details.username == username).first()
    return user
@app.get("/")
async def root():
    return {"message": "Hello! Go to /docs :)"}
@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = data.username
    password = data.password

    user = load_user(username,db)  # we are using the same function to retrieve the user
    print('in auth', user.entity_type)
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user.password:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    if user.entity_type == "Patient":
        print('Patient logged in')
        temp = db.query(models.Patient).filter(models.Patient.user_id == user.user_id).first()
        print('Practitioner logged in',temp.patient_id)
        entity_id = temp.patient_id

    if user.entity_type == "Practitioner":
        temp = db.query(models.Practitioner).filter(models.Practitioner.user_id == user.user_id).first()
        print('Practitioner logged in',temp.practitioner_id)
        entity_id = temp.practitioner_id

    if user.entity_type == "Careteam":
        print('Careteam logged in')
        temp = db.query(models.Care_team).filter(models.Care_team.user_id == user.user_id).first()
        print('ye Practitioner',temp.careteam_id)
        entity_id = temp.careteam_id

    return {'access_token': access_token, 'token_type': 'bearer', 'entity_type' : user.entity_type,
     'user_id' : user.user_id,
     'org_id': user.org_id,
     'entity_id' : entity_id }

# Org

@app.post("/org/add", response_model=schemas.Org, tags=["Organization"])
def create_org(org: schemas.OrgCreate, db: Session = Depends(get_db)):
    print(org)
    temp_obj = db.query(models.Org).filter(models.Org.org_name == org.org_name).first()
    if temp_obj:
        raise HTTPException(status_code=406, detail="Org name taken")
    return crud.create_org(db=db, org=org)


@app.get("/orgs/all", response_model=List[schemas.Org], tags=["Organization"])
def get_all_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orgs(db, skip=skip, limit=limit)

@app.get("/orgs/careteams/{org_id}", tags=["Organization"])
def get_org_careteam(org_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_careteams_of_org(db, org_id=org_id)
    print(len(temp_obj))
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="Org not found")
    return temp_obj

@app.get("/orgs/patients/{org_id}", tags=["Organization"])
def get_patients_of_org(org_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_patients_of_org(db, org_id=org_id)
    print(len(temp_obj))
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="Org not found")
    return temp_obj

@app.get("/orgs/practitioners/{org_id}", tags=["Organization"])
def get_practitioners_of_org(org_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_practitioners_of_org(db, org_id=org_id)
    print(len(temp_obj))
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="Org not found")
    return temp_obj




@app.get("/org/{org_id}", response_model=schemas.Org, tags=["Organization"])
def get_org(org_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_org(db, org_id=org_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="Org not found")
    return temp_obj

# User

@app.post("/user/add", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.userCreate, db: Session = Depends(get_db)):
    temp_obj =db.query(models.user_details).filter(models.user_details.username == user.username).first()
    if temp_obj:
        raise HTTPException(status_code=406, detail="Username name taken")
    temp_obj =db.query(models.user_details).filter(models.user_details.aadhar == user.aadhar).first()
    if temp_obj:
        raise HTTPException(status_code=406, detail="Aadhar already registered")
    temp_obj = crud.get_org(db, org_id=user.org_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="Invalid Organization ID")
    
    return crud.create_user(db=db, user=user)

@app.get("/user/all", response_model=List[schemas.User], tags=["Users"])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/user/{user_id}", response_model=schemas.User, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_user(db, user_id=user_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return temp_obj

# Patient
@app.post("/patient/add", response_model=schemas.Patient, tags=["Patient"])
def create_patient(Patient: schemas.PatientBase, db: Session = Depends(get_db)):
    return crud.create_patient(db, Patient)

@app.get("/patient/all", response_model=List[schemas.Patient], tags=["Patient"])
def get_all_patient(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip=skip, limit=limit)

@app.get("/patient/{patient_id}", response_model=schemas.Patient, tags=["Patient"])
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

# Careteam
@app.post("/careteam/add", response_model=schemas.CareTeam, tags=["Careteam"])
def create_Careteam(CareTeam: schemas.CareTeamBase, db: Session = Depends(get_db)):
    return crud.create_careteam(db ,CareTeam)

@app.get("/careteam/all/{org_id}", response_model=List[schemas.CareTeam], tags=["Careteam"])
def get_all_Careteam(org_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_careteams(db,org_id=org_id, skip=skip, limit=limit)

@app.get("/careteam/{careteam_id}/{org_id}", tags=["Careteam"])
def get_Careteam(careteam_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_careteam(db, careteam_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Practicioner
@app.post("/practitioner/add", response_model=schemas.Practitioner, tags=["Practicioner"])
def create_Practicioner(practitioner: schemas.PractitionerBase, db: Session = Depends(get_db)):
    return crud.create_practitioner(db,practitioner)

@app.get("/practitioner/all", response_model=List[schemas.Practitioner], tags=["Practicioner"])
def get_all_Practicioner(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_practitioners(db, skip=skip, limit=limit)

@app.get("/practitioner/{practitioner_id}", response_model=schemas.Practitioner, tags=["Practicioner"])
def get_Practicioner(practitioner_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_practitioner(db, practitioner_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Admin
@app.post("/admin/add", response_model=schemas.Admin, tags=["Admin"])
def create_admin(admin: schemas.AdminBase, db: Session = Depends(get_db)):
    return crud.create_admin(db, admin)

@app.get("/admin/all", response_model=List[schemas.Admin], tags=["Admin"])
def get_all_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_admins(db, skip=skip, limit=limit)

@app.get("/admin/{admin_id}", response_model=schemas.Admin, tags=["Admin"])
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_admin(db, admin_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Appointment
@app.post("/appointment/add", response_model=schemas.Appointment, tags=["Appointment"])
def create_appointment(appointment: schemas.AppointmentBase, db: Session = Depends(get_db)):
    return crud.create_appointment(db,appointment )

@app.get("/appointment/all", response_model=List[schemas.Appointment], tags=["Appointment"])
def get_all_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_appointments(db, skip=skip, limit=limit)

@app.get("/appointment/of/patient/{patient_id}", response_model=List[schemas.Appointment], tags=["Appointment"])
def get_appointments_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_appointment_of_patient(db,patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/appointment/of/practitioner/{practitioner_id}", response_model=List[schemas.Appointment], tags=["Appointment"])
def get_appointments_of_praticioner(practitioner_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_appointment_of_practitioner(db,practitioner_id)
    print('HELLO')
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj



@app.get("/appointment/{appointment_id}", response_model=schemas.Appointment, tags=["Appointment"])
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_appointment(db,appointment_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Immunization
@app.post("/immunization/add", response_model=schemas.Immunization, tags=["Immunization"])
def create_immunization(Immunization: schemas.ImmunizationBase, db: Session = Depends(get_db)):
    return crud.create_immunization(db, Immunization)

@app.get("/immunization/all", response_model=List[schemas.Immunization], tags=["Immunization"])
def get_all_immunizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_immunizations(db, skip=skip, limit=limit)

@app.get("/immunization/{immunization_id}", response_model=schemas.Immunization, tags=["Immunization"])
def get_immunization(immunization_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_immunization(db, immunization_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/immunization/of/{patient_id}", response_model=List[schemas.Immunization], tags=["Immunization"])
def get_immunizations_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_immunization_of_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Observation
@app.post("/observation/add", response_model=schemas.Observation, tags=["Observation"])
def create_observation(Observation: schemas.ObservationBase, db: Session = Depends(get_db)):
    return crud.create_observation(db, Observation)

@app.get("/observation/all", response_model=List[schemas.Observation], tags=["Observation"])
def get_all_observation(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_observations(db, skip=skip, limit=limit)

@app.get("/observation/{observation_id}", response_model=schemas.Observation, tags=["Observation"])
def get_observation(observation_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_observation(db,observation_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
@app.get("/observation/of/{patient_id}", response_model=List[schemas.Observation], tags=["Observation"])
def get_observations_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_observation_of_patient(db,patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Procedure
@app.post("/procedure/add", response_model=schemas.Procedure, tags=["Procedure"])
def create_procedure(Procedure: schemas.ProcedureBase, db: Session = Depends(get_db)):
    return crud.create_procedure(db, Procedure)

@app.get("/procedure/all", response_model=List[schemas.Procedure], tags=["Procedure"])
def get_all_procedures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_procedures(db, skip=skip, limit=limit)

@app.get("/procedure/{procedure_id}", response_model=schemas.Procedure, tags=["Procedure"])
def get_procedure(procedure_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_procedure(db, procedure_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/procedure/of/{patient_id}", response_model=List[schemas.Procedure], tags=["Procedure"])
def get_procedures_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_procedure_of_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Allergy
@app.post("/allergy/add", response_model=schemas.Allergy, tags=["Allergy"])
def create_allergy(Allergy: schemas.AllergyBase, db: Session = Depends(get_db)):
    return crud.create_allergy(db, Allergy)

@app.get("/allergy/all", response_model=List[schemas.Allergy], tags=["Allergy"])
def get_all_allergy(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_allergies(db, skip=skip, limit=limit)

@app.get("/allergy/{allergy_id}", response_model=schemas.Allergy, tags=["Allergy"])
def get_allergy(allergy_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_allergy(db, allergy_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/allergy/of/{patient_id}", response_model=List[schemas.Allergy], tags=["Allergy"])
def get_allergy_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_allergy_of_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Report
# @app.post("/report/add", response_model=schemas.Report, tags=["Report"])
# def create_report(Report: schemas.ReportBase, db: Session = Depends(get_db)):
#     return crud.create_report(db,Report)

# @app.get("/report/all", response_model=List[schemas.Report], tags=["Report"])
# def get_all_report(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.get_reports(db, skip=skip, limit=limit)

# @app.get("/report/{report_id}", response_model=schemas.Report, tags=["Report"])
# def get_report(report_id: int, db: Session = Depends(get_db)):
#     temp_obj = crud.get_report(db, report_id)
#     if temp_obj is None:
#         raise HTTPException(status_code=404, detail=" not found")
#     return temp_obj
# Medication
@app.post("/medication/add", response_model=schemas.Medication, tags=["Medication"])
def create_medication(Medication: schemas.MedicationBase, db: Session = Depends(get_db)):
    return crud.create_medication(db,Medication)

@app.get("/medication/all", response_model=List[schemas.Medication], tags=["Medication"])
def get_all_medication(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_medications(db, skip=skip, limit=limit)

@app.get("/medication/by/{medication_id}", response_model=List[schemas.Medication], tags=["Medication"])
def get_medication(medication_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_medication(db,medication_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/medication/of/patient/{patient_id}", response_model=List[schemas.Medication], tags=["Medication"])
def get_medication_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_medication_of_patient(db,patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Statement
@app.post("/statement/add", response_model=schemas.Statement, tags=["Statement"])
def create_statement(Statement: schemas.StatementBase, db: Session = Depends(get_db)):
    return crud.create_statement(db,Statement)

@app.get("/statement/all", response_model=List[schemas.Statement], tags=["Statement"])
def get_all_statement(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_statements(db, skip=skip, limit=limit)

@app.get("/statement/by/{statement_id}", response_model=schemas.Statement, tags=["Statement"])
def get_statement(statement_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_statement(db,statement_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/statement/of/{patient_id}", response_model=List[schemas.Statement], tags=["Statement"])
def get_statement_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_statement_of_patient(db,patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# BMI
@app.post("/bmi/add", response_model=schemas.BMI, tags=["BMI"])
def create_bmi(BMI: schemas.BMIBase, db: Session = Depends(get_db)):
    return crud.create_bmi(db,BMI)

@app.get("/bmi/all", response_model=List[schemas.BMI], tags=["BMI"])
def get_all_bmi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bmis(db, skip=skip, limit=limit)

@app.get("/bmi/by/{bmi_id}", response_model=schemas.BMI, tags=["BMI"])
def get_bmi(bmi_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_bmi(db, bmi_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/bmi/of/{patient_id}", response_model=List[schemas.BMI], tags=["BMI"])
def get_bmi_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_bmi_of_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Problem
@app.post("/problem/add", response_model=schemas.Problem, tags=["Problem"])
def create_problem(Problem: schemas.ProblemBase, db: Session = Depends(get_db)):
    return crud.create_problem(db,Problem)

@app.get("/problem/all", response_model=List[schemas.Problem], tags=["Problem"])
def get_all_problem(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_problems(db, skip=skip, limit=limit)

@app.get("/problem/{problem_id}", response_model=schemas.Problem, tags=["Problem"])
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_problem(db,problem_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/problem/of/{patient_id}", response_model=List[schemas.Problem], tags=["Problem"])
def get_problem_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_problem_of_patient(db,patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Family_history
@app.post("/familyhistory/add", response_model=schemas.FamilyHistory, tags=["Family_history"])
def create_familyhistory(Family_history: schemas.FamilyHistoryBase, db: Session = Depends(get_db)):
    return crud.create_family_history(db, Family_history)

@app.get("/familyhistory/all", response_model=List[schemas.FamilyHistory], tags=["Family_history"])
def get_all_familyhistory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_family_histories(db, skip=skip, limit=limit)

@app.get("/familyhistory/by/{familyhistory_id}", response_model=schemas.FamilyHistory, tags=["Family_history"])
def get_familyhistory(familyhistory_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_family_history(db, familyhistory_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/familyhistory/of/{patient_id}", response_model=List[schemas.FamilyHistory], tags=["Family_history"])
def get_familyhistory_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_family_history_of_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Earning
@app.post("/earning/add", response_model=schemas.HospitalEarning, tags=["Hospital Earning"])
def create_earning(earning: schemas.HospitalEarningBase, db: Session = Depends(get_db)):
    return crud.create_earning(db,earning)


@app.get("/earning/by/{earning_id}", response_model=schemas.HospitalEarning, tags=["Hospital Earning"])
def get_earning_by_id(earning_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_earning(db, earning_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

# Logs
@app.post("/logs/add", response_model=schemas.Logs, tags=["Logs"])
def create_Log(logs: schemas.LogsBase, db: Session = Depends(get_db)):
    return crud.create_log(db, logs)

@app.get("/logs/all", response_model=List[schemas.Logs], tags=["Logs"])
def get_all_Logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_logs(db, skip=skip, limit=limit)

@app.get("/logs/by/{log_id}", response_model=schemas.Logs, tags=["Logs"])
def get_Log(log_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_log(db, log_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/logs/of/{patient_id}", response_model=List[schemas.Logs], tags=["Logs"])
def get_Logs_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_log_of_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

# beds

@app.post("/beds/add",  tags=["Beds"])
def create_bed(bed: schemas.BedCreate, db: Session = Depends(get_db)):
    return crud.create_bed(db, bed)

@app.get("/beds/all", tags=["Beds"])
def get_all_beds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_beds(db, skip=skip, limit=limit)

@app.get("/beds/of/{patient_id}",  tags=["Beds"])
def get_bed_of_patient(patient_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_beds_of_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

@app.get("/beds/by/{bed_id}", tags=["Beds"])
def get_bed_by_ID(bed_id: int, db: Session = Depends(get_db)):
    temp_obj = crud.get_bed_by_id(db, bed_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

# Hospital Analytics

@app.get("/analytics/status/beds/{org_id}",  tags=["analytics"])
def get_occupied_beds_of_org(org_id: int, db: Session = Depends(get_db)):
    return crud.get_beds_of_org(db, org_id)


@app.get("/analytics/stats/department/careteam/{org_id}",  tags=["analytics"])
def group_careteam_by_department_of_org(org_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.group_careteam_by_department_of_org(db, org_id, skip=skip, limit=limit)


@app.get("/analytics/stats/department/practitioner/{org_id}",  tags=["analytics"])
def group_practitioner_by_department_of_org(org_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.group_practitioner_by_department_of_org(db, org_id, skip=skip, limit=limit)


@app.get("/analytics/stats/gender/patient/{org_id}",  tags=["analytics"])
def group_patients_by_gender_of_org(org_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.group_patients_by_gender_of_org(db, org_id, skip=skip, limit=limit)

@app.get("/analytics/stats/counts/allentities/{org_id}",  tags=["analytics"])
def group_entities_of_org(org_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.group_entities_of_org(db, org_id, skip=skip, limit=limit)

@app.get("/analytics/stats/hospital/earning/{org_id}",  tags=["analytics"])
def get_earning_of_org(org_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    temp_obj = crud.get_earning_of_org(db, org_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

