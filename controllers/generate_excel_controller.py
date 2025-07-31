from flask import Blueprint, jsonify
from services.generate_excel_service import GenerateExcelService
from flask import request

excel_bp = Blueprint('excel_bp', __name__)

@excel_bp.route('/createAggregatedEmployeeData', methods=['POST'])
def generate_excel():
    data = request.get_json()
    ids_param = data.get('ids')
    if not isinstance(ids_param, list):
        return jsonify({'error': 'Invalid format: expected a list of IDs'}), 400

    missing_ids = GenerateExcelService.generate_excel(employee_ids=ids_param)
    if missing_ids is None:
        return jsonify({'error': 'Internal server error while generating Excel'}), 500
    if missing_ids:
        return jsonify({
            'message': 'Excel generated',
            'warning': f"The following employee IDs were not found in the database: {missing_ids}"
        }), 200

    return jsonify({'message': 'Excel generated'}), 200
