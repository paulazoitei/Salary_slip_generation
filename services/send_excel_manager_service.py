import os
from models.employee import Employee
from models.enum import RoleEnum
from repositories.database import db
from services.email_service import EmailService
from services.archive_service import ArchiveService

class SendExcelManagerService:
    @staticmethod
    def send_excel_to_manager():
        try:
            manager = db.session.query(Employee).filter(Employee.role == RoleEnum.MANAGER).first()
        except Exception as e:
            print(f"[DB ERROR] Failed to query manager: {e}")
            return False

        if not manager:
            print("[WARNING] No manager found in database.")
            return False

        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_name = os.path.join(base_dir, "filtered_employees.xlsx")

            if not os.path.exists(file_name):
                print(f"[FILE ERROR] Excel file not found: {file_name}")
                return False
        except Exception as e:
            print(f"[PATH ERROR] Could not resolve Excel file path: {e}")
            return False

        try:
            message = f"""\
Dear {manager.name} {manager.surname},

Please find attached the salary overview for the selected employees for the month of {manager.current_month} {manager.current_year}.

The Excel file includes details such as employee names, roles, base salaries, bonuses, and total compensation.

Should you have any questions or need further clarification, please do not hesitate to reach out.

Best regards,  
HR Department  
Endava
"""

            EmailService.sendemail(
                to=manager.email,
                subject="Salary Overview for Employees",
                body=message,
                attachments=[file_name]
            )
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send email to manager: {e}")
            return False

        try:
            ArchiveService.create_flag(ArchiveService.EXCEL_FLAG)
            ArchiveService.attempt_archive_all()
        except Exception as e:
            print(f"[ARCHIVE ERROR] Archiving failed after sending Excel: {e}")

        return True
