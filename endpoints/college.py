from flask import request, make_response
from apihelpers import check_endpoint_info, organize_college_response
import json
from dbhelpers import run_statement


def post():
    is_valid_data = check_endpoint_info(request.json, ['province_id', 'name'])
    if (is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)

    results = run_statement('CALL add_college(?,?)', [
                            request.json.get('province_id'), request.json.get('name')])

    if (type(results) == list and results[0]['id'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    if (type(results) == list and results[0]['id'] == 0):
        return make_response(json.dumps('Wrong token or wrong province id.', default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)


def get():
    is_valid = check_endpoint_info(request.args, ['province_id'])
    if (is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL get_all_colleges(?)',
                            [request.args.get('province_id')])

    if (type(results) == list and len(results) != 0):
        colleges = organize_college_response(results)
        return make_response(json.dumps(colleges, default=str), 200)
    elif (type(results) == list and len(results) == 0):
        return make_response(json.dumps("Wrong college id.", default=str),
                             400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
