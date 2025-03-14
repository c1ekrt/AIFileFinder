
from flask import Flask, request
from flask_cors import CORS
from flask_cors import cross_origin
from flask_caching import Cache
import threading

from app import open_folder
from util import GetFileCount



app = Flask(__name__)
CORS(app)

mainapp = None
# Route for seeing a data
class DataStorage:
    def __init__(self):
        self.path = ""
        self.dir = None
        self.prompt = ""
        self.filecount = 0

ds = DataStorage()        

@app.route('/', methods=['GET','POST'])
def get_data():
    data = request.form.get("path")
    ds.path = data
    print("path: ", data)
    if data != None:
        mainapp = open_folder(data)
        ds.dir = mainapp
    result = {
        "path": ds.path,
    }
    return result

@app.route('/finder', methods=['GET', 'POST'])
def get_prompt():
    data = request.form.get("prompt")
    print(data)
    ds.prompt = data
    response = ds.dir.search_file(ds.prompt)
    print(response["source"])
    result = {
        "response": response["source"].tolist(),
    }
    return result

    
@app.route('/filecount', methods=['GET', 'POST'])
def get_filecount():
    data = request.form.get("path")
    
    if data != None:
        c = GetFileCount(data)
        ds.filecount = c.count
    result = {
        "filecount": ds.filecount,
    }
    print("filecount:", ds.filecount)
    return result

if __name__ == "__main__":
    
    app.run(host="127.0.0.1", port="5000", debug=True)
    

    


