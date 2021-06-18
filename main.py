import subprocess
from flask import Flask, render_template, Response
import cli_commands

# Initialize the Flask app
app = Flask(__name__)
print("Flask app initialized.")

# main page
@app.route('/')
def main():
    return render_template('main.html')

# get gcode
@app.route('/get_gcode')
def get_gcode():
    cli_commands.test_gcode(output="/root/app/test.gcode") # output: app folder in the root directory
    # return gcode (proof of concept)
    with open("/root/app/test.gcode", "r") as f:
        data = f.read()
    print("Got gcode.")
    return(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    print("Web app running.")
