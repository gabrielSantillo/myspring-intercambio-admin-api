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