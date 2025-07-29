from repositories.database import db
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from models.employee import Employee
from datetime import datetime


class EmployeePdfService:
    @staticmethod
    def generate_pdf(emp_id=None):
        employee = db.session.query(Employee).filter(Employee.employee_id == emp_id).first()
        if not employee:
            return False

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
        pdf.drawString(margin, current_y - 15, "CUI: RO12345678 | J40/1234/2020 | București, România")
        pdf.drawRightString(width - margin, current_y, "Fluturaș de salariu")

        current_y -= 40
        pdf.setLineWidth(1)
        pdf.setStrokeColor(colors.grey)
        pdf.line(margin, current_y, width - margin, current_y)
        current_y -= 30


        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, current_y, "Date angajat:")
        current_y -= 20
        pdf.setFont("Helvetica", 11)

        emp_details = [
            ("Nume", employee.name),
            ("Prenume", employee.surname),
            ("ID Angajat", employee.employee_id),
            ("CNP", employee.cnp),
            ("Lună", employee.current_month),
            ("An", employee.current_year),
        ]

        for label, value in emp_details:
            pdf.drawString(margin + 10, current_y, f"{label}:")
            pdf.drawString(margin + 120, current_y, str(value))
            current_y -= 18

        current_y -= 10


        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margin, current_y, "Detalii salariu:")
        current_y -= 20
        pdf.setFont("Helvetica", 11)

        salary_details = [
            ("Salariu de bază", f"{employee.salary_for_current_month:,.2f} RON"),
            ("Sporuri", "0.00 RON"),
            ("Bonusuri", f"{employee.additional_bonuses}"),
            ("Rețineri (CAS, CASS, Impozit)", f"{43.8*employee.salary_for_current_month/100}"),
            ("Salariu net", f"{employee.salary_for_current_month+employee.additional_bonuses:,.2f} RON"),
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
        pdf.drawString(margin, current_y, "Salariu net de încasat:")
        pdf.setFont("Helvetica-Bold", 14)
        pdf.setFillColor(colors.green)
        pdf.drawRightString(width - margin, current_y, f"{employee.salary_for_current_month:,.2f} RON")
        pdf.setFillColor(colors.black)
        current_y -= 40


        pdf.setFont("Helvetica-Oblique", 9)
        pdf.setFillColor(colors.grey)
        date_str = datetime.now().strftime("%d %B %Y")
        pdf.drawString(margin, 40, f"Generat în data de: {date_str}")
        pdf.drawRightString(width - margin, 40, "Endava - HR Department")
        pdf.line(width - 160, 60, width - margin, 60)
        pdf.drawRightString(width - margin, 50, "Semnătură")

        pdf.save()
        return True
