from flask import Blueprint,jsonify
from services.generate_pdf_service import GeneratePdfService




pdf_bp=Blueprint('pdf_bp',__name__)

@pdf_bp.route('/createPdfForEmployees', methods=['POST'])
def generate_all_pdfs():
    result = GeneratePdfService.generate_pdf_for_all()

    if result is False:
        return jsonify({'error': 'No employees found'}), 404

    return jsonify({'message': 'PDFs generated for all employees'}), 200
