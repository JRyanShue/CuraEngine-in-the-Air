
from flask import request
import subprocess
import json


def slice(input, output, form):

    shell_command = ""
    shell_command += "cd .. && cd ./ZengerEngine/build && "
    shell_command += "./CuraEngine slice -p -j /app/ZengerEngine-Presets/definitions/fdmprinter.def.json -j /app/ZengerEngine-Presets/definitions/creality_ender3.def.json "
    
    # add settings to shell command based on received FormData
    for k, v in form.items():
        shell_command = add_setting(shell_command, form, k, v)  # form.get("layer height")

    shell_command += "-l " + input + " -o " + output

    print("Executing command:", shell_command)

    subprocess.run(shell_command, shell=True)


def add_setting( shell_command, form, setting_name, setting_val ):

    shell_command += "-s " + str(setting_name) + "=" + str(setting_val) + " "
    return shell_command


def put_object( object ):

    # Save JSON object to file
    with open('data.json', 'w') as f:
        json.dump(object, f)

    shell_command = "aws s3api put-object --bucket zengerwriterbucket --key Users/testman/test.json --body data.json"

    subprocess.run(shell_command, shell=True)

    print("put object.")


def get_object():

    print("getting object")

