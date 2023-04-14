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


def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    is_valid_data = check_endpoint_info(request.json, ['loa_id'])
    if (is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)

    # getting the student by id
    loa_info = run_statement('CALL get_loa_by_id(?)', [
        request.json.get('loa_id')])

    # checking to see if the response is valid to continue with the patching process
    if (type(loa_info) == list and len(loa_info) != 0):
        update_loa_info = check_data_sent(request.json, loa_info[0],
                                              ['id', 'student_id', 'program_id', 'date_received', 'payment_date', 'payment_value', 'tuition', 'total', 'comission'])

        # calling the function that will edit a student
        results = run_statement('CALL edit_loa(?,?,?,?,?,?,?,?,?,?)',
                                [update_loa_info['id'], update_loa_info['student_id'], update_loa_info['program_id'],
                                 update_loa_info['date_received'], update_loa_info['payment_date'],
                                    update_loa_info['payment_value'], update_loa_info['tuition'], update_loa_info['total'], update_loa_info['comission'], request.headers.get('token')])

        # if the response is a list and the row_updated is equal than 1 send 200 as response
        if (type(results) == list and results[0]['row_updated'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        # if the response is a list and the row_updated is equal than 0 send 400 as response
        elif (type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        # else send 500 as an internal error
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
        

def delete():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    is_valid_data = check_endpoint_info(request.json, ['loa_id'])
    if (is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)

        # calling the function that will edit a student
    results = run_statement('CALL delete_loa(?,?)',
                            [request.json.get('loa_id'), request.headers.get('token')])

    # if the response is a list and the row_updated is equal than 1 send 200 as response
    if (type(results) == list and results[0]['row_updated'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
        # if the response is a list and the row_updated is equal than 0 send 400 as response
    elif (type(results) == list and results[0]['row_updated'] == 0):
        return make_response(json.dumps(results[0], default=str), 400)
        # else send 500 as an internal error
    else:
        return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)