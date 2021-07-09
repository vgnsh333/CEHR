from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

class Org(Base):
    __tablename__ = "org"
    org_ID = Column(Integer, primary_key=True, index=True)
    org_name = Column(String, unique=True,nullable=False)
    purpose = Column(String)
    org_type = Column(String)
    
class beds(Base):
    __tablename__ = "beds"
    id = Column(Integer, primary_key=True, index=True)
    alloted_to = Column(String)
    is_occupied = Column(Boolean, default=True)
    org_ID = Column(Integer, ForeignKey("org.org_ID"),nullable=False)

class user_details(Base):
    __tablename__ = "user_details"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True,nullable=False)
    password = Column(String)
    secret = Column(String)
    phone = Column(String)
    email = Column(String)
    entity_type = Column(String)
    aadhar = Column(String)
    org_id = Column(Integer, ForeignKey("org.org_ID"),nullable=False)
    fullname = Column(String)
    address = Column(String)
    dob = Column(String)
    blood_group = Column(String)
    gender = Column(String)
