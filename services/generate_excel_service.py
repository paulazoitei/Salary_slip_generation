import pandas as pd
from repositories.database  import db
from models.employee import Employee

class GenerateExcelService:
     @staticmethod
     def generate_excel(employee_ids=None):
          query = db.session.query(Employee)
          employees = []

          if employee_ids:
               query = query.filter(Employee.employee_id.in_(employee_ids))
               employees = query.all()
               found_ids = {e.employee_id for e in employees}
               missing_ids = list(set(employee_ids) - found_ids)
          else:
               employees = query.all()
               missing_ids = []


          data = [{
               'Name': emp.name,
               'Surname': emp.surname,
               'Salary': emp.salary_for_current_month,
               'Vacation Days': emp.number_of_vacation_days_taken,
               'Bonuses': emp.additional_bonuses
          } for emp in employees]

          df=pd.DataFrame(data)
          df.to_excel('filtered_employees.xlsx',index=False)

          return missing_ids

