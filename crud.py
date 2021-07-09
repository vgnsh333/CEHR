from sqlalchemy.orm import Session
import models, schemas


# Organization functions
def get_org(db: Session, org_id: int):
    return db.query(models.Org).filter(models.Org.org_ID == org_id).first()

def get_orgs(db: Session, skip: int = 1, limit: int = 100):
    print("hello \n \n",db.query(models.Org))
    return db.query(models.Org).offset(skip).limit(limit).all()

def create_org(db: Session, org: schemas.OrgCreate):
    db_org = models.Org(org_name=org.org_name, purpose=org.purpose, org_type=org.org_type)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

# Beds functions
def get_beds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.beds).offset(skip).limit(limit).all()

def create_bed(db: Session, bed: schemas.BedCreate):
    db_bed = models.Org(alloted_to=bed.alloted_to, org_name=bed.org_name)
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed

# User Details functions 
def create_user(db: Session, user: schemas.userCreate):
    db_obj = models.user_details(
    username = user.username,
    secret = user.secret,
    phone = user.phone,
    email = user.email,
    entity_type = user.entity_type,
    aadhar = user.aadhar,
    org_id = user.org_id,
    fullname = user.fullname,
    address = user.address,
    dob = user.dob,
    blood_group = user.blood_group,
    gender = user.gender,
    password = user.password
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_user(db: Session, user_id: int):
    return db.query(models.user_id).filter(models.user_details.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user_id).offset(skip).limit(limit).all()

