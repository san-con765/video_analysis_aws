import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')

# Example usage in your application
print(f"Using S3 Bucket: {S3_BUCKET_NAME}")
print(f"Using SQS Queue URL: {SQS_QUEUE_URL}")