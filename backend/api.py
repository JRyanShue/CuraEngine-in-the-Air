from botocore.serialize import DEFAULT_TIMESTAMP_FORMAT
from flask import Flask, render_template, Response, request, flash, url_for, redirect, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cli_commands
import webapp_utils
import os, subprocess
import json
import boto3
import base64
from binascii import a2b_base64
from web_commands import put_object_s3, ok_allow_response

# initiate class var: STL path
STL_path = "/app/Test-STLs/5mm_Cube.stl"
Master_STL_path = "/app/Master.stl"
Master_gcode_path = "/app/Master.gcode"

# Initialize the Flask app
app = Flask(__name__)
CORS(app)
# Configure from config.py variables
app.config.from_object("config")
app.config['UPLOAD_FOLDER'] = webapp_utils.UPLOAD_FOLDER
print("Flask app initialized.")

bucketname = "zengerwriterbucket"

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
    resp.headers['Access-Control-Allow-Origin'] = '*'  # RESTRICT ACCESS LATER
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

        print("POST action.")

        # Save input STL to proper format (default buffer size)
        print("STL::", request.files.get("stl"))
        request.files.get("stl").save(Master_STL_path)

        # Slice
        cli_commands.slice(input=Master_STL_path, output=Master_gcode_path, form=request.form)

        # Return an "OK" response
        resp = Response(status=200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        print("Returning response to frontend.")
        return resp


@app.route('/get_projects', methods=["GET"])
def get_projects():

    """
    Get all project numbers for a given user (username passed via headers)
    Returns a JSON object with a project_numbers key
    Values are the numbers (ID) of all the projects
    """

    # get username from headers
    if request.headers.get('username'):
        username = request.headers['username']
    else:
        username = "testman"

    projects_list = []

    if request.method == "GET":

        client = boto3.client('s3')
        global bucketname
        prefix = 'Users/' + username + '/projects/'
        projects = client.list_objects(Bucket=bucketname, Prefix=prefix, Delimiter='/')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.ObjectSummary.get
        for project in projects.get('CommonPrefixes'):  # .get('CommonPrefixes')
            
            project_name = project['Prefix']
            project_number = project_name[len(prefix):len(project_name)-1]
            projects_list.append(project_number)

    print("projects:", projects_list)

    return json.dumps({'project_numbers': projects_list})

    # Return an "OK" response
    resp = Response(status=200)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    print("Returning response to frontend.")
    return resp


@app.route('/pull_object', methods=["GET"])
def pull_object():

    """
    Pulls raw file from S3 based on path specified in header input. 
    """

    if request.headers['path']:
        path = request.headers['path']
    else:
        resp = Response(status=400)
        return resp

    if request.method == "GET":

        s3 = boto3.resource('s3')

        global bucketname
        print("Folder path:", path)
        infofile = s3.Object(bucketname, path)
        infodict = json.loads(infofile.get()['Body'].read())

        print("infodict:", infodict)

    return json.dumps({'body': infodict})

    # Return an "OK" response
    resp = Response(status=200)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    print("Returning response to frontend.")
    return resp


@app.route('/pull_object_url', methods=["GET"])
def pull_object_url():

    """
    Puts raw file from S3 into URL and returns the URL. Based on path specified in header input. 
    """

    if request.headers['path']:
        path = request.headers['path']
    else:
        resp = Response(status=400)
        return resp

    if request.method == "GET":

        client = boto3.client('s3', region_name='us-east-2')

        global bucketname
        print("Folder path:", path)

        # place image at url (url expires after set period for security)
        url = client.generate_presigned_url('get_object',
            Params={'Bucket': bucketname,
                    'Key': path},
            ExpiresIn=10000)

        print("URL:", url)

    return json.dumps({'url': url})

    # Return an "OK" response
    resp = Response(status=200)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    print("Returning response to frontend.")
    return resp


@app.route('/get_object', methods=["GET"])
def get_object():

    """
    Pulls info from S3 for previews of projects. 
    """

    if request.headers['path']:
        path = request.headers['path']
        preview_path = path + '/preview.png'
        info_path = path + '/info.json'
    else:
        resp = Response(status=400)
        return resp

    if request.method == "GET":

        client = boto3.client('s3')
        s3 = boto3.resource('s3')

        global bucketname
        print("Folder path:", path)

        # place image at url (url expires after set period for security)
        url = client.generate_presigned_url('get_object',
            Params={'Bucket': bucketname,
                    'Key': preview_path},
            ExpiresIn=10000)

        print("URL:", url)

        # get needed info for editor preview
        infofile = s3.Object(bucketname, info_path)
        infodict = json.loads(infofile.get()['Body'].read())

        name = infodict["name"]

    return json.dumps({'name': name, 'url': url})

    # Return an "OK" response
    resp = Response(status=200)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    print("Returning response to frontend.")
    return resp


@app.route('/put_object', methods=["GET", "POST", "PUT"])
def put_object():

    """
    Put Object into bucket path. 
    Used for saving single files, such as editor configurations and previews. 
    """

    if request.method == "POST" or request.method == "PUT":

        if request.headers.get('path'):
            path = request.headers.get('path')
            print("POST PATH:", path)
        else:
            resp = Response(status=400)
            return resp

        # form = request.form.get("editor")
        if request.headers['isfile'] == 'true':  # Basically, not JSON
            print("IS FILE.")
            imageURI = request.files.get('file')
            # imageURI = request.files['file']
            print("IMAGE URI::", imageURI)
            imageASCII = imageURI.stream.read()
            print("IMAGE ASCII::", imageASCII)
            print("TYPE ASCII::", type(imageASCII))
            # print("TYPE::", type(imageURI))
            # data = base64.b64decode(request.files['file'].read())  # read()
            # data = a2b_base64(imageURI.stream.read())
            data = base64.b64decode(imageASCII, altchars="-_")  # , altchars="-_"

            print("BINARY DATA::", data)
            # data = request.files['file']
        else:
            print("IS JSON.")
            data = bytes(json.dumps(request.get_json()).encode('UTF-8'))

        # print("Form:", form)
        # with 

        s3 = boto3.resource('s3')
        # for bucket in s3.buckets.all():
        #     print(bucket.name)

        # get "editor" object from FormData
        s3.Bucket('zengerwriterbucket').put_object(Key=path, Body=data, ACL="public-read")
        # cli_commands.put_object(request.form.get("editor"))

        # Return an "OK" response
        resp = Response(status=200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        print("Returning response to frontend.")
        return resp


@app.route('/put_image', methods=["GET", "POST", "PUT"])
def put_image():

    """
    Put Image into bucket path. 
    """

    if request.method == "POST" or request.method == "PUT":

        print(request.method)

        if request.headers.get('path'):
            path = request.headers.get('path')
            print("path:", path)
        else:
            resp = Response(status=400)
            return resp

        data = request.files.get('file')
        print("DATA::", data)

        s3 = boto3.resource('s3')
        s3.Bucket('zengerwriterbucket').put_object(Key=path, Body=data, ACL="public-read")
        
        # Return an "OK" response and allow CORS
        resp = Response(status=200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        print("Returning response to frontend. put_image")
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
