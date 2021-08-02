import boto3

def put_object_s3(path, data):
    s3 = boto3.resource('s3')
    s3.Bucket('zengerwriterbucket').put_object(Key=path, Body=data, ACL="public-read")
