import subprocess, os
import threading

"""
This script's function is to run everything that needs to be run, 
since the dockerfile can only execute one CMD on start.

It will serve a Flask application on port 5000, and a React app on port 3000
"""

# Run subproccesses

def run_react_app():
    subprocess.run("cd ./ZengerCuraEngine-in-the-Air/frontend", shell=True)
    subprocess.run("npx create-react-app test-app && cd test-app && npm start", shell=True)

def run_flask_app():
    subprocess.run("python3 ./ZengerCuraEngine-in-the-Air/backend/app.py", shell=True)

# subprocess.run("cd ./ZengerCuraEngine-in-the-Air/frontend/my-app", shell=True)
x = threading.Thread(target=run_react_app, args=())
x.start()

y = threading.Thread(target=run_flask_app, args=())
y.start()

# subprocess.run("cd test-app", shell=True)a
# subprocess.run("npm start", shell=True)a
# subprocess.run("npm init", shell=True)
# subprocess.run("npm start", shell=True)
