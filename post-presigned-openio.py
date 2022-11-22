import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import os
import requests    # To install: pip install requests

def create_presigned_post( bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    ACCESS_KEY = os.environ['ACCESS_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    session = boto3.Session(aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                region_name="gra")
    s3_client = session.client(service_name='s3',endpoint_url="https://s3.gra.io.cloud.ovh.net", config=Config(s3={'addressing_style': 'virtual'}))
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

def main():
    
    bucket_name="opi-standard-gra"
    # Generate a presigned S3 POST URL
    object_name = 'upload.txt'
    response = create_presigned_post(bucket_name, object_name)
    if response is None:
        exit(1)

    # Demonstrate how another Python program can use the presigned URL to upload a file
    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)
    # If successful, returns HTTP status code 204
    logging.info(f'File upload HTTP status code: {http_response.status_code}')
    if http_response.status_code != 204:
        logging.warning(f'File upload HTTP status code: {http_response.status_code}')
        print(http_response.content)
        logging.debug( http_response.content)

if __name__ == "__main__":
    main()
