from flask import request, make_response
from apihelpers import check_endpoint_info
import secrets
import json
from dbhelpers import run_statement

def post():
    is_valid = check_endpoint_info(request.json, ['email', 'password'])
    if (is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    # creating a token by using the built in function secrets
    token = secrets.token_hex(nbytes=None)
    # calling the function that will log in the client
    results = run_statement('CALL log_in_consultant(?,?,?)', [
                            request.json.get('email'), request.json.get('password'), token])

    # if the response is a list and the length is different than zero send 200 as response
    if (type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    # if the response is a list and the length is equal than zero
    elif (type(results) == list and len(results) == 0):
        return make_response(json.dumps("Bad login attempt. Your password or/and email are wrong."), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred"), 500)