

UPLOAD_FOLDER = '/app/resources'
ALLOWED_EXTENSIONS = {'stl'}

# check to see that filename is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





