import subprocess, os

"""
This script's function is to run everything that needs to be run, 
since the dockerfile can only execute one CMD on start.

It will serve a Flask application on port 5000, and a React app on port 3000
"""

# Run subproccesses

subprocess.run("cd ./ZengerCuraEngine-in-the-Air/frontend/my-app", shell=True)
subprocess.run("npm init", shell=True)
subprocess.run("npm start", shell=True)
subprocess.run("python3 ./ZengerCuraEngine-in-the-Air/backend/app.py", shell=True)