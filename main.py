import json
import os
import boto3
from botocore.exceptions import ClientError
import numpy as np
# import cv2
import mediapipe
import time
from typing import List, Tuple


def process_messages(messages: List[dict], sqs_client: boto3.client):
    """
    Processes messages retrieved from an SQS queue, extracting S3 bucket and key details,
    downloading and processing the corresponding video files, and then deleting the messages
    from the queue to prevent reprocessing.

    Args:
    messages (List[dict]): A list of message dictionaries received from SQS.
    sqs_client (boto3.client): A Boto3 SQS client used to delete messages after processing.

    Returns:
    None
    """
    for message in messages:
        receipt_handle = message['ReceiptHandle']
        body = json.loads(message['Body'])
        s3_key = body['Records'][0]['s3']['object']['key']
        s3_bucket = body['Records'][0]['s3']['bucket']['name']
        
        process_video_file(s3_bucket, s3_key)
        
        sqs_client.delete_message(
            QueueUrl=sqs_queue_url,
            ReceiptHandle=receipt_handle
        )

def process_video_file(s3_bucket: str, s3_key: str):
    """
    Retrieves a video file from an S3 bucket, processes the video, uploads the results
    (a text file and two GIFs) to another S3 bucket, and then cleans up by deleting
    the local video and GIF files to free up disk space.

    Args:
    s3_bucket (str): The name of the S3 bucket where the video file is stored.
    s3_key (str): The key of the video file in the S3 bucket.

    Returns:
    None
    """
    s3 = boto3.client('s3', region_name='us-east-1')
    local_filename = '/tmp/' + s3_key.split('/')[-1]
    
    s3.download_file(s3_bucket, s3_key, local_filename)
    
    try:
        # Call your video processing module here
        #results_text, gif1, gif2 = video_processing_module.process_video(local_filename)
        results_text, gif1, gif2 = 'test', None, None
        # Upload results back to another S3 bucket
        upload_results('ag-video-results', s3_key, results_text, gif1, gif2)

    finally:
        # Clean up: Delete the local video file
        os.remove(local_filename)
        # Clean up: Delete the local GIF files if they exist
        if os.path.exists(gif1):
            os.remove(gif1)
        if os.path.exists(gif2):
            os.remove(gif2)

def upload_results(bucket_name: str, base_key: str, results_text: str, gif1: str, gif2: str):
    """
    Uploads processing results including a text file and two GIFs to an S3 bucket.

    Args:
    bucket_name (str): The name of the S3 bucket where the results will be uploaded.
    base_key (str): The base S3 key of the original video file; used to determine result file names.
    results_text (str): The contents of the result text file.
    gif1 (str): The file path of the first GIF result.
    gif2 (str): The file path of the second GIF result.

    Returns:
    None
    """
    s3 = boto3.client('s3', region_name='us-east-1')
    result_prefix = base_key.replace('.mp4', '')  
    
    # Write text results
    s3.put_object(Bucket=bucket_name, Key=result_prefix + '_results.txt', Body=results_text)
    # Write gif results
    #s3.upload_file(gif1, bucket_name, result_prefix + '_1.gif')
    #3.upload_file(gif2, bucket_name, result_prefix + '_2.gif')

if __name__ == '__main__':
    # The URL of the SQS queue from which messages are received
    sqs_queue_url = 'your-sqs-queue-url'
    # Create an SQS client; specify the AWS region where your SQS queue is hosted
    sqs = boto3.client('sqs', region_name='us-east-1')

    # Continuously poll the queue for new messages
    while True:
        try:
            # Long polling for messages from the SQS queue to reduce the number of empty responses and lower costs
            response = sqs.receive_message(
                QueueUrl=sqs_queue_url,
                MaxNumberOfMessages=10,  # Retrieve up to 10 messages in one request
                WaitTimeSeconds=20       # Wait up to 20 seconds for a message if the queue is initially empty
            )

            # Check if there are any new messages
            messages = response.get('Messages', [])
            if messages:
                # Process each message using the process_messages function
                process_messages(messages, sqs)
        except Exception as e:
            print(f"Error polling SQS: {e}")
            time.sleep(10)  # Wait a bit before retrying to avoid flooding logs with error messages