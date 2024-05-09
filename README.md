# Video Processing Pipeline on AWS

This project automates the processing of video files uploaded to an AWS S3 bucket. It uses AWS Simple Queue Service (SQS) to trigger processing of videos whenever a new video is uploaded to the bucket. The processed results, including text files and GIFs, are then uploaded to another S3 bucket.

## System Architecture

This application integrates several AWS services:
- **Amazon S3**: Stores the uploaded video files and the processed results.
- **Amazon SQS**: Manages the messages that trigger processing based on video file uploads.
- **AWS EC2**: Is used to run the script

## Requirements

- AWS CLI configured with administrator access
- Python 3.9.16
- Boto3
- NumPy
- MediaPipe (for video processing, not included in the dummy code)
- OpenCV-Python (optional for advanced image/video manipulations)

## Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Install Dependencies**
    Ensure you have Python installed, and then install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure AWS Credentials**
    Make sure your AWS credentials are configured by following the AWS CLI configuration instructions:
    ```bash
    aws configure
    ```

4. **Set up the AWS Infrastructure**
    - Create an S3 bucket for uploading videos.
    - Create another S3 bucket for storing the processed outputs.
    - Set up an SQS queue and configure S3 to send notification messages to this queue on new video uploads.

5. **Deployment**
    - Update the `sqs_queue_url` and bucket names in the script with your specific AWS resource names.
    - Deploy the script to an AWS EC2 instance or run it locally for testing:
        ```bash
        python3 main.py
        ```

## Usage

Upload video files to the designated S3 bucket. The system is configured to automatically pick up new files, process them, and upload the results to the output bucket. Results include a text file detailing the processing outcomes and two GIF images extracted from the video.

## Troubleshooting

- Ensure that the IAM roles associated with your AWS services have the necessary permissions.
- Check the SQS queue and S3 bucket for proper configuration of notification settings.
- Logs are printed to the console for troubleshooting. Check the logs for any errors in processing or AWS service interactions.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your features or fixes.

## License
