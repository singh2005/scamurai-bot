import os
import json
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = os.getenv("AWS_S3_BUCKET")  # e.g. scamurai-bot-data
KEY = "posted_claim_ids.json"

s3 = boto3.client("s3")

def load_posted_claim_ids():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
        data = response['Body'].read()
        posted_ids = json.loads(data)
        print(f"✅ Loaded {len(posted_ids)} posted claim IDs from S3")
        return set(posted_ids)
    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            print("ℹ️ No existing posted_claim_ids.json found. Starting fresh.")
            return set()
        else:
            print(f"❌ Error loading posted IDs: {e}")
            return set()

def save_posted_claim_ids(claim_ids):
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=KEY, Body=json.dumps(list(claim_ids)))
        print(f"✅ Saved {len(claim_ids)} posted claim IDs to S3")
    except ClientError as e:
        print(f"❌ Error saving posted IDs: {e}")

if __name__ == "__main__":
    # Quick test
    ids = load_posted_claim_ids()
    print(ids)
    ids.add("test-claim-id")
    save_posted_claim_ids(ids)
