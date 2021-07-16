from flask import Flask, render_template, Response, request, flash, url_for, redirect, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cli_commands
import webapp_utils
import os, subprocess
import json

# initiate class var: STL path
STL_path = "/app/Test-STLs/5mm_Cube.stl"

# Initialize the Flask app
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = webapp_utils.UPLOAD_FOLDER
print("Flask app initialized.")


# main page
@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        global STL_path  # variable from outer scope
        STL_path = request.form.get('STL_path')  # access STL_path from form
    return render_template('main.html')


# removed /root everywhere so that a plain / denotes the root. If issues with finding items, this could be the cause (revert if needed)

# get gcode
@app.route('/get_gcode', methods=["GET", "POST", "PUT"])  # PUT for placing STL at URL
def get_gcode():
    global STL_path  # variable from outer scope
    cli_commands.test_gcode(input=STL_path, output="/app/test.gcode") # output: app folder in the root directory
    # return gcode (proof of concept)
    with open("/app/test.gcode", "r") as f:
        data = f.read()
    resp = make_response(data) 
    resp.headers['Access-Control-Allow-Origin'] = 'http://172.18.122.122:8080'  # RESTRICT ACCESS LATER
    print("Got gcode.")
    return(resp)


# put STL
@app.route('/put_stl', methods=["GET", "POST", "PUT"])
def put_stl():
    print("---------------------------")
    # print(request.files['file'].filename) 

    print("---------------------------")
    print("asd;fjadf")
    print("qrwerq", request.method)

    print("TYPE:", type(request.form))
    print(request.form)
    print("TYPE:", type(request.files))
    print(request.files)

    # HANDLING FORMDATA
    print("STL:", request.files.get("stl"))
    print("request.get_data.form.get(int)", request.get_data.form.get("int"))
    print("request.form.get(int)", request.form.get("int"))


    bytesdata = request.get_data()
    print(bytesdata)
    print("type:", type(bytesdata))
    stringdata = bytesdata.decode('utf8').replace("'", '"')
    print(stringdata, ", TYPE:", type(stringdata))
    jsondata = json.loads(stringdata)
    print(jsondata, ", TYPE:", type(jsondata))
    print(jsondata["stl"])
    # if request.method == "GET":
    #     print("req is get")
    #     resp = Response()
    #     resp.headers["Access-Control-Allow-Origin"] = "*"
    #     resp.set_data("request.get_data()")
    #     # print(request.get_json())  # parse as JSON
    #     return resp
    if request.method == "POST":
        resp = Response()
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.set_data("request.get_json()")
        # print(request.get_json())  # parse as JSON
        return resp
    # white = ["http://172.18.122.122:8080/editor/", "http://172.18.122.122:8080"]
    # req = request.get_json()
    # resp = make_response(request.files)
    # resp.headers['Access-Control-Allow-Origin'] = 'http://172.18.122.122:8080'  # RESTRICT ACCESS LATER
    # print("Displaying STL...")
    # if req:
    #     return(req)
    # else:
    #     return("resp")


# proof of concept
@app.route('/index')
def index():
    subprocess.run("cd Zenger-Writer-Frontend/editor", shell=True)
    return render_template('Zenger-Writer-Frontend/editor/index.html')


@app.route('/upload_test', methods=['GET', 'POST'])
def upload_file():
    success = "no file uploaded"
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and webapp_utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            success = "file found." + app.config['UPLOAD_FOLDER'] + filename
    return success + '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# React page
@app.route('/react', methods=["GET", "POST"])
def react():
    if request.method == 'POST':
        global STL_path  # variable from outer scope
        STL_path = request.form.get('STL_path')  # access STL_path from form
        print("post successful.")
    return render_template("Zenger-Writer-Frontend/editor/index.html", flask_token="Hello   world")


if __name__ == "__main__":
    print("Running v1.")  # Use to track code updates across machines/environments. 
    app.run(host='0.0.0.0', port=80)  # , debug=True
    print("Web app terminated.")
