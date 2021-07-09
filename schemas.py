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
    practitioner_id : str
    class Config:
        orm_mode = True

