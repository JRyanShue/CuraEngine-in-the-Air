import boto3
from flask import Response

def put_object_s3(path, data):
    s3 = boto3.resource('s3')
    s3.Bucket('zengerwriterbucket').put_object(Key=path, Body=data, ACL="public-read")


def ok_allow_response():
    # Return an "OK" response and allow CORS
    resp = Response(status=200)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    # print("Returning response to frontend.")
    return resp