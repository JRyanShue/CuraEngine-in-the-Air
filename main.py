import subprocess
from flask import Flask, render_template, Response, request
import cli_commands

# Initialize the Flask app
app = Flask(__name__)
print("Flask app initialized.")

# initiate class var: STL path
STL_path = "/root/app/Test-STLs/5mm_Cube.stl"


# main page
@app.route('/')
def main():
    if request.method == 'POST':
        global STL_path
        STL_path = request.form.get('STL_path')  # access STL_path from form
    return render_template('main.html')
    

# get gcode
@app.route('/get_gcode')
def get_gcode():
    global STL_path
    cli_commands.test_gcode(input=STL_path, output="/root/app/test.gcode") # output: app folder in the root directory
    # return gcode (proof of concept)
    with open("/root/app/test.gcode", "r") as f:
        data = f.read()
    print("Got gcode.")
    return(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    print("Web app running.")
