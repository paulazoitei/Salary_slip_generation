from flask import Blueprint,jsonify
from services.send_excel_manager_service import SendExcelManagerService

send_excel_bp=Blueprint('send_excel_bp',__name__)

@send_excel_bp.route('/sendAggregatedEmployeeData',methods=['POST'])
def send_excel_to_manager():
    result=SendExcelManagerService.send_excel_to_manager()

    if result  is False:
        return jsonify({'error':'Mail of the manager not found'})

    return jsonify({'message':'Email with the EXCEL send to manager'})