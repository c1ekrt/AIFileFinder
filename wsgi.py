from app import open_folder
from flask import Flask, request
from flask_cors import CORS
from flask_cors import cross_origin
import datetime
app = Flask(__name__)
CORS(app)

mainapp = None
# Route for seeing a data
@app.route('/', methods=['GET','POST'])

def get_data():
    data = request.form.get("path")
    if data != None:
        print(data)
        mainapp = open_folder(data)
    result = {
        "path": data,
    }
    return result

@app.route('/finder', methods=['GET', 'POST'])

def get_prompt():
    data = request.form.get("prompt")
    if data != None:
        print(data)
    try:
        return mainapp.search_file(data)
    except:
        print("path is not defined or found")
        return 

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)

    