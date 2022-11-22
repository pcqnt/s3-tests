from boto3 import Session
from botocore.client import Config
import os
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REGION_NAME = "gra"
BUCKET_NAME = "opi-standard-gra"
ENDPOINT_URL="https://s3.gra.io.cloud.ovh.net"
OBJECT_KEY="upload.txt"
session = Session(aws_access_key_id=ACCESS_KEY,
              aws_secret_access_key=SECRET_KEY,
              region_name=REGION_NAME)
s3 = session.client(service_name='s3', endpoint_url=ENDPOINT_URL, config=Config(s3={'addressing_style': 'path'})
)
resp= s3.generate_presigned_url(ClientMethod='put_object', Params={'Bucket': BUCKET_NAME, 'Key': OBJECT_KEY},ExpiresIn=36)
print(resp)
