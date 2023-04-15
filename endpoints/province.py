from flask import request, make_response
import json
from dbhelpers import run_statement

def get():  
    results = run_statement('CALL get_all_provinces(?)', [request.headers.get('token')])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results, default=str), 200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps("Wrong token", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)