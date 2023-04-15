from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)
    
    is_valid_data = check_endpoint_info(request.json, ['name'])
    if(is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)
    
    results = run_statement('CALL add_province(?,?)', [request.json.get('name'), request.headers.get('token')])

    if(type(results) != None and results[0]['id'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif(type(results) != None and results[0]['id'] == 0):
        return make_response(json.dumps('Wrong token', default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)