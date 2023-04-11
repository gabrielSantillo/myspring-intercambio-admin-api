from flask import Flask
from dbcreds import production_mode
from flask_cors import CORS
import endpoints.consultant, endpoints.consultant_login

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