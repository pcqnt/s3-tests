import boto3
import json
import os
from botocore.client import Config


def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600,
                          endpoint_url=None, aws_access_key_id=None, aws_secret_access_key=None):
    """Generates a pre-signed POST URL that allows uploading to S3-compatible services."""
    s3_client_config = {
        'region_name': 'us-east-1',  # Required by boto3, often ignored by S3-compatible services
         'config': Config(signature_version='s3')
    }
    if endpoint_url:
        s3_client_config['endpoint_url'] = endpoint_url
    if aws_access_key_id and aws_secret_access_key:
        s3_client_config['aws_access_key_id'] = aws_access_key_id
        s3_client_config['aws_secret_access_key'] = aws_secret_access_key
    s3_client = boto3.client('s3', **s3_client_config)
    try:
        response = s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration
        )
    except Exception as e:
        print(f"Error generating pre-signed POST URL: {e}")
        return None
    return response


if __name__ == "__main__":
    # --- Configuration Parameters for OVH S3-Compatible Storage ---
    my_bucket_name = "my-bucket-name"
    my_object_key = "uploads/test-upload.pdf"
    ovh_endpoint = "https://s3.eu-west-lz-lux-a.cloud.ovh.net/"
    my_access_key = os.environ['ACCESS_KEY']
    my_secret_key = os.environ['SECRET_KEY']
    optional_fields = {}  # Can be empty unless specific fields required
    optional_conditions = [
        ["content-length-range", 0, 20 * 1024 * 1024]  # Max 20 MB
    ]
    expiration_time = 600  # 10 minutes
    presigned_post_data = create_presigned_post(
        my_bucket_name,
        my_object_key,
        fields=optional_fields,
        conditions=optional_conditions,
        expiration=expiration_time,
        endpoint_url=ovh_endpoint,
        aws_access_key_id=my_access_key,
        aws_secret_access_key=my_secret_key
    )
    if presigned_post_data:
        print("Successfully generated Pre-signed POST URL for OVH:")
        print(f"  URL: {presigned_post_data['url']}")
        print("  Form Fields (as JSON):")
        print(json.dumps(presigned_post_data['fields'], indent=2))
        print("\n--- Example HTML Form Snippet for Upload ---")
        print(f'<form action="{presigned_post_data["url"]}" method="POST" enctype="multipart/form-data">')
        for key, value in presigned_post_data['fields'].items():
            print(f'  <input type="hidden" name="{key}" value="{value}" />')
        print(f'  <input type="file" name="file" />')
        print(f'  <input type="submit" value="Upload" />')
        print(f'</form>')
        print("\nNote: The file field name MUST be 'file' for S3 Pre-signed POST uploads.")
    else:
        print("Pre-signed POST URL could not be generated.")
