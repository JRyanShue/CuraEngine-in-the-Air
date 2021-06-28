from flask import Flask, render_template, Response, request, flash, url_for, redirect
from werkzeug.utils import secure_filename
import cli_commands
import webapp_utils

# initiate class var: STL path
STL_path = "/app/Test-STLs/5mm_Cube.stl"

# Initialize the Flask app
app = Flask(__name__)
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
@app.route('/get_gcode')
def get_gcode():
    global STL_path  # variable from outer scope
    cli_commands.test_gcode(input=STL_path, output="/app/test.gcode") # output: app folder in the root directory
    # return gcode (proof of concept)
    with open("/app/test.gcode", "r") as f:
        data = f.read()
    print("Got gcode.")
    return(data)


# proof of concept
@app.route('/index')
def index():
    return render_template('index.html')


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    print("Web app terminated.")