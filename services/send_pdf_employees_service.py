from models.employee import Employee
from models.enum import RoleEnum
from repositories.database import db
from services.archive_service import ArchiveService
from services.email_service import EmailService
import os

class SendPdfEmployeesService:
    @staticmethod
    def send_pdf_to_employees():
        try:
            employees = db.session.query(Employee).filter(Employee.role == RoleEnum.EMPLOYEE).all()
        except Exception as e:
            print(f"[DB ERROR] Failed to query employees: {e}")
            return False

        if not employees:
            print("[INFO] No employees found with role EMPLOYEE.")
            return False

        for employee in employees:
            if not employee.email:
                print(f"[SKIP] Employee {employee.employee_id} has no email.")
                continue

            file_name = f"salary_slip_{employee.employee_id}.pdf"

            if not os.path.exists(file_name):
                print(f"[SKIP] PDF not found for employee {employee.employee_id}: {file_name}")
                continue

            try:
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
                break
            except Exception as e:
                print(f"[EMAIL ERROR] Failed to send email to {employee.email}: {e}")
                continue

        try:
            ArchiveService.create_flag(ArchiveService.PDF_FLAG)
            ArchiveService.attempt_archive_all()
        except Exception as e:
            print(f"[ARCHIVE ERROR] Could not archive PDFs: {e}")

        return True
