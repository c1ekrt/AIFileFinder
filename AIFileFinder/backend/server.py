from flask import Flask, request
import datetime
app = Flask(__name__)

# Route for seeing a data
@app.route('/FolderInput', methods=['POST'])
def get_data():
    data = request.form.get('path')
    print(data)
    return data