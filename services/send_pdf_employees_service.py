from models.employee import Employee
from models.enum import RoleEnum
from repositories.database import db
from services.email_service import EmailService


class SendPdfEmployeesService:
    @staticmethod
    def send_pdf_to_employees():
        employees = db.session.query(Employee).filter(Employee.role == RoleEnum.EMPLOYEE).all()

        if not employees:
            return False

        for employee in employees:
            file_name = f"salary_slip_{employee.employee_id}.pdf"

            message = f"""\
Dear {employee.name} {employee.surname},

Please find attached your salary slip for {employee.current_month} {employee.current_year}.

If you have any questions, feel free to contact us.

Best regards,
HR Department
Endava"""

            EmailService.sendemail(
                to=employee.email,
                subject="Your Salary Slip",
                body=message,
                attachments=[file_name]
            )

        return True
# import os
# from models.employee import Employee
# from models.enum import RoleEnum
# from repositories.database import db
#
# class SendPdfEmployeesService:
#     @staticmethod
#     def dry_run_check():
#         employees = db.session.query(Employee).filter(Employee.role == RoleEnum.EMPLOYEE).all()
#
#         if not employees:
#             print("No employees with role EMPLOYEE found.")
#             return False
#
#         for employee in employees:
#             file_name = f"salary_slip_{employee.employee_id}.pdf"
#
#             if not employee.email:
#                 print(f"[SKIP] Employee ID {employee.employee_id} has no email.")
#                 continue
#
#             if not os.path.isfile(file_name):
#                 print(f"[MISSING PDF] {file_name} does not exist for {employee.email}")
#                 continue
#
#             print(f"[READY] Would send to: {employee.email} with attachment: {file_name}")
#
#         print("Dry-run complete.")
#         return True
