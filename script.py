from boto3 import Session
from botocore.client import Config
ACCESS_KEY = ""
SECRET_KEY = ""
REGION_NAME = "gra"
BUCKET_NAME = "opi-s3-ai-notebook-test"
ENDPOINT_URL="https://s3.gra.io.cloud.ovh.net"
OBJECT_KEY='file.csv'
LOCAL_FILE='file.csv'
session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,region_name=REGION_NAME)
s3 = session.client(service_name='s3', endpoint_url=ENDPOINT_URL)
s3.download_file(BUCKET_NAME,OBJECT_KEY,LOCAL_FILE)
with open(LOCAL_FILE) as f:
    print(f.readlines())
