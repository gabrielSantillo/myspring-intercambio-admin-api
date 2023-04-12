from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
import json
from dbhelpers import run_statement


def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    if (request.json.get('program_id') != None):
        results = run_statement('CALL add_student_program(?,?)', [
            request.json.get('program_id'), request.headers.get('token')
        ])
    else:
        is_valid_data = check_endpoint_info(request.json,
                                            ['first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'marital_status'])
        if (is_valid_data != None):
            return make_response(json.dumps(is_valid_data, default=str), 400)

        results = run_statement('CALL add_student(?,?,?,?,?,?,?)', [
            request.json.get('first_name'), request.json.get('last_name'), request.json.get('email'), request.json.get(
                'phone_number'), request.json.get('birth_date'), request.json.get('marital_status'), request.headers.get('token')
        ])

    # if the response is a list and the length is different than zero send 200 as response
    if (type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    # else a 500 as response
    else:
        return make_response(json.dumps(results, default=str), 500)


def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    if (request.args.get('id') != None):
        return
    else:
        results = run_statement('CALL get_all_students()')

        # if the response is a list and the length is different than zero send 200 as response
        if (type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        # else a 500 as response
        else:
            return make_response(json.dumps(results[0], default=str), 500)
