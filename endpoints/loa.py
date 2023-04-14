from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
import json
from dbhelpers import run_statement


def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    is_valid_data = check_endpoint_info(request.json, [
                                        'student_id', 'program_id', 'date_received', 'payment_date', 'payment_value', 'tuition', 'total', 'comission'])
    if (is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)

    results = run_statement('CALL add_loa(?,?,?,?,?,?,?,?,?)', [request.json.get('student_id'), request.json.get('program_id'), request.json.get('date_received'), request.json.get(
        'payment_date'), request.json.get('payment_value'), request.json.get('tuition'), request.json.get('total'), request.json.get('comission'), request.headers.get('token')])

    if (type(results) == list and results[0]['loa_id'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif (type(results) == list and results[0]['loa_id'] == 0):
        return make_response(json.dumps("Wrong token or wrong student id", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)


