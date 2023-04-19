from flask import request, make_response
from apihelpers import check_endpoint_info, organize_college_response, check_data_sent
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
    

def delete():
    is_valid = check_endpoint_info(request.json, ['college_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    
    results = run_statement('CALL delete_college(?)', [request.json.get('college_id')])

    if(type(results) == list and results[0]['row_updated'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif(type(results) == list and results[0]['row_updated'] == 0):
        return make_response(json.dumps("Wrong college id", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)

def patch(): 
    is_valid_data = check_endpoint_info(request.json, ['id'])
    if (is_valid_data != None):
        return make_response(json.dumps(is_valid_data, default=str), 400)
    
    college_info = run_statement('CALL get_college_by_id(?)', [
        request.json.get('id')])
    
    if (type(college_info) == list and len(college_info) != 0):
        update_college_info = check_data_sent(request.json, college_info[0],
                                              ['id', 'province_id', 'name'])

        # calling the function that will edit a college
        results = run_statement('CALL edit_college(?,?,?)',
                                [update_college_info['id'], update_college_info['province_id'], update_college_info['name'], request.headers.get('token')])

        # if the response is a list and the row_updated is equal than 1 send 200 as response
        if (type(results) == list and results[0]['row_updated'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        # if the response is a list and the row_updated is equal than 0 send 400 as response
        elif (type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        # else send 500 as an internal error
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
