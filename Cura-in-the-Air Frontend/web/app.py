# Import necessary libraries
from flask import Flask, render_template, Response

# Initialize the Flask app
app = Flask(__name__)


# main page
@app.route('/')
def main():
    return render_template('main.html')


app.run(host='0.0.0.0', port=5000)
