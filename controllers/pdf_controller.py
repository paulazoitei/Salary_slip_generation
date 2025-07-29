from flask import Blueprint,jsonify
from services.employee_pdf_service import EmployeePdfService

from services.employee_pdf_service import EmployeePdfService
from flask import request

pdf_bp=Blueprint('pdf_bp',__name__)

@pdf_bp.route('/createPdfForEmployees',methods=['POST'])
def generate_pdf():
    data=request.get_json()
    employee_id=data.get('id')
    if not isinstance(employee_id,int):
        return jsonify({'error': 'Not correct type for id'}), 400

    result=EmployeePdfService.generate_pdf(emp_id=employee_id)
    if result is False:
        return jsonify({'error':'Employee with this ID does not exist'}),404


    return jsonify({'message':'Pdf generated'})
