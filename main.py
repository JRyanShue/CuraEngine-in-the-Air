import subprocess, os

"""
This script's function is to run everything that needs to be run, 
since the dockerfile can only execute one CMD on start.

It will serve a Flask application on port 5000, and a React app on port 3000
"""

# Run subproccesses
subprocess.run(["python3", "./ZengerCuraEngine-in-the-Air/backend/app.py"])
subprocess.run(["cd", "frontend/my-app"])
subprocess.run(["npm", "start"])
