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
        is_valid_data = check_endpoint_info(request.args, ['student_id'])
        if(is_valid_data != None):
            return make_response(json.dumps(is_valid_data, default=str), 400)

        results = run_statement('CALL get_program_by_student_id(?)', [request.args.get('student_id')])

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps("Wrong student id", default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
        
    elif(request.args.get('college_id') != None):
        is_valid_data = check_endpoint_info(request.args, ['college_id'])
        if(is_valid_data != None):
            return make_response(json.dumps(is_valid_data, default=str), 400)

        results = run_statement('CALL get_program_by_college_id(?)', [request.args.get('college_id')])

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps("Wrong college id", default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
        
    else:
        results = run_statement('CALL get_all_programs()')

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
        

def patch():
    is_valid_data = check_endpoint_info(request.json, ['id'])
    if (is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)
    
    program_info = run_statement('CALL get_program_by_id(?)', [
        request.json.get('id')])

    # checking to see if the response is valid to continue with the patching process
    if (type(program_info) == list and len(program_info) != 0):
        update_program_info = check_data_sent(request.json, program_info[0],
                                              ['id', 'college_id', 'name', 'url', 'terms', 'credential'])

        # calling the function that will edit a program
        results = run_statement('CALL edit_program(?,?,?,?,?,?)',
                                [update_program_info['id'], update_program_info['college_id'],
                                 update_program_info['name'], update_program_info['url'],
                                    update_program_info['terms'], update_program_info['credential']])

        # if the response is a list and the row_updated is equal than 1 send 200 as response
        if (type(results) == list and results[0]['row_updated'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        # if the response is a list and the row_updated is equal than 0 send 400 as response
        elif (type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        # else send 500 as an internal error
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)