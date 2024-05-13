import boto3

try:
    s3_bucket = 'ag-video-to-sqs'
    s3_key = 'Test+Video3.mp4'

    s3 = boto3.client('s3', region_name='us-east-1')
    local_filename = '/tmp/' + s3_key.split('/')[-1]

    s3.download_file(s3_bucket, s3_key, local_filename)
except Exception as e:
    print(f"Error downloading video: {e}")