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

@app.post("/org/add", response_model=schemas.Org)
def create_org(org: schemas.OrgCreate, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    print(org)
    return crud.create_org(db=db, org=org)


@app.get("/orgs/all", response_model=List[schemas.Org])
def get_all_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orgs(db, skip=skip, limit=limit)


@app.get("/org/{org_id}", response_model=schemas.Org)
def get_org(org_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    db_org = crud.get_org(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Org not found")
    return db_org

# User

@app.post("/user/add", response_model=schemas.User)
def create_user(user: schemas.userCreate, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    print(user)
    return crud.create_user(db=db, user=user)


@app.get("/user/all", response_model=List[schemas.User])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/user/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db), isLoggedIn=Depends(manager)):
    db_org = crud.get_user(db, user_id=user_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_org