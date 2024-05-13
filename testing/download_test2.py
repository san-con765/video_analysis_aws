import boto3
import json
from urllib.parse import unquote_plus

# Create SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

# Specify your queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/381492146683/video-uploaded-q'

# Poll messages from the queue
while True:
    messages = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20  # Long polling
    )

    if 'Messages' in messages:
        for message in messages['Messages']:
            print("Received message: %s" % message['Body'])
            
            body = json.loads(message['Body'])
            s3_key = body['Records'][0]['s3']['object']['key']
            s3_bucket = body['Records'][0]['s3']['bucket']['name']
            print(s3_key)
            print(s3_bucket)
            object_key = unquote_plus(s3_key)
            print(object_key)
            # try:
            #     s3_bucket = 'ag-video-to-sqs'
            #     s3_key = 'Test+Video3.mp4'

            #     s3 = boto3.client('s3', region_name='us-east-1')
            #     local_filename = '/tmp/' + s3_key.split('/')[-1]

            #     s3.download_file(s3_bucket, s3_key, local_filename)
            # except Exception as e:
            #     print(f"Error downloading video: {e}")
            
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )

           