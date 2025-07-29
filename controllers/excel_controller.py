from flask import Blueprint, jsonify
from services.employee_excel_service import EmployeeExcelService
from flask import request

excel_bp = Blueprint('excel_bp', __name__)

@excel_bp.route('/createAggregatedEmployeeData', methods=['POST'])
def generate_excel():
    data=request.get_json()
    ids_param=data.get('ids')
    if not isinstance(ids_param, list):
        return jsonify({'error': 'Invalid format: expected a list of IDs'}), 400

    EmployeeExcelService.generate_excel(employee_ids=ids_param)
    return jsonify({'message': 'Excel generated'})
