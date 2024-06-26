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
 
import cv2
import mediapipe as mp
import re
 
# Local modules to be include
import video_processing_python_files.vp_gifCreater
# import video_processing_python_files.vp_calculateAngle
import video_processing_python_files.vp_analysePose
import video_processing_python_files.vp_runAnalysis
import video_processing_python_files.vp_saveImages
import video_processing_python_files.vp_results_text
 
 
 
def cleanup_files(files):
    print("Run Process cleanup_files")
    """ Removes specified files from the filesystem if they exist. """
    for file_path in files:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")       
 
def upload_results(bucket_name: str, base_key: str, results_text: str, gif1: str):
    print("Run Process upload_results")
    """
    Uploads processing results including a text file and two GIFs to an S3 bucket.
 
    Args:
    bucket_name (str): The name of the S3 bucket where the results will be uploaded.
    base_key (str): The base S3 key of the original video file; used to determine result file names.
    results_text (str): The contents of the result text file.
    gif1 (str): The file path of the first GIF result.
 
    Returns:
    None
    """
    
    print(f"Uploading {base_key}.......")
    print("bucket name " + bucket_name)
    print("base key " + base_key)
    print("results text " + results_text)
    print("gif1 " + gif1)
 
    s3 = boto3.client('s3', region_name='us-east-1')
    # result_prefix = base_key.replace('.mp4', '')
    result_prefix = re.sub(r'\.(mp4|mov)$', '', base_key)
    folder_name = result_prefix + '/'
    object_name = f"{folder_name}{result_prefix}"
 
  
    try:
        # Write text results
        s3.put_object(Bucket=bucket_name, Key=object_name + '_results.txt', Body=results_text)
        # Write gif results
        s3.upload_file(gif1, bucket_name, object_name + '_1.gif')
 
        
    except Exception as e:
            print(f"Error uploading video: {e}")
    print(f"Uploaded {object_name + '_results.txt'} sucessfully.......")
 
 
def process_video_file(s3_bucket: str, s3_key: str):
    print("Run Process process_video_files")
    """
    Retrieves a video file from an S3 bucket, processes the video, uploads the results
    (a text file and potentially two GIFs) to another S3 bucket, and then cleans up by deleting
    the local video and GIF files to free up disk space.
 
    Args:
        s3_bucket (str): The name of the S3 bucket where the video file is stored.
        s3_key (str): The key of the video file in the S3 bucket.
 
    Returns:
        None
    """
    error_occurred = False # Error flag
 
    local_filename = '/tmp/' + s3_key.split('/')[-1]
 
    print(f"Processing {s3_key}.......")
    print("File name = ", local_filename)
    print("S3 Bucket name = ", s3_bucket)
    print("S3 Key  = ", s3_key)
 
    try:
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.download_file(s3_bucket, s3_key, local_filename)
        print(f"Downloaded {s3_key} to {local_filename}")
        
    except Exception as e:
        print(f"Error downloading video: {e}")
        return
 
    try:

        print("Local File Name = ", local_filename)
         
        AnalysisArray, result_text = video_processing_python_files.vp_analysePose.AnalysePose(local_filename)
        print("Analysis Returned")
   
        print("Run Text Results file")        
        results_text_output = video_processing_python_files.vp_results_text.textResults(result_text)
        print("Run Text Results finished")
 
        print("Analysis Returned: ", local_filename)
        
      
        #Create gif
        # Combine Images
        # images = [AnalysisArray[0], AnalysisArray[1], AnalysisArray[2]]
        print("Start to create gif")
        dir = "/home/ec2-user/video_analysis_aws"
        images = [dir+"/image_1.jpg", dir+"/image_2.jpg", dir+"/image_3.jpg"]

        print("images testing")
        print(images)
        for i in range(len(images)):
            print(images[i])
        
        #results_text, gif1, gif2 = 'dummy results text', '/tmp/dummy1.gif', '/tmp/dummy2.gif'
        print(f"Processed {s3_key} successfully, results ready to upload.")
 
        # Converts Images into gif
        results_gif = video_processing_python_files.vp_gifCreater.create_gif(images)
        
        results_gif = "/home/ec2-user/video_analysis_aws/output.gif"
 
        # Upload results back to another S3 bucket
        print("Upload Results")
        upload_results(S3_BUCKET_NAME, s3_key, results_text_output, results_gif)
 
    except Exception as e:
        error_occurred = True
        print(f"Error processing/uploading results for {s3_key}: {e}")
        print(error_occurred)
        if error_occurred:
            print(f"Error Ocurred processing{s3_key}")
            fail_result = "Something went wrong, try again later."
            error_gif = "error_gif/try_again_gif.gif"
            upload_results(S3_BUCKET_NAME, object_key, fail_result, error_gif)  
        
    finally:
 
        # Clean up: Delete the local video file and any generated GIFs
        print("Try to clean up")
        cleanup_files([local_filename])

#ONLINE
load_dotenv()
 
# Access environment variables
S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')
 
# #LOCAL
# videoExample = "/Users/seanryan/Downloads"
 
 
 
if __name__ == '__main__':
    print("Run main")
    # The URL of the SQS queue from which messages are received
    # Create SQS client
    sqs = boto3.client('sqs', region_name='us-east-1')
 
    # Specify your queue URL
    sqs_queue_url = SQS_QUEUE_URL
 
    # Continuously poll the queue for new messages
    while True:
        try:
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
                    try:
                        process_video_file(s3_bucket, object_key)
                        
                        sqs.delete_message(
                            QueueUrl=sqs_queue_url,
                            ReceiptHandle=receipt_handle
                        )
                    except Exception as e:
                        print(f"Something went wrong with {object_key}: {e}")
 
        except Exception as e:
            print(f"Something went wrong: {e}")
            time.sleep(10)  # Wait a bit before retrying to avoid flooding logs with error messages