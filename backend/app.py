from flask import Flask, render_template, Response, request, flash, url_for, redirect, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cli_commands
import webapp_utils
import os, subprocess
import json

# initiate class var: STL path
STL_path = "/app/Test-STLs/5mm_Cube.stl"
Master_STL_path = "/app/Master.stl"
Master_gcode_path = "/app/Master.gcode"

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

@app.route('/get_gcode', methods=["GET", "POST", "PUT"])  # PUT for placing STL at URL
def get_gcode():

    """
    Function accesses saved gcode and returns it to the client
    """

    # return gcode
    with open(Master_gcode_path, "r") as f:
        data = f.read()
    resp = make_response(data) 
    resp.headers['Access-Control-Allow-Origin'] = 'http://172.18.122.122:8080'  # RESTRICT ACCESS LATER
    print("Got gcode.")
    return(resp)


@app.route('/put_stl', methods=["GET", "POST", "PUT"])
def put_stl():

    # request.form holds non-file key-value pairs
    # request.files holds all filefield data
    # request.files.get("stl") returns the STL, of type werkzeug.FileStorage
    # request.form.get("action") returns the action to take (string)

    """
    This function takes in a FormData which includes JSON as well as the STL for slicing. 
    It slices the STL with the given settings, and then writes thie gcode to a specified path.
    /get_gcode is used to access this path and return the gcode to the client.
    """

    if request.method == "POST":  # Slice and write STL

        # Save input STL to proper format (default buffer size)
        request.files.get("stl").save(Master_STL_path)

        # Slice
        cli_commands.test_gcode(input=Master_STL_path, output=Master_gcode_path)

        # Return an "OK" response
        resp = Response(status=200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp


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
