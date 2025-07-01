import boto3
import json
import os
from botocore.exceptions import ClientError

BUCKET_NAME = "scamurai-bot-dat"
POSTED_LOG_KEY = "posted_log.json"

# Create S3 client using environment-based credentials
s3 = boto3.client("s3")

def get_posted_log():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=POSTED_LOG_KEY)
        content = response['Body'].read().decode('utf-8')
        posted_urls = json.loads(content)
        return posted_urls
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            # First time run, no log file yet
            return []
        else:
            print(f"❌ Error fetching posted log: {e}")
            return []

def update_posted_log(posted_urls):
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=POSTED_LOG_KEY, Body=json.dumps(posted_urls))
        print("✅ Posted log updated in S3")
    except ClientError as e:
        print(f"❌ Error updating posted log: {e}")
