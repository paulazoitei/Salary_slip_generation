import pandas as pd
from repositories.database  import db
from models.employee import Employee

class EmployeeExcelService:
     @staticmethod
     def generate_excel(employee_ids=None):
          query=db.session.query(Employee)
          if employee_ids:
                query = query.filter(Employee.employee_id.in_(employee_ids))

          employees=query.all()

          data = [{
               'Name': emp.name,
               'Surname': emp.surname,
               'Salary': emp.salary_for_current_month,
               'Vacation Days': emp.number_of_vacation_days_taken,
               'Bonuses': emp.additional_bonuses
          } for emp in employees]

          df=pd.DataFrame(data)
          df.to_excel('filtered_employees.xlsx',index=False)


