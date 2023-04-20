from flask import request, make_response
from apihelpers import check_endpoint_info, organize_college_response, check_data_sent
import json
from dbhelpers import run_statement

def post():    
    is_valid_data = check_endpoint_info(request.json, ['college_id', 'name', 'url', 'terms', 'credential'])   
    if (is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)
    
    results = run_statement('CALL add_program(?,?,?,?,?)', [request.json.get('college_id'), request.json.get('name'), request.json.get('url'), request.json.get('terms'), request.json.get('credential')])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results, default=str), 200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps("Wrong token", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    

def get():
    if(request.args.get('student_id') != None):
        return
    elif(request.args.get('college_id') != None):
        return
    else:
        results = run_statement('CALL get_all_programs()')

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)