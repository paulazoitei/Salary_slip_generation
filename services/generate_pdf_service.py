from repositories.database import db
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from models.employee import Employee
from datetime import datetime
from services.encrypt_pdf_service import EncryptPdfService
import os

class GeneratePdfService:
    @staticmethod
    def generate_pdf_for_all():
        try:
            employees = db.session.query(Employee).all()
        except Exception as e:
            print(f"[DB ERROR] Failed to fetch employees: {e}")
            return False

        if not employees:
            return False

        for employee in employees:
            if str(employee.role) != "RoleEnum.EMPLOYEE":
                continue

            try:
                file_name = f'salary_slip_{employee.employee_id}.pdf'
                pdf = canvas.Canvas(file_name, pagesize=A4)
                width, height = A4
                margin = 40
                current_y = height - margin


                pdf.setFont("Helvetica-Bold", 18)
                pdf.setFillColor(colors.HexColor("#003366"))
                pdf.drawString(margin, current_y, "Endava SRL")
                pdf.setFont("Helvetica", 10)
                pdf.setFillColor(colors.black)
                pdf.drawString(margin, current_y - 15, "VAT ID: RO12345678 | Reg: J40/1234/2020 | Bucharest, Romania")
                pdf.drawRightString(width - margin, current_y, "Salary Slip")

                current_y -= 70


                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(margin, current_y, "Employee Information:")
                current_y -= 20
                pdf.setFont("Helvetica", 11)

                emp_details = [
                    ("First Name", employee.name),
                    ("Last Name", employee.surname),
                    ("Employee ID", employee.employee_id),
                    ("CNP", employee.cnp),
                    ("Month", employee.current_month),
                    ("Year", employee.current_year),
                ]

                for label, value in emp_details:
                    pdf.drawString(margin + 10, current_y, f"{label}:")
                    pdf.drawString(margin + 120, current_y, str(value))
                    current_y -= 18

                current_y -= 10


                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(margin, current_y, "Salary Details:")
                current_y -= 20
                pdf.setFont("Helvetica", 11)

                bonuses = employee.additional_bonuses or 0
                deductions = round(43.8 * employee.salary_for_current_month / 100, 2)
                net_salary = employee.salary_for_current_month + bonuses - deductions

                salary_details = [
                    ("Base Salary", f"{employee.salary_for_current_month:,.2f} RON"),
                    ("Bonuses", f"{bonuses:,.2f} RON"),
                    ("Deductions (CAS, CASS, Tax)", f"{deductions:,.2f} RON"),
                    ("Net Salary", f"{net_salary:,.2f} RON"),
                ]

                for label, value in salary_details:
                    pdf.drawString(margin + 10, current_y, f"{label}:")
                    pdf.drawRightString(width - margin - 10, current_y, value)
                    current_y -= 18

                current_y -= 15
                pdf.setStrokeColor(colors.lightgrey)
                pdf.line(margin, current_y, width - margin, current_y)
                current_y -= 25


                pdf.setFont("Helvetica-Bold", 12)
                pdf.setFillColor(colors.darkgreen)
                pdf.drawString(margin, current_y, "Net Salary Payable:")
                pdf.setFont("Helvetica-Bold", 14)
                pdf.setFillColor(colors.green)
                pdf.drawRightString(width - margin, current_y, f"{net_salary:,.2f} RON")
                pdf.setFillColor(colors.black)
                current_y -= 40


                pdf.setFont("Helvetica-Oblique", 9)
                pdf.setFillColor(colors.grey)
                date_str = datetime.now().strftime("%d %B %Y")
                pdf.drawString(margin, 40, f"Generated on: {date_str}")
                pdf.drawRightString(width - margin, 40, "Endava - HR Department")
                pdf.line(width - 160, 60, width - margin, 60)
                pdf.drawRightString(width - margin, 50, "Signature")

                pdf.save()

            except Exception as e:
                print(f"[PDF ERROR] Failed to generate PDF for {employee.email}: {e}")
                continue


            try:
                EncryptPdfService.encrypt_pdf_with_cnp(file_name, str(employee.cnp))
            except Exception as e:
                print(f"[ENCRYPT ERROR] Failed to encrypt PDF for {employee.email}: {e}")
                continue

        return True
