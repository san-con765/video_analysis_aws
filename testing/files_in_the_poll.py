#Standard Python Lib
import json
import os
import boto3

# Installed via requirements.txt
from botocore.exceptions import ClientError
import numpy as np


import time
from typing import List, Tuple
from urllib.parse import unquote_plus
from dotenv import load_dotenv

load_dotenv()

# Access environment variables
S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')



if __name__ == '__main__':
    print("Run main")
    # The URL of the SQS queue from which messages are received
    # Create SQS client
    sqs = boto3.client('sqs', region_name='us-east-1')

    # Specify your queue URL
    sqs_queue_url = SQS_QUEUE_URL

    # Continuously poll the queue for new messages
    while True:

        # Long polling for messages from the SQS queue to reduce the number of empty responses and lower costs
        print("Polling SQS.......")
        response = sqs.receive_message(
            QueueUrl=sqs_queue_url,
            MaxNumberOfMessages=10,  # Retrieve up to 10 messages in one request
            WaitTimeSeconds=20       # Wait up to 20 seconds for a message if the queue is initially empty
        )
        # Check if there are any new messages
        messages = response.get('Messages', [])
        if messages:
            # Process each message using the process_messages function
            for message in messages:
                receipt_handle = message['ReceiptHandle']
                body = json.loads(message['Body'])
                s3_key = body['Records'][0]['s3']['object']['key'] # File name
                s3_bucket = body['Records'][0]['s3']['bucket']['name'] # Upload bucket name
                # Handles the formating of the sqs message
                object_key = unquote_plus(s3_key)
                print(object_key)