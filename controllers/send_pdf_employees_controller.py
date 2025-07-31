from flask import Blueprint,jsonify
from services.send_pdf_employees_service import SendPdfEmployeesService

send_pdf_bp=Blueprint('send_pdf_bp',__name__)

@send_pdf_bp.route('/sendPdfToEmployees',methods=['POST'])
def send_pdf_to_employees():
    result=SendPdfEmployeesService.send_pdf_to_employees()

    if result is False:
        return jsonify({'error':'No emails found'})

    return jsonify({'message':'Emails with PDFs send to employees'})


