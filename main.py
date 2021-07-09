from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/org/add", response_model=schemas.Org)
def create_org(org: schemas.OrgCreate, db: Session = Depends(get_db)):
    print(org)
    return crud.create_org(db=db, org=org)


@app.get("/orgs/all", response_model=List[schemas.Org])
def get_all_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orgs(db, skip=skip, limit=limit)


@app.get("/org/{org_id}", response_model=schemas.Org)
def get_org(org_id: int, db: Session = Depends(get_db)):
    db_org = crud.get_org(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Org not found")
    return db_org
