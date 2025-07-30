from models.enum import RoleEnum
from repositories.database import db
from datetime import datetime
from sqlalchemy import Enum
class Employee(db.Model):
    __tablename__= 'employee_data'
    employee_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    surname=db.Column(db.String(30),nullable=False)
    salary_for_current_month = db.Column(db.Integer, nullable=False)
    number_of_vacation_days_taken=db.Column(db.Integer, nullable=True)
    additional_bonuses=db.Column(db.Integer,nullable=True,default=0,server_default="0")
    cnp=db.Column(db.Numeric(13),nullable=False,unique=True)
    current_month = db.Column(db.Integer, default=lambda: datetime.now().month, nullable=True)
    current_year = db.Column(db.Integer, default=lambda: datetime.now().year, nullable=True)
    email=db.Column(db.String(50),nullable=True,unique=True)
    role = db.Column(Enum(RoleEnum,name="roleenum"),  default=RoleEnum.EMPLOYEE)