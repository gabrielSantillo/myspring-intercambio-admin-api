from uuid import uuid4
from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
import secrets
import json
from dbhelpers import run_statement


def post():
    # verifying if some value was sent as header
    is_valid = check_endpoint_info(
        request.json, ['first_name', 'last_name', 'email', 'password'])
    if (is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    # creating a token by using the built in function secrets
    token = secrets.token_hex(nbytes=None)
    # creating a salt by using the built in function uuid4 to be sent and hash the password in the db
    salt = uuid4().hex

    # calling the function that will add a client
    results = run_statement('CALL add_consultant(?,?,?,?,?,?)', [request.json.get('first_name'), request.json.get(
        'last_name'), request.json.get('email'), request.json.get('password'), token, salt])

    # if the response is a list and the length is different than zero send 200 as response
    if (type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    # else a 500 as response
    else:
        return make_response(json.dumps(results[0], default=str), 500)


def get():
    # calling the procedure that will get all consultants
    results = run_statement('CALL get_all_consultants()')

    # if the response is a list and the length is different than zero send 200 as response
    if (type(results) == list and len(results) != 0):
        return make_response(json.dumps(results), 200)
    # if the response is a list and the length is equal than zero
    elif (type(results) == list and len(results) == 0):
        return make_response(json.dumps("There is no user in the system.", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred"), 500)


def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

     # in case the response from the function is "valid" will keep going with the processes of patching a client
        # getting the client info basesd on its token
    user_info = run_statement('CALL get_consultant_by_token(?)', [
        request.headers.get('token')])
    # verifying if the response is different than a list and its length is different than 1 to send a 400 as response
    if (type(user_info) != list or len(user_info) != 1):
        return make_response(json.dumps(user_info, default=str), 400)

        # updating the user info with the data sent to be updated
    update_user_info = check_data_sent(request.json, user_info[0], [
        'first_name', 'last_name', 'email', 'password'])

    # calling the function that will update the user info
    results = run_statement('CALL edit_consultant(?,?,?,?,?)', [
        update_user_info['first_name'], update_user_info['last_name'], update_user_info['email'], update_user_info['password'], request.headers.get('token')])

    # if the response is a lsit and at row_updateded is equal to 1, send 200 as response
    if (type(results) == list and results[0]['row_updated'] == 1):
        return make_response(json.dumps(results[0], default=str), 200)
     # if the response is a lsit and at row_updateded is equal to 0, send 400 as response
    elif (type(results) == list and results[0]['row_updated'] == 0):
        return make_response(json.dumps(results[0], default=str), 400)
        # else send an 500 as internal error
    else:
        return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)



# THIS DELETE PROCEDURE IS NOT WORKING. I STILL NEED TO TAKE A LOOK ON HOW DO I GRAB THE USER PASSWORD
def delete():
    # verify if the data expected to be sent was sent indeed
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # verify if the data expected to be sent was sent indeed
    is_valid = check_endpoint_info(request.json, ['password'])
    if (is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    # calling a procedure that edit the clients info
    results = run_statement('CALL delete_consultant(?,?)', [
                            request.json.get('password'), request.headers.get('token')])

    # if the results is a list and the length of the result at 'row_updated' is equal to one, return a success response
    if (type(results) == list and results[0]['row_updated'] == 1):
        return make_response(json.dumps(results[0], default=str), 200)
    # if the results is a list and the length of the result at 'row_updated' is equal to zero, return a success response
    elif (type(results) == list and results[0]['row_updated'] == 0):
        return make_response(json.dumps("Bad request."), 400)
    # otherwise, return a db failure response
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
