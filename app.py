from flask import Flask
from dbcreds import production_mode
from flask_cors import CORS
import endpoints.consultant, endpoints.consultant_login, endpoints.student, endpoints.loa, endpoints.province, endpoints.college, endpoints.program

# calling the Flask function which will return a value that will be used in my API
app = Flask(__name__)
CORS(app)

########## CONSULTANT ##########
@app.post('/api/consultant')
def post_consultant():
    return endpoints.consultant.post()

@app.get('/api/consultant')
def get_all_consultants():
    return endpoints.consultant.get()

@app.patch('/api/consultant')
def patch_consultant():
    return endpoints.consultant.patch()

@app.delete('/api/consultant')
def delete_consultant():
    return endpoints.consultant.delete()



########## CONSULTANT LOGIN ##########
@app.post('/api/consultant_login')
def login_consultant():
    return endpoints.consultant_login.post()

@app.delete('/api/consultant_login')
def delete_consultant_token():
    return endpoints.consultant_login.delete()


########## STUDENT ##########
@app.post('/api/student')
def post_student():
    return endpoints.student.post()

@app.get('/api/student')
def get_student():
    return endpoints.student.get()

@app.patch('/api/student')
def patch_student():
    return endpoints.student.patch()

@app.delete('/api/student')
def delete_student():
    return endpoints.student.delete()


########## LOA ##########
@app.post('/api/loa')
def post_loa():
    return endpoints.loa.post()

@app.patch('/api/loa')
def patch_loa():
    return endpoints.loa.patch()

@app.delete('/api/loa')
def delete_loa():
    return endpoints.loa.delete()


########## PROVINCE ##########
@app.get('/api/province')
def get_all_provinces():
    return endpoints.province.get()


########## COLLEGE ##########
@app.post('/api/college')
def post_college():
    return endpoints.college.post()

@app.get('/api/college')
def get_all_colleges():
    return endpoints.college.get()

@app.delete('/api/college')
def delete_college():
    return endpoints.college.delete()

@app.patch('/api/college')
def patch_college():
    return endpoints.college.patch()


########## PROGRAM ##########
@app.post('/api/program')
def post_program():
    return endpoints.program.post()

@app.get('/api/program')
def get_program():
    return endpoints.program.get()


# if statement to check if the production_mode variable is true, if yes, run in production mode, if not, run in testing mode
if (production_mode):
    print("Running in Production Mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5075)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")

    app.run(debug=True)