
from flask import Flask, render_template, Response, request, make_response
from flask_cors import CORS
import cli_commands, json, boto3
from api_commands import put_object_s3

# initiate class var: STL path
STL_path = "/app/Test-STLs/5mm_Cube.stl"
Master_STL_path = "/app/Master.stl"
Master_gcode_path = "/app/Master.gcode"

# Initialize the Flask app
app = Flask( __name__ )
CORS( app )

bucketname = "zengerwriterbucket"

# Default page
@app.route('/', methods=["GET", "POST"])
def main():

    return render_template('main.html')


@app.route('/get_gcode', methods=["GET"])  # PUT for placing STL at URL
def get_gcode():

    """
    Function accesses saved gcode and returns it to the client
    """

    # return gcode
    with open(Master_gcode_path, "r") as f:
        data = f.read()
    
    resp = make_response(data) 
    resp.headers['Access-Control-Allow-Origin'] = '*'  # RESTRICT ACCESS LATER AND GENERATE RANDOM URLS
    return(resp)


@app.route('/put_stl', methods=["POST"])
def put_stl():

    """
    Takes in a FormData which includes JSON as well as the STL for slicing. 
    It slices the STL with the given settings, and then writes the gcode to be accessed by /get_gcode.
    """

    if request.method == "POST":  # Get and slice STL, write gcode

        request.files.get("stl").save(Master_STL_path)

        cli_commands.slice(input=Master_STL_path, output=Master_gcode_path, form=request.form)

        return Response( status=200, headers={ "Access-Control-Allow-Origin": "*" } )


@app.route('/get_projects', methods=["GET"])
def get_projects():

    """
    Get all project numbers for a given user (username passed via headers)
    Returns a JSON object with a project_numbers key
    Values are the numbers (ID) of all the projects
    """

    # get username from headers
    if not request.headers.get('username'):
        return Response(status=400)
    
    username = request.headers['username']

    projects_list = []

    if request.method == "GET":

        client = boto3.client('s3')
        global bucketname
        prefix = 'Users/' + username + '/projects/'
        projects = client.list_objects(Bucket=bucketname, Prefix=prefix, Delimiter='/')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.ObjectSummary.get
        for project in projects.get( 'CommonPrefixes' ): 
            
            # Grab all project ID's
            project_name = project[ 'Prefix' ]  # Get raw object name ( on S3, includes entire "path" )
            project_number = project_name[ len( prefix ):len( project_name )-1 ]  # Get only the project's ID
            projects_list.append( project_number )
    
    return json.dumps( { 'project_numbers': projects_list } )


@app.route('/pull_object', methods=["GET"])
def pull_object():

    """
    Pulls raw file from S3 based on path specified in header input. 
    """

    if not request.headers['path']:
        return Response(status=400)
    
    path = request.headers['path']

    if request.method == "GET":

        s3 = boto3.resource('s3')

        global bucketname
        file = s3.Object( bucketname, path )
        dict = json.loads( file.get()[ 'Body' ].read() )

    return json.dumps( {'body': dict} )


@app.route('/pull_object_url', methods=["GET"])
def pull_object_url():

    """
    Puts raw file from S3 into URL and returns the URL. Based on path specified in header input. 
    """

    if not request.headers['path']:
        return Response(status=400)
    
    path = request.headers['path']

    if request.method == "GET":

        client = boto3.client('s3', region_name='us-east-2')

        global bucketname

        # place image at url (url expires after set period for security)
        url = client.generate_presigned_url('get_object',
            Params={'Bucket': bucketname,
                    'Key': path},
            ExpiresIn=10000)

    return json.dumps({'url': url})


@app.route('/get_object', methods=["GET"])
def get_object():

    """
    Pulls info from S3 for previews of projects. 
    """

    if not request.headers[ 'path' ]:
        return Response(status=400)

    path = request.headers[ 'path' ]
    preview_path = path + '/preview.png'
    info_path = path + '/info.json'

    if request.method == "GET":

        client = boto3.client( 's3' )
        s3 = boto3.resource( 's3' )

        # place image at temporary URL
        url = client.generate_presigned_url( 'get_object',
            Params={ 'Bucket': bucketname,
                    'Key': preview_path },
            ExpiresIn=10000 )

        # get needed info for editor preview
        object = s3.Object( bucketname, info_path )
        dict = json.loads( object.get()[ 'Body' ].read() )

        name = dict[ "name" ]

    return json.dumps( { 'name': name, 'url': url } )


@app.route( '/put_object', methods=["POST", "PUT"] )
def put_object():

    """
    Put Object into bucket path. 
    """

    if request.method == "POST" or request.method == "PUT":

        if not request.headers.get( 'path' ):
            return Response( status=400 )

        data = bytes( json.dumps( request.get_json() ).encode( 'UTF-8' ) )

        put_object_s3( request.headers.get( 'path' ), data )

        return Response( status=200, headers={ "Access-Control-Allow-Origin": "*" } )


@app.route('/put_image', methods=["GET", "POST", "PUT"])
def put_image():

    """
    Put Image into bucket path. 
    """

    if request.method == "POST" or request.method == "PUT":

        if not request.headers.get( 'path' ):
            return Response(status=400)

        data = request.files.get('file')

        put_object_s3( request.headers.get( 'path' ), data )
        
        return Response( status=200, headers={ "Access-Control-Allow-Origin": "*" } )


if __name__ == "__main__":

    print("Running v1.")  # Use to track code updates across machines/environments. 
    app.run(host='0.0.0.0', port=80)  # , debug=True
    print("Web app terminated.")
