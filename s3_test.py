import boto3
import os
import json

# Load .env if needed
from dotenv import load_dotenv
load_dotenv()

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bucket = os.getenv("S3_BUCKET_NAME")
key = "test/scamurai_test.json"

# Example data
data = {"test": "hello scamurai"}

# Upload
s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data))
print(f"✅ Uploaded {key}")

# Download
response = s3.get_object(Bucket=bucket, Key=key)
content = response['Body'].read().decode('utf-8')
print(f"📦 Downloaded content: {content}")
