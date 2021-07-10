from typing import List
from fastapi_login import LoginManager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
import crud, models, schemas
from database import SessionLocal, engine
from fastapi import FastAPI

models.Base.metadata.create_all(bind=engine)

SECRET = "your-secret-key"
app = FastAPI()


manager = LoginManager(SECRET, token_url='/auth/token')
fake_db = {'j': {'password': 'h'}}
@manager.user_loader
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
async def root():
    return {"message": "Hello! Go to /docs :)"}
@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

# Org

@app.post("/org/add", response_model=schemas.Org, tags=["Organization"])
def create_org(org: schemas.OrgCreate, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    print(org)
    return crud.create_org(db=db, org=org)


@app.get("/orgs/all", response_model=List[schemas.Org], tags=["Organization"])
def get_all_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orgs(db, skip=skip, limit=limit)


@app.get("/org/{org_id}", response_model=schemas.Org, tags=["Organization"])
def get_org(org_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_org(db, org_id=org_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="Org not found")
    return temp_obj

# User

@app.post("/user/add", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.userCreate, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    print(user)
    return crud.create_user(db=db, user=user)

@app.get("/user/all", response_model=List[schemas.User], tags=["Users"])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/user/{user_id}", response_model=schemas.User, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_user(db, user_id=user_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return temp_obj

# Patient
@app.post("/patient/add", response_model=schemas.Patient, tags=["Patient"])
def create_patient(Patient: schemas.PatientBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_patient(db, Patient)

@app.get("/patient/all", response_model=List[schemas.Patient], tags=["Patient"])
def get_all_patient(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip=skip, limit=limit)

@app.get("/patient/{patient_id}", response_model=schemas.Patient, tags=["Patient"])
def get_patient(patient_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_patient(db, patient_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

# Careteam
@app.post("/careteam/add", response_model=schemas.CareTeam, tags=["Careteam"])
def create_Careteam(CareTeam: schemas.CareTeamBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_careteam(db ,CareTeam)

@app.get("/careteam/all", response_model=List[schemas.CareTeam], tags=["Careteam"])
def get_all_Careteam(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_careteams(db, skip=skip, limit=limit)

@app.get("/careteam/{careteam_id}", response_model=schemas.CareTeam, tags=["Careteam"])
def get_Careteam(careteam_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_careteam(db, careteam_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Practicioner
@app.post("/practitioner/add", response_model=schemas.Practitioner, tags=["Practicioner"])
def create_Practicioner(practitioner: schemas.PractitionerBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_practitioner(db,practitioner)

@app.get("/practitioner/all", response_model=List[schemas.Practitioner], tags=["Practicioner"])
def get_all_Practicioner(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_practitioners(db, skip=skip, limit=limit)

@app.get("/practitioner/{practitioner_id}", response_model=schemas.Practitioner, tags=["Practicioner"])
def get_Practicioner(practitioner_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_practitioner(db, practitioner_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Admin
@app.post("/admin/add", response_model=schemas.Admin, tags=["Admin"])
def create_admin(admin: schemas.AdminBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_admin(db, admin)

@app.get("/admin/all", response_model=List[schemas.Admin], tags=["Admin"])
def get_all_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_admins(db, skip=skip, limit=limit)

@app.get("/admin/{admin_id}", response_model=schemas.Admin, tags=["Admin"])
def get_admin(admin_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_admin(db, admin_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Appointment
@app.post("/appointment/add", response_model=schemas.Appointment, tags=["Appointment"])
def create_appointment(appointment: schemas.AppointmentBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_appointment(db,appointment )

@app.get("/appointment/all", response_model=List[schemas.Appointment], tags=["Appointment"])
def get_all_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_appointments(db, skip=skip, limit=limit)

@app.get("/appointment/{appointment_id}", response_model=schemas.Appointment, tags=["Appointment"])
def get_appointment(appointment_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_appointment(db,appointment_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Immunization
@app.post("/immunization/add", response_model=schemas.Immunization, tags=["Immunization"])
def create_immunization(Immunization: schemas.ImmunizationBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_immunization(db, Immunization)

@app.get("/immunization/all", response_model=List[schemas.Immunization], tags=["Immunization"])
def get_all_immunizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_immunizations(db, skip=skip, limit=limit)

@app.get("/immunization/{immunization_id}", response_model=schemas.Immunization, tags=["Immunization"])
def get_immunization(immunization_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_immunization(db, immunization_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Observation
@app.post("/observation/add", response_model=schemas.Observation, tags=["Observation"])
def create_observation(Observation: schemas.ObservationBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_observation(db, Observation)

@app.get("/observation/all", response_model=List[schemas.Observation], tags=["Observation"])
def get_all_observation(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_observations(db, skip=skip, limit=limit)

@app.get("/observation/{observation_id}", response_model=schemas.Observation, tags=["Observation"])
def get_observation(observation_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_observation(db,observation_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Procedure
@app.post("/procedure/add", response_model=schemas.Procedure, tags=["Procedure"])
def create_procedure(Procedure: schemas.ProcedureBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_procedure(db, Procedure)

@app.get("/procedure/all", response_model=List[schemas.Procedure], tags=["Procedure"])
def get_all_procedures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_procedures(db, skip=skip, limit=limit)

@app.get("/procedure/{procedure_id}", response_model=schemas.Procedure, tags=["Procedure"])
def get_procedure(procedure_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_procedure(db, procedure_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Allergy
@app.post("/allergy/add", response_model=schemas.Allergy, tags=["Allergy"])
def create_allergy(Allergy: schemas.AllergyBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_allergy(db, Allergy)

@app.get("/allergy/all", response_model=List[schemas.Allergy], tags=["Allergy"])
def get_all_allergy(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_allergies(db, skip=skip, limit=limit)

@app.get("/allergy/{allergy_id}", response_model=schemas.Allergy, tags=["Allergy"])
def get_allergy(allergy_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_allergy(db, allergy_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Report
@app.post("/report/add", response_model=schemas.Report, tags=["Report"])
def create_report(Report: schemas.ReportBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_report(db,Report)

@app.get("/report/all", response_model=List[schemas.Report], tags=["Report"])
def get_all_report(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reports(db, skip=skip, limit=limit)

@app.get("/report/{report_id}", response_model=schemas.Report, tags=["Report"])
def get_report(report_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_report(db, report_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Medication
@app.post("/medication/add", response_model=schemas.Medication, tags=["Medication"])
def create_medication(Medication: schemas.MedicationBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_medication(db,Medication)

@app.get("/medication/all", response_model=List[schemas.Medication], tags=["Medication"])
def get_all_medication(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_medications(db, skip=skip, limit=limit)

@app.get("/medication/{medication_id}", response_model=schemas.Medication, tags=["Medication"])
def get_medication(medication_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_medication(db,medication_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Statement
@app.post("/statement/add", response_model=schemas.Statement, tags=["Statement"])
def create_statement(Statement: schemas.StatementBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_statement(db,Statement)

@app.get("/statement/all", response_model=List[schemas.Statement], tags=["Statement"])
def get_all_statement(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_statements(db, skip=skip, limit=limit)

@app.get("/statement/{statement_id}", response_model=schemas.Statement, tags=["Statement"])
def get_statement(statement_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_statement(db,statement_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# BMI
@app.post("/bmi/add", response_model=schemas.BMI, tags=["BMI"])
def create_bmi(BMI: schemas.BMIBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_bmi(db,BMI)

@app.get("/bmi/all", response_model=List[schemas.BMI], tags=["BMI"])
def get_all_bmi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bmis(db, skip=skip, limit=limit)

@app.get("/bmi/{bmi_id}", response_model=schemas.BMI, tags=["BMI"])
def get_bmi(bmi_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_bmi(db, bmi_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Problem
@app.post("/problem/add", response_model=schemas.Problem, tags=["Problem"])
def create_problem(Problem: schemas.ProblemBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_problem(db,Problem)

@app.get("/problem/all", response_model=List[schemas.Problem], tags=["Problem"])
def get_all_problem(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_problems(db, skip=skip, limit=limit)

@app.get("/problem/{problem_id}", response_model=schemas.Problem, tags=["Problem"])
def get_problem(problem_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_problem(db,problem_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Family_history
@app.post("/familyhistory/add", response_model=schemas.FamilyHistory, tags=["Family_history"])
def create_familyhistory(Family_history: schemas.FamilyHistoryBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_family_history(db, Family_history)

@app.get("/familyhistory/all", response_model=List[schemas.FamilyHistory], tags=["Family_history"])
def get_all_familyhistory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_family_histories(db, skip=skip, limit=limit)

@app.get("/familyhistory/{familyhistory_id}", response_model=schemas.FamilyHistory, tags=["Family_history"])
def get_familyhistory(familyhistory_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_family_history(db, familyhistory_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj
# Invoice
@app.post("/invoice/add", response_model=schemas.Invoice, tags=["Invoice"])
def create_invoice(invoice: schemas.InvoiceBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_invoice(db,invoice)

@app.get("/invoice/all", response_model=List[schemas.Invoice], tags=["Invoice"])
def get_all_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_invoices(db, skip=skip, limit=limit)

@app.get("/invoice/{invoice_id}", response_model=schemas.Invoice, tags=["Invoice"])
def get_invoice(invoice_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_invoice(db, invoice_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj

# Logs
@app.post("/logs/add", response_model=schemas.Logs, tags=["Logs"])
def create_Log(logs: schemas.LogsBase, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    return crud.create_log(db, logs)

@app.get("/logs/all", response_model=List[schemas.Logs], tags=["Logs"])
def get_all_Logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_logs(db, skip=skip, limit=limit)

@app.get("/logs/{log_id}", response_model=schemas.Logs, tags=["Logs"])
def get_Log(log_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    temp_obj = crud.get_log(db, log_id)
    if temp_obj is None:
        raise HTTPException(status_code=404, detail=" not found")
    return temp_obj