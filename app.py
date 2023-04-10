from flask import Flask
from dbcreds import production_mode
from flask_cors import CORS

# calling the Flask function which will return a value that will be used in my API
app = Flask(__name__)
CORS(app)


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