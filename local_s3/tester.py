import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Configure the S3Proxy endpoint
s3proxy_endpoint = 'http://localhost:8020'

# Initialize an S3 client with the S3Proxy endpoint
s3 = boto3.client('s3', endpoint_url=s3proxy_endpoint, config=Config(signature_version=UNSIGNED))

# Create a bucket if it doesn't exist
bucket_name = 'test-bucket'
existing_buckets = s3.list_buckets()['Buckets']
existing_bucket_names = [b['Name'] for b in existing_buckets]
if bucket_name not in existing_bucket_names:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created successfully.")
else:
    print(f"Bucket '{bucket_name}' already exists.")

# Upload a file to the bucket
file_content = b'Hello, S3Proxy!'
object_key = 'test-object.txt'
s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)

# List objects in the bucket
response = s3.list_objects(Bucket=bucket_name)
objects = response.get('Contents', [])
if objects:
    print("Objects in bucket:")
    for obj in objects:
        print(obj['Key'])
else:
    print("No objects found in the bucket.")

# Download the uploaded file
response = s3.get_object(Bucket=bucket_name, Key=object_key)
file_content = response['Body'].read().decode('utf-8')
print("Downloaded file content:")
print(file_content)

# Delete all objects in the bucket
if objects:
    for obj in objects:
        s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
    print("All objects deleted from the bucket.")


# Delete the bucket
s3.delete_bucket(Bucket=bucket_name)
print(f"Bucket '{bucket_name}' deleted.")
